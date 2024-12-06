WITH task_record(orderID,username) AS 
    ((SELECT orderID, act.username FROM Ordered JOIN Act ON (Ordered.supervisor=Act.username) WHERE Act.roleid='2' AND (orderDate BETWEEN '${start_date}' AND '${end_date}')) 
    UNION 
    (SELECT orderID, act.username FROM Delivered Join Act ON (Delivered.username=Act.username) WHERE Act.roleid='2' AND (date BETWEEN '${start_date}' AND '${end_date}'))) 
SELECT COUNT(DISTINCT orderID) AS task_count,username FROM task_record GROUP BY username ORDER BY COUNT(DISTINCT orderID);