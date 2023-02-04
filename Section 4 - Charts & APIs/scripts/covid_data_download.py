import os
import datetime
import time
import functions as fun
import parameters as param


today_date = datetime.datetime.today()
confirmed_out_file = os.path.join(param.OUT_FOLDER, 'confirmed_cases.csv')

url, param.DOWNLOAD_MODE = fun.get_url(param.CONFIRMED_CASE_URL, confirmed_out_file, today_date, param.DOWNLOAD_MODE)

print(url)
if param.DOWNLOAD_MODE != 'SKIP':
    confirmed_dict = fun.get_dataset(url)
    if len(confirmed_dict) > 0:
        confirmed_change = fun.delta_change(confirmed_dict)
        confirmed_df = fun.to_dataframe(confirmed_dict, confirmed_change)
        fun.output_data(confirmed_df, confirmed_out_file, param.DOWNLOAD_MODE)


death_out_file = os.path.join(param.OUT_FOLDER, 'death_cases.csv')
url, param.DOWNLOAD_MODE = fun.get_url(param.DEATH_CASE_URL, death_out_file, today_date, param.DOWNLOAD_MODE)

print(url)
if param.DOWNLOAD_MODE != 'SKIP':
    death_dict = fun.get_dataset(url)
    if len(death_dict) > 0:
        death_change = fun.delta_change(death_dict)
        death_df = fun.to_dataframe(death_dict, death_change)
        fun.output_data(death_df, death_out_file, param.DOWNLOAD_MODE)

