# Main script to run for processing application
# Created by: Vincent Ngoh
# Created on: 2023-02-03
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-03

import pandas as pd
import datetime
import functions as fun
import parameters as param

processing_hour = datetime.datetime.now().strftime("%Y%m%d%H")
# Read Data
df, process_list = fun.read_files(param.IN_FOLDER, param.ERROR_FOLDER, "applications_dataset_", processing_hour, param.EXPECTED_HEADER)
if df is None:
    exit()

# Cleaning and Processing
df = fun.process_names(df)
df = fun.process_emails(df)
df = fun.process_mobile(df)
df = fun.process_dob(df, cutoff_date=datetime.date(2022, 1, 1))
successful_df, unsuccessful_df = fun.review_application(df)

# Output Data
fun.output_data(successful_df, param.OUT_S_FOLDER, f"successful_{processing_hour}.csv")
fun.output_data(unsuccessful_df, param.OUT_US_FOLDER, f"unsuccessful_{processing_hour}.csv")

# Archiving of processed file
fun.archive_file(param.IN_FOLDER, param.ARCHIVE_FOLDER, process_list, processing_hour)

