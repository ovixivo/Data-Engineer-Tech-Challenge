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

---

### Docker file

```Dockerfile
FROM postgres:latest
ENV POSTGRES_PASSWORD P@ssw0rd
ENV POSTGRES_DB tech_challenge

RUN mkdir /tmp/sql_scripts
RUN mkdir /tmp/sample_data
RUN mkdir /tmp/sql_queries
COPY ./sql_scripts/* /tmp/sql_scripts
COPY ./sample_data/* /tmp/sample_data
COPY ./sql_queries/* /tmp/sql_queries

COPY ./sql_scripts/1-create_tables.sql /docker-entrypoint-initdb.d/
```
The Dockerfile will pull the latest version of postgres and create a database tech_challenge

Scripts and test data from the Git folder are copied into tmp folder in the container

1-create_tables.sql script will create the postgres upon stand up

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
### Table design - Entity-relationship diagram
![alt text](https://github.com/ovixivo/Data-Engineer-Tech-Challenge/blob/main/Section%202%20-%20Databases/Entity-relationship%20diagram.png "Entity-relationship diagram")

The tables are designed based on star schema where items and members tables are the dimension table, and sales is the fact table.

This design provide easy-to-understand structure for data, making it easy for users to query and analyze data.
This design also allows easy scaling of tables where new dimensions does not impact existing queries or BI reports.
### DDL for tables

#### items table

```sql
CREATE TABLE items (
	item_id VARCHAR ( 50 ) PRIMARY KEY,
	item_name VARCHAR ( 255 ),
	make_name VARCHAR ( 255 ),
	cost DECIMAL,
	weight_kg INTEGER,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	last_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```
items table is design to store details such as cost and weight of the item.
For analysis propose, it is not recommended to delete record from dimension table. 
Hence, is_active column is introduced in the table to track record status. 

#### members table

```sql
CREATE TABLE members (
	membership_id VARCHAR ( 50 ) PRIMARY KEY,
	first_name VARCHAR ( 66 ) NOT NULL,
	last_name VARCHAR ( 66 ) NOT NULL,
	date_of_birth VARCHAR ( 8 ),
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	mobile_no VARCHAR ( 8 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	last_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```
members table is design to store details from membership application file.
For analysis propose, it is not recommended to delete record from dimension table. 
Hence, is_active column is introduced in the table to track record status. 

#### sales table

```sql
CREATE TABLE sales (
	sales_id serial PRIMARY KEY,
	membership_id VARCHAR ( 50 ) NOT NULL,
	item_id VARCHAR ( 50 ) NOT NULL,
	total_price DECIMAL,
	total_weight INTEGER,
	is_fullfiled BOOLEAN NOT NULL DEFAULT FALSE,
	fullfiled_on TIMESTAMP,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	last_modified_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (membership_id) REFERENCES members(membership_id),
	FOREIGN KEY (item_id) REFERENCES items(item_id)
);
CREATE INDEX idx_sales_membership_id ON sales(membership_id);
CREATE INDEX idx_sales_item_id ON sales(item_id);
CREATE INDEX idx_sales_total_price ON sales(total_price);
CREATE INDEX idx_sales_total_weight ON sales(total_weight);
```

sales table make use of foreign keys reference to members and items tables, to ensure the sales record can link to an existing member or item.
Indices are created on commonly joined columns and on columns that will be used in aggregation functions. This is to speed up any queries using the columns.
The is_fullfiled and fullfiled_on columns are for logistic team to update on the completion of sales.

---

### Analytical queries

#### Which are the top 10 members by spending
```sql
/* Which are the top 10 members by spending */

SELECT m.membership_id, m.first_name, m.last_name, SUM(s.total_price) as total_spending
FROM sales s inner join members m on 
	s.membership_id = m.membership_id 
GROUP BY m.membership_id, m.first_name, m.last_name
ORDER BY total_spending desc
LIMIT 10;

```
- To find the top 10 spender, analyst can aggregate the sum of sales total price group by membership_id.
- To get the member's name, analyst can join the sales query with members table for the detail.

#### Which are the top 3 items that are frequently brought by members
```sql
/* Which are the top 3 items that are frequently brought by members */

-- By quantity sold
SELECT i.item_id, i.item_name, SUM(s.total_weight/i.weight_kg) as total_quantity_sold
FROM sales s inner join items i on 
	s.item_id = i.item_id 
GROUP BY i.item_id, i.item_name
ORDER BY total_quantity_sold desc
LIMIT 3;

-- By purchase frequency
SELECT i.item_id, i.item_name, count(i.item_id) as purchase_frequency
FROM sales s inner join items i on 
	s.item_id = i.item_id 
GROUP BY i.item_id, i.item_name
ORDER BY purchase_frequency desc
LIMIT 3;

```
- To find the top 3 items that are frequently brought
  - Determine by quantity sold
    - Using the sales total_weight, analyst can find out how the quantity sold in each sale by dividing the values against the item weight
    - By aggregating the sum of quantity sold and group by item_id, it is possible to find out the most frequently bought items
  - Determine by purchase frequency
    - Using the appearance of item_id in sales table
    - Aggregate the count of appearance and group by item_id, it is possible to find out the most frequently bought items
    - To get the item's name, analyst can join the sales query with item table for the detail.

#### Query testing
```shell
# In Docker bash
psql -d tech_challenge -U postgres -p 5432 -a -f /tmp/sql_queries/top_spending_members.sql

psql -d tech_challenge -U postgres -p 5432 -a -f /tmp/sql_queries/frequently_bought_items.sql
```
