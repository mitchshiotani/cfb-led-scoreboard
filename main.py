from datetime import datetime, timedelta
from src.data.scoreboard_config import ScoreboardConfig
from src.renderers.main import MainRenderer
from src.infra.rgb_matrix_wrapper import RGBMatrix, RGBMatrixOptions
from src.utils import args, led_matrix_options
from src.data.data import Data
# import renderers.standings
from src.api.cfb import FootballAPIWrapper as cfbgame
import debug
import os

SCRIPT_NAME = "CFB LED Scoreboard"
SCRIPT_VERSION = "4.0.1"

# Get supplied command line arguments
args = args()

# Check for led configuration arguments
matrixOptions = led_matrix_options(args)

# Initialize the matrix
matrix = RGBMatrix(options = matrixOptions)

# Print some basic info on startup
debug.info("{} - v{} ({}x{})".format(SCRIPT_NAME, SCRIPT_VERSION, matrix.width, matrix.height))

# Read scoreboard options from config.json if it exists
script_dir = os.path.dirname(os.path.abspath(__file__))
config = ScoreboardConfig(f'{script_dir}/config', matrix.width, matrix.height)
debug.set_debug_status(config)

# Create a new data object to manage the CFB data
# This will fetch initial data from CFB
data = Data(config)

MainRenderer(matrix, data).render()
