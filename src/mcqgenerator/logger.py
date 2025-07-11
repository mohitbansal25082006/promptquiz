import logging
import os
from datetime import datetime

# Create a unique log filename with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the directory to save log files
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# Full path to the log file
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE_PATH,
    filemode="a",  # append mode
    format="[%(asctime)s] [%(levelname)s] %(name)s (%(lineno)d): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Optionally also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)
