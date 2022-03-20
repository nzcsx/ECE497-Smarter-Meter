import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update

import Power_Analysis.analysis as anal
import Power_Analysis.spatial as space
import Power_Analysis.plot as plot
import Power_Analysis.bill as money
from datetime import datetime
import sys

# referenced from: https://www.kansai-td.co.jp/english/home/guide/article-04.html

def display_report(db, collection, usr_id, min_date, max_date, export = False):
    original_stdout = sys.stdout  # Save a reference to the original standard output

    if export:
        with open('your_report.txt', 'w') as f:
            sys.stdout = f  # Change the standard output to the file we created.

            print("------------ Your Report of Electricity Consumption ------------")
            print("     From", min_date, "To", max_date)

            sys.stdout = original_stdout  # Reset the standard output to its original value

            # get power meter readings within the list
            power_readings, dates = search.search_power_reading_date(collection,
                                                                     usr_id, min_date, max_date, return_string=False)
            # find the number of hours in the period
            max_hrs = space.hrs_in_period(dates[0], dates[-1])

            # find the total power consumed during the period
            power_consumed = int(float(power_readings[-1]) - float(power_readings[0])) * 1000

            # get power meter readings within the list
            power_readings, dates = search.search_power_reading_date(collection,
                                                                     usr_id, min_date, max_date, return_string=True)

            power_diff = [int(power_readings[i]) - int(power_readings[i-1]) for i in range(1, len(power_readings))]
            max_power = max(power_diff)
            max_index = power_diff.index(max_power)

            sys.stdout = f  # Change the standard output to the file we created.
            print()
            print("------------ Power consumption Recorded ------------")
            for idx in range(len(dates)):
                print("Date:",dates[idx], " has a record of",str(power_readings[idx]), "KWh.")
            print("-> In a total of",str(max_hrs), "hours used", str(power_consumed/1000), "kWh.")
            print("-> Maximum power difference of",max_power,"KWh between",dates[max_index])
            print("and", dates[max_index+1])
            sys.stdout = original_stdout  # Reset the standard output to its original value

            names, hrs, consumption = space.spatial_itertool(db=db, collection=collection, usr_id=usr_id,
                                                             min_date=min_date,
                                                             max_date=max_date)

            app_list = search.search_appliance_list(db=db, collection=collection, usr_id=usr_id)



            consumption_dict = []
            for j in range(len(names)):
                consumption_dict.append({"name":names[j], "consumption":consumption[j]})

            consumption_dict.sort(key = lambda x: x.get("consumption"), reverse = True)
            alert_list = [ele for ele in consumption_dict if ele.get("consumption")/1000 > 10]
            print(consumption_dict)

            sys.stdout = f  # Change the standard output to the file we created.
            print()
            print("------------ Spatial Allocation of consumption ------------")
            for idx in range(len(names)):
                print("Household Appliance "+names[idx]+" has been used for approximately",str(round(hrs[idx], 3)),
                      "hours. Estimated to consume ", str(round(consumption[idx]/1000, 3)),"kWh")

            suggest = "-> The order of consumption in appliance is: "
            for ele in consumption_dict:
                suggest += ele.get('name') +" > "
            print(suggest[:-2])

            suggest = "-> Please pay attention to these appliances which potentially overuse power: "
            for ele in alert_list:
                suggest += ele.get("name")+", "
            print(suggest[:-2])

            for app in app_list:
                if app[-1] == "all day" and app[1] > 500:
                    print("-> Appliance "+ app[0]+
                          "has a frequency of all day while itself consumes more than 500 watts, "+
                          "please consider to unplug it regularly if possible")

                if app[0] == 'fridge' or app[0] == 'freezer':
                    print("-> Try not overfill your "+app[0]+", since overfilling impedes the flow of cold air, " \
                                                            "resulting in wasted electricity.")

                if app[0] == 'tv' or app[0] == 'television':
                    print("-> Turn off your TV using the main switch before bedtime or when going out")

                if app[0] == 'ac' or app[0] == 'air conditioner':
                    print("-> AC is also a major source of electricity consumption. "
                          "Try appliance with ENERGY STAR label if you haven't had one. ")
                    print("-> Also, the ideal room temperature is 28 degrees Celcius for air-conditioning and 20 degrees Celcius for heating. ")
                    print("-> Using blinds or curtains can reduce heat from outside and allow air conditioning to function more efficiently.")
                if app[0] == "lamp" or app[0] == 'light bulb' or app[0] == 'bulb' or app[0] == 'light':
                    print("-> Fluorescent bulbs and LED bulbs last longer and use less electricity than incandescent bulbs"
                          "and consider turn off unnecessary lights regularly.")


            sys.stdout = original_stdout  # Reset the standard output to its original value

            # Bill estimation here
            bill = money.estimate_bill_period(collection=collection, usr_id=usr_id, min_date=min_date,
                                              max_date=max_date)


            sys.stdout = f  # Change the standard output to the file we created.
            print()
            print("------------ Your Bill Estimation ------------")

            for key in bill.price_calendar.keys():
                print("Date:", key, "has an estimated total payment of", bill.price_calendar[key])
                if bill.price_calendar_divided[key]['on_peak'] != 0:
                    print("which composes of $", str(bill.price_calendar_divided[key]['on_peak']), "on peak, $",
                          str(bill.price_calendar_divided[key]['off_peak']), "off peak and $",
                          str(bill.price_calendar_divided[key]['mid_peak']), "mid peak")
                else:
                    print("which composes of $", str(bill.price_calendar_divided[key]['off_peak']), "off peak")

            print("                       IN TOTAL")

            print("->", str(round(bill.hours_divided[0], 3)), "kWh on peak,",
                  str(round(bill.hours_divided[1], 3)), "kWh off peak,",
                  str(round(bill.hours_divided[2], 3)), "kWh mid peak,")

            print("-> $", str(round(bill.price_divided[0], 3)), "on peak, $",
                  str(round(bill.price_divided[1], 3)), "off peak, $",
                  str(round(bill.price_divided[2], 3)), "mid peak,")

            print("-> Bill Payment = $", str(round(bill.total_bill, 3)))

            power_info = [{"time": "on peak", "power": bill.hours_divided[0]},
                          {"time": "off peak", "power": bill.hours_divided[1]},
                          {"time": "mid peak", "power": bill.hours_divided[2]}, ]

            power_info.sort(key=lambda x: x.get("power"), reverse=True)

            suggest = "-> Your period of use rank is: "
            for ele in power_info:
                suggest += "'"+ ele.get('time')+"'"+" > "
            print(suggest[:-2])

            if power_info[0].get("time") == "on peak":
                print("-> You have spent the most power on peak, please try to do more housework at off/mid peak hours")
            print()

            print("------------ Some useful hints ------------")
            print("The time-of-use periods are divided by:")
            print("Winter: Nov 1 - Apr 30 and Summer: May 1 - Oct 31")
            print("In summer: Off-peak: 7 pm to 7 am, on-peak: 11 am to 5 pm, mid-peak: the rest of the time")
            print("In winter: Off-peak: 7 pm to 7 am, mid-peak: 11 am to 5 pm, on-peak: the rest of the time")
            print("Regardless of season: weekends or statuatory holidays - all off-peak")



            sys.stdout = original_stdout  # Reset the standard output to its original value

    else:
        #sys.stdout = f  # Change the standard output to the file we created.

        print("------------ Your Report of Electricity Consumption ------------")
        print("     From", min_date, "To", max_date)

        sys.stdout = original_stdout  # Reset the standard output to its original value

        # get power meter readings within the list
        power_readings, dates = search.search_power_reading_date(collection,
                                                                 usr_id, min_date, max_date, return_string=False)
        # find the number of hours in the period
        max_hrs = space.hrs_in_period(dates[0], dates[-1])

        # find the total power consumed during the period
        power_consumed = int(float(power_readings[-1]) - float(power_readings[0])) * 1000

        # get power meter readings within the list
        power_readings, dates = search.search_power_reading_date(collection,
                                                                 usr_id, min_date, max_date, return_string=True)

        power_diff = [int(power_readings[i]) - int(power_readings[i - 1]) for i in range(1, len(power_readings))]
        max_power = max(power_diff)
        max_index = power_diff.index(max_power)

        #sys.stdout = f  # Change the standard output to the file we created.
        print()
        print("------------ Power consumption Recorded ------------")
        for idx in range(len(dates)):
            print("Date:", dates[idx], "Has a record of", str(power_readings[idx]), "kWh.")
        print("-> In a total of", str(max_hrs), "hours used", str(power_consumed), "watts.")
        print("-> Maximum power difference of", max_power, "KWh between", dates[max_index], "and",
              dates[max_index + 1])
        sys.stdout = original_stdout  # Reset the standard output to its original value

        app_list = search.search_appliance_list(db = db, collection=collection, usr_id = usr_id)

        names, hrs, consumption = space.spatial_itertool(db=db, collection=collection, usr_id=usr_id,
                                                         min_date=min_date,
                                                         max_date=max_date)
        #sys.stdout = f  # Change the standard output to the file we created.
        print()
        print("------------ Spatial Allocation of consumption ------------")
        for idx in range(len(names)):
            print("Household Appliance " + names[idx] + " has been used for approximately", str(hrs[idx]),
                  "hours. Estimated to consume", str(consumption[idx]), "KWh")
        sys.stdout = original_stdout  # Reset the standard output to its original value

        # Bill estimation here
        bill = money.estimate_bill_period(collection=collection, usr_id=usr_id, min_date=min_date,
                                          max_date=max_date)

        consumption_dict = []
        for j in range(len(names)):
            consumption_dict.append({"name": names[j], "consumption": consumption[j]})

        consumption_dict.sort(key=lambda x: x.get("consumption"), reverse=True)
        alert_list = [ele for ele in consumption_dict if ele.get("consumption")/1000 > 10]

        print()
        print("------------ Spatial Allocation of consumption ------------")
        for idx in range(len(names)):
            print("Household Appliance " + names[idx] + " has been used for approximately", str(round(hrs[idx], 3)),
                  "hours. Estimated to consume ", str(round(consumption[idx] / 1000, 3)), "kWh")

        suggest = "-> The order of consumption in appliance is: "
        for ele in consumption_dict:
            suggest += ele.get('name') + " > "
        print(suggest[:-2])

        suggest = "-> Please pay attention to these appliances which potentially overuses power:"
        for ele in alert_list:
            suggest += ele.get("name") + ", "

        print(suggest[:-2])

        for app in app_list:
            if app[-1] == "all day" and app[1] > 500:
                print("-> Appliance " + app[0] +
                      "has a frequency of all day while itself consumes more than 500 watts, " +
                      "please consider to unplug it regularly if possible")

            if app[0] == 'fridge' or app[0] == 'freezer':
                print("-> Try not overfill your " + app[0] + ", since overfilling impedes the flow of cold air, " \
                                                             "resulting in wasted electricity.")

            if app[0] == 'tv' or app[0] == 'television':
                print("-> Turn off your TV using the main switch before bedtime or when going out")

            if app[0] == 'ac' or app[0] == 'air conditioner':
                print("-> AC is also a major source of electricity consumption. "
                      "Try appliance with ENERGY STAR label if you haven't had one")

            if app[0] == "lamp" or app[0] == 'light bulb' or app[0] == 'bulb' or app[0] == 'light':
                print("-> Fluorescent bulbs and LED bulbs last longer and use less electricity than incandescent bulbs"
                      "and consider turn off unnecessary lights regularly.")

        print()
        print("------------ Your Bill Estimation ------------")

        for key in bill.price_calendar.keys():
            print("Date:", key, "has an estimated total payment of", bill.price_calendar[key])
            if bill.price_calendar_divided[key]['on_peak'] != 0:
                print("which composes of $", bill.price_calendar_divided[key]['on_peak'], "on peak,",
                      bill.price_calendar_divided[key]['off_peak'], "off peak and",
                      bill.price_calendar_divided[key]['mid_peak'], "mid peak")
            else:
                print("which composes of $", bill.price_calendar_divided[key]['off_peak'], "off peak")

        print("                       IN TOTAL")
        print("->", str(round(bill.hours_divided[0], 3)), "kWh on peak,",
              str(round(bill.hours_divided[1], 3)), "kWh off peak,",
              str(round(bill.hours_divided[2], 3)), "kWh mid peak,")

        print("-> $", str(round(bill.price_divided[0], 3)), "on peak, $",
              str(round(bill.price_divided[1], 3)), "off peak, $",
              str(round(bill.price_divided[2], 3)), "mid peak,")

        print("-> Bill Payment = $", str(round(bill.total_bill, 3)))

        power_info = [{"time": "on peak", "power": bill.hours_divided[0]},
                      {"time": "off peak", "power": bill.hours_divided[1]},
                      {"time": "mid peak", "power": bill.hours_divided[2]}, ]

        power_info.sort(key=lambda x: x.get("power"), reverse=True)

        suggest = "-> Your period of use rank is: "
        for ele in power_info:
            suggest += "'" + ele.get('time') + "'" + " > "
        print(suggest[:-2])

        if power_info[0].get("time") == "on peak":
            print("-> You have spent the most power on peak, please try to do more housework at off/mid peak hours")

        print()

        print("------------ Some useful hints ------------")
        print("The time-of-use periods are divided by:")
        print("Winter: Nov 1 - Apr 30 and Summer: May 1 - Oct 31")
        print("In summer: Off-peak: 7 pm to 7 am, on-peak: 11 am to 5 pm, mid-peak: the rest of the time")
        print("In winter: Off-peak: 7 pm to 7 am, mid-peak: 11 am to 5 pm, on-peak: the rest of the time")
        print("Regardless of season: weekends or statuatory holidays - all off-peak")

        sys.stdout = original_stdout  # Reset the standard output to its original value
