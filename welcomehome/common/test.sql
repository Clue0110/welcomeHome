SELECT o.OrderId,orderDate,ordernotes,supervisor,client,username AS volunteer, status, date
FROM Ordered AS o LEFT JOIN Delivered AS d ON o.OrderID=d.OrderID 
WHERE supervisor='${username}' OR client='${username}' OR username='${username}'; 