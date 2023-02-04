CREATE TEMPORARY TABLE t (
	first_name VARCHAR ( 255 ),
	last_name VARCHAR ( 255 ),
	email VARCHAR ( 255 ),
	date_of_birth VARCHAR ( 255 ),
	mobile_no VARCHAR ( 255 ),
	above_18 VARCHAR ( 255 ),
	membership_id VARCHAR ( 255 )
);


COPY t (first_name, last_name, email, date_of_birth, mobile_no, above_18, membership_id)
FROM '/tmp/sample_data/successful_applicants.csv' DELIMITER ',' CSV HEADER;

INSERT INTO members(membership_id, first_name, last_name, date_of_birth, email, mobile_no)
select membership_id, first_name, last_name, date_of_birth, email, mobile_no
from t;

DROP TABLE t;


COPY items (item_id, item_name, make_name, cost, weight_kg)
FROM '/tmp/sample_data/item_list.csv' DELIMITER ',' CSV HEADER;


COPY sales (membership_id, item_id, total_price, total_weight)
FROM '/tmp/sample_data/sales.csv' DELIMITER ',' CSV HEADER;
