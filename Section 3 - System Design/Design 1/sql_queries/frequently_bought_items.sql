/* Which are the top 3 items that are frequently brought by members */

-- By quantity sold
SELECT s.item_id, i.item_name, SUM(s.total_weight/i.weight_kg) as total_quantity_sold
FROM sales s inner join items i on 
	s.item_id = i.item_id 
GROUP BY s.item_id, i.item_name
ORDER BY total_quantity_sold desc
LIMIT 3;

-- By purchase frequency
SELECT s.item_id, i.item_name, count(s.item_id) as purchase_frequency
FROM sales s inner join items i on 
	s.item_id = i.item_id 
GROUP BY s.item_id, i.item_name
ORDER BY purchase_frequency desc
LIMIT 3;
