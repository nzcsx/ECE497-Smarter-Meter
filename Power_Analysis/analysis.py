import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
from datetime import datetime

import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates

def plot_temporal(collection, usr_id, min_date, max_date):
    power, date = search.search_power_reading_date(collection, usr_id, min_date = min_date, max_date = max_date)
    for idx,p in enumerate(power):
        power[idx] = float(p)
        date[idx] = datetime.strptime(date[idx], "%b-%d-%Y %H:%M:%S")

    fig, ax = plt.subplots()
    fig.suptitle("Temporal plot")
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d-%Y'))
    fig.gca().xaxis.set_major_locator(mdates.DayLocator())

    ax.plot(date, power, label = 'Power')
    ax.grid()

    plt.gcf().autofmt_xdate()
    plt.show()

def plot_temporal_incremental(collection, usr_id, min_date, max_date):
    power, date = search.search_power_reading_date(collection, usr_id, min_date = min_date, max_date = max_date)

    if power == -1:
        print("No data found!")
        return

    last_power = float(power[0])
    for idx,p in enumerate(power):
        temp = float(p)
        power[idx] = temp - last_power
        last_power = temp
        date[idx] = datetime.strptime(date[idx], "%b-%d-%Y %H:%M:%S")

    fig, ax = plt.subplots()
    fig.suptitle("Temporal plot")
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d-%Y'))
    fig.gca().xaxis.set_major_locator(mdates.DayLocator())

    ax.plot(date, power, label = 'Power')
    ax.grid()

    plt.gcf().autofmt_xdate()
    plt.show()