##### pip install Flask #####

from datetime import datetime
from flask import Flask, jsonify, render_template, request
import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal

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

    if request.method == 'POST':
        name = data.split('=')[-1]
        id = login.get_id_by_name(tab, name)
        res = search.search_appliance_list(db, tab, id)

    app_list = ""
    for app in res:
        app_list += app[0]+"*"+str(app[2])+": Wattage "+str(app[1])+" kWh"+ "| Frequency "+app[-1]+"\n"
    print("Sent:", app_list)
        #if table_verified[name]
    return jsonify({"appliance": app_list})#render_template('/Users/dongxuening/Desktop/SmartMeterApp/BackEnd/index.html', name=name)

if __name__ == '__main__':
    now = datetime.now()
    global client, db, tab
    client, db, tab = login.connect_host("Power", "user_info")
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
        "appliance": [["Fridge", 362, 3, "often"], ["Oven", 362, 3, "rare"]],
        "password": "yes",
        "reset_Q": "My name?",
        "reset_A": "Default"
    }
    login.add_user(db, db["user_info"], user_info)
    print("Done")
    search.print_collection(tab)

    app.run(debug=True)
    login.remove_user(db, tab, 1)
    login.remove_collection(tab)
    login.remove_connection(client)



