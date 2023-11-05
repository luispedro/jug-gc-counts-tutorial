import pandas as pd
from glob import glob

from jug import TaskGenerator

@TaskGenerator
def process(fna):
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

@TaskGenerator
def gc_fraction(c):
    gcf = c.eval('GCf = (G+C)/(G+C+T+A)')['GCf']
    return gcf.describe()

@TaskGenerator
def build_table(partials):
    return pd.DataFrame(partials).T

ifiles = glob('demo-data/*.fna.gz')
ifiles.sort()

partials = {}
for i, fna in enumerate(ifiles):
    per_seq = process(fna)
    partials[fna] = gc_fraction(per_seq)

final = build_table(partials)

