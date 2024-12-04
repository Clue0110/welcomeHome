from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
from flask_login import current_user, login_required
from flask import request
import sys

class DonatedItem():
    def __init__(self,payload):
        self.SQL_DATA={}
        self.request_json_payload=payload
        self.populate_item_table_entry(payload)
        self.populate_donated_by_table_entry(payload)
        self.populate_piece_table_entry(payload)

    def get_item_sql_data(self):
        return self.SQL_DATA["item"]
    
    def get_donated_by_sql_data(self):
        return self.SQL_DATA["donatedby"]
    
    def get_piece_sql_data(self):
        return self.SQL_DATA["piece"]
    
    def get_current_user_id(self):
        return current_user.get_id()
        #return self.request_json_payload["current_user"]
    
    def get_donor_user_id(self):
        return self.request_json_payload["donor_username"]

    def populate_item_table_entry(self,payload):
        '''
        ItemID SERIAL NOT NULL,
        iDescription TEXT,
        photo VARCHAR(20),
        color VARCHAR(20),
        isNew BOOLEAN DEFAULT TRUE,
        hasPieces BOOLEAN,
        material VARCHAR(50),
        mainCategory VARCHAR(50) NOT NULL,
        subCategory VARCHAR(50) NOT NULL,
        '''
        sql_data={
            "ItemID":payload["ItemID"],
            "iDescription":payload["iDescription"],
            "photo":payload["photo"],
            "color":payload["color"],
            "isNew":payload["isNew"],
            "hasPieces":payload["hasPieces"],
            "material":payload["material"],
            "mainCategory":payload["mainCategory"],
            "subCategory":payload["subCategory"]
        }
        self.SQL_DATA["item"]=sql_data

    def populate_donated_by_table_entry(self,payload):
        '''
        ItemID SERIAL NOT NULL,
        userName VARCHAR(50) NOT NULL,
        donateDate DATE NOT NULL,
        '''
        sql_data={
            "ItemID":payload["ItemID"],
            "userName":payload["donor_username"],
            "donateDate":payload["donateDate"]
        }
        self.SQL_DATA["donatedby"]=sql_data

    def populate_piece_table_entry(self,payload):
        '''
        ItemID INT NOT NULL,
        pieceNum INT NOT NULL,
        pDescription VARCHAR(200),
        length INT NOT NULL, -- for simplicity
        width INT NOT NULL,
        height INT NOT NULL,
        roomNum INT NOT NULL,
        shelfNum INT NOT NULL, 
        pNotes TEXT
        '''
        sql_rows=[]
        for piece_info in payload["pieces"]:
            sql_data={
                "ItemID":payload["ItemID"],
                "pieceNum":piece_info["pieceNum"],
                "pDescription":piece_info["pDescription"],
                "length":piece_info["length"],
                "width":piece_info["width"],
                "height":piece_info["height"],
                "roomNum":piece_info["roomNum"],
                "shelfNum":piece_info["shelfNum"],
                "pNotes":piece_info["pNotes"]
            }
            sql_rows.append(sql_data)
        self.SQL_DATA["piece"]=sql_rows
    

class Donation(Resource):

    @classmethod
    def validatePostReqParams(self,db=None,donatedItem=None):
        # Validation 1: Checking if the donor username is registered as a Donor
        res=db.execute_query_with_args(PredefinedQueries.get_role_by_username,{"userName":donatedItem.get_donor_user_id()})
        if len(res)==0:
            return False,"Donor Doesnt Exist"
        if not RoleMappings.isDonor(id=int(res[0].roleid)):
            return False,"Donor Not Registered"
        
        # Validation 2: Checking if the current user is a staff member
        res=db.execute_query_with_args(PredefinedQueries.get_role_by_username,{"userName":donatedItem.get_current_user_id()})
        if len(res)==0:
            return False,"Staff Member does not exist"
        if not RoleMappings.isStaff(id=int(res[0].roleid)):
            return False,"Non Staff Member is not Authrized to Accept Donation"
        
        #Additional Validations
        pass

        return True, "Validation Successful"

    def get(self):
        db=DatabaseConn()
        donatedItem=DonatedItem(request.json)
        validationResult,msg=self.validatePostReqParams(db,donatedItem)
        if not validationResult:
            return {"message":f"ValidationError for Donation: {msg}"},400
        return donatedItem.SQL_DATA,200

    def post(self):
        db=DatabaseConn()
        donatedItem=DonatedItem(request.json)
        msg,validationResult=self.validatePostReqParams(db,donatedItem)
        if not validationResult:
            return {"message":f"ValidationError for Donation: {msg}"},400
        try:
            #INSERTING into Item Table
            db.insert_query_with_values(PredefinedQueries.insert_item,donatedItem.get_item_sql_data())
            #INSERTING into Piece Table
            for piece_table_row in donatedItem.get_piece_sql_data():
                db.insert_query_with_values(PredefinedQueries.insert_piece,piece_table_row)
            #INSERTING into DonatedBy Table
            db.insert_query_with_values(PredefinedQueries.insert_donatedby,donatedItem.get_donated_by_sql_data())
            db.commit()
        except Exception as e:
            return {"message":f"DBInsertionError while processing Donation: {str(e)}"},400
        return {"message":"Donation Accepted Succesfully"},200
