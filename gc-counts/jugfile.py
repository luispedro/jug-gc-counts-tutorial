from glob import glob
from jug import TaskGenerator

@TaskGenerator
def process(fna, ofile):
    from collections import Counter
    import pandas as pd
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

ifiles = glob('demo-data/*.fna.gz')
ifiles.sort()

ofiles = []
for i, fna in enumerate(ifiles):
    ofile = f'outputs/chunk{i:02}.tsv'
    process(fna, ofile)
    ofiles.append(ofile)
