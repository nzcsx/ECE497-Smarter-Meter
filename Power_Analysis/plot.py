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

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

def connect():
    gauth = GoogleAuth()
    # Create local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)  # Create GoogleDrive instance with authenticated GoogleAuth instance
    return drive

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
    path = "/Users/dongxuening/Desktop/SmartMeterApp_combined/assets/report/temporal" + str(usr_id) + ".png"
    plt.savefig(path, transparent = True)
    drive = connect()
    dir_id = "14GouHLUpFsIe9GP5Wcg2nIjXfJcmXoeK"

    dir_local = 'saved_file/'
    # upload these photo to google drive
    # filenames_local = os.listdir(dir_local)
    # for filename_local in filenames_local:
    #     print(filename_local)
    #     file_drive = drive.CreateFile({'parents': [{'id': dir_id}]})
    #     file_drive['title'] = filename_local
    #     file_drive.SetContentFile(os.path.join(dir_local, filename_local))
    #     file_drive.Upload()
    #     os.remove(os.path.join(dir_local, filename_local))
    #
    # plt.show()

def pie_plot(labels, data, usr_id, title, colors = None):
    fig = plt.figure()
    fig.suptitle("User " + str(usr_id) +" " + title)
    if colors is None:
        colors = ['#DBC9E9', '#C9F4FB', '#C9EFCB', '#FFFAC9', '#FFE7C9', '#FDC9C9']
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')

    ax.pie(data, labels=labels, autopct='%1.2f%%', colors=colors)
    plt.savefig("/Users/dongxuening/Desktop/SmartMeterApp_combined/assets/report/spatial" + str(usr_id) + ".png", transparent = True)
    # drive = connect()
    # dir_id = "14GouHLUpFsIe9GP5Wcg2nIjXfJcmXoeK"
    #
    # dir_local = 'saved_file/'
    # # upload these photo to google drive
    # filenames_local = os.listdir(dir_local)
    # for filename_local in filenames_local:
    #     print(filename_local)
    #     file_drive = drive.CreateFile({'parents': [{'id': dir_id}]})
    #     file_drive['title'] = filename_local
    #     file_drive.SetContentFile(os.path.join(dir_local, filename_local))
    #     file_drive.Upload()
    #     os.remove(os.path.join(dir_local, filename_local))
    # plt.show()

def bar_plot(labels, data, usr_id, title, xlabel ="", ylabel = "", colors = None):
    fig, ax = plt.subplots()
    fig.suptitle("User " + str(usr_id) + " " + title)

    ax.bar(labels, data)
    # new helper method to auto-label bars
    ax.bar_label(ax.containers[0])

    ax.set_ylabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    plt.savefig("/Users/dongxuening/Desktop/SmartMeterApp_combined/assets/report/bill" + str(usr_id) + ".png", transparent = True)
    # drive = connect()
    # dir_id = "14GouHLUpFsIe9GP5Wcg2nIjXfJcmXoeK"
    #
    # dir_local = 'saved_file/'
    # # upload these photo to google drive
    # filenames_local = os.listdir(dir_local)
    # for filename_local in filenames_local:
    #     print(filename_local)
    #     file_drive = drive.CreateFile({'parents': [{'id': dir_id}]})
    #     file_drive['title'] = filename_local
    #     file_drive.SetContentFile(os.path.join(dir_local, filename_local))
    #     file_drive.Upload()
    #     os.remove(os.path.join(dir_local, filename_local))
    # plt.show()