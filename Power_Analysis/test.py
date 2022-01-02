import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal
from datetime import datetime

now = datetime.now()
client, db, tab = login.connect_host("Power", "user_info")
login.remove_collection(tab)

# dd-mm-YY H:M:S
now = datetime.now()
dt_string = now.strftime("%b-%d-%Y %H:%M:%S")
print("date and time =", dt_string)

user_info = {
# need to add more information here
        "id": 1,
        "name": "Default",
        "size": "3",
        "readings": {"1": "123"}, # readings should be in a dictionary form with {t_id: reading}
        "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
        "appliance": {"fridge":3}
}
login.add_user(tab, user_info)
search.print_collection(tab)

# test 1
update.update_appliance_info(tab,1,{"laptop":1})
search.print_collection(tab)

# test 2
# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["125"],dates = ["Dec-31-2021 17:45:24"])
search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["128"],dates = ["Dec-31-2021 19:13:24"])
search.print_collection(tab)

# dd-mm-YY H:M:S
now = datetime.now()
dt_string = now.strftime("%b-%d-%Y %H:%M:%S")
print("date and time =", dt_string)
update.add_power_reading(tab,1,readings = ["145"],dates = [dt_string])
search.print_collection(tab)

# test 3
p,d = search.search_power_reading_date(tab, 1, min_date = 'Dec-29-2021 18:50:12', max_date = "Dec-31-2021 18:14:00")
print(p,d)
#anal.plot_temporal_incremental(tab, 1, min_date = 'Dec-29-2021 12:50:12', max_date = "Jan-31-2022 20:14:00")

# test 4
p,d = search.search_power_interval(tab, 1, 120, 130)
print(p,d)

# test 5
user_info = {
# need to add more information here
        "id": 2,
        "name": "Someone",
        "size": "3",
        "readings": {"1": "123"}, # readings should be in a dictionary form with {t_id: reading}
        "date": {"1": "Dec-29-2021 19:20:21"},  # date should be in a dictionary form with {t_id:date}
        "appliance": {"fridge":3}
}
login.add_user(tab, user_info)
search.print_collection(tab)

print("after deletion")
login.remove_user(tab,2)
search.print_collection(tab)

search.print_user_info(tab,1)

login.remove_collection(tab)
login.remove_connection(client)

# dates = []
# dates.append('Apr-1-2005')
# dates.append('Aug-28-2007')
# from datetime import datetime
# for d in dates:
#      date = datetime.strptime(d, '"%b-%m-%Y %H:%M:%S"')
#      print (type(date))
#      print (date)
#
# print(datetime.strptime(dates[0], '%b-%d-%Y')<datetime.strptime(dates[1], '%b-%d-%Y'))
# now = datetime.now()
# dt_string = now.strftime("%b-%d-%Y %H:%M:%S")
# date = datetime.strptime(dt_string, "%b-%d-%Y %H:%M:%S")
# print(date)