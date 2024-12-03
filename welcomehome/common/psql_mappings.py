class PredefinedQueries:
    get_item_by_id = "SELECT * FROM Item WHERE ItemID = ${ItemID}"
    get_order_by_id = "SELECT * FROM Ordered WHERE orderID = ${orderID}"
    get_all_pieces_locations = "SELECT p.ItemID, p.pieceNum, p.roomNum, p.shelfNum, l.shelfDescription FROM Piece AS p NATURAL JOIN location AS l WHERE p.ItemID=${ItemID};"
    get_person_by_username="SELECT * FROM Person WHERE userName='${userName}';"
    get_role_by_username="SELECT roleID FROM Act WHERE userName='${userName}';"

    get_items_in_order="SELECT ItemID FROM itemin WHERE orderID=${orderID};"
    get_order_by_id="SELECT * FROM ordered WHERE orderID=${orderID};"

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

    def isStaff(id=None,role=None):
        if id:
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_STAFF,0)==id: 
                return True
            return False
        if role:
            if role.lower()==Constants.ROLE_STAFF:
                return True
        return False
    
    def isDonor(id=None,role=None):
        if id:
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_DONOR,0)==id: 
                return True
            return False
        if role:
            if role.lower()==Constants.ROLE_DONOR:
                return True
        return False
    
    def isClient(id=None,role=None):
        if id:
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_CLIENT,0)==id: 
                return True
            return False
        if role:
            if role.lower()==Constants.ROLE_CLIENT:
                return True
        return False
    
    def isVolunteer(id=None,role=None):
        if id:
            if RoleMappings.role_name_id_mapping.get(Constants.ROLE_VOLUNTEER,0)==id: 
                return True
            return False
        if role:
            if role.lower()==Constants.ROLE_VOLUNTEER:
                return True
        return False