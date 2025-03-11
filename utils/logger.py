# logger.py
# Basic logging utility.

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FakeNewsDetector")

if __name__ == "__main__":
    logger.info("Logger is set up.")
