import pymongo
from pymongo import MongoClient
import pprint

# connect with the client host
# setup a database with db_name and start a new table with tab_name
def connect_host(db_name, tab_name):
    client = MongoClient(host="localhost", port=27017)

    # Create database
    db = client[db_name]

    # Create collection
    collection = db[tab_name]

    return client, db, collection

# setup a new database with db_name
def add_db(client, db_name):
    # Create database
    db = client[db_name]
    return db

# start a new table with tab_name
def add_table(db, tab_name):
    # Create collection
    collection = db[tab_name]
    return collection

# add a new user to the reading database
def add_user(collection, user_info):
    new_user = {
        # need to add more information here
        "_id": user_info['id'],
        "name": user_info['name'],
        "family_size": user_info['size'],
        "readings": user_info['readings'], # readings should be in a dictionary form with {t_id: reading}
        "dates": user_info['date'],  # date should be in a dictionary form with {t_id:date}
        "time": user_info['time'], # time should be in a dictionary form with {t_id:time}
        "appliance": user_info['appliance']
    }
    collection.insert_one(new_user)
    return collection

# remove all the entries in a table
def remove_collection(collection):
    x = collection.delete_many({})
    print(x.deleted_count, " documents deleted.")

# remove a specific user from the table
def remove_user(collection, usr_id):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    collection.find_one_and_update({'_id': usr_id})
    return 1