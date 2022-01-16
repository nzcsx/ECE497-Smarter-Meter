import pymongo
from pymongo import MongoClient
import pprint
from datetime import datetime

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
def search_power_reading_date(collection, usr_id, min_date, max_date, return_string = True):
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

        if return_string:
            dates.append(res_d[key])
        else:
            dates.append(datetime.strptime(res_d[key], "%b-%d-%Y %H:%M:%S"))

    return power_readings, dates

def search_power_interval(collection, usr_id, min_power, max_power, return_string = True):
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
        if return_string:
            dates.append(res_d[key])
        else:
            dates.append(datetime.strptime(res_d[key], "%b-%d-%Y %H:%M:%S"))

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