import sqlite3
from database import db

class StoreModel(db.Model) :

    __tablename__ = 'stores'

    #columns
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel' , lazy='dynamic')

    def __init__(self , name) :

        self.name = name

    def json(self) :
        return {"name" : self.name , "item" : [item.json() for item in self.items.all()]}
    
    @classmethod
    def find_by_name(cls , name) :
        return cls.query.filter_by(name=name).first() # same as SELECT * from items WHERE name = name LIMIT 1
     
    def save_to_database(self) :
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self) :
        
        db.session.delete(self)
        db.session.commit()