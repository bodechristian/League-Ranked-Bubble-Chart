import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os


class C:
    def __init__(self, r, lbls):
        print(r)

        r = np.asarray(r)
        max_freq = r.max()
        normalize_value = 1.2
        r = r/normalize_value + max_freq*((normalize_value-1)/normalize_value)
        print(r)
        self.lbls = lbls
        self.N = len(r)
        self.x = np.ones((self.N, 3))
        self.x[:, 2] = r
        maxstep = 2*self.x[:, 2].max()
        length = np.ceil(np.sqrt(self.N))
        grid = np.arange(0, length*maxstep, maxstep)
        gx, gy = np.meshgrid(grid, grid)
        self.x[:, 0] = gx.flatten()[:self.N]
        self.x[:, 1] = gy.flatten()[:self.N]
        self.x[:, :2] = self.x[:, :2] - np.mean(self.x[:, :2], axis=0)

        self.step = self.x[:, 2].min()
        self.p = lambda x, y: np.sum((x**2+y**2)**2)
        self.E = self.energy()
        self.iter = 1.

    def minimize(self):
        while self.iter < 1000*self.N:
            for i in range(self.N):
                rand = np.random.randn(2)*self.step/self.iter
                self.x[i, :2] += rand
                e = self.energy()
                if e < self.E and self.isvalid(i):
                    self.E = e
                    self.iter = 1.
                else:
                    self.x[i, :2] -= rand
                    self.iter += 1.

    def energy(self):
        return self.p(self.x[:, 0], self.x[:, 1])

    @staticmethod
    def distance(x1, x2):
        return np.sqrt((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) - x1[2] - x2[2]

    def isvalid(self, i):
        for j in range(self.N):
            if i != j:
                if C.distance(self.x[i, :], self.x[j, :]) < 0:
                    return False
        return True

    def plot(self, ax):
        for i in range(self.N):
            x, y, rad = self.x[i, 0], self.x[i, 1], self.x[i, 2]
            im = ax.imshow(plt.imread(os.path.join("assets", self.lbls[i]+".png")), extent=[x-rad, x+rad, y-rad, y+rad])
            circ = patches.Circle((x, y), radius=rad, transform=ax.transData)
            im.set_clip_path(circ)

