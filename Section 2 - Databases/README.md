## Section2: Databases

This section will cover creating a container postgresql DB using docker.
Scripts to create the database, sample data for the database and SQL query to answer analysts' questions

Running on Docker Desktop for Windows
 
### Summary of task:

1. Create a Dockerfile to pull postgres image
2. Generate DDL to create relevant tables
	- items
	- members
	- sales
3. Update Dockerfile to stand up database with relevant tables
4. Generate sample data the tables
5. Create script for population of data
6. Answer analysts' questions:
	- Which are the top 10 members by spending
	- Which are the top 3 items that are frequently brought by members
7. Documentation on the ER diagram of created tables

