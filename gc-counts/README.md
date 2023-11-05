# GC counting

## Using the tutorial

The goal is work through 4 successive versions of `jugfile.py` (named
`jugfile1.py`, `jugfile2.py`...); successively replacing `jugfile.py` with the
next version.

Step by step

1. Copy `jugfile1.py` to `jugfile.py`
2. Run `jug execute`.
3. Run `mkdir outputs` and re-run `jug execute`.
4. **Overwrite** `jugfile.py` with `jugfile2.py` by running `cp jugfile2.py jugfile.py`
This simulates editing the code in `jugfile.py`
5. `jug execute`
6. `cp jugfile3.py jugfile.py`
7. `jug execute`
8. `cp jugfile4.py jugfile.py`
9. `jug execute`

The files `LoadingFromJupyter.ipynb` and `plot-results.py` show how to load jug
results from standard Python/Jupyter

## The task

**Note**: this is a toy dataset, no conclusions should be drawn from it.
Nonetheless, the setting is realistic.

We want to measure the GC content in a set of FASTA files.

### Some basic bioinformatics

1. _FASTA files_ are text-based and look like the following:

```
>GMGC10.033_133_404.UNKNOWN
ATGAAAGGGTTAGTTGTAACGGGCTTAACGGTTGCTTTTGGATTTGTAGCGTATGAGAAATTAACGTATGTAGTTGATGTTGTGAAACATTTGATCGCTTAG
>GMGC10.026_381_531.UNKNOWN
ATGATCTGGCGTTCGGGCCGGTTTGCCGCCGTTGCCCTGCAGCGCAAACCGCCGGTGGGTTGGGCCGGCAACCTGGTGCAGCCTGAAAAATTACGGGTATAA
>GMGC10.013_658_495.UNKNOWN
ATGATGAACAAAATGAAATCAAACAAATTTTTCAATACAATGGGCATGGTGCTATCCGCACTTATCGATGCAAAAGCAGTTGCAACTACATTAAACAAATAA
```

Header lines start with `>` and name the next sequence.


2. _GC content_ is simply the fraction of nucleotides (the ATCGs of DNA) that are either G or C.

That's all you need to know from biology.

### The task

We have 14 FASTA files in the `demo-data` directory. These are extracts from the [GMGCv1](https://gmgc.embl.de) ([Coelho et al., 2022](https://www.nature.com/articles/s41586-021-04233-4)), but only the first 1,000 lines).

1. We want to count the nucleotides (fancy word for letters) in each sequence and produce a table
2. We want to summarize the results by habitat (what is the average in each habitat)
3. We want to plot the results

## The result (annotated version)

This is the final `jugfile.py` (`jugfile4.py`)


Basic imports:

```python
import pandas as pd
from glob import glob

from jug import TaskGenerator
```


The `@TaskGenerator` decorator transforms `process` from a standard Python
function into a Jug `TaskGenerator`. Other than that, this is just Python code:

```python
@TaskGenerator
def process(fna, ofile):
    from collections import Counter
    from fasta import fasta_iter
    from time import sleep
    from os import makedirs
    sleep(4) # Pretend we are doing a lot of work

    makedirs('outputs', exist_ok=True)

    r = []
    hs = []
    for h,seq in fasta_iter(fna):
        r.append(pd.Series(Counter(seq)))
        hs.append(h)
    return pd.DataFrame(r, index=hs)
```

We do the same for the `gc_fraction` and `build_table` functions:

```python

@TaskGenerator
def gc_fraction(c):
    gcf = c.eval('GCf = (G+C)/(G+C+T+A)')['GCf']
    return gcf.describe()

@TaskGenerator
def build_table(partials):
    return pd.DataFrame(partials).T
```

It is best if Jug functions are [pure
functions](https://en.wikipedia.org/wiki/Pure_function).

This is not strictly necessary, but you need to start watching out if they're
not. Writing out files is not a problem, though, unless other tasks depend on them.

```python
@TaskGenerator
def plot_results(data):
    from matplotlib import pyplot as plt
    from matplotlib import style
    style.use('default')

    data = data.rename(index=lambda ix: ix.split('/')[1].split('.')[1], )
    data = data.sort_values(by='mean')

    fig,ax = plt.subplots()
    ax.plot(data['25%'], label='Q1')
    ax.plot(data['50%'], label='Q2')
    ax.plot(data['75%'], label='Q3')
    ax.legend(loc='best')

    ax.set_ylabel('GC fraction')
    ax.set_xlabel('Habitat')

    for x in ax.get_xticklabels():
        x.set_rotation(90)

    fig.tight_layout()
    fig.savefig('gc-per-habitat-jugfile.pdf')
```

Until now, we have only defined functions, now we start actually setting up the computation:

```python
ifiles = glob('demo-data/*.fna.gz')
ifiles.sort()
```
We sort the files so that they are processed in the same order every time (not
strictly needed, but simplifies a lot of logic/debugging).


```python

partials = {}
for i, fna in enumerate(ifiles):
    ofile = f'outputs/chunk{i:02}.tsv'
    ofile = process(fna, ofile)
    partials[fna] = gc_fraction(ofile)

final = build_table(partials)
plot_results(final)
```

## Potential improvements/changes

### Write the tables to intermediate files

Instead of returning the DataFrame in `process`, we can save it to disk and
return the path. As mentioned above, this can be error prone, but it can work
if done correctly. A few tips:

1. Make the results filename depend on the input filename
2. Return the results filename from the function that generates it

```python
@TaskGenerator
def process(fna):
    from collections import Counter
    from fasta import fasta_iter
    from time import sleep
    from os import makedirs, path
    sleep(4) # Pretend we are doing a lot of work

    makedirs('outputs', exist_ok=True)
    ofile = path.join('outputs',
            fna.split('/')[-1].replace('.fna.gz', '.tsv.gz'))

    r = []
    hs = []
    for h,seq in fasta_iter(fna):
        r.append(pd.Series(Counter(seq)))
        hs.append(h)
    r = pd.DataFrame(r, index=hs)
    r.to_csv(ofile, sep='\t')
    return ofile
@TaskGenerator
def gc_fraction(counts_fname):
    c = pd.read_table(counts_fname, index_col=0)
    gcf = c.eval('GCf = (G+C)/(G+C+T+A)')['GCf']
    return gcf.describe()

...
partials = {}
for i, fna in enumerate(ifiles):
    ofile = process(fna)
    partials[fna] = gc_fraction(ofile)
```

### Use `cached_glob`

The combination of `glob` and `sort` that we have at the top of the file is
very common:

```python
ifiles = glob('demo-data/*.fna.gz')
ifiles.sort()
```

In a large directory (particularly on a network) it can also be very slow (up
to 10s of seconds). `cached_glob` deals with this:

```python
from jug.utils import cached_glob

ifiles = cached_glob('demo-data/*.fna.gz')
```

