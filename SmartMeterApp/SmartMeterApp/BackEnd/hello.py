##### pip install Flask #####

from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask import redirect, render_template, send_file, session, url_for

import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal
import Power_Analysis.spatial as space
import Power_Analysis.plot as plot
import base64
import requests
from PIL import Image
import Power_Analysis.bill as money

def timeNow():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def return_interesting():
    return 'interesting'

app = Flask(__name__)

table_verified = {
    'value1': True,
    'value2': False
}

@app.route('/time')
def serve():
    return jsonify({"time": timeNow()})

@app.route('/verify', methods=['GET', 'POST'])
def index():
    name = None
    print("content",request.data)

    # request manipulation
    data = str(request.data)[2:-1]
    print("Received content:", data)

    res = None
    print("user_name:", curr_name)

    if request.method == 'POST':
        name = data.split('=')[-1]
        id = login.get_id_by_name(tab, curr_name)
        res = search.search_appliance_list(db, tab, id)

    app_list = ""
    last_update = search.search_last_update(tab, id)
    last_login = search.search_last_login(tab, id)
    for app in res:
        app_list += app[0]+"*"+str(app[2])+": Wattage "+str(app[1])+" kWh"+ "| Frequency "+app[-1]+"\n"
    print("Sent:", app_list)
        #if table_verified[name]
    return jsonify({"name": curr_name, "id": id,
                    "appliance": app_list, "lastupdate": last_update,
                    "lastlogin": last_login})

@app.route('/login', methods=['GET', 'POST'])
def login_verification():
    # request manipulation
    data = str(request.data)[2:-1]
    print("Received content:", data)

    name, password = data.split('&')[0], data.split('&')[-1]
    name = name.split('=')[-1]
    password = password.split('=')[-1]
    print("User name:", name, ", password", password)

    valid_user = True
    uid = login.get_id_by_name(tab, name)

    if uid == -1:
        valid_user = False
    else:
        valid_user = login.check_pwd(tab, uid, password)

    if valid_user:
        global curr_name
        curr_name = name
        update.update_last_login(tab, uid)


    print("Sending:", valid_user)

    return jsonify({"valid": str(valid_user)})

@app.route('/report', methods=['GET', 'POST'])
def send_report():
    # request manipulation
    data = str(request.data)[2:-1]
    print("Received content:", data)
    print()

    path = ''
    uid = login.get_id_by_name(tab, curr_name)
    if data == 'temporal':
        path = "/Users/dongxuening/Desktop/SmartMeterApp_combined/assets/report/temporal" + str(uid) + ".png"

    # with open("saved_file/temporal1.png", "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    #
    # print(encoded_string)

    #
    # with open("yourfile.ext", "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    return jsonify({"imgurl": path})
    #send_file(path_or_file="saved_file/temporal1.png",mimetype='report/png', as_attachment=True)


if __name__ == '__main__':
    now = datetime.now()
    global client, db, tab
    client, db, tab = login.connect_host("Power", "user_info")
    #curr_name = ""
    login.remove_collection(db["user_1"])
    login.remove_collection(db["user_2"])
    login.remove_collection(tab)

    user_info = {
        # need to add more information here
        "id": 1,
        "name": "Lee",
        "size": "3",
        "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
        "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
        "appliance": [["fridge", 600, 1, "all day"],
                      ["laptop", 0.1, 1, "often"],
                      ["lamp", 0.2, 1, "often"],
                      ["oven", 1, 1, "rare"]],
        "password": "Yes",
        "reset_Q": "My name?",
        "reset_A": "Default"
    }
    login.add_user(db, db["user_info"], user_info)
    # Just for testing
    # dd-mm-YY H:M:S
    update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
    update.add_power_reading(tab, 1, readings=["190"], dates=["Jan-01-2022 19:13:24"])
    update.add_power_reading(tab, 1, readings=["217"], dates=["Jan-03-2022 07:13:24"])
    update.add_power_reading(tab, 1, readings=["236"], dates=["Jan-05-2021 15:23:45"])
    update.add_power_reading(tab, 1, readings=["293"], dates=["Jan-10-2022 12:13:24"])
    update.add_power_reading(tab, 1, readings=["292.882"], dates=["Jan-12-2021 22:13:24"])
    print("Done")
    search.print_collection(tab)

    anal.plot_temporal(tab, 1, min_date='Dec-29-2021 12:50:12', max_date="Jan-15-2022 20:14:00")
    names, hrs, consumption = space.spatial_itertool(db=db, collection=tab, usr_id=1,
                                                     min_date='Dec-29-2021 12:50:12', max_date="Jan-10-2022 22:13:25")
    print(names, hrs)
    plot.pie_plot(labels=names, data=hrs, usr_id=1, title="Spatial time breakdown",
                  colors=['#BDC7D3', '#D9CDC1', '#E4E1D0', '#F1E1D0'])

    bill = money.estimate_bill_period(collection=tab, usr_id=1, min_date='Jan-02-2022 6:50:12',
                                      max_date="Jan-10-2022 18:14:00")

    #bar_plot(labels, data, usr_id, title, xlabel ="", ylabel = "", colors = None):
    pd = bill.price_calendar
    bills, day = [], []
    print("Bill")
    for key in pd.keys():
        print(key)
        day.append(key)
        bills.append(pd[key])
    plot.bar_plot(day, bills, 1, "Bill Payment by day", "Date", "$")

    app.run(debug=True)
    login.remove_user(db, tab, 1)
    login.remove_collection(tab)
    login.remove_connection(client)



