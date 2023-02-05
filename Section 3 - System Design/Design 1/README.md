## Section3: System Design
### Design 1

This section will cover the design for database access for the various teams in the company.
Dockerfile and script of section2 will be reused and updated with the permission in place

Running on Docker Desktop for Windows

---
### Summary of task:

1. Create users and roles in Database
2. Assign permission to users and roles base on the following condition:
	- Logistics:
		- Get the sales details (in particular the weight of the total items bought)
        - Update the table for completed transactions
    - Analytics:
        - Perform analysis on the sales and membership status
        - Should not be able to perform updates on any tables
    - Sales:
        - Update database with new items
        - Remove old items from database
3. Update sql script to apply permission on stand up of docker

---
### Steps to stand up docker and populate test data

```shell
# In current folder
docker build -t postgres-db ./ ; 
docker run -d --name postgresdb-container -p 5432:5432 postgres-db

# Enter Docker Bash
docker exec -it postgresdb-container /bin/bash

# In Docker Bash
/tmp/sql_scripts/populate_tables.sh

```

---

### Design idea

Note: For testing purposes superuser account is still active, for production system account access should be disabled or replace with a lower power admin account

As an e-commerce company, the company is dealing with logistics, sales, membership application and analytics.
Hence, the following roles are created in the database:
- Logistics Team
- Sales Team
- Analytic Team
- Application Team

#### Logistics Team
Logistics team will be able to view sales information, however, limited to sales and items information only.
The team also handles the fullfilment of sales.

```sql
GRANT SELECT(sales_id, item_id, total_weight, is_fullfiled, fullfiled_on, created_on) ON sales TO logistics_team;
GRANT UPDATE(is_fullfiled, fullfiled_on, last_modified_on) ON sales TO logistics_team;
```
With the above permissions, members of logistics team can only select information relevant to logistic only.
The update permissions given only allow the team to close transaction.

#### Sales Team
Sales team will handle the company's product and sales information.
The team will be able to add/ remove/ update product's detail in the item table.
As sales team they will be able to view sales information and make any change upon user request.

```sql
GRANT SELECT ON items TO sales_team;
GRANT UPDATE ON items TO sales_team;
GRANT INSERT ON items TO sales_team;
GRANT DELETE ON items TO sales_team;
GRANT SELECT ON sales TO sales_team;
GRANT UPDATE ON sales TO sales_team;
GRANT INSERT ON sales TO sales_team;
GRANT DELETE ON sales TO sales_team;
```
With the above permissions, members of sales team have full operation access to both items and sales tables.

#### Analytic Team
Analytic team will handle analyzing the product's performance and customer's spending habits
The team will only have view access to tables they need to use.

```sql
GRANT SELECT ON members TO analytics_team;
GRANT SELECT ON items TO analytics_team;
GRANT SELECT ON sales TO analytics_team;
```
With the above permissions, members of analytic team have viewing permission membership details, sales details and products details.
This will allow the team to answer questions such as 
- Which are the top 10 members by spending
- Which are the top 3 items that are frequently brought by members

#### Application Team
Application team will handle uploading of successfully applicants into the database.
The team can consist of service accounts to run backend job automatically.

```sql
GRANT SELECT ON members TO application_team;
GRANT UPDATE ON members TO application_team;
GRANT INSERT ON members TO application_team;
GRANT DELETE ON members TO application_team;
```
With the above permissions, service account in application_team will be able to add/ remove/ update applicants data.

---
### Access Matrix

![alt text](https://github.com/ovixivo/Data-Engineer-Tech-Challenge/blob/main/Section%203%20-%20System%20Design/Design%201/Access%20Matrix.png "Access Matrix")


---
### For testing

```shell
# In docker bash
# logistics team. SELECT and UPDATE permission on sales table
psql -d tech_challenge -U user_1

# analytics team SELECT permission on members, items and sales table
psql -d tech_challenge -U user_2

# sales team SELECT, UPDATE, INSERT, DELETE permission on items and sales table
psql -d tech_challenge -U user_3

# application team SELECT, UPDATE, INSERT, DELETE permission on members table
psql -d tech_challenge -U service_account

```

