from datetime import datetime
import pymongo , pprint , os
from helper import decorator
from dotenv import load_dotenv
load_dotenv()

host = os.environ.get("MONGO_HOST")
port = os.environ.get("MONGO_PORT")


mongo_uri = f"mongodb://{host}:{port}"  
client = pymongo.MongoClient(mongo_uri)

print(client.list_database_names())
db = client.coffee

cnames = db.list_collection_names()
print(cnames)

table = db.action

count = table.count_documents({})
print(f"Total documents count for collections {table} is {count}")



def printAll():
    for doc in table.find():
        pprint.pprint(doc)

def seedTestData():
    for i in range(1,5):
        obj = {"coffee" : 1 , "timestamp" : datetime.now(), "brew_id" : 1 ,"qty":i , "barista":"nick"}
        oid = table.insert_one(obj).inserted_id
        print(oid)

@decorator.timer
def search_all(**kwargs):
    for k,v in kwargs.items() :
        # find function will return cursor object
        result = table.find({k:v}) 

    for v in result :
        print(f"Search results :{v}")

    return result

@decorator.timer
def search_date():
    # decorator add to measure and benchmark the time complexity.
    from_date = datetime(2021,3,16,16,40,52,0)
    to_date = datetime(2021,7,16,16,41,0,0)

    # for more comparison operator refer readme's operator table.
    for post in table.find({"timestamp": {"$gte": from_date, "$lt": to_date}}):
        print("Date filter")
        print(post)

def deleteCollectionWithFilter():
    table.delete_many({"time":1})


# Seed 
seedTestData()

# filter by date with operator
search_date()

# filter by argument
filter = {"brew_id":"0"}
search_all(**filter)

# print all in collections
printAll()


