# GC counting

The goal is work through 4 successive versions of `jugfile.py` (named
`jugfile1.py`, `jugfile2.py`...)

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

