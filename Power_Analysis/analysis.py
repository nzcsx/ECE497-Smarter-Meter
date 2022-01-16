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

class bill():
    def __init__(self, usr_info):
        self.usr_id = usr_info['id']
        self.min_date = usr_info['min_date']
        self.max_date = usr_info['max_date']
        self.power = usr_info['power']
        self.dates = usr_info['dates']

        self.price_off_peak = 8.2
        self.price_mid_peak = 11.3
        self.price_on_peak = 17.0

        self.off_peak = 0
        self.mid_peak = 0
        self.on_peak = 0

        self.power_calendar = {}
        self.power_calendar_divided = {}
        self.price_calendar = {}
        self.price_calendar_divided = {}

        self.total_bill = 0

    def mins_in_period(self, date_1, date_2):
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        return round(total_seconds / 60)

    def gen_date_list(self, max_d, min_d):
        # date_2 = datetime.strptime((min_d.strftime("%b-%d-%Y") + " 23:59:59"), "%b-%d-%Y %H:%M:%S")
        dates, mins = [], []

        for i in range((max_d - min_d).days + 1):
            dates.append((min_d + timedelta(i)).strftime("%b-%d-%Y"))

            if i != (max_d - min_d).days:
                date_2 = datetime.strptime(((min_d + timedelta(i)).strftime("%b-%d-%Y") + " 23:59:59")
                                           , "%b-%d-%Y %H:%M:%S")
            else:
                date_2 = max_d

            min = self.mins_in_period(date_1 = min_d, date_2 = date_2)
            mins.append(min - sum(mins))

        return dates, mins

    # divide the day into different electricity price hours
    def divide_hours(self, begin, date, first_day = True):
        off1_begin = datetime.strptime((date + " 00:00:00"), "%b-%d-%Y %H:%M:%S")
        off1_end = datetime.strptime((date + " 06:59:59"), "%b-%d-%Y %H:%M:%S")
        off2_begin = datetime.strptime((date + " 19:00:00"), "%b-%d-%Y %H:%M:%S")
        #off2_end = datetime.strptime((date + " 23:59:59"), "%b-%d-%Y %H:%M:%S")
        mid_begin = datetime.strptime((date + " 11:00:00"), "%b-%d-%Y %H:%M:%S")
        mid_end = datetime.strptime((date + " 16:59:59"), "%b-%d-%Y %H:%M:%S")
        on1_begin = datetime.strptime((date + " 7:00:00"), "%b-%d-%Y %H:%M:%S")
        on1_end = datetime.strptime((date + " 10:59:59"), "%b-%d-%Y %H:%M:%S")
        on2_begin = datetime.strptime((date + " 17:00:00"), "%b-%d-%Y %H:%M:%S")
        on2_end = datetime.strptime((date + " 19:59:59"), "%b-%d-%Y %H:%M:%S")
        res = [0, 0, 0] # off_peak, mid_peak, on_peak

        if begin < off1_end:
            res[0] += self.mins_in_period(date_1 = off1_begin, date_2 = begin)
        elif begin < on1_end:
            res[0] += 7 * 60
            res[2] += self.mins_in_period(date_1 = on1_begin, date_2 = begin)
        elif begin < mid_end:
            res[0] += 7 * 60
            res[1] += self.mins_in_period(date_1 = mid_begin, date_2 = begin)
            res[2] += 4 * 60
        elif begin < on2_end:
            res[0] += 7 * 60
            res[1] += 6 * 60
            res[2] += 4 * 60 + self.mins_in_period(date_1 = on2_begin, date_2 = begin)
        else:
            res[0] += 7 * 60 + self.mins_in_period(date_1 = off2_begin, date_2 = begin)
            res[1] += 6 * 60
            res[2] += 6 * 60

        if first_day:
            res[0] = 12 * 60 - res[0]
            res[1] = 6 * 60 - res[1]
            res[2] = 6 * 60 - res[2]
        return res

    def count_mins(self):
        if len(self.dates) == 0 or len(self.dates) == 1:
            return

        for idx in range(1, len(self.dates)):
            prev_date, prev_power = self.dates[idx-1], self.power[idx-1]
            curr_date, curr_power = self.dates[idx], self.power[idx]
            minutes = self.mins_in_period(prev_date, curr_date)
            power = int(curr_power) - int(prev_power)
            p_min = power / minutes
            date_list, mins_list = self.gen_date_list(max_d = curr_date, min_d = prev_date)

            for id, d in enumerate(date_list):

                # update the total power consumption per day
                if d in self.power_calendar:
                    self.power_calendar[d] += p_min * mins_list[id]
                else:
                    self.power_calendar.update({d: p_min * mins_list[id]})

                # update the power usage by category each day
                date_time_d = datetime.strptime(d, "%b-%d-%Y")
                if date_time_d.weekday() > 5:  # weekend
                    self.off_peak += p_min * mins_list[id]

                    if d in self.power_calendar_divided:
                        self.power_calendar_divided[d]["off_peak"] += p_min * mins_list[id]
                    else:
                        self.power_calendar_divided.update(
                            {d: {"off_peak":p_min * mins_list[id], "on_peak": 0, "mid_peak": 0}})

                else: #non-weekend
                    if mins_list[id] == 24 * 60: # whole day
                        if d in self.power_calendar_divided:
                            self.power_calendar_divided[d]["off_peak"] += p_min * 12 * 60
                            self.power_calendar_divided[d]["on_peak"] += p_min * 6 * 60
                            self.power_calendar_divided[d]["mid_peak"] += p_min * 6 * 60
                        else:
                            self.power_calendar_divided.update(
                                {d: {"off_peak": round(0.1 * 12 * 60),
                                     "on_peak": round(0.1 * 6 * 60),
                                     "mid_peak": round(0.1 * 6 * 60)}})
                    else: # non-whole day
                        if id == 0: # first day
                            begin = prev_date
                            prefix = begin.strftime("%b-%d-%Y")
                            division = self.divide_hours(begin = begin, date = prefix, first_day=True)
                        else:
                            begin = curr_date
                            prefix = begin.strftime("%b-%d-%Y")
                            division = self.divide_hours(begin=begin, date=prefix, first_day=False)

                        if d in self.power_calendar_divided:
                            self.power_calendar_divided[d]["off_peak"] += p_min * division[0]
                            self.power_calendar_divided[d]["on_peak"] += p_min * division[2]
                            self.power_calendar_divided[d]["mid_peak"] += p_min * division[1]
                        else:
                            self.power_calendar_divided.update(
                                {d: {"off_peak": p_min * division[0],
                                     "on_peak": p_min * division[2],
                                     "mid_peak": p_min * division[1]}})

    def calculate_bill(self):
        self.count_mins()

        for date in self.power_calendar_divided.keys():
            price_list = {
                "off_peak": round(self.power_calendar_divided[date]["off_peak"] * self.price_off_peak),
                "on_peak": round(self.power_calendar_divided[date]["on_peak"] * self.price_on_peak),
                "mid_peak": round(self.power_calendar_divided[date]["mid_peak"] * self.price_mid_peak)
            }
            total = round(self.power_calendar_divided[date]["off_peak"] * self.price_off_peak) \
                    + round(self.power_calendar_divided[date]["on_peak"] * self.price_on_peak) \
                    + round(self.power_calendar_divided[date]["mid_peak"] * self.price_mid_peak)

            self.price_calendar.update({date: total})
            self.power_calendar_divided.update({date:price_list})
            self.total_bill += total

    def update_price(self, on  = None, off = None, mid = None):
        if on != None:
            self.price_on_peak = on

        if off != None:
            self.price_off_peak =  off

        if mid != None:
            self.price_mid_peak = mid

def estimate_bill_month(collection, usr_id, month = None):
    if month == None:
        month = datetime.now().strftime("%b")

    num_days = monthrange(int(datetime.now().strftime("%Y"))
                          , int(datetime.now().strftime("%m")))[1]

    min_date = month + '-01' + datetime.now().strftime("-%Y") + " 00:00:00"
    max_date = month + '-' + str(num_days) + datetime.now().strftime("-%Y") + " 23:59:59"

    return estimate_bill_period(collection, usr_id, min_date, max_date)

def estimate_bill_period(collection, usr_id, min_date, max_date):
    power_readings, dates = search.search_power_reading_date(collection,
                                                             usr_id, min_date, max_date, return_string = False)

    user_info = {
        "id": usr_id,
        "min_date": min_date,
        "max_date": max_date,
        "power": power_readings,
        "dates": dates
    }
    new_bill = bill(user_info)
    new_bill.calculate_bill()
    return new_bill