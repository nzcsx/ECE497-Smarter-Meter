import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
from datetime import datetime, timedelta
import Power_Analysis.plot as plot
from calendar import monthrange

import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates

import Power_Analysis.bill as money

now = datetime.now()
client, db, tab = login.connect_host("Power", "user_info")
login.remove_collection(db["user_1"])
login.remove_collection(db["user_2"])
login.remove_collection(tab)

# dd-mm-YY H:M:S
now = datetime.now()
dt_string = now.strftime("%b-%d-%Y %H:%M:%S")
print("date and time =", dt_string)

user_info = {
# need to add more information here
        "id": 1,
        "name": "Lee",
        "size": "3",
        "readings": {"1": "123"}, # readings should be in a dictionary form with {t_id: reading}
        "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
        "appliance": [["fridge", 362, 3, "often"]],
        "password": "yes",
        "reset_Q": "My name?",
        "reset_A": "Default"
}
login.add_user(db, db["user_info"], user_info)
search.print_collection(tab)

# test 2
# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["125"],dates = ["Dec-31-2021 17:45:24"])

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["128"],dates = ["Jan-01-2022 19:13:24"])

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["232"],dates = ["Jan-03-2022 07:13:24"])

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["335"],dates = ["Jan-05-2022 15:23:45"])

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["499"],dates = ["Jan-10-2022 12:13:24"])

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["589"],dates = ["Jan-12-2022 22:13:24"])

bill = money.estimate_bill_period(collection=tab, usr_id=1, min_date = 'Jan-05-2022 6:50:12', max_date = "Jan-10-2022 18:14:00")

print(bill.dates)
print(bill.usr_id)
print(bill.power)
print(bill.power_calendar)
print(bill.power_calendar_divided)
print(bill.price_calendar)