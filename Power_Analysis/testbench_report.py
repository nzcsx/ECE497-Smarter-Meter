import Power_Analysis.power_report as report
import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal
import Power_Analysis.spatial as space
import Power_Analysis.plot as plot

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
                      ["laptop", 0.1, 1, "often"],
                      ["lamp", 0.2, 1, "often"],
                      ["ac", 1, 1, "rare"]], #"all day", "often", "rare", "not in use"
        "password": "yes",
        "reset_Q": "My name?",
        "reset_A": "Default"
}
login.add_user(db, db["user_info"], user_info)
#search.print_collection(tab)
# test 2
# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["125"],dates = ["Dec-31-2021 17:45:24"])
#search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["290"],dates = ["Jan-01-2022 19:13:24"])
#search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["317"],dates = ["Jan-03-2022 07:13:24"])
#search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["436"],dates = ["Jan-05-2021 15:23:45"])
#search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["593"],dates = ["Jan-10-2022 12:13:24"])
#search.print_collection(tab)

# dd-mm-YY H:M:S
update.add_power_reading(tab,1,readings = ["692.882"],dates = ["Jan-12-2021 22:13:24"])
#search.print_collection(tab)

report.display_report(db = db, collection = tab, usr_id = 1,
                       min_date = 'Dec-29-2021 12:50:12', max_date = "Jan-10-2022 22:13:25", export=True)

print("report done")