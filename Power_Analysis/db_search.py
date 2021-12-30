import pymongo
from pymongo import MongoClient
import pprint

# Print all the entries in the current table
def print_collection(collection):
    for doc in collection.find():
        pprint.pprint(doc)

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
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    power_readings, time, dates = [], [], []

    res = collection.find_one({'_id': usr_id})
    res_d = res["dates"]
    res_t = res["time"]
    res_p = res["readings"]

    for key in res_d:
        if res_d[key] < min_date or res_d[key] > max_date:
            continue

        power_readings.append(res_p[key])
        time.append(res_t[key])
        dates.append(res_d[key])

    return power_readings, time, dates

# Look for the power meter reading in a specific date and time duration
# Needs to be updated to comparison in date and format
def search_power_reading_date_time(collection, usr_id, min_date, max_date, min_time, max_time):
    if collection.count_documents({'_id': usr_id}) == 0:
        print("Unable to find the specified user")
        return -1

    power_readings, time, dates = [], [], []

    res = collection.find_one({'_id': usr_id})
    res_d = res["dates"]
    res_t = res["time"]
    res_p = res["readings"]

    for key in res_d:
        if res_d[key] < min_date or res_d[key] > max_date:
            continue

        if res_d[key] >= min_date and res_t[key] < min_time:
            continue

        if res_d[key] <= max_date and res_t[key] > max_time:
            continue

        power_readings.append(res_p[key])
        time.append(res_t[key])
        dates.append(res_d[key])

    return power_readings, time, dates