from flask_restful import Resource , reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3

class Item(Resource) :
    
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price' ,
        type=float,
        required=True,
        help='This cannot be left blank'
    )

    parser.add_argument(
        'store_id' ,
        type=int,
        required=True,
        help='Every item should have store id'
    )

    @jwt_required()
    def get(self , name) :
        
        item = ItemModel.find_by_name(name)
        if item :
            return item.json()
        return {"message" : "Item not found"} , 404

    

    def post(self , name) :

        if ItemModel.find_by_name(name) :
            return {'message' : f'a item named {name} already exists..'} , 400

        data = Item.parser.parse_args()
        item = ItemModel(name , **data)

        try :
            item.save_to_database()
        except Exception as e :
            return {"Error" : "Error occurred while inserting item"} , 500

        return item.json() , 201

    def delete(self , name) :
        
        item = ItemModel.find_by_name(name)
        if item :
            item.delete_from_database()
            return {'message' : f'item {name} deleted'}
        return {"message" : "item not found"}

    def put(self , name) :
        
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item :
            item = ItemModel(name, **data)
            

        else :
            item.price = data['price']
        item.save_to_database()

        return item.json()
    # get method works with get request
    # same for post , put , delete


# itemsList
class ItemsList(Resource) :
    
    @jwt_required()
    def get(self) :
        #items = [item.json() for item in ItemModel.query.all()]
        items = list(map(lambda x: x.json() , ItemModel.query.all()))
        return {"items" : items}