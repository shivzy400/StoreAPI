from flask_restful import Resource
from models.store import StoreModel

class Store(Resource) :

    def get(self , name) :
        store = StoreModel.find_by_name(name) 
        if store :
            return store.json()
        return {"message" : "Store not found"} , 404
    
    def post(self , name) :
        if StoreModel.find_by_name(name) :
            return {"message" : f"Store '{name}' Already exist"} , 400
        
        store = StoreModel(name)
        try :
            store.save_to_database()
        except :
            return {"message" : "An error occured while adding store"} , 500

        return store.json() , 201

    def delete(self , name) :
        store = StoreModel.find_by_name(name) 
        if store :
            store.delete_from_database()
            return {"message" : "Store Deleted"}
        return {"message" : "Store does'nt exist"} , 400


class StoreList(Resource) :

    def get(self) :
        stores = [store.json for store in StoreModel.query.all()]
        return {"stores" : stores}