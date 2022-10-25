from pymongo import MongoClient, errors

DOMAIN = 'host-mongo'
PORT = 27017

try:
    client = MongoClient(
        host = [DOMAIN + ':' + str(PORT)],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = 'root',
        password = 'admin'
    )
    # print the version of MongoDB server if connection successful
    print ("server version:", client.server_info()["version"])

    mydb = client['mydatabase']
    mycol = mydb["customers"]
    # mydict = { "name": "John", "address": "Highway 37" }

    # x = mycol.insert_one(mydict)

    # get the database_names from the MongoClient()
    database_names = client.list_database_names()
except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print ("pymongo ERROR:", err)

print ("\ndatabases:", database_names)
