import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ.get('DATABASE_URL', "postgresql://postgres:DGJ#%&@localhost:5432/sample")


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



#Item model, it has item id, name and current availability in the warehouse.

class Item(db.Model):
    __tablename__ = 'Item'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(120))
    availability = db.Column(db.Boolean, default=False)
    shipment_items = db.relationship('Shipment_items', backref=db.backref('Item', lazy=True))

    def __init__(self, name, availability):
        self.name = name
        self.availability = availability

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()      

    def update(self):
        db.session.commit()      

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'availability': self.availability
        }


class Shipment(db.Model):
    __tablename__ = 'Shipment'

    id = Column(db.Integer, primary_key=True)
    address = Column(db.String(120))
    phone = Column(db.String(120))
    email = Column(db.String(120))
    shipment_items = db.relationship('Shipment_items', backref=db.backref('Shipment', lazy=True))

    def __init__(self, address, phone, email):
        self.address = address
        self.phone = phone
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()      

    def update(self):
        db.session.commit()      

    def format(self):
        return {
            'id': self.id,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }


class Shipment_items(db.Model):
    __tablename__ = 'Shipment_items'

    shipment_id = db.Column(db.Integer, db.ForeignKey('Shipment.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'), primary_key=True)
    quantity = Column(db.Integer)

    def __init__(self, shipment_id, item_id, quantity):
        self.shipment_id = shipment_id
        self.item_id = item_id
        self.quantity = quantity

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()      

    def update(self):
        db.session.commit()      

    def format(self):
        return {
            'shipment_id': self.shipment_id,
            'item_id': self.item_id,
            'quantity': self.quantity
        }
