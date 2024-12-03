from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
from flask import request
import sys


class Order(Resource):

    @classmethod
    def validatePostPutReqParams(self):
        if not request.json.get("orderID",None):
            return False,"orderID Invalid and Cannot be Null"
        if not request.json.get("orderDate",None):
            return False,"orderDate cannot be null"
        if not request.json.get("supervisor",None):
            return False,"supervisor should be assigned and cannot be left empty"
        if not request.json.get("client",None):
            return False,"Client should be assigned and cannot be left empty"
        items=request.json.get("items",[])
        if len(items)==0:
            return False,"There cannot be an empty order with no Items"
        for item_id in items:
            pass
            #if item_id is valid:
            #    return False
        return True,"Validation Succesfull"

    def get(self):
        orderID=int(request.json.get("orderID",None))
        if not orderID:
            return {"message":"OrderID cannot be null"},400
        db=DatabaseConn()
        result={}
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_order_by_id,{"orderID":orderID})
            if len(q_res)==0:
                return {"message":"Order doesnt exist"},400
            q_res=q_res[0]
            result["orderID"]=int(q_res.orderid)
            result["orderDate"]=str(q_res.orderdate)
            result["orderNotes"]=q_res.ordernotes
            result["supervisor"]=q_res.supervisor
            result["client"]=q_res.client
        except Exception as e:
            return {"message":f"GET Failed for Order Details: {str(e)}"}
        
        result["items"]=[]
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_items_in_order,{"orderID":orderID})
            if len(q_res)==0:
                return {"message":"Order doesnt exist"},400
            for item in q_res:
                result["items"].append(item.itemid)
        except Exception as e:
            return {"message":f"GET Failed for Order Items: {str(e)}"}
        return result,200

    def post(self):
        res,msg=self.validatePostPutReqParams()
        if not res:
            return {"message":f"RequestParametersValidationFailed: {msg}"},400
        update_ordered_payload={
            "orderID":request.json.get("orderID",None),
            "orderDate":request.json.get("orderDate",None),
            "orderNotes":request.json.get("orderNotes",None),
            "supervisor":request.json.get("supervisor",None),
            "client":request.json.get("client",None)
        }
        db=DatabaseConn()
        try:
            db.insert_query_with_values(PredefinedQueries.update_ordered,update_ordered_payload)
            for item_id in request.json.get("items"):
                update_itemin_payload={"ItemID":item_id,"orderID":request.json.get("orderID",None),"found":request.json.get("found",False)}
                db.insert_query_with_values(PredefinedQueries.update_itemin,update_itemin_payload)
                db.commit()
        except Exception as e:
            return {"message":f"OrderCreationError:{str(e)}"},400
        
        return {"message":f"Succesfully Updated the Order with OrderID: {request.json.get('orderID')}"},200
        

    def put(self):
        res,msg=self.validatePostPutReqParams()
        if not res:
            return {"message":f"RequestParametersValidationFailed: {msg}"},400
        insert_ordered_payload={
            "orderID":request.json.get("orderID",None),
            "orderDate":request.json.get("orderDate",None),
            "orderNotes":request.json.get("orderNotes",None),
            "supervisor":request.json.get("supervisor",None),
            "client":request.json.get("client",None)
        }
        db=DatabaseConn()
        try:
            db.insert_query_with_values(PredefinedQueries.insert_ordered,insert_ordered_payload)
            for item_id in request.json.get("items"):
                insert_itemin_payload={"ItemID":item_id,"orderID":request.json.get("orderID",None),"found":request.json.get("found",False)}
                db.insert_query_with_values(PredefinedQueries.insert_itemin,insert_itemin_payload)
                db.commit()
        except Exception as e:
            return {"message":f"OrderCreationError:{str(e)}"},400
        
        return {"message":f"Succesfully Created the Order with OrderID: {request.json.get('orderID')}"},200
