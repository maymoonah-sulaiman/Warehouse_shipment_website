import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Item, Shipment


class WarehouseTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "warehouse_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'DGJ#%&','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        
        self.new_correct_item = {
            'name': 'table',
            'availability': True
            } 
        self.new_incorrect_item = {
            'name': 'cup'
            }

        self.new_correct_shipment = {
            "address": "street 5",
            "phone": "2323456789",
            "email": "12@gmail.com",
            "items": [{"item_id": 1, "quantity": 4}, {"item_id": 2, "quantity": 1}]
            }
        self.new_incorrect_shipment = {
            'address': 'street 7'
            }

        self.availability_value = {
            "availability": False
            }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    #works
    def test_get_items(self):
        res = self.client().get('/items')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['items'])
    #works    
    #def test_no_items(self):
        #res = self.client().get('/items')
        #data = json.loads(res.data)
        #self.assertEqual(res.status_code, 404)
        #self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], 'resource not found')
    
   
    
    #def test_get_shipments(self):
        #res = self.client().get('/shipments')
        #data = json.loads(res.data)
        #self.assertEqual(res.status_code, 200)
        #self.assertEqual(data['success'], True)
        
    #def test_no_shipments(self):
        #res = self.client().get('/shipments')
        #data = json.loads(res.data)
        #self.assertEqual(res.status_code, 404)
        #self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], 'resource not found')

    #works
    def test_delete_shipment(self):
        res = self.client().delete('/shipments/3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    #works    
    def test_shipment_not_found_to_delete(self):
        res = self.client().delete('/shipments/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #works
    def test_create_item(self):
        res = self.client().post('/items', json=self.new_correct_item)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    #works
    def test_422_create_item(self):
        res = self.client().post('/items', json=self.new_incorrect_item)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

   
    #works
    def test_create_shipment(self):
        res = self.client().post('/shipments', json=self.new_correct_shipment)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    #works
    def test_422_create_shipment(self):
        res = self.client().post('/shipments', json=self.new_incorrect_shipment)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")    



    def test_edit_item_availablity(self):
        res = self.client().patch('/items/1', json=self.availability_value)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    
    def test_edit_item_does_not_exist(self):
        res = self.client().patch('/items/1000', json=self.availability_value)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
