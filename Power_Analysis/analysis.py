import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
from datetime import datetime, timedelta
from calendar import monthrange
import copy

import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates
import Power_Analysis.plot as plot

def plot_temporal(collection, usr_id, min_date, max_date):
    power, date = search.search_power_reading_date(collection, usr_id, min_date = min_date, max_date = max_date)
    for idx,p in enumerate(power):
        power[idx] = float(p)
        date[idx] = datetime.strptime(date[idx], "%b-%d-%Y %H:%M:%S")
    plot. line_plot(date, power, usr_id, title = 'Time Variation')

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

    plot.line_plot(date, power, usr_id, title = 'Time Incremental Variation')
