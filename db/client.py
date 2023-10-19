from pymongo import MongoClient

#Conexion Local
#db_client = MongoClient().local

#Conexion remota
db_client = MongoClient(
    "mongodb+srv://DBTest:Admin@cluster0.zwpr923.mongodb.net/?retryWrites=true&w=majority").test