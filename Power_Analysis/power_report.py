import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update

import Power_Analysis.analysis as anal
import Power_Analysis.spatial as space
import Power_Analysis.plot as plot
import Power_Analysis.bill as money
from datetime import datetime
import sys

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
                print("Date:",dates[idx], "has a record of",str(power_readings[idx]), "KWh.")
            print("-> In a total of",str(max_hrs), "hours used", str(power_consumed/1000), "kWh.")
            print("-> Maximum power difference of",max_power,"KWh between",dates[max_index])
            print("and", dates[max_index+1])
            sys.stdout = original_stdout  # Reset the standard output to its original value

            names, hrs, consumption = space.spatial_itertool(db=db, collection=collection, usr_id=1,
                                                             min_date=min_date,
                                                             max_date=max_date)
            sys.stdout = f  # Change the standard output to the file we created.
            print()
            print("------------ Spatial Allocation of consumption ------------")
            for idx in range(len(names)):
                print("Household Appliance "+names[idx]+" has been used for approximately",str(round(hrs[idx], 3)),
                      "hours. Estimated to consume ", str(round(consumption[idx]/1000, 3)),"kWh")
            sys.stdout = original_stdout  # Reset the standard output to its original value

            # Bill estimation here
            bill = money.estimate_bill_period(collection=collection, usr_id=1, min_date=min_date,
                                              max_date=max_date)

            sys.stdout = f  # Change the standard output to the file we created.
            print()
            print("------------ Your Bill Estimation ------------")

            for key in bill.price_calendar.keys():
                print("Date:", key, "has an estimated total payment of", bill.price_calendar[key])
                if bill.price_calendar_divided[key]['on_peak'] != 0:
                    print("which composes of $", str(bill.price_calendar_divided[key]['on_peak']), "on peak, $",
                          str(bill.price_calendar_divided[key]['off_peak']), "off peak and $",
                          str(bill.price_calendar_divided[key]['mid_peak']), "mid peal")
                else:
                    print("which composes of $", str(bill.price_calendar_divided[key]['off_peak']), "off peak")

            print("                       IN TOTAL")
            print("-> On peak", str(round(bill.hours_divided[0], 3)), "kWh on peak,",
                  str(round(bill.hours_divided[1], 3)), "kWh off peak,",
                  str(round(bill.hours_divided[2], 3)), "kWh mid peak,")

            print("-> Bill Payment = $", str(round(bill.total_bill, 3)))

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

        names, hrs, consumption = space.spatial_itertool(db=db, collection=collection, usr_id=1,
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
        bill = money.estimate_bill_period(collection=collection, usr_id=1, min_date=min_date,
                                          max_date=max_date)

        print()
        print("------------ Your Bill Estimation ------------")

        for key in bill.price_calendar.keys():
            print("Date:", key, "has an estimated total payment of", bill.price_calendar[key])
            if bill.price_calendar_divided[key]['on_peak'] != 0:
                print("which composes of $", bill.price_calendar_divided[key]['on_peak'], "on peak,",
                      bill.price_calendar_divided[key]['off_peak'], "off peak and",
                      bill.price_calendar_divided[key]['mid_peak'], "mid peal")
            else:
                print("which composes of $", bill.price_calendar_divided[key]['off_peak'], "off peak")

        print("                       IN TOTAL")
        print("-> On peak", str(round(bill.hours_divided[0], 3)), "kWh on peak,",
              str(round(bill.hours_divided[1], 3)), "kWh off peak,",
              str(round(bill.hours_divided[2], 3)), "kWh mid peak,")

        print("-> Bill Payment = $", str(round(bill.total_bill, 3)))

        sys.stdout = original_stdout  # Reset the standard output to its original value
