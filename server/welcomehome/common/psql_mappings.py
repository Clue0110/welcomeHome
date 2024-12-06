from welcomehome.common.util.database_util import DatabaseConn
import sys

class PredefinedQueries:
    get_item_by_id = "SELECT * FROM Item WHERE ItemID = ${ItemID}"
    get_order_by_id = "SELECT * FROM Ordered WHERE orderID = ${orderID}"
    get_delivery_status_by_orderid="SELECT * FROM delivered WHERE orderid=${orderID};"
    get_all_pieces_locations = "SELECT p.ItemID, p.pieceNum, p.roomNum, p.shelfNum, l.shelfDescription FROM Piece AS p NATURAL JOIN location AS l WHERE p.ItemID=${ItemID};"
    get_all_pieces_locations_using_orderid="SELECT itemin.itemid,piecenum,orderid,roomnum,shelfnum,shelfdescription FROM itemin JOIN piece NATURAL JOIN location ON(itemin.ItemId=piece.ItemID) WHERE OrderId=${orderID};"
    get_person_by_username="SELECT * FROM Person WHERE userName='${userName}';"
    get_role_by_username="SELECT roleID FROM Act WHERE userName='${userName}';"
    get_distinct_itemids_in_itemin="SELECT DISTINCT(ItemID) FROM ItemIn;"
    get_all_orders_related_to_user="SELECT o.OrderId,orderDate,ordernotes,supervisor,client,username AS volunteer, status, date FROM Ordered AS o LEFT JOIN Delivered AS d ON o.OrderID=d.OrderID WHERE supervisor='${username}' OR client='${username}' OR username='${username}';"
    get_role_by_orderid_and_userid="SELECT supervisor,username AS volunteer, status, date FROM Delivered AS d LEFT JOIN Ordered AS o ON o.OrderID=d.OrderID WHERE d.OrderID=${orderID} AND (supervisor='${username}' OR username='${username}');"

    get_items_in_order="SELECT ItemID FROM itemin WHERE orderID=${orderID};"
    get_order_by_id="SELECT * FROM ordered WHERE orderID=${orderID};"
    get_highest_orderid="SELECT max(orderid) AS max_order_id FROM Ordered;"

    get_inventory_items="SELECT * FROM Item WHERE ItemId NOT IN (SELECT distinct(ItemID) from ItemIn);"
    get_inventory_items_with_category="SELECT * FROM Item WHERE mainCategory='${mainCategory}' AND ItemId NOT IN (SELECT distinct(ItemID) from ItemIn);"
    get_inventory_items_with_subcategory="SELECT * FROM Item WHERE mainCategory='${mainCategory}' AND subCategory='${subCategory}' AND ItemId NOT IN (SELECT distinct(ItemID) from ItemIn);"
    get_volunteer_task_ranking="WITH task_record(orderID,username) AS ((SELECT orderID, act.username FROM Ordered JOIN Act ON (Ordered.supervisor=Act.username) WHERE Act.roleid='2') UNION (SELECT orderID, act.username FROM Delivered Join Act ON (Delivered.username=Act.username) WHERE Act.roleid='2')) SELECT COUNT(DISTINCT orderID) AS task_count,username FROM task_record GROUP BY username ORDER BY COUNT(DISTINCT orderID);"
    #get_volunteer_task_ranking_between_dates="WITH task_record(orderID,username) AS ((SELECT orderID, act.username FROM Ordered JOIN Act ON (Ordered.supervisor=Act.username) WHERE Act.roleid='2') UNION (SELECT orderID, act.username FROM Delivered Join Act ON (Delivered.username=Act.username) WHERE Act.roleid='2')) SELECT COUNT(DISTINCT orderID) AS task_count,username FROM task_record GROUP BY username ORDER BY COUNT(DISTINCT orderID);"
    get_volunteer_task_ranking_between_dates='''
    WITH task_record(orderID,username) AS 
        ((SELECT orderID, act.username FROM Ordered JOIN Act ON (Ordered.supervisor=Act.username) WHERE Act.roleid='2' AND (orderDate BETWEEN '${start_date}' AND '${end_date}')) 
    UNION 
        (SELECT orderID, act.username FROM Delivered Join Act ON (Delivered.username=Act.username) WHERE Act.roleid='2' AND (date BETWEEN '${start_date}' AND '${end_date}'))) 
    SELECT COUNT(DISTINCT orderID) AS task_count,username FROM task_record GROUP BY username ORDER BY COUNT(DISTINCT orderID);
    '''

    insert_person = "INSERT INTO person(userName,password,fname,lname,email) VALUES ('${userName}','${password}','${fname}','${lname}','${email}');"
    insert_person_phone = "INSERT INTO PersonPhone(userName,phone) VALUES ('${userName}','${phone}');"
    insert_act = "INSERT INTO Act(userName,roleID) VALUES ('${userName}','${roleID}');"

    insert_item = "INSERT INTO Item(ItemID,iDescription,photo,color,isNew,hasPieces,material,mainCategory,subCategory) VALUES (${ItemID},'${iDescription}','${photo}','${color}',${isNew},${hasPieces},'${material}','${mainCategory}','${subCategory}');"
    insert_item_without_id = "INSERT INTO Item(iDescription,photo,color,isNew,hasPieces,material,mainCategory,subCategory) VALUES ('${iDescription}','${photo}','${color}',${isNew},${hasPieces},'${material}','${mainCategory}','${subCategory}') RETURNING ItemID;"
    insert_donatedby="INSERT INTO DonatedBy(ItemID,userName,donateDate) VALUES (${ItemID},'${userName}','${donateDate}');" # donateDate String?
    insert_piece="INSERT INTO Piece(ItemID,pieceNum,pDescription,length,width,height,roomNum,shelfNum,pNotes) VALUES (${ItemID},${pieceNum},'${pDescription}',${length},${width},${height},${roomNum},${shelfNum},'${pNotes}');"

    insert_itemin="INSERT INTO ItemIn(ItemID,orderID,found) VALUES (${ItemID},${orderID},${found});"
    insert_ordered="INSERT INTO Ordered(orderID,orderDate,orderNotes,supervisor,client) VALUES (${orderID},'${orderDate}','${orderNotes}','${supervisor}','${client}');"

    update_person = "UPDATE person SET userName='${userName}', password='${password}', fname='${fname}', lname='${lname}', email='${email}' WHERE userName='${userName}';"
    update_person_phone = "UPDATE PersonPhone SET userName='${userName}', phone='${phone}' WHERE userName='${userName}' AND phone='${phone}';"
    update_act = "UPDATE Act SET userName='${userName}', roleID='${roleID}' WHERE userName='${userName}' AND roleID='${roleID}';"
    
    update_ordered="UPDATE Ordered SET orderID=${orderID}, orderDate='${orderDate}', orderNotes='${orderNotes}', supervisor='${supervisor}',client='${client}' WHERE orderID=${orderID};"
    update_itemin="UPDATE ItemIn SET ItemID=${ItemID}, orderID=${orderID},found=${found} WHERE orderID=${orderID} AND ItemID=${ItemID};"
    update_order_status_by_orderid="UPDATE Delivered SET status='${status}', date='${date}' WHERE orderID=${orderID};"


