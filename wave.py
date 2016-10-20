import math
import os
import time


class ResponsiveTerminalApplication:
    i = 0
    rows = 80
    columns = 50


    def __init__(self, fps=30):
        self.quantum = 1 / fps

    def update_dims(self):
        o = os.popen('stty size', 'r').read().split()
        self.rows = int(o[0])
        self.columns = int(o[1])

    def run(self):
        while True:
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


class ResponsiveWave2(ResponsivePrintDoer):
    # chars, quots = ['_', '.', '-', '\''], [ 8, 16, 4]

    # chars, quots = (['#', '/', '#', '-', '#', '.', '#'],
    #                 [10, 11, 12, 13, 14, 15])

    chars, quots = (['.', ' ', ',', 'x', '-'],
                    [100, 150, 200, 10])

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


if __name__=='__main__':
    t = ResponsiveWave2(fps=30)
    t.run()
