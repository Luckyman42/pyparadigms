| Fogalom | Mit jelent? | Oktatási példa |
|---------|------------|----------------|
| Pickle | Objektum sorosítás Pythonban | ProcessPoolExecutor minden argumentum és return érték picklezve megy |
| Overhead | Idő, ami a sorosítás/deszerializálás miatt megy el | Nagy listák, dict-ek, numpy array-k átadása |
| Optimalizálás | Shared memory, long-running worker, csak szükséges adatok | multiprocessing.shared_memory vagy job queue |

