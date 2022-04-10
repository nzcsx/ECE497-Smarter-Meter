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

class bill():
    def __init__(self, usr_info):
        self.usr_id = usr_info['id']
        self.min_date = usr_info['min_date']
        self.max_date = usr_info['max_date']
        self.power = usr_info['power']
        self.dates = usr_info['dates']

        self.price_off_peak = 8.2 / 100
        self.price_mid_peak = 11.3 / 100
        self.price_on_peak = 17.0 / 100

        self.off_peak = 0
        self.mid_peak = 0
        self.on_peak = 0

        self.power_calendar = {} # unit is Wh
        self.power_calendar_divided = {} # unit is Wh
        self.price_calendar = {}
        self.price_calendar_divided = {}

        self.hours_divided = [0, 0, 0] # Unit in kWh
        self.price_divided = [0, 0, 0]

        self.total_bill = 0

    # calculate the total number of minutes in a period
    def mins_in_period(self, date_1, date_2):
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        return round(total_seconds / 60)

    # get a list of dates during the period
    def gen_date_list(self, max_d, min_d):
        # date_2 = datetime.strptime((min_d.strftime("%b-%d-%Y") + " 23:59:59"), "%b-%d-%Y %H:%M:%S")
        dates, mins = [], []

        for i in range((max_d - min_d).days + 2):
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

        # determine if it is within the winter period
        date_curr = datetime.strptime((date.split("-")[0] + "-" + date.split("-")[1]), "%b-%d")
        winter_begin, winter_end = datetime.strptime(("Nov-01"), "%b-%d"), datetime.strptime(("Apr-30"), "%b-%d")
        if date_curr > winter_begin or date_curr < winter_end:
            temp = copy.deepcopy(res[-1])
            res[1] = res[-1]
            res[-1] = temp
        return res

    def count_mins(self):
        # if there is no duration in the period
        if len(self.dates) == 0 or len(self.dates) == 1:
            return

        for idx in range(1, len(self.dates)):
            # find out the max and min dates
            prev_date, prev_power = self.dates[idx-1], self.power[idx-1]
            curr_date, curr_power = self.dates[idx], self.power[idx]
            minutes = self.mins_in_period(prev_date, curr_date)
            power = int(curr_power) - int(prev_power)

            # assume a uniform power consumption over the period
            p_min = power / minutes

            # get a list of dates and the corresponding minutes in the date where the period covers
            date_list, mins_list = self.gen_date_list(max_d = curr_date, min_d = prev_date)
            print("mins_list:", mins_list, "p_min:", p_min)
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
                            self.power_calendar_divided[d]["off_peak"] = p_min * 12 * 60
                            self.power_calendar_divided[d]["on_peak"] = p_min * 6 * 60
                            self.power_calendar_divided[d]["mid_peak"] = p_min * 6 * 60
                        else:
                            self.power_calendar_divided.update(
                                {d: {"off_peak": round(p_min * 12 * 60, 3),
                                     "on_peak": round(p_min * 6 * 60, 3),
                                     "mid_peak": round(p_min * 6 * 60, 3)}})
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

    def collect_divided_hours(self):
        for key in self.power_calendar_divided.keys():
            self.hours_divided[0] += self.power_calendar_divided[key]['off_peak']/1000
            self.hours_divided[1] += self.power_calendar_divided[key]['on_peak']/1000
            self.hours_divided[2] += self.power_calendar_divided[key]['mid_peak']/1000

    def collect_divided_price(self):
        print(self.price_calendar_divided)
        for key in self.price_calendar_divided.keys():
            self.price_divided[0] += self.price_calendar_divided[key]['off_peak']
            self.price_divided[1] += self.price_calendar_divided[key]['on_peak']
            self.price_divided[2] += self.price_calendar_divided[key]['mid_peak']

    # calculate the money spent according to the power consumption
    def calculate_bill(self):
        self.count_mins()

        for date in self.power_calendar_divided.keys():
            # price = time * hourly price
            price_list = {
                "off_peak": round(self.power_calendar_divided[date]["off_peak"] * self.price_off_peak, 3),
                "on_peak": round(self.power_calendar_divided[date]["on_peak"] * self.price_on_peak, 3),
                "mid_peak": round(self.power_calendar_divided[date]["mid_peak"] * self.price_mid_peak, 3)
            }
            total = round(self.power_calendar_divided[date]["off_peak"] * self.price_off_peak, 3) \
                    + round(self.power_calendar_divided[date]["on_peak"] * self.price_on_peak, 3) \
                    + round(self.power_calendar_divided[date]["mid_peak"] * self.price_mid_peak, 3)

            self.price_calendar.update({date: round(total, 3)})
            self.price_calendar_divided.update({date:price_list})
            self.total_bill += total

        self.collect_divided_hours()
        self.collect_divided_price()

    # update the price if needed
    def update_price(self, on  = None, off = None, mid = None):
        if on is not None:
            self.price_on_peak = on

        if off is not None:
            self.price_off_peak =  off

        if mid is not None:
            self.price_mid_peak = mid

# estimate the bill payment over a month
# start from the morning first day of the month to midnight of the last day
def estimate_bill_month(collection, usr_id, month = None):
    if month == None:
        month = datetime.now().strftime("%b")

    num_days = monthrange(int(datetime.now().strftime("%Y"))
                          , int(datetime.now().strftime("%m")))[1]

    min_date = month + '-01' + datetime.now().strftime("-%Y") + " 00:00:00"
    max_date = month + '-' + str(num_days) + datetime.now().strftime("-%Y") + " 23:59:59"

    return estimate_bill_period(collection, usr_id, min_date, max_date)

# calculate the bill payment over a specified period
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