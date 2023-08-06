import sys
import threading
import time


class Bullets:

    @staticmethod
    def spinning_cursor():
        c = [
            "[-    ]",
            "[ -   ]",
            "[  -  ]",
            "[   - ]",
            "[    -]",
            "[   - ]",
            "[  -  ]",
            "[ -   ]"
        ]
        while 1: 
            for cursor in c:
                yield cursor

    def __init__(self, msg="Working on it..."):
        self.spinner_generator = self.spinning_cursor()
        self.busy = False
        self.delay = 0.1
        self.msg = msg
        self.linelen = len(msg) + 8

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(
                "{0} {1}".format(
                    next(self.spinner_generator),
                    self.msg
                )
            )
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\r')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)
        spacers = " " * self.linelen
        sys.stdout.write("\r{0}\r".format(spacers))
