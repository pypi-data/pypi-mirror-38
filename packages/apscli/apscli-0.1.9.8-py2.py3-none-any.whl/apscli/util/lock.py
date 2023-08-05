# encoding=utf-8
import functools
import fcntl
import os

def lock_method(lock_filename):
    ''' Use an OS lock such that a method can only be called once at a time. '''

    def decorator(func):

        @functools.wraps(func)
        def lock_and_run_method(*args, **kwargs):

            # Only run this program if it's not already running
            # Snippet based on
            # http://linux.byexamples.com/archives/494/how-can-i-avoid-running-a-python-script-multiple-times-implement-file-locking/
            fd = None
            try:
                fd = os.open(lock_filename, os.O_CREAT | os.O_RDWR)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return func(*args, **kwargs)
            except IOError:
                raise SystemExit(
                    "This program is already running.  Please stop the current process or " +
                    "remove " + lock_filename + " to run this script."
                )
            finally:
                if fd is not None:
                    fcntl.flock(fd, fcntl.LOCK_UN)

        return lock_and_run_method

    return decorator 