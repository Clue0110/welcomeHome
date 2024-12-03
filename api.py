from flask import Flask

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from welcomehome.resource.register import Register
from welcomehome.resource.donation import Donation
from welcomehome.resource.order import Order
from welcomehome.resource.auth import *

app = Flask(__name__)
app.secret_key="i_wish_i_cou1d_sleep_pe@cefu11y"
login_manager.init_app(app)

api=Api(app=app)
api.add_resource(Register,'/api/register/')
api.add_resource(Donation,'/api/donation/')
api.add_resource(Person,'/api/person/update/') #Only for developement purpose
api.add_resource(Order,'/api/order/')
api.add_resource(Login,'/api/login/',endpoint="login")
api.add_resource(Logout,'/api/logout/',endpoint="logout")

@app.route('/')
def home():

    return '<h1> Flask Rest API </h1>'

if __name__=="__main__":
    app.run(debug=True)