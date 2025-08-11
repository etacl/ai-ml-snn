import numpy as np
from snn.network import SNN
from config import *

class AIController:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake
        self.snn = SNN(INPUT_NEURONS, HIDDEN_NEURONS, OUTPUT_NEURONS)

    def get_action(self):
        # 1. Encode game state into input currents
        input_currents = self._encode_state()

        # 2. Simulate SNN for a number of timesteps
        output_spike_counts = np.zeros(OUTPUT_NEURONS)
        self.snn.reset() # Reset neuron states before a new decision
        for _ in range(TIMESTEPS):
            input_spikes = input_currents > np.random.rand(INPUT_NEURONS) * 20.0 # Simple rate encoding
            output_spikes = self.snn.update(input_spikes)
            output_spike_counts += output_spikes

        # 3. Decode output spikes into an action
        action = self._decode_spikes(output_spike_counts)

        # 4. Convert action to a new direction
        return self._get_new_direction(action)

    def _encode_state(self):
        head = self.snake.get_head()
        food = self.game.food
        other_snake = self.game.snake1 if self.snake == self.game.snake2 else self.game.snake2

        # Input features
        food_up = 1.0 if food[1] < head[1] else 0.0
        food_down = 1.0 if food[1] > head[1] else 0.0
        food_left = 1.0 if food[0] < head[0] else 0.0
        food_right = 1.0 if food[0] > head[0] else 0.0

        danger_up = self._is_danger((head[0], head[1] - 1), other_snake)
        danger_down = self._is_danger((head[0], head[1] + 1), other_snake)
        danger_left = self._is_danger((head[0] - 1, head[1]), other_snake)
        danger_right = self._is_danger((head[0] + 1, head[1]), other_snake)

        # Convert features to input currents
        currents = np.array([
            food_up, food_down, food_left, food_right,
            danger_up, danger_down, danger_left, danger_right
        ]) * 20.0  # Scale to a reasonable current value

        return currents

    def _is_danger(self, pos, other_snake):
        # Check wall collision
        if not (0 <= pos[0] < GRID_WIDTH and 0 <= pos[1] < GRID_HEIGHT):
            return 1.0
        # Check self collision
        if pos in self.snake.body:
            return 1.0
        # Check other snake collision
        if pos in other_snake.body:
            return 1.0
        return 0.0

    def _decode_spikes(self, spike_counts):
        if np.sum(spike_counts) == 0:
            return 1 # Default to going straight if no spikes

        return np.argmax(spike_counts) # 0: left, 1: straight, 2: right

    def _get_new_direction(self, action):
        # 0: turn left, 1: go straight, 2: turn right
        current_dir = self.snake.direction

        if action == 1: # Go straight
            return current_dir

        dx, dy = current_dir
        if action == 0: # Turn left
            new_dir = (dy, -dx)
        else: # Turn right (action == 2)
            new_dir = (-dy, dx)

        return new_dir
