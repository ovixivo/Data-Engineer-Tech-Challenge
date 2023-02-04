import requests
import json
import pandas as pd
import os
import time
from datetime import datetime, timedelta


def get_dataset(url):
    response = requests.request("GET", url)
    result = json.loads(response.text)
    if type(result) is dict:
        time.sleep(5)
        data_dict = get_dataset(url)
        return data_dict

    data_dict = {}
    for i in result:
        data_dict[i['Date'][:10]] = i['Cases']
    return data_dict


def delta_change(d):
    change = {}
    for i, (date, value) in enumerate(d.items()):
        if i == 0:
            change[date] = 0
            continue
        prev_value = list(d.values())[i - 1]
        change[date] = value - prev_value
    return change


def to_dataframe(cumulative_count, daily_change):
    df = pd.DataFrame({'date': list(cumulative_count.keys()),
                       'cumulative count': list(cumulative_count.values()),
                       'new cases': list(daily_change.values())})
    return df


def output_data(df, out_file, mode='FULL'):
    if mode == 'FULL':
        df.to_csv(out_file, index=False, header=True, mode='w')
    else:
        df.to_csv(out_file, index=False, header=False, mode='a')


def get_last_date(csv_file):
    final_date = None
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            final_date = f.readlines()[-1].split(',')[0]
    return final_date


def get_url(url, csv_file, today_date, download_mode):
    if download_mode != 'FULL':
        final_date = get_last_date(csv_file)

        if final_date is not None:
            final_date = datetime.strptime(final_date, "%Y-%m-%d")
            final_date = final_date + timedelta(days=1)
            if final_date > today_date:
                url = ''
                download_mode = 'SKIP'
            else:
                url = url + '?from=' + final_date.strftime('%Y-%m-%d') + '&to=' + today_date.strftime('%Y-%m-%dT00:00:01')
        else:
            url = url
            download_mode = 'FULL'
    return url, download_mode
