from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
from flask import request, session
import sys
from flask_login import current_user, login_required
from welcomehome.resource.auth import load_user
import json

item_get_req_parser = reqparse.RequestParser()
item_get_req_parser.add_argument('item_id',type=int,help="Item ID",required=True)

class Item(Resource):
    def get(self):
        # Input: "ItemID":<item_id>
        #Validating if the ItemID is valid
        ItemID=request.args.get("ItemID",None)
        if ItemID==None:
            return {"message":"RequestParametersValidationFailed: ItemID value cannot be Null or empty"},400
        db=DatabaseConn()
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_item_by_id,{"ItemID":ItemID})
            if not len(q_res)>0:
                return {"message":f"Item with ItemID: {ItemID} does not exist"},400
        except Exception as e:
            return {"message":"DBReadError: Error while validating the ItemID"},400
        
        db=DatabaseConn()
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_all_pieces_locations,{"ItemID":ItemID})
            locations=[]
            for piece in q_res:
                location_info={
                    "piecenum":piece.piecenum,
                    "roomnum":piece.roomnum,
                    "shelfnum":piece.shelfnum,
                    "shelfdescription":piece.shelfdescription
                }
                locations.append(location_info)
        except Exception as e:
            return {"message":"Error while extracting Pieces Locations"},400
        return {"locations":locations},200


