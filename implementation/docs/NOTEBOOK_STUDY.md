# CSV study: 200 datasets, 12 cases, 10 seeds, 80 iterations

Configuration: configs/notebook_study.json. The new study has not started.

Inputs: 40 CSVs each at 100, 200, 300, 400, 500 users. Selection and renaming records: data/dataset_selection_200.json and data/dataset_renaming_200.csv. All 200 datasets have matching views.

Cases: GA, PSO, H-PSO-GA, H-WOA-PSO, WOA, WOA-K, WOA-O, WOA-L, WOA-KO, WOA-KL, WOA-OL, I-WOA (WOA-KOL). Only WOA has K/O/L variants.

Each run uses population 25, four UAVs, 80 iterations and 81 history checkpoints (0 through 80). Total: 200 x 12 x 10 = 24,000 tasks; 120 per dataset. Equal iterations do not imply equal fitness evaluations (FE). Reports include observed FE and runtime.

Run only when requested by the user:

```powershell
python implementation/scripts/run_notebook_study.py --workers 4
```

Notebook: implementation/notebooks/full_study_80_iterations.ipynb (CONFIRM_RUN=False by default).
Output: implementation/results/study_80_iterations.

Progress and logs are in the output directory. Resume requires matching source, configuration, data and worker count. Final tables and reports require all paired tasks. Do not rank an incomplete study.
