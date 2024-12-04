from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
from flask import request, session
import sys
from flask_login import current_user, login_required
from welcomehome.resource.auth import load_user
import json

class PersonOrders(Resource):
    def get(self):
        current_userid=current_user.get_id()
        db=DatabaseConn()
        order_details=[]
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_all_orders_related_to_user,{"username":current_userid})
            if len(q_res)==0:
                return {"current_user":current_userid,"order_details":[]},200
            for row in q_res:
                order={}
                order["orderid"]=row.orderid
                if row.volunteer==current_userid:
                    order["role"]="volunteer"
                if row.supervisor==current_userid:
                    order["role"]="supervisor"
                if row.client==current_userid:
                    order["role"]="client"
                order_details.append(order)
        except Exception as e:
            return {"message":f"There was an Error while fetching order for userid:{current_userid}: {str(e)}"},400
        return {"current_user":current_userid,"order_details":order_details},200