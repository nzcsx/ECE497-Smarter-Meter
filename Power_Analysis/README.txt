#######################################################################
Created: December 21st, 2021
Last updated: Mar 19, 2022
#######################################################################

MacOS Catalina: Cannot use the MongoDB Community version 5.0
brew tap mongodb/brew
brew install mongodb-community@4.4

extra installs:
$ pip install pymongo==3.11.2
$ pip install mongoengine==0.22.1
$ pip install sympy
$ pip install scipy

Brief Introduction:
The current versions of the functions are written in separate files.
They can be aggregated into one file after all are tested. (see database.py)

Notice:
Please use string formatted datetime in all the arguments
For all inquiries related to appliance, need to specify the database name

Issues:
Need to update the functions for dictionaries to allow direct addition to the dictionary (fixed)

-------------- Database entries --------------
id: a unique id for identifying the user
name: the name of the user specified during registration
family_size: how many people are there in the family?
readings: power meter readings with a time_id as the key for research
datetime: the time and date the corresponding power meter reading with the same time_id is recorded (format: %b-%d-%Y %H:%M:%S)
appliance:
    - In user_info (input):
        format: [[appliance, wattage, quantity, usage frequency],...] -> [[string, int/float, int, string],...]
        usage frequency choices: "all day", "often" (12-24 hrs per day, e.g. shut down when sleeping), "rare"(0-12 hrs per day, e.g. switch on per use), "not in use"
    - Actually stored:
        The name of the collection
