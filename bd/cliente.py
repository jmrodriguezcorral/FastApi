from pymongo import MongoClient
import config

# ARRANCAR MONGODB EN LOCAL
# "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath="c:\mongodb"

# En local
#db_cliente = MongoClient().local #Por defecto a localhost
#Usando el servicio remoto de atlas de mongodb
db_cliente = MongoClient("mongodb+srv://"+
                         config.USUARIO+":"+config.PASSWORD+
                         "@cluster0.tp3q4om.mongodb.net/?retryWrites=true&w=majority").test_fastapi


