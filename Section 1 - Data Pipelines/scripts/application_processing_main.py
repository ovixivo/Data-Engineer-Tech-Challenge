# Main script to run for processing application.
# Contains the pipeline workflow
# Created by: Vincent Ngoh
# Created on: 2023-02-03
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-03


import datetime
import functions as fun
import parameters as param

processing_hour = datetime.datetime.now().strftime("%Y-%m-%d_%H0000")
logger = fun.get_logger(param.LOG_FOLDER, processing_hour, param.LOG_LEVEL)

logger.info(f"Start of Pipeline - Session {processing_hour}")

# Reading Data from IN folder
df, process_list = fun.read_files(logger, param.IN_FOLDER, param.ERROR_FOLDER,
                                  "applications_dataset_", processing_hour, param.EXPECTED_HEADER)
if df is None:
    logger.warning(f"There is no file to process")
    logger.info(f"End of Pipeline - Session {processing_hour} \n\n")
    exit()


logger.info("Cleaning and Processing data...")
# Cleaning and Processing Steps
df = fun.process_names(df)
df = fun.process_emails(df)
df = fun.process_mobile(df)
df = fun.process_dob(df, cutoff_date=datetime.date(2022, 1, 1))
successful_df, unsuccessful_df = fun.review_application(df)


logger.info("Outputting application results...")
# Output Data into OUT folder
fun.output_data(logger, successful_df, param.OUT_S_FOLDER, f"successful_{processing_hour}.csv")
fun.output_data(logger, unsuccessful_df, param.OUT_US_FOLDER, f"unsuccessful_{processing_hour}.csv")


logger.info("Archiving raw file...")
# Archiving of processed file into ARCHIVE folder
fun.archive_file(logger, param.IN_FOLDER, param.ARCHIVE_FOLDER, process_list, processing_hour)
logger.info(f"End of Pipeline - Session {processing_hour} \n\n")
