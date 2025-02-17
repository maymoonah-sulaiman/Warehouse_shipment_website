import os
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from models import setup_db, Item, Shipment, Shipment_items
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def get_greeting():
        greeting = "Hello! Welcome to the warehouse shipment system!"
        return greeting


    @app.route('/items')
    @requires_auth('get:items')
    def get_all_items(payload):
        items = Item.query.all()
        if len(items) == 0:
            abort(404)
        all_items = []
        for item in items:
            all_items.append(item.format())
        return jsonify({
            'success': True,
            'items': all_items
        })


    @app.route('/items', methods=['POST'])
    @requires_auth('post:items')
    def create_new_item(payload):
        request_data = request.get_json()
        try:
            if(request_data.get('name') is None or request_data.get('availability') is None):
                abort(422)
            item = Item(name=request_data.get('name'), availability=request_data.get('availability'))
            item.insert()
            return jsonify({
                'success': True,
                'item': item.item_id
            })
        except:
            abort(422) 



    @app.route('/items/<int:item_id>', methods=['PATCH'])
    @requires_auth('patch:items')
    def edit_item_availability(payload, item_id):
        request_data = request.get_json()
        item = Item.query.filter_by(item_id=item_id).one_or_none()
        if item is None:
            abort(404)
        if request_data.get('availability') is not None:
            item.availability = request_data.get('availability')
        item.update()

        return jsonify({
            'success': True,
            'item': item.item_id
        })



    @app.route('/shipments')
    @requires_auth('get:shipments')
    def get_all_shipments(payload):
        shipments = Shipment.query.all()
        if len(shipments) == 0:
            abort(404)

        all_shipments = []
        for shipment in shipments:
            all_shipments.append(shipment.format())
   
        items = Shipment_items.query.join(Item).filter(Shipment_items.shipment_id == shipments[0].shipment_id).all()
        shipment_items = []
        for item in items:
            shipment_items.append({
            #"item": item.name,
            "quantity": item.quantity})
            #all_shipments.append(shipment.format(items))
        return jsonify({
            'success': True,
            'shipments': all_shipments
        })



    @app.route('/shipments', methods=['POST'])
    @requires_auth('post:shipments')
    def create_new_shipment(payload):
        request_data = request.get_json()
        try:
            if(request_data.get('address') is None or request_data.get('phone') is None or request_data.get('email') is None or request_data.get('items') is None):
                abort(422)

            shipment = Shipment(address=request_data.get('address'), phone=request_data.get('phone'), email=request_data.get('email'))
            shipment.insert()
            items = request_data.get('items')
            for item in items:
                shipment_item = Shipment_items(shipment_id=shipment.shipment_id, item_id=item['item_id'], quantity=item['quantity'])
                shipment_item.insert()
            #[{'id':'1', 'quantity':'4'}, {'id':'6', 'quantity':'9'}]
            return jsonify({
                'success': True,
                'shipment': shipment.format()
            })
        except:
            abort(422)



    @app.route('/shipments/<int:shipment_id>', methods=['DELETE'])
    @requires_auth('delete:shipments')
    def delete_a_shipment(payload, shipment_id):
        shipment = Shipment.query.filter_by(shipment_id=shipment_id).one_or_none()
        if shipment is None:
            abort(422)
        shipment_items = Shipment_items.query.filter_by(shipment_id=shipment.shipment_id).all()
        for item in shipment_items:
            item.delete()
        shipment.delete()
        return jsonify({
            "success": True,
            "delete": shipment.shipment_id
        })





    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    