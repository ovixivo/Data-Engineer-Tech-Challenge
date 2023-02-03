## Main script to run for processing application
## Created by: Vincent Ngoh
## Created on: 2023-02-03 13:40pm
## Last Modified by: Vincent Ngoh
## Last Modified on: 2023-02-03 13:40pm

import pandas as pd
import os
import shutil
import datetime

in_folder = "../simulation/IN"
out_folder = "../simulation/OUT"
archive_folder = "../simulation/ARCHIVE"
error_folder = "../simulation/ERROR"


processing_hour = datetime.datetime.now().strftime("%Y%m%d%H")
## Read files combine into 1
expected_header = ['name', 'email', 'date_of_birth', 'mobile_no']
df_list = []

all_files = os.listdir(in_folder)
for filename in all_files:
    if filename.startswith("applications_dataset_") and filename.endswith(".csv"):
        file_path = os.path.join(in_folder, filename)
        df = pd.read_csv(file_path, header=0)
        if list(df.columns) == expected_header:
            df_list.append(df)
        else:
            print(f"{filename} does not have the expected headers")
            error_subfolder = os.path.join(error_folder, processing_hour)
            if not os.path.exists(error_subfolder):
                os.makedirs(error_subfolder)
            error_file_path = os.path.join(error_subfolder, filename)
            shutil.move(file_path, error_file_path)

df = pd.concat(df_list, axis=0, ignore_index=True)
#print(df.head())

## Clean name, remove title, spilt name into first and last name

def remove_titles(name):
    titles = ["Mr.", "Ms.", "Miss", "Mrs.", "Dr.", "PhD", "MD", "DDS", 'II', 'III', 'Jr.', 'DVM']
    for title in titles:
        if name.startswith(title + " "):
            name = name.replace(title + " ", "")
        if name.endswith(" " + title):
            name = name.replace(" " + title, "")
    return name

df['cleaned_name'] = df['name'].apply(remove_titles)

df[['first_name', 'last_name']] = df['cleaned_name'].str.split(" ", expand=True)

#print(df.head())
## Check email domain

def extract_email_domain(email):
    if email.count('@') != 1:
        return None
    return email.split('@')[-1]

df['email_domain'] = df['email'].apply(extract_email_domain)

#print(df)

## Check phone number length of 8

## Standardize DOB, Check age of customer as of 1 Jan 2022