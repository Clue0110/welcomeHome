from flask import Flask
from flask_session import Session

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from welcomehome.resource.register import Register
from welcomehome.resource.donation import Donation
from welcomehome.resource.order import *
from welcomehome.resource.auth import *
from welcomehome.resource.item import Item


app = Flask(__name__)
app.secret_key="i_wish_i_cou1d_sleep_pe@cefu11y"
login_manager.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # Or "redis", "memcached", etc.
#Session(app)

api=Api(app=app)
api.add_resource(Register,'/api/register/') #POST
api.add_resource(Donation,'/api/donation/') #POST
api.add_resource(Person,'/api/person/update/') #Only for developement purpose
api.add_resource(Order,'/api/order/') #GET,POST
api.add_resource(Login,'/api/login/',endpoint="login") #POST
api.add_resource(Logout,'/api/logout/',endpoint="logout") #POST
api.add_resource(OrderStart,'/api/order/start') #POST
api.add_resource(OrderModify,'/api/order/modify') #POST, DELETE
api.add_resource(OrderPlace,'/api/order/place') #POST
api.add_resource(OrderDelete,'/api/order/delete') #DELETE
api.add_resource(Inventory,'/api/inventory') #GET

api.add_resource(Item,'/api/item/locations') #GET
api.add_resource(OrderLocations,'/api/order/locations') #GET

@app.route('/')
def home():

    return '<h1> Flask Rest API </h1>'

if __name__=="__main__":
    app.run(debug=True)