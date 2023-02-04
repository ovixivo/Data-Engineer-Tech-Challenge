CREATE TABLE members (
	membership_id VARCHAR ( 50 ) PRIMARY KEY,
	first_name VARCHAR ( 66 ) NOT NULL,
	last_name VARCHAR ( 66 ) NOT NULL,
	date_of_birth VARCHAR ( 8 ),
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
	mobile_no VARCHAR ( 8 ) UNIQUE NOT NULL,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE items (
	item_id VARCHAR ( 50 ) PRIMARY KEY,
	item_name VARCHAR ( 255 ),
	make_name VARCHAR ( 255 ),
	cost DECIMAL,
	weight_kg INTEGER,
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
	created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



