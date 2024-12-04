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
from welcomehome.resource.person import *


app = Flask(__name__)
app.secret_key="i_wish_i_cou1d_sleep_pe@cefu11y"
login_manager.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # Or "redis", "memcached", etc.
#Session(app)

api=Api(app=app)

# FEATURE 1
api.add_resource(Register,'/api/register/') #POST
api.add_resource(Login,'/api/login/',endpoint="login") #POST
api.add_resource(Logout,'/api/logout/',endpoint="logout") #POST
# FEATURE 2
api.add_resource(Item,'/api/item/locations') #GET
# FEATURE 3
api.add_resource(OrderLocations,'/api/order/locations') #GET
# FEATURE 4
api.add_resource(Donation,'/api/donation/') #POST
# FEATURE 5
api.add_resource(OrderStart,'/api/order/start') #POST
# FEATURE 6
api.add_resource(OrderModify,'/api/order/modify') #POST, DELETE
api.add_resource(Inventory,'/api/inventory') #GET
# FEATURE 7
api.add_resource(OrderPlace,'/api/order/place') #POST
api.add_resource(OrderDelete,'/api/order/delete') #DELETE
# FEATURE 8
api.add_resource(PersonOrders,'/api/person-orders/') #GET

# OTHERS
api.add_resource(Order,'/api/order/') #GET,POST
api.add_resource(Person,'/api/person/update/') #Only for developement purpose

@app.route('/')
def home():

    return '<h1> Flask Rest API </h1>'

if __name__=="__main__":
    app.run(debug=True)