#!/bin/bash

# To run script with user listed in cron.allow
# User should have execute permission to scripts and access to the required folders

# Add cron job to run covid_data_download_main.py script daily at 12PM
echo "0 12 * * * python3 /path/to/covid_data_download_main.py" | crontab -

# Check cron job list
crontab -l