import os
import time


def heartbeat(timeout, operation="alert"):
    base_dir = '/kml/log'
    heartbeat_file_name = 'heartbeats.log'
    heartbeat_file_Path = os.path.join(base_dir, heartbeat_file_name)
    with open(heartbeat_file_Path, 'a') as f:
        f.write("%d %d %s\n" % (time.time(), timeout, operation))
