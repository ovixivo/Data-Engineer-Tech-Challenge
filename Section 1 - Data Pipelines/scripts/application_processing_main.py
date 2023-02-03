## Main script to run for processing application
## Created by: Vincent Ngoh
## Created on: 2023-02-03 13:40pm
## Last Modified by: Vincent Ngoh
## Last Modified on: 2023-02-03 13:40pm

import pandas as pd
import os
import shutil
import datetime
import hashlib

pd.set_option('display.max_columns', None)

in_folder = "../simulation/IN"
out_s_folder = "../simulation/OUT/successful"
out_us_folder = "../simulation/OUT/unsuccessful"
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

# print(df.head())

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


# print(df.head())
## Check email domain

def check_email(email):
    if (email.count('@') == 1 and
            (email.endswith('.com') or
             email.endswith('.net'))):
        return True
    else:
        return False


df['is_valid_email'] = df['email'].apply(check_email)

#print(df)


## Check phone number length of 8
def check_phone(mobile_no):
    if (mobile_no.isdigit() and
            len(mobile_no) == 8):
        return True
    else:
        return False


df['is_valid_mobile'] = df['mobile_no'].apply(check_phone)
#print(df)

## Standardize DOB, Check age of customer as of 1 Jan 2022

df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], infer_datetime_format=True, dayfirst=False)


def get_age(dob):
    cutoff_date = datetime.date(2022, 1, 1)
    age = cutoff_date.year - dob.year - ((cutoff_date.month, cutoff_date.day) < (dob.month, dob.day))
    return age


target_year = 2022
df['above_18'] = df['date_of_birth'].apply(get_age) >= 18
df['date_of_birth'] = df['date_of_birth'].dt.strftime('%Y%m%d')

#print(df.columns)

## Reviewing application
application_status = df.groupby((df["is_valid_email"]) & (df["is_valid_mobile"]) & (df["above_18"]))
application_status = application_status[["first_name", "last_name", "email", "date_of_birth", "mobile_no", "above_18"]]

successful = application_status.get_group(True)
unsuccessful = application_status.get_group(False)

## Generate membership ID
def hash_sha256_truncate(value):
    sha256 = hashlib.sha256()
    sha256.update(value.encode('utf-8'))
    hashed_value = sha256.hexdigest()
    return hashed_value[:5]


successful["membership_id"] = successful["last_name"] + "_" + successful["date_of_birth"].apply(hash_sha256_truncate)

print(successful.head())
print(unsuccessful.head())

## Output file
successful_filename = f"successful_{processing_hour}.csv"
unsuccessful_filename = f"unsuccessful_{processing_hour}.csv"


successful.to_csv(os.path.join(out_s_folder, successful_filename), index=False, header=True)
unsuccessful.to_csv(os.path.join(out_us_folder, unsuccessful_filename), index=False, header=True)

