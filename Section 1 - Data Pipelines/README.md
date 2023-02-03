## Section1: Data Pipelines

This section will cover building a data pipeline for reviewing and processing membership application.

Pipeline will be written in Python 3.9
 
### Summary of task:

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
4. To consolidate datasets and output successful and unsuccessful applications into different folder
5. Schedule pipeline to run hourly