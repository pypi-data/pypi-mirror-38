import numpy as np
import quaternion
import tracemalloc # requires python 3.6

tracemalloc.start()

def doit():
    q = np.quaternion(0.1, 0.1, 0.1, 0.1)
    qa = quaternion.as_quat_array([1.0] * 100000000)
    x = q * qa # THIS IS THE PROBLEMATIC LINE.

def snapshot_trace():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

snapshot_trace()
doit()
snapshot_trace()
doit()
snapshot_trace()

# just here so you can check memory usage while this runs.
while True:
    pass
