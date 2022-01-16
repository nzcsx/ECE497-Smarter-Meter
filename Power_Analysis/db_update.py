import pymongo
from pymongo import MongoClient
import pprint
from datetime import datetime

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
    for app in appliance.keys():
        if app in curr:
            curr[app] += appliance[app]
        else:
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