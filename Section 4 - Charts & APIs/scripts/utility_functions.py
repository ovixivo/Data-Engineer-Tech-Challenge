# Utility function - Common function that can use across different projects
# Created by: Vincent Ngoh
# Created on: 2023-02-03
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-03


import os
import logging


# Create a logger object
def create_logger(log_folder, filename, log_level):
    log_file = os.path.join(log_folder, filename + '.log')
    logger = logging.getLogger("Pipeline")
    level = logging.getLevelName(log_level)
    logger.setLevel(level)

    # Add a file handler to the logger
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    return logger
