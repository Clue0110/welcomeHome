from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
#from api import db
from welcomehome.common.util.database_util import DatabaseConn

item_get_req_parser = reqparse.RequestParser()
item_get_req_parser.add_argument('item_id',type=int,help="Item ID",required=True)

class Item(Resource):
    def get(self):
        db=DatabaseConn()
        args=item_get_req_parser.parse_args()
        query_args={"ITEM_ID":args.item_id}
        result=db.execute_query_with_args(PredefinedQueries.get_all_pieces_locations,query_args)
        return result

    def post(self):
        # Update the ITEM table
        # Update the PIECE table
        pass


