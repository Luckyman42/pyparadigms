import psutil
import sys

MAX_MB = 500

rss = psutil.Process().memory_info().rss / (1024**2)

# ha túl sok memória → failed probe → K8s restartolja a Pod-ot
if rss > MAX_MB:
    sys.exit(1)

sys.exit(0)
