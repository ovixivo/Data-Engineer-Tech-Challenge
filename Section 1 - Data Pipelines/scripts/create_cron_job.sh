#!/bin/bash

# To run script with user listed in cron.allow
# User should have execute permission to scripts and access to the required fodler

# Add cron job to run application_processing_main.py script every hourly
echo "0 * * * * python3 /path/to/application_processing_main.py" | crontab -

# Check cron job list
crontab -l