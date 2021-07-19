import pandas as pd

from jug.utils import glob_sort
from jug import TaskGenerator

@TaskGenerator
def process(fna, ofile):
    from collections import Counter
    from fasta import fasta_iter
    from time import sleep
    sleep(4) # Pretend we are doing a lot of work

    r = []
    hs = []
    with open(ofile, 'wt') as out:
        for h,seq in fasta_iter(fna):
            r.append(pd.Series(Counter(seq)))
            hs.append(h)
    r = pd.DataFrame(r, index=hs)
    r.to_csv(ofile, sep='\t')
    return ofile

@TaskGenerator
def gc_fraction(c):
    c = pd.read_table(c, index_col=0)
    gcf = c.eval('GCf = (G+C)/(G+C+T+A)')['GCf']
    return gcf.describe()

@TaskGenerator
def build_table(partials):
    return pd.DataFrame(partials).T

ifiles = glob_sort('demo-data/*.fna.gz')

partials = {}
for i, fna in enumerate(ifiles):
    ofile = f'outputs/chunk{i:02}.tsv'
    process(fna, ofile)
    partials[fna] = gc_fraction(ofile)

final = build_table(partials)
