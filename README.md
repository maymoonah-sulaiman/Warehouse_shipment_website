# Capstone project Full-stack Nanodegree Udacity

# Warehouse shipment system

## Motivation:

This project is one of the requirment to graduate from FSND program and it is considered the capstone project.
This Warehouse shipment system serves the managers and employees of the warehouse to view all shipments and maintain them as well as to add new items that are available at the warehouse.


## Project Dependencies:

### Python 3.8
Get and install the latest version of Python for your OS platform at https://www.python.org/downloads/

### requirments.txt
run the following command to install all needed packages.
```bash
pip install -r requirements.txt
```

### Local server run
To run the app on your local server, go to the project folder and run the following command:
```bash
FLASK_APP=app.py flask run --reload
```


## API Documentation:
### Warehouse Shipment system is live at:
https://warehouse-shipment-capstone.herokuapp.com/

### Authentication
for more conviniance a postman collection is included and it is ready to be used with the JWTs included.
but, the JWTs are also listed below.
There are two types of user roles:

manager: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJxWUJhckpwQW5jQUUyWFA1cHFxQyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wLWFwaS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMGZmYjNhZWRiMzcwMDEzN2M1NWYyIiwiYXVkIjoid2FyZWhvdXNlX3NoaXBtZW50X3dlYnNpdGUiLCJpYXQiOjE1OTM5MDM3ODksImV4cCI6MTU5MzkxMDk4OSwiYXpwIjoiOTNhNnRuYnRKMVhaaTRUdGJZNWR0WUZaalh5UUxiTlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzaGlwbWVudHMiLCJnZXQ6aXRlbXMiLCJnZXQ6c2hpcG1lbnRzIiwicGF0Y2g6aXRlbXMiLCJwb3N0Oml0ZW1zIiwicG9zdDpzaGlwbWVudHMiXX0.X2NyUM7L-LVnyz--WI-R_Mx76JqutBCdPfHFFfAoTFD1aA8s4c0ORwzFd348Xr_1r16b4Ig0keaOSuJIFKgthooLwx-nY58J5pY4otTqd39cRAx3TIcZ_UcQtHljeNaMMOxzfq6fCQ7mbVuU2XTpyIFDWSlcIxFe0DPugq8effxuQjhKAOkQrzvgDENgZuoLUJBEu84C7TfsO8oD91GjlndhZf-yYo-g_xDSIXhZ9KbzHPodl2epmTNgcT8GZnIAgytp5Kxc7m1Yq2oEMuhXJwGNL-F6DG-nNSHGs3PNEAxRB9_03B65gwcIfpMWMQY3RmS7eWrrhPB6sPQJwSv6oA


employee: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJxWUJhckpwQW5jQUUyWFA1cHFxQyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wLWFwaS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMTAxNzk5Mjg4MmMwMDEzNWNhMDIwIiwiYXVkIjoid2FyZWhvdXNlX3NoaXBtZW50X3dlYnNpdGUiLCJpYXQiOjE1OTM5MDQxOTUsImV4cCI6MTU5MzkxMTM5NSwiYXpwIjoiOTNhNnRuYnRKMVhaaTRUdGJZNWR0WUZaalh5UUxiTlciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDppdGVtcyIsImdldDpzaGlwbWVudHMiXX0.NML5uhieN8q3TM74D0Q80L9zhzrmC-PNRH9QfsWYpwrICj7szxuDnJsM1Xw7hijZlj0UmB0l12INJRccBWB3igtL-ANO86QO3YkDVnAHcBRKdgXyWR3sLc7fkULlZdggBMZmhtDjjbgTA5KFV7zrFRYjm2OldhS9rNWjwf8iFAuab4qOEVBE_nzuYALlcrjHFOoB3CZuv3xgy0EJtyuv_4YxaRrAzpafmDEVqkArf4QnkcuOWnE-wjFpA1Z0Rl20udyAGNKE0dwcTw-sfx3-bMbqDiaJEX_Uf8eZRCWJ-Fo4oMtUOv4Lb_WUe8ddDxnvlPY9f4v3GLHZTFFpxwgvrg

those users have different permission:
manager: 
  - get:items
  - post:items
  - patch:items
  - get:shipments
  - post:shipments
  - delete:shipments

employee:
  - get:items
  - get:shipments

### Endpoints:

#### GET '/items'
- Fetches a dictionary of all available items in the database. 
- Request Arguments: None
- Returns: An object with a single key, items, that contains list of items.
```
{
    "items": [
        {
            "availability": true,
            "item_id": 1,
            "name": "table"
        }
    ],
    "success": true
}

```

#### POST '/items'
- Adds a new item to the database. 
- Request Arguments: 
```
{
    "name": "jar",
    "availability": true
}
```
- Returns: An object with a single key, item, that contains the added item's id.
```
{
    "item": 3,
    "success": true
}
```

#### PATCH '/items/1'
- Updates item's availability in the warehouse 
- Request Arguments: 
```
{
   "availability": false
}
```
- Returns: An object with a single key, item, that contains the updated item's id.
```
{
    "item": 1,
    "success": true
}
```

#### GET '/shipments'
- Fetches a dictionary of all available shipments in the database. 
- Request Arguments: None
- Returns: An object with a single key, shipments, that contains list of shipments.
```
{
    "shipments": [
        {
            "address": "street 5",
            "email": "12@gmail.com",
            "phone": "2323456789",
            "shipment_id": 1
        },
        {
            "address": "street 7",
            "email": "12@gmail.com",
            "phone": "2323456789",
            "shipment_id": 2
        }
    ],
    "success": true
}

```

#### POST '/shipments' 
- Adds a new shipment to the database. 
- Request Arguments: 
```
{
    "address": "street 7",
    "phone": "2323456789",
    "email": "12@gmail.com",
    "items": [{"item_id": 1, "quantity": 4}, {"item_id": 2, "quantity": 1}]
}
```
- Returns: An object with a single key, shipment, that contains the added shipment's id.
```
{
    "shipment": {
        "address": "street 7",
        "email": "12@gmail.com",
        "phone": "2323456789",
        "shipment_id": 2
    },
    "success": true
}
```

#### DELETE '/shipment/3'
- Deletes a shipment from the database. 
- Request Arguments: None
- Returns: An object with a single key, delete, that contains the deleted shipment's id.
```
{
    "delete": 2,
    "success": true
}
```


### Error Handling
Errors are returned as JSON objects:

The API will return three error types when requests fail:

400: Bad Request
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
404: Resource Not Found
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
422: Not Processable
```
{
    "success": False, 
    "error": 422,
    "message": "not processable"
}
```