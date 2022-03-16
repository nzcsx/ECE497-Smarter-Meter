'''
Created on Tue Mar 15 23:00:32 2022
@author: Xuening Dong
'''

import Power_Analysis.db_login as login
import Power_Analysis.db_search as search
import Power_Analysis.db_update as update
import Power_Analysis.analysis as anal
from datetime import datetime

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

if __name__ == '__main__':
    now = datetime.now()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    outfile = open("/Users/dongxuening/Desktop/capstone_code/Power_Analysis/saved_file/report.html", "w")
    runner = HtmlTestRunner.HTMLTestRunner(
        stream=outfile,
        # title="Unit Test Report",
        # description="Database unit test result"
    )
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'
    runner.run(suite)
