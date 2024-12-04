from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from welcomehome.common.psql_mappings import *
from welcomehome.common.util.database_util import DatabaseConn
from flask import request, session
import sys
from flask_login import current_user, login_required
from welcomehome.resource.auth import load_user
import json

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

class OrderUtils_old:
    def safe_intialize_order_storage():
        if not session.get("orders",None):
            session["orders"]={}

    def get_order_with_orderid(OrderID):
        if type(OrderID)==int:
            OrderID=str(OrderID)
        OrderUtils.safe_intialize_order_storage()
        return session["orders"].get(OrderID,None)
    
    def get_order_with_clientid(client):
        OrderUtils.safe_intialize_order_storage()
        for orderID in session["orders"]:
            if session["orders"][orderID]["client"]==client:
                return session["orders"][orderID]
        return None
    
    def get_order_with_orderid_or_clientid(OrderID=None,client=None):
        if not OrderID and not client:
            return None
        if OrderID:
            return OrderUtils.get_order_with_orderid(OrderID)
        if client:
            return OrderUtils.get_order_with_clientid(client)
        return None
    
    def add_new_order_to_storage(OrderID,client):
        OrderUtils.safe_intialize_order_storage()
        if type(OrderID)==int:
            OrderID=str(OrderID)
        session["orders"][OrderID]={}
        session["orders"][OrderID]["OrderID"]=OrderID
        session["orders"][OrderID]["client"]=client
        session["orders"][OrderID]["cart"]=[]
        return session["orders"][OrderID]
    
    def give_me_new_order_id():
        OrderUtils.safe_intialize_order_storage()
        max_order_id=-1
        for orderID in session["orders"]:
            max_order_id=max(max_order_id,orderID)
        #Finding the Next Max Key from the Database
        db=DatabaseConn()
        prev_orderid=-1
        try:
            q_res=db.execute_query(PredefinedQueries.get_highest_orderid)
            if len(q_res)==0:
                prev_orderid=0
            else:
                q_res=q_res[0]
                prev_orderid=int(q_res.max_order_id)
        except Exception as e:
            return None
        #Returnig the New Order ID
        max_order_id=max(prev_orderid,max_order_id)
        return max_order_id+1

    def validate_item_with_id(ItemID):
        db=DatabaseConn()
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_item_by_id,{"ItemID":ItemID})
            if len(q_res)==0:
                return False
        except Exception as e:
            return False
        return True
    
    def add_item_to_order(OrderID,ItemID):
        OrderUtils.safe_intialize_order_storage()
        # Checking if this Item exists in Database
        if not OrderUtils.validate_item_with_id(ItemID):
            return None
        # Fetch the appropriate order
        current_order=OrderUtils.get_order_with_orderid(OrderID)
        if current_order==None:
            return None
        # If Item is already in the Cart
        if ItemID in current_order["cart"]:
            return None
        #session["orders"][str(current_order["OrderID"])]["cart"].append(ItemID)
        current_order["cart"].append(ItemID)
        #session["orders"][str(current_order["OrderID"])]["cart"]=current_order["cart"]
        #return session["orders"][str(current_order["OrderID"])]["cart"]
        return current_order["cart"]
    
    def remove_order_from_storage(OrderID):
        if type(OrderID)==int:
            OrderID=str(OrderID)
        return session["orders"].pop(OrderID)
    
    def place_order(OrderID=None,client=None):
        if type(OrderID)==int:
            OrderID=str(OrderID)
        OrderUtils.safe_intialize_order_storage()
        if OrderID:
            if not OrderID in session["orders"]:
                return None
        elif client:
            current_order=OrderUtils.get_order_with_clientid(client)
            if current_order==None:
                return None
            OrderID=current_order["OrderID"]
        
        return OrderUtils.remove_order_from_storage(OrderID)
    
    def get_all_items_in_carts():
        OrderUtils.safe_intialize_order_storage()
        cart_items=[]
        for OrderID in session["orders"]:
            for item in session["orders"][OrderID]["cart"]:
                cart_items.append(item)
        return cart_items
    
    def get_current_shopping_cart(OrderID):
        current_order=OrderUtils.get_order_with_orderid(OrderID)
        if current_order==None:
            return None
        return current_order.get("cart",None)
    
    def remove_item_from_shopping_cart(OrderID,ItemID):
        current_order=OrderUtils.get_order_with_orderid(OrderID)
        if not current_order:
            return None
        if ItemID in current_order["cart"]:
            current_order.remove(ItemID)
            return current_order["cart"]
        return current_order["cart"]
    
    def clear_session():
        session["orders"]={}

