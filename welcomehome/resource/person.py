from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
from flask import request, session
import sys
from flask_login import current_user, login_required
from welcomehome.resource.auth import load_user
import json
from datetime import datetime

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
                    order["role"]="delivery"
                if row.supervisor==current_userid:
                    order["role"]="supervisor"
                if row.client==current_userid:
                    order["role"]="client"
                order_details.append(order)
        except Exception as e:
            return {"message":f"There was an Error while fetching order for userid:{current_userid}: {str(e)}"},400
        return {"current_user":current_userid,"order_details":order_details},200
    
class VolunteerScoreboard(Resource):
    def get(self):
        #Input:
        #   "start_date":<starting date>
        #   "end_date":<ending date>
        
        start_date_str=request.args.get("start_date",None)
        end_date_str=request.args.get("end_date",None)

        # Considering start_date and end_date are required inputs
        if not start_date_str:
            return {"message":"Start Date cannot be Empty"},400
        if not end_date_str:
            return {"message":"End Date cannot be Empty"},400
        
        #Validate if start_date < end_date
        start_date=datetime.strptime(start_date_str, '%d-%m-%Y').date()
        end_date=datetime.strptime(end_date_str, '%d-%m-%Y').date()
        if end_date<start_date:
            return {"message":"Invalid Start and End Dates, End Date should be after Start Date"},400
        
        #Extracting the score Board
        scoreboard=[]
        db=DatabaseConn()
        try:
            #Do a query to get the desired result
            q_res=db.execute_query_with_args(PredefinedQueries.get_volunteer_task_ranking_between_dates,{"start_date":str(start_date),"end_date":str(end_date)})
            #If no rows then no tasks, return empty scoreboard
            if len(q_res)==0:
                return {"scoreboard":[]},200
            for row in q_res:
                scoreboard_entry={
                    "num_tasks":row.task_count,
                    "volunteer":row.username
                }
                scoreboard.append(scoreboard_entry)
        except Exception as e:
            return {"message":f"Error while generating the scoreboard: {str(e)}"}
        
        return {"scoreboard":scoreboard},200

        