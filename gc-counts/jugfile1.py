from glob import glob
from jug import TaskGenerator

@TaskGenerator
def process(fna):
    from collections import Counter
    import pandas as pd
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

ifiles = glob('demo-data/*.fna.gz')
ifiles.sort()

partials = []
for i, fna in enumerate(ifiles):
    p = process(fna)
    partials.append(p)
