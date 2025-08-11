# Game settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Snake settings
SNAKE_INITIAL_LENGTH = 3
SNAKE_INITIAL_POS = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
SNAKE_INITIAL_DIR = (1, 0) # Right

# SNN settings
# We will fill this in later
INPUT_NEURONS = 8  # Example: 4 directions for food, 4 for wall/self
HIDDEN_NEURONS = 10
OUTPUT_NEURONS = 3  # Turn left, right, or go straight
TIMESTEPS = 100 # ms, simulation time for one decision
LIF_PARAMS = {
    'tau_m': 10.0,  # Membrane time constant
    'v_thresh': -50.0, # Spike threshold
    'v_reset': -65.0,  # Reset potential
    'v_rest': -65.0,   # Resting potential
    'tau_refrac': 5.0 # Refractory period
}
