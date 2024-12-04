SELECT o.OrderId,orderDate,ordernotes,supervisor,client,username AS volunteer, status, date 
FROM Delivered AS d LEFT JOIN Ordered AS o ON o.OrderID=d.OrderID 
WHERE d.OrderID=${orderID} AND (supervisor='${username}' OR username='${username}'); 