class OrderObject:
    def __init__(self,json_str=None,args=None):
        if not args==None:
            self.orderid=args["OrderID"]
            self.client=args["client"]
            self.cart=[]
            self.json_data={
                "OrderID":self.orderid,
                "client":self.client,
                "cart":[]
            }
            return
        data = json.loads(json_str)
        self.orderid=data["OrderID"]
        self.client=data["client"]
        self.cart=data["cart"]
        self.json_data=data

    def get_json_object(self):
        return self.json_data
    
    def get_json_str(self):
        return json.dumps(self.json_data)
    
    def get_orderid(self):
        return self.orderid
    
    def get_client(self):
        return self.client
    
    def get_cart(self):
        return self.cart
    
    def add_item(self,ItemID):
        if not ItemID in self.cart:
            self.cart.append(ItemID)

    def remove_item(self,ItemID):
        if ItemID in self.cart:
            self.cart.remove(ItemID)

class OrderUtils:
    def safe_intialize_order_storage():
        if not session.get("orders",None):
            session["orders"]={}

    def get_order_with_orderid(OrderID,need_obj=False):
        if type(OrderID)==int:
            OrderID=str(OrderID)
        OrderUtils.safe_intialize_order_storage()
        if not session["orders"].get(OrderID,None):
            return None
        current_order=OrderObject(json_str=session["orders"].get(OrderID))
        return current_order.get_json_object() if not need_obj else current_order
    
    def get_order_with_clientid(client,need_obj=False):
        OrderUtils.safe_intialize_order_storage()
        for orderID in session["orders"]:
            temp_order=OrderObject(json_str=session["orders"][orderID])
            if temp_order.get_client()==client:
                return temp_order.get_json_object() if not need_obj else temp_order
        return None
    
    def get_order_with_orderid_or_clientid(OrderID=None,client=None,need_obj=False):
        if not OrderID and not client:
            return None
        if OrderID:
            return OrderUtils.get_order_with_orderid(OrderID,need_obj)
        if client:
            return OrderUtils.get_order_with_clientid(client,need_obj)
        return None
    
    def modify_order_with_orderid(OrderID,json_str):
        #print(f"session orders:{session['orders']}",file=sys.stdout)
        if type(OrderID)==int:
            OrderID=str(OrderID)
        temp_copy=session["orders"].copy()
        temp_copy.pop(OrderID)
        temp_copy[OrderID]=json_str
        session["orders"]=temp_copy
    
    def add_new_order_to_storage(OrderID,client):
        OrderUtils.safe_intialize_order_storage()
        if type(OrderID)==int:
            OrderID=str(OrderID)
        current_order=OrderObject(args={"OrderID":OrderID,"client":client})
        session["orders"][OrderID]=current_order.get_json_str()
        return current_order
    
    def give_me_new_order_id():
        OrderUtils.safe_intialize_order_storage()
        max_order_id=-1
        for orderID in session["orders"]:
            max_order_id=max(max_order_id,int(orderID))
        #Finding the Next Max Key from the Database
        db=DatabaseConn()
        prev_orderid=-1
        try:
            q_res=db.execute_query(PredefinedQueries.get_highest_orderid)
            if len(q_res)==0:
                prev_orderid=0
            else:
                q_res=q_res[0]
                prev_orderid=int(q_res.max_order_id)
        except Exception as e:
            return None
        #Returnig the New Order ID
        max_order_id=max(prev_orderid,max_order_id)
        return max_order_id+1

    def validate_item_with_id(ItemID):
        db=DatabaseConn()
        try:
            q_res=db.execute_query_with_args(PredefinedQueries.get_item_by_id,{"ItemID":ItemID})
            if len(q_res)==0:
                return False
        except Exception as e:
            return False
        return True
    
    def add_item_to_order(OrderID,ItemID):
        OrderUtils.safe_intialize_order_storage()
        # Checking if this Item exists in Database
        if not OrderUtils.validate_item_with_id(ItemID):
            return None
        # Fetch the appropriate order
        current_order=OrderUtils.get_order_with_orderid(OrderID,need_obj=True)
        if current_order==None:
            return None
        #Add Item to the Order Object
        current_order.add_item(ItemID)
        #Modify the Session data for that ID
        OrderUtils.modify_order_with_orderid(current_order.get_orderid(),current_order.get_json_str())
        return current_order.get_cart()
    
    def remove_order_from_storage(OrderID):
        if type(OrderID)==int:
            OrderID=str(OrderID)
        temp_copy=session["orders"].copy()
        current_order_str=temp_copy.pop(OrderID)
        session["orders"]=temp_copy
        return OrderObject(json_str=current_order_str).get_json_object()
    
    def place_order(OrderID=None,client=None): 
        if type(OrderID)==int:
            OrderID=str(OrderID)
        OrderUtils.safe_intialize_order_storage()
        if OrderID:
            if not OrderID in session["orders"]:
                return None
        elif client:
            current_order=OrderUtils.get_order_with_clientid(client,need_obj=True)
            if current_order==None:
                return None
            OrderID=current_order.get_orderid()
        return OrderUtils.remove_order_from_storage(OrderID)
    
    def get_all_items_in_carts():
        OrderUtils.safe_intialize_order_storage()
        cart_items=[]
        for OrderID in session["orders"]:
            temp_order=OrderObject(json_str=session["orders"][OrderID])
            for item in temp_order.get_cart():
                cart_items.append(item)
        return cart_items
    
    def get_current_shopping_cart(OrderID):
        current_order=OrderUtils.get_order_with_orderid(OrderID,need_obj=True)
        if current_order==None:
            return None
        return current_order.get_cart()
    
    def remove_item_from_shopping_cart(OrderID,ItemID):
        current_order=OrderUtils.get_order_with_orderid(OrderID,need_obj=True)
        if not current_order:
            return None
        current_order.remove_item(ItemID)
        OrderUtils.modify_order_with_orderid(current_order.get_orderid(),current_order.get_json_str())
        return current_order.get_cart()
    
    def clear_session():
        session["orders"]={}

