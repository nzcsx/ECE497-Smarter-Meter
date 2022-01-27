import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal
import Power_Analysis.spatial as space
import Power_Analysis.plot as plot
from datetime import datetime

client, db, tab = login.connect_host("Power", "user_info")
login.remove_collection(db["user_1"])
login.remove_collection(db["user_2"])
login.remove_collection(tab)

user_info = {
# need to add more information here
        "id": 1,
        "name": "Lee",
        "size": "3",
        "readings": {"1": "123"}, # readings should be in a dictionary form with {t_id: reading}
        "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
        "appliance": [["fridge", 600, 1, "all day"],
                      ["laptop", 3, 1, "often"],
                      ["oven", 1, 1, "rare"]], #"all day", "often", "rare", "not in use"
        "password": "yes",
        "reset_Q": "My name?",
        "reset_A": "Default"
}
login.add_user(db, db["user_info"], user_info)
search.print_collection(tab)
# test 2
# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["125"],dates = ["Dec-31-2021 17:45:24"])
search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["190"],dates = ["Jan-01-2022 19:13:24"])
search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["217"],dates = ["Jan-03-2022 07:13:24"])
search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["236"],dates = ["Jan-05-2021 15:23:45"])
search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["293"],dates = ["Jan-10-2022 12:13:24"])
search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["292.882"],dates = ["Jan-12-2021 22:13:24"])
search.print_collection(tab)



names, hrs, consumption = space.power_allocation(db = db, collection = tab, usr_id = 1,
                       min_date = 'Dec-29-2021 12:50:12', max_date = "Jan-15-2022 20:14:00")
print(names, hrs)
plot.pie_plot(labels=names, data=hrs, usr_id=1, title="Spatial time breakdown")
plot.pie_plot(labels=names, data=consumption, usr_id=1, title="Spatial power breakdown")

login.remove_user(db, tab,1)
login.remove_collection(tab)
login.remove_connection(client)