class Constants:
    ROLE_STAFF="staff"
    ROLE_VOLUNTEER="volunteer"
    ROLE_CLIENT="client"
    ROLE_DONOR="donor"

class RoleMappings:
    role_name_id_mapping={
        Constants.ROLE_STAFF:1,
        Constants.ROLE_VOLUNTEER:2,
        Constants.ROLE_CLIENT:3,
        Constants.ROLE_DONOR:4
    }

    def get_roleid_with_username(username):
        db=DatabaseConn()
        id=[]
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_role_by_username,{"userName":username})
            if not len(q_res)==0:
                for row in q_res:
                    if not row.roleid==None:
                        id.append(int(row.roleid))
                return id
        except Exception as e:
            return None
        return None

    def isStaff(id=None,username=None):
        if username:
            #Get the role id from database
            id=RoleMappings.get_roleid_with_username(username)
        if not id==None:
            if type(id)==int:
                id=[id]
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_STAFF,0) in id: 
                return True
        return False
    
    def isDonor(id=None,username=None):
        if username:
            id=RoleMappings.get_roleid_with_username(username)
        if not id==None:
            if type(id)==int:
                id=[id]
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_DONOR,0) in id: 
                return True
            return False
        return False
    
    def isClient(id=None,username=None):
        if username:
            id=RoleMappings.get_roleid_with_username(username)
        if not id==None:
            if type(id)==int:
                id=[id]
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_CLIENT,0) in id: 
                return True
            return False
        return False
    
    def isVolunteer(id=None,username=None):
        if username:
            id=RoleMappings.get_roleid_with_username(username)
        if not id==None:
            if type(id)==int:
                id=[id]
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_VOLUNTEER,0) in id: 
                return True
            return False
        return False