# GC counting

The goal is to start with `jugfile.py` and modify it to resemble `jugfile2.py`,
then `jugfile3.py`, and finally `jugfile4.py`.

Step by step

1. Run `jug execute`.
2. Run `mkdir outputs` and re-run `jug execute`.
3. **Overwrite** `jugfile.py` with `jugfile2.py` by running `cp jugfile2.py jugfile.py`
This simulates editing the code in `jugfile.py`
4. `jug execute`
5. `cp jugfile3.py jugfile.py`
6. `jug execute`
7. `cp jugfile4.py jugfile.py`
8. `jug execute`

The files `LoadingFromJupyter.ipynb` and `plot-results.py` show how to load jug
results from standard Python/Jupyter

