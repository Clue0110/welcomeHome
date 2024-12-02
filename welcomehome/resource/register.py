from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
#from api import db
from flask import request


class Register(Resource):
    @classmethod
    def validateRequestParams(self):
        if not request.json.get('username',None):
            return False
        if not request.json.get('password',None):
            return False
        if not request.json.get('fname',None):
            return False
        if not request.json.get('lname',None):
            return False
        if not request.json.get('email',None):
            return False
        if not request.json.get('phone',None):
            return False
        if not request.json.get('roleID',None) and type(request.json.get('roleID'))==int:
            return False
        return True

    def get(self):
        if not self.validateRequestParams():
            return {"message":"Invalid Fields"},400
        payload={
            "userName": request.json.get('username'),
            "password": request.json.get('password'),
            "fname":request.json.get('fname'),
            "lname":request.json.get('lname'),
            "email":request.json.get('email'),
            "phone":request.json.get("phone"),
            "roleID":request.json.get('roleID')
        }
        return payload,200

    def post(self):
        db=DatabaseConn()
        if not self.validateRequestParams():
            return {"message":"Invalid Fields"},400
        # INSERTING into the Person Table
        insert_person_payload={
            "userName": request.json.get('username'),
            "password": request.json.get('password'),
            "fname":request.json.get('fname'),
            "lname":request.json.get('lname'),
            "email":request.json.get('email')
        }
        try:
            db.insert_query_with_values(PredefinedQueries.insert_person,insert_person_payload)
            db.commit()
        except Exception as e:
            return {"message":f"RegistrationError: {str(e)}"}
        
        #INSERTING into the PersonPhone Table
        phoneNums=request.json.get("phone")
        for phoneNum in phoneNums:
            insert_person_phone_payload={
                "userName":request.json.get('username'),
                "phone":phoneNum
            }
            try:
                db.insert_query_with_values(PredefinedQueries.insert_person_phone,insert_person_phone_payload)
                db.commit()
            except Exception as e:
                return {"message":f"RegistrationError while enetering Phone Number: {str(e)}"}

        #INSERTING into the Act Table
        insert_act_payload={
            "userName":request.json.get('username'),
            "roleID":request.json.get('roleID')
        }

        try:
            db.insert_query_with_values(PredefinedQueries.insert_act,insert_act_payload)
            db.commit()
        except Exception as e:
            return {"message":f"RegistrationError: {str(e)}"}
        
        return {"message":"Registration Successful"},200
    
    


