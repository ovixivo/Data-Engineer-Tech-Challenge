# Functions script for individual function
# Created by: Vincent Ngoh
# Created on: 2023-02-04
# Last Modified by: Vincent Ngoh
# Last Modified on: 2023-02-05


import requests
import json
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import utility_functions as uf


# Generate url for API call. Purpose to reduce data retrieval by setting date range
def get_url(logger, url, csv_file, today_date, download_mode):
    if download_mode != 'FULL':
        final_date = get_last_date(csv_file)

        if final_date is not None:
            final_date = datetime.strptime(final_date, "%Y-%m-%d")
            final_date = final_date + timedelta(days=1)
            if final_date > today_date:
                logger.warn('Data is already up to date')
                url = ''
                download_mode = 'SKIP'
            else:
                url = url + '?from=' + final_date.strftime('%Y-%m-%d') + '&to=' + today_date.strftime('%Y-%m-%dT00:00:01Z')
        else:
            logger.warn('File does not exist')
            url = url
            download_mode = 'FULL'
    return url, download_mode


# Get last updated date
def get_last_date(csv_file):
    final_date = None
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            final_date = f.readlines()[-1].split(',')[0]
    return final_date


# Download data from API
def download_data(logger, url, download_mode, out_file):

    if download_mode == 'UPDATE':
        # Get last record info for delta change calculation
        data_dict = get_dataset(logger, url, get_last_record(out_file))
        if len(data_dict) > 0:
            change = delta_change(data_dict)
            # Remove existing record
            change.pop(next(iter(change)))
            data_dict.pop(next(iter(data_dict)))
            df = to_dataframe(data_dict, change)
            output_data(df, out_file, download_mode)

    if download_mode == 'FULL':
        data_dict = get_dataset(logger, url)
        if len(data_dict) > 0:
            change = delta_change(data_dict)
            df = to_dataframe(data_dict, change)
            output_data(df, out_file, download_mode)


# get_last_record in the file (For delta change calculation)
def get_last_record(csv_file):
    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
        date, cumulative_count, new_cases = f.readlines()[-1].split(',')
        data_dict = {date: int(cumulative_count)}
    return data_dict


# Get API result
def get_dataset(logger, url, data_dict = {}):
    response = requests.request("GET", url)
    result = json.loads(response.text)
    # If API return error
    if type(result) is dict:
        logger.error(result)
        logger.error('Retrying in 5 seconds')
        time.sleep(5)
        data_dict = get_dataset(url)
        return data_dict

    for i in result:
        data_dict[i['Date'][:10]] = i['Cases']
    return data_dict


# Calculate daily change in number of cases
def delta_change(d):
    change = {}
    for i, (date, value) in enumerate(d.items()):
        if i == 0:
            change[date] = 0
            continue
        prev_value = list(d.values())[i - 1]
        change[date] = value - prev_value
        if (value - prev_value) < 0:
            change[date] = 0
    return change


# Convert direction to dataframe
def to_dataframe(cumulative_count, daily_change):
    df = pd.DataFrame({'date': list(cumulative_count.keys()),
                       'cumulative count': list(cumulative_count.values()),
                       'new cases': list(daily_change.values())})
    return df


# Output dataframe as csv
def output_data(df, out_file, mode='FULL'):
    if mode == 'FULL':
        df.to_csv(out_file, index=False, header=True, mode='w')
    else:
        df.to_csv(out_file, index=False, header=False, mode='a')


# Create logging
def get_logger(log_folder, today_date, log_level):
    return uf.create_logger(log_folder, today_date.strftime('%Y%m%d'), log_level)





