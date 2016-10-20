from __future__ import division
import math
import os
import sys
import time


class ResponsiveTerminalApplication:
    i = 0
    rows = 80
    columns = 50


    def __init__(self, fps=30, timeout=float('+inf')):
        self.quantum = 1 / fps
        self.timeout = timeout

    def update_dims(self):
        o = os.popen('stty size', 'r').read().split()
        self.rows = int(o[0])
        self.columns = int(o[1])

    def run(self):
        while self.i < self.timeout:
            self.i += 1
            self.update_dims()
            self.update()
            time.sleep(self.quantum)


class ResponsivePrintDoer(ResponsiveTerminalApplication):
    """
    every n frames per second, print a thing returned by the function self.get_line()
    """
    def update(self):
        print(self.get_text())


class ResponsiveSysStdOutDoer(ResponsiveTerminalApplication):
    """
    every n frames per second, print a thing returned by the function self.get_line()
    """
    def update(self):
        sys.stdout.write(self.get_text())


class ResponsiveWave(ResponsivePrintDoer):
    # chars, quots = ['_', '.', '-', '\''], [ 8, 16, 4]

    # chars, quots = (['#', '/', '#', '-', '#', '.', '#'],
    #                 [10, 11, 12, 13, 14, 15])

    chars, quots = (['.', ' ', ',', 'x', '-'],
                    [100, 150, 200, 10])

    def __init__(self, *args, **kwargs):
        chars = kwargs.pop('chars', None)
        if chars:
            self.chars = chars
        quots = kwargs.pop('quots', None)
        if quots:
            self.quots = quots

        super().__init__(*args, **kwargs)

    def get_text(self):
        nums = []
        for q in self.quots:
            k = math.sin(self.i / q) + 1
            n = int(k * (self.columns/2))
            nums.append(n)

        nums.sort()
        nums.append(self.columns)
        locs = []
        for i in range(len(nums)):
            q = nums[i]
            if i > 0:
                q -= nums[i-1]
            locs.append(q)

        return ''.join([char * n for char,n in zip(self.chars, locs)])

class ResponsiveCaveOfDreams(ResponsiveSysStdOutDoer):
    chars, quots = ['/','\\','#','.'], [1, 2, 5]


    def get_text(self):
        k = (math.sin(self.i / 4) + 1) * 100

        lines = []
        for i in range(self.rows):
            l = []
            for j in range(self.columns):
                e = j * i
                cc = self.chars[-1]
                for c, q in zip(self.chars, self.quots):
                    if e > q*k:
                        cc = c
                l.append(cc)
            lines.append(l)

        return '\n'.join([''.join(l) for l in lines])

playlist = [
    (ResponsiveWave, {
        'chars': ['-', ' ', '#'],
        'quots': [8, 16],
        'timeout': 30,
    }),
    (ResponsiveWave, {
        'chars': ['-', ' ', '#', '_'],
        'quots': [8, 16, 2],
        'timeout': 120,
    }),
    (ResponsiveCaveOfDreams, {
        'timeout': 20,
    }),
]

if __name__=='__main__':
    while True:
        for c, args in playlist:
            resp_obj = c(**args)
            resp_obj.run()
