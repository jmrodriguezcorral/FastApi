from pymongo import MongoClient

# ARRANCAR MONGODB EN LOCAL
# "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="c:\mongodb"

db_cliente = MongoClient() #Por defecto a localhost
