"""Windows process-tree caps, narrowly adapted from the original Omega runner.

The physical model and numerical queries do not depend on this platform wrapper.
"""

import ctypes
import os
import stat
import subprocess
import time
from ctypes import wintypes as w
from pathlib import Path


def tree_bytes(root):
    """Atomic writers may move a temporary file between enumeration and stat."""
    total = 0
    for path in root.rglob("*"):
        try:
            info = path.stat()
        except FileNotFoundError:
            continue
        if stat.S_ISREG(info.st_mode):
            total += info.st_size
    return total


def capped(command, out, seconds=120, memory=1024**3, output_cap=256 * 1024**2, *, cwd):
    if os.name != "nt":
        raise RuntimeError("Windows Job Object required by this runner")
    out = Path(out)
    if not out.is_dir() or seconds <= 0 or memory <= 0 or output_cap <= 0:
        raise ValueError("Existing output directory and positive caps required")

    class Basic(ctypes.Structure):
        _fields_ = [
            ("process_time", ctypes.c_longlong),
            ("job_time", ctypes.c_longlong),
            ("flags", w.DWORD),
            ("min_ws", ctypes.c_size_t),
            ("max_ws", ctypes.c_size_t),
            ("active", w.DWORD),
            ("affinity", ctypes.c_size_t),
            ("priority", w.DWORD),
            ("scheduling", w.DWORD),
        ]

    class IO(ctypes.Structure):
        _fields_ = [
            (n, ctypes.c_ulonglong)
            for n in (
                "read_ops",
                "write_ops",
                "other_ops",
                "read_bytes",
                "write_bytes",
                "other_bytes",
            )
        ]

    class Extended(ctypes.Structure):
        _fields_ = [
            ("basic", Basic),
            ("io", IO),
            ("process_memory", ctypes.c_size_t),
            ("job_memory", ctypes.c_size_t),
            ("peak_process", ctypes.c_size_t),
            ("peak_job", ctypes.c_size_t),
        ]

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
    k.CreateJobObjectW.restype = w.HANDLE
    k.SetInformationJobObject.argtypes = [
        w.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        w.DWORD,
    ]
    k.QueryInformationJobObject.argtypes = [
        w.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        w.DWORD,
        ctypes.c_void_p,
    ]
    k.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
    k.TerminateJobObject.argtypes = [w.HANDLE, w.UINT]
    k.CloseHandle.argtypes = [w.HANDLE]
    job = k.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    limits = Extended()
    limits.basic.flags = 0x200 | 0x2000  # job memory + kill on close
    limits.job_memory = memory
    child = None
    start = time.perf_counter()
    reason = None
    try:
        if not k.SetInformationJobObject(
            job, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        env = os.environ.copy()
        for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
            env[key] = "1"
        with (out / "worker.log").open("w", encoding="utf-8") as log:
            child = subprocess.Popen(
                command,
                cwd=cwd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            if not k.AssignProcessToJobObject(job, w.HANDLE(int(child._handle))):
                child.kill()
                child.wait()
                raise ctypes.WinError(ctypes.get_last_error())
            child.stdin.write("GO\n")
            child.stdin.flush()
            child.stdin.close()
            while child.poll() is None:
                if time.perf_counter() - start > seconds:
                    reason = "wall_cap"
                size = tree_bytes(out)
                if size > output_cap:
                    reason = "output_cap"
                if reason:
                    k.TerminateJobObject(job, 124)
                    child.wait()
                    break
                time.sleep(0.1)
        measured = Extended()
        ok = k.QueryInformationJobObject(
            job, 9, ctypes.byref(measured), ctypes.sizeof(measured), None
        )
        final_bytes = tree_bytes(out)
        if final_bytes > output_cap:
            reason = "output_cap"
        return {
            "exit_code": child.returncode,
            "cap_reason": reason,
            "wall_seconds": time.perf_counter() - start,
            "wall_cap_seconds": seconds,
            "job_memory_cap_bytes": memory,
            "peak_job_bytes": measured.peak_job if ok else None,
            "output_bytes": final_bytes,
        }
    finally:
        if child is not None and child.poll() is None:
            k.TerminateJobObject(job, 125)
            child.wait()
        k.CloseHandle(job)
