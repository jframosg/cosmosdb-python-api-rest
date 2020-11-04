# Dockerized Python API REST for Azure Cosmos DB

## Dockerized Python API REST example to CRUD operations over an Azure Cosmos DB Account, by using Core/SQL API.

## Prerrequisites:

1. Create an [Azure Subscription](https://azure.microsoft.com/en-us/).
2. Create an Azure Cosmos DB account in your Azure subscription. You can create it by following [this quickstart](https://docs.microsoft.com/en-us/azure/cosmos-db/create-cosmosdb-resources-portal).
3. In config.py, to connect with your Cosmos DB account, you have to change the values for those that appear in your Cosmos DB account, in the Keys section.

## Getting started:

To run without Docker:
```
python3 main.py
```

In the web browser, type: http://localhost:8080

To run with Docker:

1. Create image:
```
docker build -f Dockerfile -t cosmosdb-python-api-rest-image .
```

2. Run image:
```
docker run -d -p 8080:8080 cosmosdb-python-api-rest-image
```

In the web browser, type: http://localhost:8080

## Operations:

In the first running, the app will create a database (OrderDB) and a container (PurchaseOrders). We can call the following API services:

### GET:
- http://localhost:8080/orders/ to get all orders in the container.
- http://localhost:8080/orders/1 to get the order with id "1" in the container.

### POST:
- http://localhost:8080/order to add a new item. Here is an example of the body:
```
{
    "item": "test example",
    "cname": "test example",
    "description": "this is the test example",
    "origin": "test example",
    "quantity": 20
}
```

### PUT: 
- http://localhost:8080/order to update an existing item. The body is the same as in the post example by adding the 'id' attribute of the item.

### DELETE: 
- http://localhost:8080/order to delete an existing item. Here is an example of the body to delete the item widh id 1:
```
{
  "id": "1"
}
```

Enjoy!
