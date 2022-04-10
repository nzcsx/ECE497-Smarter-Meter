'''
Created on Tue Mar 15 23:00:32 2022
@author: Xuening Dong
'''

import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal
import Power_Analysis.spatial as space
import Power_Analysis.bill as money
from datetime import datetime
import numpy as np

import unittest
import HtmlTestRunner

class TestDatabase(unittest.TestCase):

    def test_login_single_user(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        self.assertEqual(search.print_user_info(db, tab, 2), -1)
        self.assertEqual(search.search_appliance_list(db, tab, 1),[["fridge", 362, 3, "often"]])
        self.assertEqual(search.search_power_reading_all(tab, 1),["123"])
        self.assertEqual(login.get_new_id(tab), 2)
        self.assertEqual(login.get_id_by_name(tab, "Lee"), 1)
        self.assertEqual(login.get_id_by_name(tab, "Someone"), -1)

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        self.assertEqual(login.get_id_by_name(tab, "Lee"), -1)
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_login_multiple_user(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(db["user_2"])
        login.remove_collection(db["user_3"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        user_info = {
            # need to add more information here
            "id": login.get_new_id(tab),
            "name": "Someone",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 19:20:21"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["oven", 33, 1, "rare"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, tab, user_info)
        self.assertEqual(search.print_user_info(db, tab, 2), None)
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 362, 3, "often"]])
        self.assertEqual(search.search_appliance_list(db, tab, 2), [["oven", 33, 1, "rare"]])
        self.assertEqual(login.get_new_id(tab), 3)

        user_info = {
            # need to add more information here
            "id": login.get_new_id(tab),
            "name": "Alice",
            "size": "5",
            "readings": {"1": "199"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 19:20:21"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["oven", 33, 1, "rare"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, tab, user_info)
        self.assertEqual(search.search_power_reading_all(tab, 3), ["199"])

        self.assertEqual(login.get_id_by_name(tab, "Lee"), 1)
        self.assertEqual(login.get_id_by_name(tab, "Someone"), 2)
        self.assertEqual(login.get_id_by_name(tab, "Alice"), 3)
        self.assertEqual(login.get_id_by_name(tab, "Yang"), -1)

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])

        self.assertEqual(login.get_id_by_name(tab, "Lee"), -1)
        self.assertEqual(login.get_id_by_name(tab, "Someone"), 2)
        self.assertEqual(login.get_id_by_name(tab, "Alice"), 3)

        login.remove_user(db, tab, 2)
        login.remove_collection(db["user_2"])

        self.assertEqual(login.get_id_by_name(tab, "Lee"), -1)
        self.assertEqual(login.get_id_by_name(tab, "Someone"), -1)
        self.assertEqual(login.get_id_by_name(tab, "Alice"), 3)

        login.remove_user(db, tab, 3)
        login.remove_collection(db["user_3"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_update_power_single(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)
        # dd-mm-YY H:M:S
        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 1, readings=["128"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["132"], dates=["Jan-03-2022 07:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "128", "132"])

        update.add_power_reading(tab, 1, readings=["135"], dates=["Jan-05-2021 15:23:45"])
        update.add_power_reading(tab, 1, readings=["138"], dates=["Jan-10-2022 12:13:24"])
        update.add_power_reading(tab, 1, readings=["142"], dates=["Jan-12-2021 22:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "128", "132", "135", "138", "142"])

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_update_power_multiple(self):
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
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        user_info = {
            # need to add more information here
            "id": login.get_new_id(tab),
            "name": "Alice",
            "size": "5",
            "readings": {"1": "117"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 19:20:21"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["oven", 33, 1, "rare"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)
        # dd-mm-YY H:M:S
        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 2, readings=["128"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["132"], dates=["Jan-03-2022 07:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "132"])
        self.assertEqual(search.search_power_reading_all(tab, 2), ["117", "128"])

        update.add_power_reading(tab, 2, readings=["135"], dates=["Jan-05-2021 15:23:45"])
        update.add_power_reading(tab, 1, readings=["138"], dates=["Jan-10-2022 12:13:24"])
        update.add_power_reading(tab, 2, readings=["142"], dates=["Jan-12-2021 22:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "132", "138"])
        self.assertEqual(search.search_power_reading_all(tab, 2), ["117", "128", "135", "142"])

        login.remove_user(db, tab, 1)
        login.remove_user(db, tab, 2)
        login.remove_collection(db["user_1"])
        login.remove_collection(db["user_2"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_update_appliance(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        update.update_appliance_info(db, tab, 1, [["laptop", 192, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["laptop", 192, 2, "all day"]])

        update.update_appliance_info(db, tab, 1, [["fridge", 362, 3, "often"], ["laptop", 192, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 362, 3, "often"],
                                                                    ["laptop", 192, 2, "all day"]])

        update.update_appliance_info(db, tab, 1, [["fridge", 362, 3, "often"],
                                                  ["laptop", 192, 2, "all day"],
                                                  ["AC", 577, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 362, 3, "often"],
                                                                    ["laptop", 192, 2, "all day"],
                                                                    ["AC", 577, 2, "all day"]])

        update.update_appliance_info(db, tab, 1, [["laptop", 192, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["laptop", 192, 2, "all day"]])

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_update_family(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        update.update_family_info(tab, 1, '5')
        self.assertEqual(search.search_family_info(tab, 1), "5")

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_update_password(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        update.update_password(tab, 1, "nice")
        self.assertEqual(login.check_pwd(tab, 1, "yes"), False)
        self.assertEqual(login.check_pwd(tab, 1, "nice"), True)

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_password_validity(self):
        # illegal length
        pwd = "Hi!3"
        self.assertEqual(login.check_pwd_validity(pwd), False)
        pwd = "Hiwowowowowowowoowowowo!3"
        self.assertEqual(login.check_pwd_validity(pwd), False)

        # Missing part
        pwd = "higoodmoing!3"
        self.assertEqual(login.check_pwd_validity(pwd), False)
        pwd = "higoodMorning!"
        self.assertEqual(login.check_pwd_validity(pwd), False)
        pwd = "hiMorning9"
        self.assertEqual(login.check_pwd_validity(pwd), False)

        # Correct
        pwd = "ECE496Capst!ne"
        self.assertEqual(login.check_pwd_validity(pwd), True)

    def test_reset_QA(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        self.assertEqual(login.get_reset_question(tab, 1), "My name?")
        self.assertEqual(login.reset_pwd(tab, 1, "Not Default", "Hey"), None)
        self.assertEqual(login.check_pwd(tab, 1, "yes"), True)

        self.assertEqual(login.reset_pwd(tab, 1, "Default", "Hey"), None)
        self.assertEqual(login.check_pwd(tab, 1, "yes"), False)
        self.assertEqual(login.check_pwd(tab, 1, "Hey"), True)

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_reading_correction(self):
        res_1 = login.is_reading_legal(['xx'],
                                       [1], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], ['xx'])
        self.assertEqual(res_1[1], [1])

        res_1 = login.is_reading_legal(['xx'],
                                       [18], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], [])
        self.assertEqual(res_1[1], [])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz'],
                                       [1, 1, 1], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], ['xx', 'yy', 'zz'])
        self.assertEqual(res_1[1], [1, 1, 1])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz'],
                                       [2, 2, 4], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], ['xx', 'yy', 'zz'])
        self.assertEqual(res_1[1], [2, 2, 4])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz'],
                                       [1, 3, 10], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], ['xx', 'yy'])
        self.assertEqual(res_1[1], [1, 3])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz'],
                                       [9, 0, 2], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], ['zz'])
        self.assertEqual(res_1[1], [2])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz'],
                                       [9, 0, 15], last_reading=1, max_inc=2)
        self.assertEqual(res_1[0], [])
        self.assertEqual(res_1[1], [])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz', 'kk', 'ff'],
                                                [1, 0, 3, 8, 0], last_reading=1, max_inc=1)
        self.assertEqual(res_1[0], ['xx', 'zz'])
        self.assertEqual(res_1[1], [1, 3])

        res_1 = login.is_reading_legal(['xx', 'yy', 'zz', 'kk', 'ff'],
                                       [1, 1, 1, 1, 1], last_reading=1, max_inc=3)
        self.assertEqual(res_1[0], ['xx', 'yy', 'zz', 'kk', 'ff'])
        self.assertEqual(res_1[1], [1, 1, 1, 1, 1])

class TestPowerAnalysis(unittest.TestCase):
    def test_power_by_date_range(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        # dd-mm-YY H:M:S
        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 1, readings=["128"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["132"], dates=["Jan-03-2022 07:13:24"])
        update.add_power_reading(tab, 1, readings=["135"], dates=["Jan-05-2022 15:23:45"])
        update.add_power_reading(tab, 1, readings=["138"], dates=["Jan-10-2022 12:13:24"])
        update.add_power_reading(tab, 1, readings=["142"], dates=["Jan-12-2022 22:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "128", "132", "135", "138", "142"])

        # power search result
        p,d = search.search_power_reading_date(tab, 1, min_date='Dec-29-2021 18:50:12', max_date="Dec-31-2021 18:14:00")
        self.assertEqual(p, ['125'])
        self.assertEqual(d, ['Dec-31-2021 17:45:24'])

        p, d = search.search_power_reading_date(tab, 1, min_date='Dec-29-2021 12:50:12',
                                                max_date="Dec-31-2021 18:14:00")
        self.assertEqual(p, ['123','125'])
        self.assertEqual(d, ['Dec-29-2021 17:13:24', 'Dec-31-2021 17:45:24'])

        p, d = search.search_power_reading_date(tab, 1, min_date='Dec-29-2021 12:50:12',
                                                max_date="Jan-05-2022 18:14:00")
        self.assertEqual(p, ['123', '125', "128", "132", "135"])
        self.assertEqual(d, ['Dec-29-2021 17:13:24', 'Dec-31-2021 17:45:24',
                             "Jan-01-2022 19:13:24", "Jan-03-2022 07:13:24", "Jan-05-2022 15:23:45"])

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        self.assertEqual(login.get_id_by_name(tab, "Lee"), -1)
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_date_by_power_range(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)

        # dd-mm-YY H:M:S
        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 1, readings=["128"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["132"], dates=["Jan-03-2022 07:13:24"])
        update.add_power_reading(tab, 1, readings=["135"], dates=["Jan-05-2022 15:23:45"])
        update.add_power_reading(tab, 1, readings=["138"], dates=["Jan-10-2022 12:13:24"])
        update.add_power_reading(tab, 1, readings=["142"], dates=["Jan-12-2022 22:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "128", "132", "135", "138", "142"])

        # power search result
        p,d = search.search_power_interval(tab, 1, 120, 130)
        self.assertEqual(p, ['123', '125', '128'])
        self.assertEqual(d, ['Dec-29-2021 17:13:24', 'Dec-31-2021 17:45:24', 'Jan-01-2022 19:13:24'])

        # power search result
        p, d = search.search_power_interval(tab, 1, 110, 120)
        self.assertEqual(p, [])
        self.assertEqual(d, [])

        # power search result
        p, d = search.search_power_interval(tab, 1, 130, 140)
        self.assertEqual(p, ['132', '135', '138'])
        self.assertEqual(d, ["Jan-03-2022 07:13:24","Jan-05-2022 15:23:45", "Jan-10-2022 12:13:24"])

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        self.assertEqual(login.get_id_by_name(tab, "Lee"), -1)
        login.remove_collection(tab)
        login.remove_connection(client)

class TestSpatialAnalysis(unittest.TestCase):
    def test_appliance_list(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)
        self.assertEqual(login.get_id_by_name(tab, "Lee"), 1)

        update.update_appliance_info(db, tab, 1, [["laptop", 192, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["laptop", 192, 2, "all day"]])

        update.update_appliance_info(db, tab, 1, [["fridge", 362, 3, "often"], ["laptop", 192, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 362, 3, "often"],
                                                                    ["laptop", 192, 2, "all day"]])

        update.update_appliance_info(db, tab, 1, [["fridge", 362, 3, "often"],
                                                  ["laptop", 192, 2, "all day"],
                                                  ["AC", 577, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 362, 3, "often"],
                                                                    ["laptop", 192, 2, "all day"],
                                                                    ["AC", 577, 2, "all day"]])

        update.update_appliance_info(db, tab, 1, [["laptop", 192, 2, "all day"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["laptop", 192, 2, "all day"]])

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_appliace_has_solution(self):
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
            "appliance": [["fridge", 600, 1, "all day"],
                          ["laptop", 0.1, 1, "often"],
                          ["lamp", 0.2, 1, "often"],
                          ["oven", 1, 1, "rare"]],  # "all day", "often", "rare", "not in use"
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)
        self.assertEqual(login.get_id_by_name(tab, "Lee"), 1)

        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 1, readings=["190"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["217"], dates=["Jan-03-2022 07:13:24"])
        update.add_power_reading(tab, 1, readings=["236"], dates=["Jan-05-2022 15:23:45"])
        update.add_power_reading(tab, 1, readings=["293"], dates=["Jan-10-2022 12:13:24"])
        #update.add_power_reading(tab, 1, readings=["292.882"], dates=["Jan-12-2022 22:13:24"])

        res_appliance = search.search_appliance_list(db, tab, 1)
        self.assertEqual(res_appliance, [["fridge", 600, 1, "all day"],
                          ["laptop", 0.1, 1, "often"],
                          ["lamp", 0.2, 1, "often"],
                          ["oven", 1, 1, "rare"]])

        power_app = np.array([600, 0.1, 0.2, 1])
        names, hrs, consumption = space.spatial_itertool(db=db, collection=tab, usr_id=1,
                                                         min_date='Dec-29-2021 12:50:12',
                                                         max_date="Jan-10-2022 22:13:25")
        self.assertEqual(int(np.dot(hrs, power_app)), (293-123)*1000)
        self.assertGreater(hrs[1], hrs[3])
        self.assertGreater(hrs[2], hrs[3])

        update.update_appliance_info(db, tab, 1, [["fridge", 600, 1, "all day"],
                                                  ["laptop", 1, 3, "rare"],
                                                  ["AC", 577, 2, "not in use"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 600, 1, "all day"],
                                                  ["laptop", 1, 3, "rare"],
                                                  ["AC", 577, 2, "not in use"]])

        names, hrs, consumption = space.spatial_itertool(db=db, collection=tab, usr_id=1,
                                                         min_date='Dec-29-2021 12:50:12',
                                                         max_date="Jan-10-2022 22:13:25")

        self.assertEqual(int(np.dot(hrs, [600, 3, 577*2])), (293 - 123) * 1000)
        self.assertEqual(hrs[2], 0)

        login.remove_user(db, tab, 1)
        login.remove_collection(tab)
        login.remove_connection(client)

    def test_appliace_no_solution(self):
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
            "appliance": [["fridge", 600, 1, "all day"],
                          ["laptop", 0.1, 1, "often"],
                          ["lamp", 0.2, 1, "often"],
                          ["oven", 1, 1, "rare"]],  # "all day", "often", "rare", "not in use"
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)
        self.assertEqual(login.get_id_by_name(tab, "Lee"), 1)

        # dd-mm-YY H:M:S
        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 1, readings=["290"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["317"], dates=["Jan-03-2022 07:13:24"])
        update.add_power_reading(tab, 1, readings=["436"], dates=["Jan-05-2022 15:23:45"])
        update.add_power_reading(tab, 1, readings=["593"], dates=["Jan-10-2022 12:13:24"])
        update.add_power_reading(tab, 1, readings=["692.882"], dates=["Jan-12-2021 22:13:24"])
        #update.add_power_reading(tab, 1, readings=["292.882"], dates=["Jan-12-2022 22:13:24"])

        res_appliance = search.search_appliance_list(db, tab, 1)
        self.assertEqual(res_appliance, [["fridge", 600, 1, "all day"],
                          ["laptop", 0.1, 1, "often"],
                          ["lamp", 0.2, 1, "often"],
                          ["oven", 1, 1, "rare"]])

        names, hrs, consumption = space.spatial_itertool(db=db, collection=tab, usr_id=1,
                                                         min_date='Dec-29-2021 12:50:12',
                                                         max_date="Jan-10-2022 22:13:25")
        self.assertNotEqual(int(np.dot(hrs, [600, 0.1, 0.2, 1])), (593-123)*1000)
        self.assertGreater(hrs[1], hrs[3])
        self.assertGreater(hrs[2], hrs[3])

        update.update_appliance_info(db, tab, 1, [["fridge", 600, 1, "all day"],
                                                  ["laptop", 3, 3, "rare"],
                                                  ["AC", 577, 2, "not in use"]])
        self.assertEqual(search.search_appliance_list(db, tab, 1), [["fridge", 600, 1, "all day"],
                                                  ["laptop", 3, 3, "rare"],
                                                  ["AC", 577, 2, "not in use"]])

        names, hrs, consumption = space.spatial_itertool(db=db, collection=tab, usr_id=1,
                                                         min_date='Dec-29-2021 12:50:12',
                                                         max_date="Jan-10-2022 22:13:25")

        self.assertNotEqual(int(np.dot(hrs, [600, 9, 577*2])), (293 - 123) * 1000)
        self.assertEqual(hrs[2], 0)

        login.remove_user(db, tab, 1)
        login.remove_collection(tab)
        login.remove_connection(client)
        
class TestBillPayment(unittest.TestCase):
    def test_bill_calculation(self):
        client, db, tab = login.connect_host("Power", "user_info")
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)

        user_info = {
            # need to add more information here
            "id": 1,
            "name": "Lee",
            "size": "3",
            "readings": {"1": "123"},  # readings should be in a dictionary form with {t_id: reading}
            "date": {"1": "Dec-29-2021 17:13:24"},  # date should be in a dictionary form with {t_id:date}
            "appliance": [["fridge", 362, 3, "often"]],
            "password": "yes",
            "reset_Q": "My name?",
            "reset_A": "Default"
        }
        login.add_user(db, db["user_info"], user_info)
        self.assertEqual(login.get_id_by_name(tab, "Lee"), 1)

        # dd-mm-YY H:M:S
        update.add_power_reading(tab, 1, readings=["125"], dates=["Dec-31-2021 17:45:24"])
        update.add_power_reading(tab, 1, readings=["128"], dates=["Jan-01-2022 19:13:24"])
        update.add_power_reading(tab, 1, readings=["232"], dates=["Jan-03-2022 07:13:24"])
        update.add_power_reading(tab, 1, readings=["335"], dates=["Jan-05-2022 15:23:45"])
        update.add_power_reading(tab, 1, readings=["499"], dates=["Jan-10-2022 12:13:24"])
        update.add_power_reading(tab, 1, readings=["589"], dates=["Jan-12-2022 22:13:24"])

        self.assertEqual(search.search_power_reading_all(tab, 1), ["123", "125", "128", "232", "335", "499", "589"])
        bill = money.estimate_bill_period(collection=tab, usr_id=1, min_date='Jan-05-2022 6:50:12',
                                          max_date="Jan-10-2022 18:14:00")
        # correctness of the user id and the range of power
        self.assertEqual(bill.usr_id, 1)
        self.assertEqual(bill.power, ['335', '499'])

        max_d = datetime.strptime(('Jan-10-2022' + " 23:59:59")
                                           , "%b-%d-%Y %H:%M:%S")
        min_d = datetime.strptime(('Jan-05-2022' + " 00:00:00")
                                           , "%b-%d-%Y %H:%M:%S")
        # check if the power is correctly summed up
        for key in bill.power_calendar.keys():
            self.assertEqual(round(bill.power_calendar_divided[key]['on_peak'] +
                                 bill.power_calendar_divided[key]['off_peak'] +
                                 bill.power_calendar_divided[key]['mid_peak']), round(bill.power_calendar[key]))

            date = datetime.strptime(key, ("%b-%d-%Y"))
            #self.assertIn(date, range(min_d, max_d))

            if date.weekday() > 5:
                self.assertEqual(bill.power_calendar_divided[key]['on_peak'], 0)
                self.assertEqual(bill.power_calendar_divided[key]['mid_peak'], 0)
        # check if the price is correctly summed up
        sum = 0
        for key in bill.price_calendar_divided.keys():
            sum += bill.price_calendar[key]
            self.assertEqual(round(bill.price_calendar_divided[key]['on_peak'] +
                                 bill.price_calendar_divided[key]['off_peak'] +
                                 bill.price_calendar_divided[key]['mid_peak']), round(bill.price_calendar[key]))

        self.assertEqual(sum, bill.total_bill)

        login.remove_user(db, tab, 1)
        login.remove_collection(db["user_1"])
        login.remove_collection(tab)
        login.remove_connection(client)

if __name__ == '__main__':
    now = datetime.now()
    suite = unittest.TestSuite()
    suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestDatabase),
        unittest.TestLoader().loadTestsFromTestCase(TestPowerAnalysis),
        unittest.TestLoader().loadTestsFromTestCase(TestSpatialAnalysis),
        unittest.TestLoader().loadTestsFromTestCase(TestBillPayment)
    ])
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    # suite1 = unittest.TestLoader().loadTestsFromTestCase(TestPowerAnalysis)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    outfile = open("/Users/dongxuening/Desktop/capstone_code/Power_Analysis/saved_file/report.html", "w")
    runner = HtmlTestRunner.HTMLTestRunner(
        stream=outfile,
        report_title="Unit Test Report",
    )
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'
    runner.run(suite)
    # runner.run(suite1)
