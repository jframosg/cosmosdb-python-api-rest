import os
from flask import Flask, request, jsonify, make_response, abort
from jsonschema import validate, ValidationError
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import config
import schemas

app = Flask(__name__)

# Create cosmos client
client = CosmosClient(config.endpoint, config.key)

# Create database if not exists
database_name = 'OrderDB'
database = client.create_database_if_not_exists(id=database_name)

# Create container if not exists
container_name = 'PurchaseOrders'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

@app.route('/')
def hello_world():
    return 'Hello and welcome to the Python API REST for AKS and Cosmos DB'

@app.route('/orders/', methods = ['GET'])
def orders():
    item_list = list(container.read_all_items(max_item_count=10))
    return make_response(jsonify({"orders": item_list}))

@app.route('/orders/<id>/', methods = ['GET'])
def order(id):
    try:
        response = container.read_item(item=id, partition_key=id)
    except exceptions.CosmosResourceNotFoundError:
        return {"message": "Order does not exist", "status_code": 500}, 500
    return make_response(jsonify({"order": response}))

@app.route('/order', methods = ['POST'])
def add_orders():
    if request.is_json == False:        
        return {"message": "Non-JSON body", "status_code": 400}, 400

    json_message = request.get_json()
    
    # validate the json content
    try:
        validate(json_message, schema=schemas.SCHEMA_ADD_ORDER)
    except ValidationError as err:
        return {"message": "JSON not valid:" + err.message, "status_code": 500}, 500

    # get values from body
    item_json = str(json_message['item'])
    cname = str(json_message['cname'])
    description = str(json_message['description'])
    origin = str(json_message['origin'])
    quantity = json_message['quantity']

    # check if item exists
    query = "SELECT * FROM c WHERE c.item = @item_json"
    current_orders = list(container.query_items(
        query=query,
        parameters=[
            { "name":"@item_json", "value": item_json }
        ],
        enable_cross_partition_query=True
    ))
    if current_orders:
        return {"message": "Existing order", "status_code": 500}, 500

    # get max id to insert in DB
    query = "Select TOP 1 c.id from c ORDER BY c.id DESC"
    max_id_order = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    if max_id_order:
        max_id = int(max_id_order[0]['id'])
    else:
        max_id = 0
    new_id = str(max_id + 1)

    # add item to DB
    order_to_add = {'id' : new_id, 
        'item' : item_json, 
        'cname' : cname, 
        'description' : description, 
        'origin' : origin, 
        'quantity' : quantity }
    return container.create_item(body=order_to_add)

@app.route('/order', methods=['PUT'])
def update_order():
    if request.is_json == False:        
        return {"message": "Non-JSON body", "status_code": 400}, 400

    json_message = request.get_json()
    
    # validate the json content
    try:
        validate(json_message, schema=schemas.SCHEMA_UPDATE_ORDER)
    except ValidationError as err:
        return {"message": "JSON not valid:" + err.message, "status_code": 500}, 500

    # get values from body
    id = str(json_message['id'])
    item_json = str(json_message['item'])

    # check if item exists
    try:
        current_order = container.read_item(item=id, partition_key=id)
    except exceptions.CosmosResourceNotFoundError:
        return {"message": "Order does not exist", "status_code": 500}, 500 

    # update item in DB
    current_order.update({'item' : item_json})

    if 'cname' in json_message:
        current_order.update({'cname' : str(json_message['cname'])})

    if 'description' in json_message:
        current_order.update({'description' : str(json_message['description'])})

    if 'origin' in json_message:
        current_order.update({'origin' : str(json_message['origin'])})

    if 'quantity' in json_message:
        current_order.update({'quantity' : json_message['quantity']})

    return container.upsert_item(body=current_order)


@app.route('/order', methods=['DELETE'])
def delete_order():
    if request.is_json == False:        
        return {"message": "Non-JSON body", "status_code": 400}, 400

    json_message = request.get_json()
    
    # validate the json content
    try:
        validate(json_message, schema=schemas.SCHEMA_DELETE_ORDER)
    except ValidationError as err:
        return {"message": "JSON not valid:" + err.message, "status_code": 500}, 500

    # get values from body
    id = str(json_message['id'])

    # check if item exists
    try:
        _ = container.read_item(item=id, partition_key=id)
    except exceptions.CosmosResourceNotFoundError:
        return {"message": "Order does not exist", "status_code": 500}, 500

    # delete item from DB
    _ = container.delete_item(item=id, partition_key=id)
    return {"result" : id}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
