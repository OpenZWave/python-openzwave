
import sys
import threading
import subprocess
from distutils import log

PIPE = subprocess.PIPE


def Popen(command, stdout, stderr, cwd=None):
    if cwd is None:
        proc = subprocess.Popen(
            command,
            stdout=stdout,
            stderr=stderr
        )
    else:
        proc = subprocess.Popen(
            command,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd
        )

    event = threading.Event()
    res = [True]

    def stream_watcher(identifier, stream):
        dot = False
        while proc.poll() is None:
            line = stream.readline()
            if (
                line.strip() and
                identifier == 'STDERR' and
                'Visual C++ Package' not in line and
                'Microsoft' not in line
            ):
                log.error('{0}\n'.format(line))
                if dot:
                    sys.stdout.write('\n')
                    dot = False
                sys.stderr.write(line)
                res[0] = False
            elif line.strip():
                dot = True
                sys.stdout.write('.')

        if not stream.closed:
            stream.close()
        if dot:
            sys.stdout.write('\n')

        event.set()

    out_t = threading.Thread(
        target=stream_watcher,
        name='stdout-watcher',
        args=('STDOUT', proc.stdout)
    )
    err_t = threading.Thread(
        target=stream_watcher,
        name='stderr-watcher',
        args=('STDERR', proc.stderr)
    )

    out_t.daemon = True
    err_t.daemon = True

    out_t.start()
    err_t.start()

    event.wait()

    out_t.join()
    err_t.join()

    return res[0]