class OrderStart(Resource):
    def post(self):
        # Input: "client":"<client_id>"
        #print(f"Orders: {session["orders"]}",file=sys.stdout)
        #Validate if Current User is a Staff Member
        if not RoleMappings.isStaff(current_user.get_role()):
            return {"message":"Only Staff Members are authorized to start an order"},400
        #Validate if Client is not Empty
        if not request.json.get("client",None):
            return {"message":"Client ID cannot be empty"},400
        
        #Checking if Client exists in DB and has the Client role
        client_user=load_user(request.json.get("client"))
        if client_user==None:
            return {"message":"Client does not exist"},400
        if not RoleMappings.isClient(client_user.get_role()):
            return {"message":f"User not registered as a Client"},400
        
        #Validate if the Client already has an ongoing order
        current_order=OrderUtils.get_order_with_clientid(request.json.get("client"))
        if current_order:
            return {"message":f"There is already an Order: {current_order["OrderID"]} Ongoing for Client: {current_order['client']}"},400
        
        OrderID=OrderUtils.give_me_new_order_id()
        OrderUtils.add_new_order_to_storage(OrderID,request.json.get("client"))
        return {"message":f"Order: {OrderID} created for client: {request.json.get('client')}"},200



class OrderModify(Resource):
    def post(self):
        # Input: "ItemID":<ItemID>, 
        # Input: "client:<client ID>
        # Input: "OrderID":<OrderID>
        #print(f"Orders: {session["orders"]}",file=sys.stdout)
        # Get the order with Client ID ot Order ID
        current_order=OrderUtils.get_order_with_orderid_or_clientid(OrderID=request.json.get("OrderID",None),
                                                                    client=request.json.get("client",None))
        #print(f"current_order={current_order}",file=sys.stdout)
        if current_order==None:
            return {"message":"Order not found"},400
        
        #Validate that the item exists
        if not request.json.get("ItemID",None):
            return {"message":"Please provide an Item to Add to the Order"},400
        # Validate the Item ID
        current_cart=OrderUtils.add_item_to_order(OrderID=current_order["OrderID"],ItemID=request.json.get("ItemID"))
        if not current_cart:
            return {"message":f"Cannot add Item: {request.json.get('ItemID')} to Order: {current_order['OrderID']}"},400
        print(f"Session: {session["orders"]}",file=sys.stdout)
        return {"message":f"Added Item: {request.json.get('ItemID')} to Order: {current_order['OrderID']}. Cart: {current_cart}"},200

    def delete(self):
        # Input: "ItemID":<ItemID>
        # Input: "client:<client ID>
        # Input: "OrderID":<OrderID>

        #OrderUtils.clear_session()
        #return {},400

        # Checking if the Order Exists
        # Get the order with Client ID ot Order ID
        current_order=OrderUtils.get_order_with_orderid_or_clientid(OrderID=request.json.get("OrderID",None),
                                                                    client=request.json.get("client",None))
        #print(f"current_order={current_order}",file=sys.stdout)
        if current_order==None:
            return {"message":"Order not found"},400
        
        current_cart=OrderUtils.get_current_shopping_cart(current_order["OrderID"])
        current_item=request.json.get("ItemID",None)
        if current_item==None:
            return {"message":"Item cannot be Empty"},400
        current_cart=OrderUtils.remove_item_from_shopping_cart(current_order["OrderID"],current_item)
        if current_cart==None:
            return {"message":f"Removing Item: {current_item} from {current_order['OrderID']} failed"},400
        #print(f"Session: {session["orders"]}",file=sys.stdout)
        return {"message":f"Removed Item: {current_item} from {current_order['OrderID']}. Cart: {current_cart}"},200

