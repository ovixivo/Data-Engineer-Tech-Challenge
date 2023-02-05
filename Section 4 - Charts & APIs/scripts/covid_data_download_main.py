# Main script to run for downloading data via API
# Created by: Vincent Ngoh
# Created on: 2023-02-04
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-05


import os
import datetime
import time
import functions as fun
import parameters as param


today_date = datetime.datetime.today()
logger = fun.get_logger(param.LOG_FOLDER, today_date, param.LOG_LEVEL)

logger.info(f"Start of covid data download - Session {today_date}")


logger.info(f"Start of confirmed cases data download")
# Define confirmed cases output file
confirmed_out_file = os.path.join(param.OUT_FOLDER, 'confirmed_cases.csv')
# Get API url and download_mode
url, download_mode = fun.get_url(logger, param.CONFIRMED_CASE_URL, confirmed_out_file, today_date, param.DOWNLOAD_MODE)

logger.info(f'confirmed_cases url: {url}')
logger.info(f'download_mode: {download_mode}')
# Download confirmed cases data
fun.download_data(logger, url, download_mode, confirmed_out_file)


logger.info(f"Start of death cases data download")
# Define death cases output file
death_out_file = os.path.join(param.OUT_FOLDER, 'death_cases.csv')
# Get API url and download_mode
url, download_mode = fun.get_url(logger, param.DEATH_CASE_URL, death_out_file, today_date, param.DOWNLOAD_MODE)

logger.info(f'death_cases url: {url}')
logger.info(f'download_mode: {download_mode}')
# Download death cases data
fun.download_data(logger, url, download_mode, death_out_file)


logger.info(f"End of covid data download  - Session {today_date} \n\n")