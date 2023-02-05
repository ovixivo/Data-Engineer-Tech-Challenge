# Utility function - Common function that can use across different projects
# Created by: Vincent Ngoh
# Created on: 2023-02-03
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-03


import os
import shutil
import hashlib
import logging


# Move file to another location
def move_file(current_path, target_folder, filename):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target_file_path = os.path.join(target_folder, filename)
    shutil.move(current_path, target_file_path)


# Remove titles from name
def remove_titles(name):
    titles = ["Mr.", "Ms.", "Miss", "Mrs.", "Dr.", "PhD", "MD", "DDS", 'II', 'III', 'Jr.', 'DVM']
    for title in titles:
        if name.startswith(title + " "):
            name = name.replace(title + " ", "")
        if name.endswith(" " + title):
            name = name.replace(" " + title, "")
    return name


# Check if email ends with .com or .net
def check_email(email):
    if (email.count('@') == 1 and
            (email.endswith('.com') or
             email.endswith('.net'))):
        return True
    else:
        return False


# Check if mobile number contains 8 digits
def check_phone(mobile_no):
    if (mobile_no.isdigit() and
            len(mobile_no) == 8):
        return True
    else:
        return False


# Get age by given date
def get_age(dob, cutoff_date):
    age = cutoff_date.year - dob.year - ((cutoff_date.month, cutoff_date.day) < (dob.month, dob.day))
    return age


# Hash and truncate a value
def hash_sha256_truncate(value):
    sha256 = hashlib.sha256()
    sha256.update(value.encode('utf-8'))
    hashed_value = sha256.hexdigest()
    return hashed_value[:5]


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
