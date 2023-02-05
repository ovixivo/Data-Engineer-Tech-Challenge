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




-- Create a new role
CREATE ROLE logistics_team;
CREATE ROLE analytics_team;
CREATE ROLE sales_team;
CREATE ROLE application_team;

-- Create a new users
CREATE USER user_1 WITH LOGIN PASSWORD 'password';
CREATE USER user_2 WITH LOGIN PASSWORD 'password';
CREATE USER user_3 WITH LOGIN PASSWORD 'password';
CREATE USER service_account WITH LOGIN PASSWORD 'password';

-- Grant the role to the user
GRANT logistics_team TO user_1;
GRANT analytics_team TO user_2;
GRANT sales_team TO user_3;
GRANT application_team TO service_account;

-- Grant SELECT and UPDATE permission to logistics_team on sales table
GRANT SELECT(sales_id, item_id, total_weight, is_fullfiled, fullfiled_on, created_on) ON sales TO logistics_team;
GRANT UPDATE(is_fullfiled, fullfiled_on, last_modified_on) ON sales TO logistics_team;

-- Grant SELECT permission to analytics_team on members, items and sales table
GRANT SELECT ON members TO analytics_team;
GRANT SELECT ON items TO analytics_team;
GRANT SELECT ON sales TO analytics_team;

-- Grant SELECT, UPDATE, INSERT, DELETE permission to sales_team on items and sales table
GRANT SELECT ON items TO sales_team;
GRANT UPDATE ON items TO sales_team;
GRANT INSERT ON items TO sales_team;
GRANT DELETE ON items TO sales_team;
GRANT SELECT ON sales TO sales_team;
GRANT UPDATE ON sales TO sales_team;
GRANT INSERT ON sales TO sales_team;
GRANT DELETE ON sales TO sales_team;

-- Grant SELECT, UPDATE, INSERT, DELETE permission to application_team on members table
GRANT SELECT ON members TO application_team;
GRANT UPDATE ON members TO application_team;
GRANT INSERT ON members TO application_team;
GRANT DELETE ON members TO application_team;