password:
    Should have at least one number.
    Should have at least one uppercase and one lowercase character.
    Should have at least one special symbol (@$!%*#?&).
    Should be between 5 to 15 characters long.
reset_Q: question to be asked per password reset
reset_A: answer to the question^
last_login_date: last date and time the user logged in

*** to do ***

-------------- db_login.py --------------
def connect_host(db_name, tab_name)
- Create a database and a table with specified names.

def add_db(client, db_name) # setup a new database with db_name
- Add a new database in the given client host connection

def add_table(db, tab_name)
- Add a new table to the given database with specified names.

def init_appliance(collection, app_info)
- Initialize all the appliance information in the database

def add_user(db, collection, user_info)
- Add a new entry to the database, usually a new user.
- Should check if the ids are replicated

def remove_collection(collection)
- Remove the whole table from database

def remove_user(db, collection, usr_id)
- Remove a specific user with his/her id.

def check_pwd(collection, usr_id, pwd)
- Check if the given password matches the one set in database

def get_new_id(collection)
- Assign a new id to the latest user.
- to do: (could be reusable ids for future considerations)

def get_id_by_name(collection, name)
- Get the id of the user with specified name

def get_reset_question(collection, usr_id)
- Get the reset password question

def reset_pwd(collection, usr_id, ans, new_pwd)
- Check the answer to the reset question
- Reset the password in the database

def check_pwd_validity(passwd)
- Check if the input password meets the requirement:
    - Should have at least one number.
    - Should have at least one uppercase and one lowercase character.
    - Should have at least one special symbol (@$!%*#?&).
    - Should be between 5 to 15 characters long.

*** to do ***

-------------- db_update.py --------------
def add_power_reading(collection, usr_id, readings, dates, time)
- Add new power meter readings to the present database

def update_family_info(collection, usr_id, family)
- Update the number of family members

def update_appliance_info(db, collection, usr_id, updated_info)
- Update the household appliance information
- Need to specify all the appliance information in the database (as we will delete all the former information)
- updated_info format: [[appliance, wattage, quantity, usage frequency],...] -> [[string, int/float, int, string],...]

def update_password(collection, usr_id, pwd)
- Update a password

def update_last_login(collection, usr_id)
- Update the last log in time of the user

def fetch_power_data(collection, usr_id, dir_id):
- dir_id: the id in the Google Drive at which the photos stored
- Should be called each time during the login of a user
- Fetch all the images from the Google Drive, use OCR to read the data and then delete
- Check if the readings are legal and then store them in the database

*** to do ***
def check_reading()

-------------- db_search.py --------------
def print_collection(collection)
def print_user_info(db, collection, usr_id)
def print_appliance_info(db, collection, usr_id)

def search_appliance_list(db, collection, usr_id)
- Get all appliance infomation in an array
- return format: [[appliance, wattage, quantity, usage frequency],...] -> [[string, int/float, int, string],...]

def search_family_info(collection, usr_id)
- return the family size of the user

def search_power_reading_all(collection, usr_id, return_string = True)
- return all power meter readings
- return power_readings, dates in corresponding chronological orders
- can choose either as a string or a datetime return format

def search_power_reading_date(collection, usr_id, min_date, max_date, return_string = True)
- return the power meter readings during the given time interval
- return power_readings, dates in corresponding chronological orders
- can choose either as a string or a datetime return format

def search_last_update(collection, usr_id, return_string = True)
- return the latest update datetime of the readings
- can choose either as a string or a datetime return format

*** to do ***

-------------- analysis.py --------------
def plot_temporal(collection, usr_id, min_date, max_date)
- plot the power meter readings during the given time interval

def plot_temporal_incremental(collection, usr_id, min_date, max_date)
- plot the power meter reading increments during the given time interval

--------------bill.py --------------
def estimate_bill_month(collection, usr_id, month = None)
def estimate_bill_period(collection, usr_id, min_date, max_date)
- returns the bill class with specified bill payments by various factors
- bill class contains:
    usr_id: user id
    min_date: start date of calculation
    max_date: end date of calculation
    power: power readings during the period
    dates: recorded dates and time during the period

    different prices:
        price_off_peak
        price_mid_peak
        price_on_peak

    Power spent at hours that belongs to:
        off_peak
        mid_peak
        on_peak

    power_calendar: power spent on each day over the period (key: date, value: power spent)
    power_calendar_divided: power spent on each day over the period divided into three categories by time (key: date, value: {key: category, value: power}})
    price_calendar: bill payment on each day over the period (key: date, value: bill payment)
    price_calendar_divided: bill payment on each day over the period divided into three categories by time (key: date, value: {key: category, value: bill payment}}

    total_bill: total estimated payment

-------------- spatial.py --------------
Preliminary idea:
- solve the Linear Diophantine equations: ax + by + cz +... = alpha
- a,b,c,... are the wattage of the appliances
- x, y, z are the hours of usage estimated by the solver (time("all day") = period length, time("not in use") = 0)
- sub in values to the dummy variable in the estimated time with in range [0,24] and find all reliable results
- eliminate the results that have time('rare') >= time('often')
--> working version 1: able to calculate the integer time value for up to 3 non-constant appliances

Method 1: Brute force
-> using the itertool to iterate through all the possible combination of wattage
-> find out the one sum up to the total consumption
-> if not found one, report the closest solution
-> constraints include time('rare') < time('often'), time("all day") = 24, time("not in use") = 0
-> add some assumptions? hrs/2<often<hrs (shut down when sleeping) and 0<rare<hrs/2 (switch on per time of usage)

Method 2: Brute force + CSP (for future implementation)
-> we now limit the estimation range to a specific day
-> use the power reading from the beginning to the end of a day (we need some extra function here)
-> then the maximum # hours would be 24
-> we parse through all the hours with only 1 significant bit
-> constraints include time('rare') < time('often'), time("all day") = 24, time("not in use") = 0
-> together with the total sum constraint
-> at most search 240^n iterations (where n is the number of appliances)
-> add some assumptions? 12<often<24 (shut down when sleeping) and 0<rare<12 (switch on per time of usage)

Method 2: Least Square Regression
-> impossible because we only have one equation


Problems:
- the current version of solver can only solve integer based solutions (partially solved by transferring kW into W)
- the number of hours from the results are all integers
- due to the last problem, it is possible that no feasible solution is found

def power_allocation(db, collection, usr_id, min_date, max_date)
- estimate the amount of power each of the appliances used with user id

*** to do ***
-> create a database for all the existing appliance models

*** to do ***
def plot_spatial()
def generate_warning()
bill payment estimations subject to the seasons

-------------- power_report.py --------------
def display_report(db, collection, usr_id, min_date, max_date, export = False)
- generate a series of report according to the power consumption data stored
- can be printed out into .txt file

def how_you_should_use_your_electricity_wisely()

*** to do ***
check the bill estimation functions and add them to the report
provide some preliminary analysis into the data patterns

-------------- Datetime format --------------
%b Month as locale’s abbreviated name(Jun)
%d Day of the month as a zero-padded decimal number(1)
%Y Year with century as a decimal number(2015)
%I Hour (12-hour clock) as a zero-padded decimal number(01)
%H Hour (24-hour clock) as a zero-padded decimal number(19)
%M Minute as a zero-padded decimal number(33)
%S Seconds as a zero-padded decimal number(11)
%p Locale’s equivalent of either AM or PM(PM)