class Inventory(Resource):
    def get(self):
        #Inputs:
        #   client or OrderID
        #   category -> Priority 1
        #   sub_category -> Priority 2 (Needs Category too)

        #Get list of all Items
        category=request.json.get("mainCategory",None)
        sub_category=request.json.get("sub_category",None)
        get_inventory_query=PredefinedQueries.get_inventory_items_with_subcategory
        get_inventory_payload={"mainCategory":category,"subCategory":sub_category}
        if not sub_category:
            get_inventory_query=PredefinedQueries.get_inventory_items_with_category
            get_inventory_payload.pop("subCategory")
        if not category:
            get_inventory_query=PredefinedQueries.get_inventory_items
            get_inventory_payload.pop("mainCategory")
        
        # Getting the current Cart Items by either clientid or orderid
        current_order=OrderUtils.get_order_with_orderid_or_clientid(OrderID=request.json.get("OrderID",None),
                                                                    client=request.json.get("client",None))
        if current_order==None:
            return {"message":"Order Does not exist for this Client or OrderID. Please Create an Order to view Inventory"},400
        current_cart=OrderUtils.get_current_shopping_cart(current_order["OrderID"])
        
        # Fetching the Inventory Items
        db=DatabaseConn()
        inventory=[]
        try:
            q_res=db.execute_query_with_args(get_inventory_query,get_inventory_payload)
            for item_row in q_res:
                if item_row.itemid in current_cart:
                    continue
                inventory_dict={
                    "itemid":item_row.itemid,
                    "idescription":item_row.idescription,
                    "photo":item_row.photo,
                    "isnew":item_row.isnew,
                    "haspieces":item_row.haspieces,
                    "material":item_row.material,
                    "maincategory":item_row.maincategory,
                    "subcategory":item_row.subcategory
                }
                inventory.append(inventory_dict)
        except Exception as e:
            return {"message":"DBRead Error while extracting Inventory"},400
        return {"inventory":inventory},200

