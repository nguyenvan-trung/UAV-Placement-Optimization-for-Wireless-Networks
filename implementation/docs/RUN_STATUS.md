# Study status

Stopped at the user request. All generated study results, pipeline-check artifacts, logs, checkpoints, and temporary audit outputs have been deleted as requested.

No study coordinator or workers remain running. There is no completed study or final ranking to report. Previous run progress is no longer available.

The 500 original CSV datasets in `data/stores` are unchanged (verified using SHA-256 before and after cleanup). Configuration is preserved: 30 cases, 30 seeds, 100 iterations, population 25, and 4 UAVs.

Notebook execution remains disabled by default. Do not restart the study without a new user instruction. A future run will start from scratch because all checkpoints were deleted.

- [Run instructions](../../REPRODUCE.md)
- [Reading future results](../results/READING_RESULTS.md)
- [Data guide](../../data/README.md)
