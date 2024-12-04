WITH orderedItems(ItemID) AS (SELECT ItemID FROM ItemIn) SELECT * FROM Item WHERE mainCategory='Furniture' AND ItemId NOT IN (select * from orderedItems);

WITH orderedItems(ItemID) AS (SELECT ItemID FROM ItemIn) 

SELECT * FROM Item WHERE mainCategory='${mainCategory}' AND subCategory='${subCategory}' AND ItemId NOT IN (SELECT distinct(ItemID) from ItemIn);