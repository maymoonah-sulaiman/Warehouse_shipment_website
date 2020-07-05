import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json



database_path = os.environ['DATABASE_URL']
#"postgresql://postgres:DGJ#%&@localhost:5432/website"

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
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    availability = db.Column(db.Boolean, default=False)
    shipment_items = db.relationship('Shipment_items', backref=db.backref('item', lazy=True))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'availability': self.availability
        }


class Shipment(db.Model):
    __tablename__ = 'shipment'

    shipment_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    email = db.Column(db.String(120))
    shipment_items = db.relationship('Shipment_items', backref=db.backref('shipment', lazy=True))


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
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }


class Shipment_items(db.Model):
    __tablename__ = 'shipment_items'

    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.shipment_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True)
    quantity = db.Column(db.Integer)

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
