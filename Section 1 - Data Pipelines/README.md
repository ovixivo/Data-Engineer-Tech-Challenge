## Section1: Data Pipelines

This section will cover building a data pipeline for reviewing and processing membership application.

Pipeline will be written in Python 3.9
 
### Summary of tasks:

1. Read datasets from a defined folder (Can be multiple files)
2. Review each application with the following condition:
	- Application mobile number is 8 digits
	- Applicant is over 18 years old as of 1 Jan 2022
	- Applicant has a valid email (email ends with @emailprovider.com or @emailprovider.net)
3. To format the dataset with the following manner:
	- Split name into first_name and last_name
	- Format birthday field into YYYYMMDD
	- Remove any rows which do not have a name field (treat this as unsuccessful applications)
	- Create a new field named above_18 based on the applicant's birthday
	- Membership IDs for successful applications should be the user's last name, followed by a SHA256 hash of the applicant's birthday, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>)  
4. To consolidate datasets and output successful and unsuccessful applications into different folders
5. Schedule pipeline to run hourly

---

### Pipeline design

![alt text](https://github.com/ovixivo/Data-Engineer-Tech-Challenge/blob/main/Section%201%20-%20Data%20Pipelines/Pipeline%20design.png "Pipeline design")

#### The high-level pipeline design

1. Read datasets from IN folder and combine files into 1 dataframe
2. Clean and process dataframe
   - Process name
     - Remove titles from name
     - Spilt name into first and last name columns
   - Process email
     - Check if email ends with .com or .net
   - Process mobile
     - Check if mobile is of 8 digits
   - Process dob
     - Standardize date format to YYYMMDD in the dataframe
     - Check if applicant is over 18 years old as of 1 Jan 2022
3. Review application
   - Split dataframe into 2 set successful and unsuccessful
   - successful applicant will have Membership ID generated
4. Output successful and unsuccessful dataframes as CSV into respective folders in OUT folder
5. Archived processed dataset into ARCHIVE folder

### Code design

- application_processing_main.py -> Contains the pipeline workflow 
- parameters.py -> Contains configuration information used in the pipeline 
- functions.py -> Contains the processing steps use in the pipeline
- utility_functions.py -> Contains common functions that can be reused in other projects

### Schedule pipeline

```shell
# Add cron job to run application_processing_main.py script every hourly
echo "0 * * * * python3 /path/to/application_processing_main.py" | crontab -
```

Using the above command, a user listed in cron.allow will be able to create a schedule job to run the python script hourly.

Note that the user should have execute permission to scripts and access to the required folders