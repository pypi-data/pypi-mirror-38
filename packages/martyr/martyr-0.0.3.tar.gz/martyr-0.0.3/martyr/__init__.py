#!/usr/bin/env python3
from multiprocessing import Process
from subprocess import run, PIPE
import psutil
import time
import math
import sys
import os


kill_message = """\
Process {pid} has been killed because it was using {gb:.1f}Gb of RAM ({ratio:.0%} of physical memory) while it was capped to {gb_threshold}Gb ({pc_threshold}%)
{cmdline}
"""


def _watcher(pid, *, gb_threshold, pc_threshold, callback, kbint=True):
    ps = psutil.Process(pid)
    totalmem = psutil.virtual_memory().total
    while ps.is_running():
        try:
            processes = [ps, *(c for c in ps.children(recursive=True))]
            usedmem = _get_memory_usage(processes)
            ratio = usedmem / totalmem
            gb = usedmem / 1e9
            if gb >= gb_threshold or 100*ratio >= pc_threshold:
                with open("martyr.log", "a") as f:
                    f.write(kill_message.format(**locals(),
                                                cmdline=" ".join(ps.cmdline())
                                                )
                            )
                ps.terminate()
                break
            if callback is not None:
                callback(**locals())
            time.sleep(1)
        except KeyboardInterrupt:
            if kbint:
                raise


def _get_memory_usage(processes):
    occ = 0
    for p in processes:
        occ += p.memory_info().rss
    return occ


def watch(gb_threshold=math.inf, pc_threshold=math.inf, kbint=False):
    if getattr(watch, "_done", False):
        return
    setattr(watch, "_done", True)
    kwargs = locals().copy()
    pid = os.getpid()
    kwargs["pid"] = pid
    kwargs["callback"] = None
    p = Process(target=_watcher, kwargs=kwargs, daemon=True)
    p.start()


def get_free_gpus():
    proc = run(r'''nvidia-smi -q -d PIDS | grep "Processes"''', shell=True, stdout=PIPE)
    result = proc.stdout.decode("utf-8")
    result = result.split("\n")
    free_gpus = [i for i, res in enumerate(result) if res.endswith(": None")]
    return free_gpus


def set_visible_gpu(preferred=None):
    free_gpus = get_free_gpus()
    if free_gpus:
        if preferred in free_gpus:
            gpu = preferred
            print("Choosing preferred GPU {}"
                  .format(gpu), file=sys.stderr)
        elif preferred is None:
            gpu = free_gpus[0]
            print("No GPU preferred, choosing first available GPU: {}"
                  .format(gpu), file=sys.stderr)
        else:
            gpu = free_gpus[0]
            print("Preferred GPU {} not available, choosing first available GPU: {}"
                  .format(preferred, gpu), file=sys.stderr)
    else:
        if preferred is not None:
            gpu = preferred
            print("No free GPU was found, still trying on {}"
                  .format(gpu), file=sys.stderr)
        else:
            raise Exception("No free GPU was found and no preference was set, please set one to at least try.")
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)
    return gpu
