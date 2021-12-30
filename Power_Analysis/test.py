import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update

client, db, tab = login.connect_host("Power", "user_info")
login.remove_collection(tab)

user_info = {
# need to add more information here
        "id": 1,
        "name": "Default",
        "size": "3",
        "readings": {"1": "123"}, # readings should be in a dictionary form with {t_id: reading}
        "date": {"1": "Dec-29-2021"},  # date should be in a dictionary form with {t_id:date}
        "time": {"1": "23:31"}, # time should be in a dictionary form with {t_id:time}
        "appliance": {"fridge":3}
}
login.add_user(tab, user_info)
search.print_collection(tab)

# test 1
update.update_appliance_info(tab,1,{"laptop":1})
search.print_collection(tab)

# test 2
update.add_power_reading(tab,1,readings = ["125"],dates = ["Dec-29-2021"], time = ["23:48"])
search.print_collection(tab)

update.add_power_reading(tab,1,readings = ["128"],dates = ["Dec-30-2021"], time = ["23:48"])
search.print_collection(tab)

update.add_power_reading(tab,1,readings = ["145"],dates = ["Dec-31-2021"], time = ["23:48"])
search.print_collection(tab)

# test 3
p,t,d = search.search_power_reading_date(tab, 1, min_date = "Dec-29-2021", max_date = "Dec-30-2021")
print(p,t,d)

# test 4
p,t,d = search.search_power_reading_date_time(tab, 1, min_date = "Dec-29-2021", max_date = "Dec-30-2021",
                                            min_time = "23:45", max_time="23:50")
print(p,t,d)

login.remove_collection(tab)
login.remove_connection(client)