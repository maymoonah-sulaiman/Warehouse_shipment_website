import os
from flask import Flask, jsonify, abort, request
from models import setup_db
from flask_cors import CORS
from models import *

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        greeting = "Hello first app"
        return greeting

    @app.route('/items')
    def get_all_items():
        items = Item.query.all()
        #if len(items) == 0:
            #abort(404)

        return jsonify({
            'success': True,
            'items': items
        }), 200

    @app.route('/items', methods=['POST'])
    def create_new_item():
        #request_data = request.get_json()

        #item = Item(name=request_data.get('name'), availability=request_data.get('availability'))
        #item.insert()

        return jsonify({
            'success': True,
            'item': 'request_data.get('name')'
        }), 200

    @app.route('/items/<int:item_id>', methods=['PATCH'])
    def edit_item_availability(payload, item_id):
        request_data = request.get_json()
        item = Item.query.filter_by(id=item_id).one_or_none()
        if item is None:
            abort(404)
        if request_data.get('availability'):
            item.availability = request_data.get('availability')
        item.update()

        return jsonify({
            'success': True,
            'item': item.id
        }), 200    

    @app.route('/shipments')
    def get_all_shipments():
        shipments = Shipment.query.all()
        if len(shipments) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'shipments': shipments
        }), 200


    @app.route('/shipments', methods=['POST'])
    def create_new_shipment(payload):
        request_data = request.get_json()

        shipment = Shipment(address=request_data.get('address'), phone=request_data.get('phone'), email=request_data.get('email'))
        shipment.insert()

        items = request_data.get('items')
        for item in items:
            shipment_item = Shipment_items(shipment_id=shipment.id, item_id=item.id, quantity=item.quantity)
            shipment_item.insert()
        #[{'id':'1', 'quantity':'4'}, {'id':'6', 'quantity':'9'}]

        return jsonify({
            'success': True,
            'shipment': shipment.format()
        }), 200

    @app.route('/shipments/<int:shipment_id>', methods=['PATCH'])
    def edit_shipment(payload, shipment_id):
        request_data = request.get_json()
        shipment = Shipment.query.filter_by(id=shipment_id).one_or_none()
        if shipment is None:
            abort(404)
        if request_data.get('address'):
            shipment.address = request_data.get('address')
        if request_data.get('phone'):
            shipment.phone = request_data.get('phone')
        if request_data.get('email'):
            shipment.email = request_data.get('email')   
        shipment.update()

        return jsonify({
            'success': True,
            'item': shipment.format()
        }), 200    

    @app.route('/shipments/<int:shipment_id>', methods=['DELETE'])
    def delete_a_shipment(payload, shipment_id):
        shipment = Shipment.query.filter_by(id=shipment_id).one_or_none()
        if shipment is None:
            abort(404)
        shipment.delete()
        shipment_items = Shipment_items.query.filter_by(shipment_id=shipment.id).all()
        for item in shipment_items:
            item.delete()
        return jsonify({
            "success": True,
            "delete": shipment_id
        }), 200    


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    