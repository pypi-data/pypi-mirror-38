import argparse
import martyr
import math
import os


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gb", "--gb-threshold", type=float, default=math.inf)
parser.add_argument("-p", "--pc", "--pc-threshold", type=int, default=math.inf)

parser.add_argument("pid", type=int)

args = parser.parse_args()


def callback(usedmem, **kwargs):
    print(usedmem/1e9)


martyr._watcher(pid=args.pid,
                callback=callback,
                gb_threshold=args.gb,
                pc_threshold=args.pc,
                kbint=True
                )