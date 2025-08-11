import numpy as np
from snn.neuron import LIFNeuron
from config import *

class SNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Create neuron populations
        self.hidden_layer = [LIFNeuron() for _ in range(hidden_size)]
        self.output_layer = [LIFNeuron() for _ in range(output_size)]

        # Initialize weights
        # Glorot initialization
        limit_ih = np.sqrt(6.0 / (input_size + hidden_size))
        limit_ho = np.sqrt(6.0 / (hidden_size + output_size))

        self.w_ih = np.random.uniform(-limit_ih, limit_ih, (hidden_size, input_size))
        self.w_ho = np.random.uniform(-limit_ho, limit_ho, (output_size, hidden_size))

    def update(self, input_spikes, dt=1.0):
        # Input to hidden layer
        i_hidden = np.dot(self.w_ih, input_spikes)

        hidden_spikes = np.array([neuron.update(i_hidden[i], dt) for i, neuron in enumerate(self.hidden_layer)])

        # Hidden to output layer
        i_output = np.dot(self.w_ho, hidden_spikes)

        output_spikes = np.array([neuron.update(i_output[i], dt) for i, neuron in enumerate(self.output_layer)])

        return output_spikes

    def reset(self):
        for neuron in self.hidden_layer:
            neuron.v_mem = neuron.v_rest
            neuron.refractory_time = 0
        for neuron in self.output_layer:
            neuron.v_mem = neuron.v_rest
            neuron.refractory_time = 0
