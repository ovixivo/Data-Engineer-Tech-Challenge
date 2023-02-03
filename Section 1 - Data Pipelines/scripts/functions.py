# Function script to process individual process in the pipeline
# Created by: Vincent Ngoh
# Created on: 2023-02-03
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-03


import datetime
import pandas as pd
import os
import utility_functions as uf


# Read files combine into 1
def read_files(logger, in_folder, error_folder, prefix, processing_hour, header, extension=".csv"):
    df = None
    df_list = []
    process_list = []
    all_files = os.listdir(in_folder)
    for filename in all_files:
        if filename.startswith(prefix) and filename.endswith(extension):
            file_path = os.path.join(in_folder, filename)
            error_subfolder = os.path.join(error_folder, processing_hour)
            try:
                data = pd.read_csv(file_path, header=0)
            except:
                logger.error(f"Failed to read {filename}")
                uf.move_file(file_path, error_subfolder, filename)
                continue

            if list(data.columns) == header:
                df_list.append(data)
                process_list.append(filename)
                logger.debug(f"{filename} read")
            else:
                logger.error(f"{filename} does not have the expected header")
                uf.move_file(file_path, error_subfolder, filename)

    if len(process_list) > 0:
        df = pd.concat(df_list, axis=0, ignore_index=True)
        logger.info(f"Number of file read {len(process_list)}")
        logger.info(f"Number of application found {len(df.index)}")
    return df, process_list


# Process names
def process_names(df):
    df['cleaned_name'] = df['name'].apply(uf.remove_titles)
    df[['first_name', 'last_name']] = df['cleaned_name'].str.split(" ", expand=True)
    return df


# Process email
def process_emails(df):
    df['is_valid_email'] = df['email'].apply(uf.check_email)
    return df


# Process mobile
def process_mobile(df):
    df['is_valid_mobile'] = df['mobile_no'].apply(uf.check_phone)
    return df


# Process Date of birth
def process_dob(df, cutoff_date=datetime.datetime.today()):
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], infer_datetime_format=True, dayfirst=False)
    df['above_18'] = df['date_of_birth'].apply(uf.get_age, args=(cutoff_date,)) >= 18
    df['date_of_birth'] = df['date_of_birth'].dt.strftime('%Y%m%d')
    return df


# Review application
def review_application(df):
    application_status = df.groupby((df["is_valid_email"]) & (df["is_valid_mobile"]) & (df["above_18"]))
    application_status = application_status[
        ["first_name", "last_name", "email", "date_of_birth", "mobile_no", "above_18"]]

    successful = application_status.get_group(True)
    unsuccessful = application_status.get_group(False)

    successful["membership_id"] = successful["last_name"] + "_" + successful["date_of_birth"].apply(
        uf.hash_sha256_truncate)

    return successful, unsuccessful


# Output data into csv
def output_data(logger, df, out_folder, filename):
    df.to_csv(os.path.join(out_folder, filename), index=False, header=True, mode='w+')
    logger.debug(f"Saved {filename} to {out_folder}")


# Archiving processed file
def archive_file(logger, in_folder, archive_folder, process_list, processing_hour):
    for filename in process_list:
        file_path = os.path.join(in_folder, filename)
        archive_subfolder = os.path.join(archive_folder, processing_hour)
        uf.move_file(file_path, archive_subfolder, filename)
        logger.debug(f"Archived {filename} to {archive_subfolder}")


# Create logging
def get_logger(log_folder, processing_hour, log_level):
    return uf.create_logger(log_folder, processing_hour, log_level)