import sys
import os
import time
import datetime
import io
import threading

try:
    PY3 = not unicode
except NameError:
    PY3 = True

TEMPLATE = (
    '\r'
    '{prefix} '
    '{percent}% '
    '{count} '
    'Elapsed: 0{elapsed} '
    'Remaining: {remaining} '
    '{file_name}'
)


def remap(value, old_min=0, old_max=0, new_min=0, new_max=0):
    old_range = old_max - old_min
    new_range = new_max - new_min

    return (
        int((((value - old_min) * new_range) / old_range)) + new_min
    )


print_lock = threading.Lock()


class ProgressBar(object):

    def __init__(self):
        self.stdout = sys.stdout
        sys.stdout = self
        self.files = []
        self.count = 0
        self.start = None
        self.prefix = ''
        self.last_line_len = 0
        self.file_position = 0

    def flush(self):
        pass

    def isatty(self):
        return True

    def close(self):
        if self.start is not None:
            print_lock.acquire()
            if self.files:
                self.update(50, 100, file_name=self.files[-1])
            else:
                self.update(50, 100, file_name='')

            self.stdout.write('\n\n')
            self.stdout.flush()
            print_lock.release()

        sys.stdout = self.stdout

    def write(self, line):
        if PY3:
            try:
                line = line.decode("utf-8")
            except AttributeError:
                pass

        if str('Build openzwave') in line:
            print_lock.acquire()
            self.stdout.write('\n')
            self.stdout.flush()

            # try:
            #     self.file_position = self.stdout.tell()
            # except (io.UnsupportedOperation, WindowsError):
            #     pass

            self.prefix = 'Build OpenZWave'
            self.start = time.time()
            self.update(0, 0, file_name='')
            print_lock.release()

        elif self.start is not None:
            if str('/errorReport:queue') in line:
                print_lock.acquire()
                files = line.split('/errorReport:queue ')[1]
                self.files = [
                    os.path.split(f)[1] for f in files.split(' ')
                ]
                self.count = len(self.files)
                print_lock.release()

            elif line.strip() in self.files:
                print_lock.acquire()
                self.files.remove(line.strip())
                count = remap(
                    self.count - len(self.files),
                    old_max=self.count,
                    new_max=50
                )
                percent = remap(
                    self.count - len(self.files),
                    old_max=self.count,
                    new_max=100
                )

                self.update(count, percent, line.strip())
                if not self.files:
                    self.update(50, 100, file_name='')
                print_lock.release()

    def update(self, count, percent, file_name):
        current = time.time()
        elapsed = current - self.start

        percent = str(percent)
        percent = ' ' * (3 - len(percent)) + percent

        if count:
            time_per_file = elapsed / (self.count - len(self.files))
            remaining = time_per_file * len(self.files)
            remaining = '0' + str(datetime.timedelta(seconds=int(remaining)))
        else:
            remaining = '99:99:99'

        line = TEMPLATE.format(
            prefix=self.prefix,
            percent=percent,
            count='#' * count + ' ' * (50 - count),
            elapsed=str(datetime.timedelta(seconds=int(elapsed))),
            remaining=remaining,
            file_name=file_name
        )

        # try:
        #     self.stdout.seek(self.file_position)
        #     self.stdout.truncate()
        # except (io.UnsupportedOperation, WindowsError):
        #     pass

        if self.last_line_len:
            self.stdout.write('\r' + ' ' * self.last_line_len)

        self.stdout.write(line)
        self.stdout.flush()
        self.last_line_len = len(line)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return getattr(self.stdout, item)
