import pymongo
from pymongo import MongoClient
import pprint
from datetime import datetime
import re

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
        "_id": user_info['id'],
        "name": user_info['name'],
        "family_size": user_info['size'],
        "readings": user_info['readings'], # readings should be in a dictionary form with {t_id: reading}
        "datetime": user_info['date'],  # date should be in a dictionary form with {t_id:date}
        #"time": user_info['time'], # time should be in a dictionary form with {t_id:time}
        "appliance": user_info['appliance'],
        "password": user_info['password'],
        "reset_Q": user_info['reset_Q'],
        "reset_A": user_info['reset_A'],
        "last_login_date": datetime.now().strftime("%b-%d-%Y %H:%M:%S")
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

    collection.find_one_and_delete({'_id': usr_id})
    return 1

def remove_connection(client):
    client.close()

def check_pwd(collection, usr_id, pwd):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    res = collection.find_one({'_id': usr_id})
    if pwd == res['password']:
        return True
    else:
        return False

def get_new_id(collection):
    x = collection.find().sort("_id", -1)
    for s in x:
        return int(s['_id']) + 1

def get_id_by_name(collection, name):
    if collection.count_documents({'name': name}) == 0:
        print("Unable to find the specified user")
        return -1

    return collection.find_one({'name': name})['_id']

def get_reset_question(collection, usr_id):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    return collection.find_one({'_id': usr_id})['reset_Q']

def reset_pwd(collection, usr_id, ans, new_pwd):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    if collection.find_one({'_id': usr_id})['reset_A'] == ans:
        collection.find_one_and_update({'_id': usr_id}, {'$set': {'password':new_pwd}})

def check_pwd_validity(passwd):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,15}$"

    # compiling regex
    pat = re.compile(reg)

    # searching regex
    # validating conditions
    if re.search(pat, passwd):
        return True
    else:
        return False
