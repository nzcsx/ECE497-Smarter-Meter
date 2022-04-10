import pymongo
from pymongo import MongoClient
import pprint
from datetime import datetime
import re
import OCR.power_record as record
import os
import copy

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

# format: [[appliance, wattage, quantity, usage frequency],...] -> [[string, int/float, int, string],...]
# usage frequency choices: "all day", "often", "rare", "not in use"
def init_appliance(collection, app_info):
    for idx, info in enumerate(app_info):
        new_appl = {
            "_id": idx,
            "appliance": info[0],
            "wattage": str(info[1]),
            "quantity": str(info[2]),
            "usage_freq": info[3]
        }
        collection.insert_one(new_appl)

# add a new user to the reading database
def add_user(db, collection, user_info):
    app_name = "user_" + str(user_info['id'])
    app_collection = add_table(db, app_name)
    init_appliance(collection=app_collection, app_info=user_info["appliance"])

    new_user = {
        "_id": user_info['id'],
        "name": user_info['name'],
        "family_size": user_info['size'],
        "readings": user_info['readings'], # readings should be in a dictionary form with {t_id: reading}
        "datetime": user_info['date'],  # date should be in a dictionary form with {t_id:date}
        #"time": user_info['time'], # time should be in a dictionary form with {t_id:time}
        "appliance": app_name,
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
def remove_user(db, collection, usr_id):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    res = collection.find_one({'_id': usr_id})
    app_collection = db[res["appliance"]]
    app_collection.delete_many({})

    collection.find_one_and_delete({'_id': usr_id})
    return 1

def remove_connection(client):
    client.close()

def check_pwd(collection, usr_id, pwd):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return False

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



def is_reading_legal(date, reading, last_reading, max_inc):
    leng = len(date)
    storage = copy.deepcopy(last_reading)

    if leng == 0:
        return date, reading
    elif leng == 1:
        if reading[0] < last_reading:
            return [], []
        elif reading[0] == last_reading:
            return date, reading
        else: # leng > last_reading
            if reading[0] - last_reading >= 3 * max_inc:
                return [], []
            else:
                return date, reading
    elif leng == 2:
        if reading[0] == reading[1]:
            if reading[0] < last_reading:
                return [], []
            elif reading[0] == last_reading:
                return date, reading
            else:  # leng > last_reading
                if reading[0] - last_reading >= 3 * max_inc:
                    return [], []
                else:
                    return date, reading
        elif reading[0] < reading[1]:
            if reading[0] < last_reading:
                if reading[1] - last_reading < 3 * max_inc:
                    return date[1], reading[1]
                else:
                    return [], []
            elif reading[0] == last_reading:
                if reading[1] - reading[0] < 3 * max_inc:
                    return date, reading
                else:
                    return date[0], reading[0]
            else:  # reading[0] > last_reading
                if reading[0] - last_reading >= 3 * max_inc:
                    return [], []
                else:
                    return date[0], reading[0]
        else: # reading[0] > reading[1]
            if reading[1] < last_reading:
                return [], []
            elif reading[1] == last_reading:
                return date, reading
            else:  # leng > last_reading
                if reading[1] - last_reading >= 3 * max_inc:
                    return [], []
                else:
                    return date, reading

    # sliding window of size 3
    # at least 2 out of 3 should be identical
    next_last_reading = copy.deepcopy(reading[0])
    i = 1
    while i in range(1, len(reading) - 1):
        print(reading)
        next_last_reading = copy.deepcopy(reading[i])
        if reading[i-1] == reading[i] and reading[i] == reading[i+1]:
            last_reading = copy.deepcopy(next_last_reading)
            if i + 1 > len(reading) - 2:
                break
            i = i + 1
            continue
        elif reading[i - 1] == reading[i]:
            if reading[i+1] < reading[i]:
                reading.pop(i + 1)
                date.pop(i + 1)
        elif reading[i] == reading[i + 1]:
            if reading[i-1] > reading[i]:
                reading.pop(i - 1)
                date.pop(i - 1)
        elif i == 1 and reading[i-1] == last_reading:
            if reading[i] == reading[i + 1]:
                last_reading = copy.deepcopy(next_last_reading)
                if i + 1 > len(reading) - 2:
                    break
                i = i + 1
                continue
            else:
                pop_idx = []
                if reading[i + 1] < reading[i - 1]:
                    if i+1 not in pop_idx:
                        pop_idx.append(i + 1)

                if reading[i] < reading[i - 1]:
                    if i not in pop_idx:
                        next_last_reading = copy.deepcopy(reading[i - 1])
                        pop_idx.append(i)
                elif reading[i] > reading[i + 1]:
                    if i not in pop_idx:
                        next_last_reading = copy.deepcopy(reading[i - 1])
                        pop_idx.append(i)
                else:
                    if i+1 not in pop_idx:
                        pop_idx.append(i + 1)

                pop_idx.sort()
                pop_idx.reverse()
                for idx in pop_idx:
                    reading.pop(idx)
                    date.pop(idx)
        else: # all different, leave the smallest difference one
            diff, diff_idx = float("inf"), -1
            for idx in range(i-1, i+2):
                if reading[idx] - last_reading >= 0 and reading[idx] - last_reading < diff:
                    diff_idx = idx
                    diff = reading[idx] - last_reading

            if diff_idx != i + 1:
                reading.pop(i + 1)
                date.pop(i + 1)

            if diff_idx != i:
                next_last_reading = copy.deepcopy(reading[i - 1])
                reading.pop(i)
                date.pop(i)

            if diff_idx != i - 1:
                reading.pop(i - 1)
                date.pop(i - 1)

        last_reading = copy.deepcopy(next_last_reading)
        print("Last reading:", last_reading)

        if i + 1 > len(reading) - 2:
            break
        i = i + 1

    leng = len(date)
    last_reading = storage

    if leng == 0:
        return date, reading
    elif leng == 1:
        if reading[0] < last_reading:
            return [], []
        elif reading[0] == last_reading:
            return date, reading
        else:  # leng > last_reading
            if reading[0] - last_reading >= 3 * max_inc:
                return [], []
            else:
                return date, reading
    elif leng == 2:
        if reading[0] == reading[1]:
            if reading[0] < last_reading:
                return [], []
            elif reading[0] == last_reading:
                return date, reading
            else:  # leng > last_reading
                if reading[0] - last_reading >= 3 * max_inc:
                    return [], []
                else:
                    return date, reading
        elif reading[0] < reading[1]:
            if reading[0] < last_reading:
                if reading[1] - last_reading < 3 * max_inc:
                    return date[1], reading[1]
                else:
                    return [], []
            elif reading[0] == last_reading:
                if reading[1] - reading[0] < 3 * max_inc:
                    return date, reading
                else:
                    return date[0], reading[0]
            else:  # reading[0] > last_reading
                if reading[0] - last_reading >= 3 * max_inc:
                    return [], []
                else:
                    return date[0], reading[0]
        else:  # reading[0] > reading[1]
            if reading[1] < last_reading:
                return [], []
            elif reading[1] == last_reading:
                return date, reading
            else:  # leng > last_reading
                if reading[1] - last_reading >= 3 * max_inc:
                    return [], []
                else:
                    return date, reading

    return date, reading