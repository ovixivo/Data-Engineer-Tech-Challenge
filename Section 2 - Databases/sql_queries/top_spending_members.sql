/* Which are the top 10 members by spending */

SELECT m.membership_id, m.first_name, m.last_name, SUM(s.total_price) as total_spending
FROM sales s inner join members m on 
	s.membership_id = m.membership_id 
GROUP BY m.membership_id, m.first_name, m.last_name
ORDER BY total_spending desc
LIMIT 10;
