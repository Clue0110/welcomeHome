from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required
from welcomehome.common.util.database_util import DatabaseConn
from welcomehome.common.psql_mappings import *
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sys

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self):
        self.userName=""
        self.fname=""
        self.lname=""
        self.email=""
        self.role=-1

    def set_username(self,userName):
        self.userName=userName
    
    def set_fname(self,fname):
        self.fname=fname
    
    def set_lname(self,lname):
        self.lname=lname
    
    def set_email(self,email):
        self.email=email

    def set_role(self,role):
        self.role=role

    def get_role(self):
        return self.role

    def set_password(self,password):
        self.password=password

    def authenticate_password(self,password):
        #print(f"Is {self.password} == {hashed_password}??",file=sys.stdout)
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.userName



@login_manager.user_loader
def load_user(user_id):
    db=DatabaseConn()
    # Getting Details from Person Table
    q_res=db.execute_query_with_args(PredefinedQueries.get_person_by_username,{"userName":user_id})
    if len(q_res)==0:
        return None
    q_res=q_res[0]
    user=User()
    user.set_username(user_id)
    user.set_email(q_res.email)
    user.set_fname(q_res.fname)
    user.set_lname(q_res.lname)
    user.set_password(q_res.password)
    # Getting Details from Act Table
    q_res=db.execute_query_with_args(PredefinedQueries.get_role_by_username,{"userName":user_id})
    if len(q_res)==0:
        return None
    q_res=q_res[0]
    user.set_role(int(q_res.roleid))

    return user

class Login(Resource):
    def post(self):
        if current_user.is_authenticated:
            return {"message":"User Logged In"},200
        data=request.json
        username=data["username"]
        password=data["password"]
        user=load_user(username)
        if not user:
            return {'message': f'Username ({username}) Doesnt Exist, Please Register'}, 400
        #Authenticate the User
        #hashed_password=generate_password_hash(password)
        if not user.authenticate_password(password):
            return {'message': 'Invalid Password, Try Again'}, 400
        #Login the user
        login_user(user)
        return {"message":f"User Logged In #{current_user.get_id()}"},200
    
class Logout(Resource):
    def post(self):
        print(f"Logging our Current User: {current_user.get_id()}",file=sys.stdout)
        logout_user()
        return {"message":"User Logged Out"},200
    
class Person(Resource):

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

    def post(self):
        db=DatabaseConn()
        if not self.validateRequestParams():
            return {"message":"Invalid Fields"},400
        # INSERTING into the Person Table
        update_person_payload={
            "userName": request.json.get('username'),
            "password": generate_password_hash(request.json.get('password')),
            "fname":request.json.get('fname'),
            "lname":request.json.get('lname'),
            "email":request.json.get('email')
        }
        try:
            db.update_query_with_values(PredefinedQueries.update_person,update_person_payload)
            db.commit()
        except Exception as e:
            return {"message":f"PersonUpdateError: {str(e)}"}
        
        #INSERTING into the PersonPhone Table
        phoneNums=request.json.get("phone")
        for phoneNum in phoneNums:
            update_person_phone_payload={
                "userName":request.json.get('username'),
                "phone":phoneNum
            }
            try:
                db.update_query_with_values(PredefinedQueries.update_person_phone,update_person_phone_payload)
                db.commit()
            except Exception as e:
                return {"message":f"PersonUpdateError while enetering Phone Number: {str(e)}"}

        #INSERTING into the Act Table
        update_act_payload={
            "userName":request.json.get('username'),
            "roleID":request.json.get('roleID')
        }

        try:
            db.update_query_with_values(PredefinedQueries.update_act,update_act_payload)
            db.commit()
        except Exception as e:
            return {"message":f"PersonUpdateError: {str(e)}"}
        
        return {"message":"Person Update Successful"},200