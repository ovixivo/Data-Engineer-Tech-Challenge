# Parameters file to define download mode, file output location and api url
# Contains configuration information used in the pipeline
# Created by: Vincent Ngoh
# Created on: 2023-02-04
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-05

# Valid values ["FULL","UPDATE"]
DOWNLOAD_MODE = 'UPDATE'

OUT_FOLDER = '../output_file'
LOG_FOLDER = '../logs'

# Valid values ["DEBUG","INFO","WARN","ERROR"]
LOG_LEVEL = "INFO"

CONFIRMED_CASE_URL = 'https://api.covid19api.com/country/singapore/status/confirmed'
DEATH_CASE_URL = 'https://api.covid19api.com/country/singapore/status/deaths'
