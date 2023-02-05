# Parameters file to define file location and file header
# Contains configuration information used in the pipeline
# Created by: Vincent Ngoh
# Created on: 2023-02-03
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-03


IN_FOLDER = "../simulation/IN"
OUT_S_FOLDER = "../simulation/OUT/successful"
OUT_US_FOLDER = "../simulation/OUT/unsuccessful"
ARCHIVE_FOLDER = "../simulation/ARCHIVE"
ERROR_FOLDER = "../simulation/ERROR"
LOG_FOLDER = "../simulation/logs"

# Valid values ["DEBUG","INFO","WARN","ERROR"]
LOG_LEVEL = "INFO"

# Expected raw dataset header
EXPECTED_HEADER = ['name', 'email', 'date_of_birth', 'mobile_no']