from flask import Flask

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

#from welcomehome.common.util.database_util import DatabaseConn
from welcomehome.resource.register import Register
from welcomehome.resource.donation import Donation
from welcomehome.resource.order import PlaceOrder



#db_uri=URL.create(
#    drivername="postgresql",
#    username="postgres",
#    password="clueless1001",
#    host="hostname",
#    database="welcomehome"
#)
#db=DatabaseConn(db_uri=db_uri)

app = Flask(__name__)

api=Api(app=app)
api.add_resource(Register,'/api/register/')
api.add_resource(Donation,'/api/donation/')
api.add_resource(PlaceOrder,'/api/order/place')

@app.route('/')
def home():

    return '<h1> Flask Rest API </h1>'

if __name__=="__main__":
    app.run(debug=True)