import math
import numpy as np
import time

class CPGN:
    def __init__(self, name, t1, t2, w, b, u0, ue, uf, ve, vf):
        self.name = name

        self.t1 = t1
        self.t2 = t2
        self.w = w
        self.b = b
        self.u0 = u0

        self.ue_init = ue
        self.uf_init = uf
        self.ve_init = ve
        self.vf_init = vf

        self.ue = ue
        self.uf = uf
        self.ve = ve
        self.vf = vf

        self.ue_n = 0
        self.uf_n = 0
        self.ve_n = 0
        self.vf_n = 0

        self.y = 0

        self.connected_cpgn = []

    def connect(self, cpgn, w):
        self.connected_cpgn.append([cpgn, w])

    def euler(self, dt):
        if self.t1 == 0:
            return
        if self.t2 == 0:
            return
        fue = -self.ue + self.w * max(0, self.uf) - self.b * self.ve + self.u0
        fuf = -self.uf + self.w * max(0, self.ue) - self.b * self.vf + self.u0
        for [cpgn, w] in self.connected_cpgn:
            fue += w * max(0, cpgn.ue)
            fuf += w * max(0, cpgn.uf)
        fve = -self.ve + max(0, self.ue)
        fvf = -self.vf + max(0, self.uf)
        self.ue_n = self.ue + dt * fue / self.t1
        self.uf_n = self.uf + dt * fuf / self.t1
        self.ve_n = self.ve + dt * fve / self.t2
        self.vf_n = self.vf + dt * fvf / self.t2

    def step(self):
        self.ue = self.ue_n
        self.uf = self.uf_n
        self.ve = self.ve_n
        self.vf = self.vf_n
        self.y = -max(0, self.ue) + max(0, self.uf)

    def reset(self):
        self.ue_init = self.ue_init
        self.uf_init = self.uf_init
        self.ve_init = self.ve_init
        self.vf_init = self.vf_inti
        self.y = 0