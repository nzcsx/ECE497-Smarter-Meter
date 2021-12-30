import pymongo
from pymongo import MongoClient
import pprint

# add new power reading to database
# readings, dates and time are in array format
def add_power_reading(collection, usr_id, readings, dates, time):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    if len(readings) != len(dates) or len(readings) != len(time) or len(dates) != len(time):
        print("Unmatched input sizes")
        return -1

    res = collection.find_one({'_id': usr_id})
    curr_reading = res["readings"]
    curr_time = res["time"]
    curr_dates = res["dates"]

    max_key = int( max(curr_reading, key=curr_reading.get)) + 1

    for itr in range(len(readings)):
        temp_r = {str(max_key): readings[itr]}
        temp_t = {str(max_key): time[itr]}
        temp_d = {str(max_key): dates[itr]}

        curr_reading.update(temp_r)
        curr_time.update(temp_t)
        curr_dates.update(temp_d)
        max_key += 1

    collection.find_one_and_update({'_id':usr_id},{'$set':{'readings':curr_reading}})
    collection.find_one_and_update({'_id': usr_id}, {'$set': {'time': curr_time}})
    collection.find_one_and_update({'_id': usr_id}, {'$set': {'dates': curr_dates}})
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