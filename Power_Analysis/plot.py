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

def line_plot(date, power, usr_id, title):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d-%Y'))
    fig.gca().xaxis.set_major_locator(mdates.DayLocator())

    ax.plot(date, power, label='User: ' + str(usr_id))
    ax.grid()
    ax.set_xlabel("Date")
    ax.set_ylabel("Power [kWh]")
    ax.legend(loc='best')
    plt.tight_layout()

    plt.gcf().autofmt_xdate()
    plt.show()

def pie_plot(labels, data, usr_id, title, colors = None):
    fig = plt.figure()
    fig.suptitle("User " + str(usr_id) +" " + title)
    if colors == None:
        colors = ['#DBC9E9', '#C9F4FB', '#C9EFCB', '#FFFAC9', '#FFE7C9', '#FDC9C9']
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')

    ax.pie(data, labels=labels, autopct='%1.2f%%', colors=colors)
    plt.show()