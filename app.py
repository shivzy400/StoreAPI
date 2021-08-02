from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate , identity
from resources.user import UserRegister
from resources.item import Item , ItemsList
from resources.store import Store , StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'shivam'
api = Api(app)

@app.before_first_request
def create_table() :
    db.create_all()

jwt = JWT(app , authenticate , identity) # it creates an endpoint '/auth'


api.add_resource(Item , '/item/<string:name>')
# address http://localhost:5000/item/any_name
api.add_resource(ItemsList , '/items')
# address http://localhost:5000/items
api.add_resource(UserRegister , '/register')
# address http://localhost:5000/register
api.add_resource(Store , '/store/<string:name>')
api.add_resource(StoreList , '/stores')

if __name__ == '__main__' :
    from database import db
    db.init_app(app)
    app.run(port=5001 , debug=True)