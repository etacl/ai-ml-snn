import numpy as np
from config import LIF_PARAMS

class LIFNeuron:
    def __init__(self):
        self.tau_m = LIF_PARAMS['tau_m']
        self.v_thresh = LIF_PARAMS['v_thresh']
        self.v_reset = LIF_PARAMS['v_reset']
        self.v_rest = LIF_PARAMS['v_rest']
        self.tau_refrac = LIF_PARAMS['tau_refrac']

        self.v_mem = self.v_rest
        self.refractory_time = 0.0
        self.spike = False

    def update(self, i_in, dt=1.0):
        self.spike = False
        if self.refractory_time > 0:
            self.refractory_time -= dt
            return self.spike

        # Leaky integrate
        dv = (-(self.v_mem - self.v_rest) + i_in) / self.tau_m * dt
        self.v_mem += dv

        # Check for spike
        if self.v_mem >= self.v_thresh:
            self.spike = True
            self.v_mem = self.v_reset
            self.refractory_time = self.tau_refrac

        return self.spike
