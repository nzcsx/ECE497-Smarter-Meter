import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient(host="localhost", port=27017)

# Create database
db = client.rptutorials

# Create collection
tutorial = db.tutorial

tutorial1 = {
     "title": "Working With JSON Data in Python",
     "author": "Lucas",
     "contributors": [
         "Aldren",
         "Dan",
         "Joanna"
     ],
     "url": "https://realpython.com/python-json/"
}

result = tutorial.insert_one(tutorial1)
for doc in tutorial.find():
     pprint.pprint(doc)

mycol = db["customers"]

x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")

mylist = [
  { "_id": 1, "name": "John", "address": "Highway 37"},
  { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
  { "_id": 3, "name": "Amy", "address": "Apple st 652"},
  { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
  { "_id": 5, "name": "Michael", "address": "Valley 345"},
  { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
  { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
  { "_id": 8, "name": "Richard", "address": "Sky st 331"},
  { "_id": 9, "name": "Susan", "address": "One way 98"},
  { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
  { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
  { "_id": 12, "name": "William", "address": "Central st 954"},
  { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
  { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
]

x = mycol.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(x.inserted_ids)

print("In customer table")
for doc in mycol.find():
     pprint.pprint(doc)

print()
print()

tr = 14

mycol.find_one_and_update({'_id':tr},{'$set':{'address':'None'}})
for doc in mycol.find():
     pprint.pprint(doc)

x = tutorial.delete_many({})
print(x.deleted_count, " documents deleted.")

x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")
client.close()