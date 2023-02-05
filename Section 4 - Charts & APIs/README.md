## Section 4: Charts & APIs

This section will cover the designing of Singapore covid-19 cases dashboard

Script to pull data will be written in Python 3.9

Dashboard use will be a locally hosted Grafana
 
### Summary of tasks:

1. Create a script to pull data from public data
	- Data can be pull via Full download or Partial download
	- Confirmed cases and Death cases will be pulled
	- Additional processing to get daily new cases
	- Design script to be run daily
	- Output data in csv format for dashboard usage
2. Create a dashboard to display data pulled
3. Export dashboard in image form for review

---
### Dashboard
![alt text](https://github.com/ovixivo/Data-Engineer-Tech-Challenge/blob/main/Section%204%20-%20Charts%20%26%20APIs/Dashboard.png "Dashboard")

Screenshot is taken on 4 Feb 2023

To try out the interactive Grafana dashboard use the link below: (Link expires on 12 Feb 2023)
- https://snapshots.raintank.io/dashboard/snapshot/bfhNCZbM0Z6P96diVBOhjDZRvRbU744B

#### Top row - Confirmed covid cases in Singapore
1. The dashboard displays the latest confirmed covid cases in Singapore.
2. On the left, the latest cumulative number and the number of new confirmed cases
3. In the middle, the cumulative confirmed cases over time
4. On the right, the daily new confirmed cases over time

#### Bottom row - Death covid cases in Singapore
1. The dashboard displays the latest death covid cases in Singapore.
2. On the left, the latest cumulative number and the number of new death cases
3. In the middle, the cumulative death cases over time
4. On the right, the daily new death cases over time

#### Data source
Grafana will read data from local CSV files to generate dashboard.

CSV files is generated using python download script that will be covered in the next section

---
### Download script
Python script is used to download the data via API
#### High-level design
1. Get API link to call for confirmed cases
   - API link is affected by the defined download mode
      1. For full download - API link will not contain parameters
      2. For file update - API link will contain last updated date in output file and today's date as from & to parameters
2. Call API and convert JSON result to Python Dictionary 
3. Calculate daily change in cases
4. Generate dataframe
5. Output dataframe as csv into OUTPUT folder
6. Repeat step 1 to 5 for Death cases

#### Scheduling
Script can be schedule to run daily at 12PM to get the latest information on the dashboard
```shell
# Add cron job to run covid_data_download_main.py script daily at 12PM
echo "0 12 * * * python3 /path/to/covid_data_download_main.py" | crontab -
```

Using the above command, a user listed in cron.allow will be able to create a schedule job to run the python script hourly.

Note that the user should have execute permission to scripts and access to the required folders

