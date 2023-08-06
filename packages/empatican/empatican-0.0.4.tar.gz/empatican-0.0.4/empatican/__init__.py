import logging

__version__ = "0.0.4"

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p')