class OrderPlace(Resource):
    def validatePostRequestArguments(self):
        if not request.json.get("orderDate",None):
            return False,"orderDate cannot be Empty"
        if not request.json.get("orderNotes",None):
            return False,"OrderNotes cannot be empty"
        #Checking if Supervisor exists and has a staff role
        if not request.json.get("supervisor",None):
            return False,"Supervisor Field Cannot be Empty"
        return True, "Validation Successful"
        
        
    def post(self):
        #Input:
        #   "orderDate":"<Date>"
        #   "orderNotes":"<notes>"
        #   "supervisor":"<person_id>"
        #   "orderID" or "clientID"
        print(f"Session: {session["orders"]}",file=sys.stdout)
        #Checking if the Order Exists with current Order ID or Client ID
        current_order=OrderUtils.get_order_with_orderid_or_clientid(OrderID=request.json.get("OrderID"),client=request.json.get("client"))
        if current_order==None:
            return {"message":"There is no current order in progress"},400
        #Checking if the Post Request Parameters Pass the Validation Check
        validation_res,msg=self.validatePostRequestArguments()
        if not validation_res:
            return {"message":f"Parameter Validation Failed. Error: {msg}"},400
        #Checking if the Current Cart is empty
        current_cart=OrderUtils.get_current_shopping_cart(OrderID=current_order["OrderID"])
        print(f"cart: {current_cart}",file=sys.stdout)
        if current_cart==None:
            return {"message":f"Shopping Cart for Order: {current_order['OrderID']} is empty"},400
        if len(current_cart)==0:
            return {"message":f"Shopping Cart is Empty for the Order: {current_order['OrderID']}"},400
        #Checking if the Supervisor is actually registered as a staff member
        supervisor=load_user(request.json.get("supervisor"))
        if supervisor==None:
            return {"message":"Supervisor does not exist"},400
        if not RoleMappings.isStaff(supervisor.get_role()):
            return {"message":f"User not registered as a Staff"},400
        #TODO Add a Validation Check the current item isnt in ItemIn Table
        #Creating an Entry for the Ordered Table
        insert_ordered_payload={
            "orderID":int(current_order["OrderID"]),
            "orderDate":request.json.get("orderDate",None),
            "orderNotes":request.json.get("orderNotes",None),
            "supervisor":request.json.get("supervisor",None),
            "client":current_order["client"]
        }
        db=DatabaseConn()
        try:
            db.insert_query_with_values(PredefinedQueries.insert_ordered,insert_ordered_payload)
            #Adding Each Item in the ItemIn Table
            for ItemID in current_cart:
                insert_itemin_payload={
                    "ItemID":ItemID,
                    "orderID":int(current_order["OrderID"]),
                    "found":False
                }
                db.insert_query_with_values(PredefinedQueries.insert_itemin,insert_itemin_payload)
            db.commit()
        except Exception as e:
            return {"message":f"DBInsertException: {str(e)}"},400
        
        #Remove The Order from Pending Orders (Session variable)
        removed_order=OrderUtils.place_order(OrderID=current_order["OrderID"])
        if removed_order==None:
            return {"message":f"Error while removing Order:{current_order['OrderID']} from Storage"},400
        return {"message":f"Successfully Placed Order: {removed_order["OrderID"]} with the Items: {removed_order["cart"]}"},200

class OrderDelete(Resource):
    def delete(self):
        #Input: "orderID" or "clientID"
        #Checking if the Order Exists with current Order ID or Client ID
        print(f"Session Orders:{session["orders"]}",file=sys.stdout)
        current_order=OrderUtils.get_order_with_orderid_or_clientid(OrderID=request.json.get("OrderID"),client=request.json.get("client"))
        if current_order==None:
            return {"message":"There is no current order in progress"},400
        #Remove The Order from Pending Orders (Session variable)
        removed_order=OrderUtils.place_order(OrderID=current_order["OrderID"])
        if removed_order==None:
            return {"message":f"Error while removing Order:{current_order['OrderID']} from Storage"},400
        return {"message":f"Removed Order: {removed_order["OrderID"]} with the Items: {removed_order["cart"]}"},200