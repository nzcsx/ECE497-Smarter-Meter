# Updated Jan-11 23:05

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

# Print all the entries in the current table
def print_collection(collection):
    for doc in collection.find():
        pprint.pprint(doc)

# Print the information of a specific user
def print_user_info(collection, usr_id):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    res = collection.find_one({'_id': usr_id})
    print("User name:", res['name'])
    print("Family size:", res['family_size'])
    res_p = res["readings"]
    for key in res_p:
        print("Reading at time:",datetime.strptime(res["datetime"][key], "%b-%d-%Y %H:%M:%S"),
              " with reading: ",res_p[key], "W")
    print("Appliance information:",res["appliance"])

# Look for all power meter readings in the database
def search_power_reading_all(collection, usr_id):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    power_readings = []
    res = collection.find_one({'_id': usr_id})
    res_p = res["readings"]

    for key in res_p:
        power_readings.append(res_p[key])

    return power_readings


# Look for the power meter reading in a specific date duration
# Needs to be updated to comparison in date format
def search_power_reading_date(collection, usr_id, min_date, max_date):
    min_d = datetime.strptime(min_date, "%b-%d-%Y %H:%M:%S")
    max_d = datetime.strptime(max_date, "%b-%d-%Y %H:%M:%S")

    if min_d > max_d:
        print("Begin date larger than end date.")
        return -1, -1

    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1,-1

    power_readings, time, dates = [], [], []

    res = collection.find_one({'_id': usr_id})
    res_d = res["datetime"]
    res_p = res["readings"]

    for key in res_d:
        curr_d = datetime.strptime(res_d[key], "%b-%d-%Y %H:%M:%S")
        if curr_d < min_d or curr_d > max_d:
            continue

        power_readings.append(res_p[key])
        dates.append(res_d[key])

    return power_readings, dates

def search_power_interval(collection, usr_id, min_power, max_power):
    min_p = float(min_power)
    max_p = float(max_power)

    if min_p > max_p:
        print("Begin date larger than end date.")
        return -1, -1

    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1,-1

    power_readings, time, dates = [], [], []

    res = collection.find_one({'_id': usr_id})
    res_d = res["datetime"]
    res_p = res["readings"]

    for key in res_d:
        curr_p = float(res_p[key])
        if curr_p < min_p or curr_p > max_p:
            continue

        power_readings.append(res_p[key])
        dates.append(res_d[key])

    return power_readings, dates

def search_last_update(collection, usr_id, return_string = True):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    res = collection.find_one({'_id': usr_id})
    max_key = max(res["datetime"], key=res["datetime"].get)

    if return_string:
        return res["datetime"][max_key]
    else:
        return datetime.strptime(res["datetime"][max_key], "%b-%d-%Y %H:%M:%S")


# add new power reading to database
# readings, dates and time are in array format
# check power consistency?
def add_power_reading(collection, usr_id, readings, dates):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    if len(readings) != len(dates):
        print("Unmatched input sizes")
        return -1

    res = collection.find_one({'_id': usr_id})
    curr_reading = res["readings"]
    curr_dates = res["datetime"]

    max_key = int( max(curr_reading, key=curr_reading.get)) + 1

    for itr in range(len(readings)):
        temp_r = {str(max_key): readings[itr]}
        temp_d = {str(max_key): dates[itr]}

        curr_reading.update(temp_r)
        curr_dates.update(temp_d)
        max_key += 1

    collection.find_one_and_update({'_id':usr_id},{'$set':{'readings':curr_reading}})
    collection.find_one_and_update({'_id': usr_id}, {'$set': {'datetime': curr_dates}})
    return 1

# update family information
def update_family_info(collection, usr_id, family):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    collection.find_one_and_update({'_id': usr_id}, {'$set': {'family_size': family}})
    return 1

# update appliance information
def update_appliance_info(collection, usr_id, appliance):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1
    res = collection.find_one({'_id': usr_id})

    curr = res["appliance"]
    curr.update(appliance)
    collection.find_one_and_update({'_id': usr_id}, {'$set': {'appliance':curr}})
    return 1

# update password
def update_password(collection, usr_id, pwd):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    collection.find_one_and_update({'_id': usr_id}, {'$set': {'password':pwd}})
    return 1

# update the last login time
def update_last_login(collection, usr_id):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    collection.find_one_and_update({'_id': usr_id},
                                   {'$set': {"last_login_date": datetime.now().strftime("%b-%d-%Y %H:%M:%S")}})
    return 1