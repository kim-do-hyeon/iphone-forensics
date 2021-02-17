import os
import pathlib
import sqlite3
import plistlib
import src.util

def auto(self, extract_path) :
    try :
        try :
            # Apple Accounts Artifact
            apple_accounts_location = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/Accounts/Accounts3.sqlite")
            conn = sqlite3.connect(apple_accounts_location)
            cur_zaccount = conn.cursor()
            cur_zaccount.execute("SELECT ZUSERNAME, ZIDENTIFIER, ZDATE, ZACCOUNTDESCRIPTION, ZACCOUNTTYPE FROM ZACCOUNT")
            zaccount = cur_zaccount.fetchall()
            cur_zaccount_type = conn.cursor()
            cur_zaccount_type.execute("SELECT Z_PK, ZACCOUNTTYPEDESCRIPTION, ZCREDENTIALTYPE FROM ZACCOUNTTYPE")
            zaccount_type = cur_zaccount_type.fetchall()
            zaccount = list(zaccount)
            apple_account = zaccount
            for i in range(len(zaccount)) :
                zaccount[i] = list(zaccount[i])
            for i in range(len(zaccount)) :
                for j in range(len(zaccount_type)) :
                    if zaccount[i][4] == zaccount_type[j][0] :
                        apple_account[i].append(zaccount_type[j][1])
                        apple_account[i].append(zaccount_type[j][2])
            for i in range(len(apple_account)) :
                apple_account[i][2] = src.util.cocoa_date_to_human_date(apple_account[i][2])
            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table AppleAccounts (Username text, Identifier text, Date text, Account_Description text, Account_Type text, Account_Type_Description text, Credential_type text)")
                cur.executemany("insert into AppleAccounts values (?, ?, ?, ?, ?, ?, ?)", apple_account)
                conn.commit()
                conn.close()
                message = ("[AUTO] Apple Account Artifacts Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(10)
            except :
                print("[AUTO] Apple Account Artifacts Analyze Fail")
                pass
        except :
            print("[AUTO] Apple Account Artifacts Analyze Fail")
            pass

        # SIM Card Artifact
        try :
            sim_card_location = pathlib.Path(extract_path + "/extract_file/WirelessDomain/Library/Databases/CellularUsage.db")
            conn = sqlite3.connect(sim_card_location)
            cur_subcriber_info = conn.cursor()
            cur_subcriber_info.execute("SELECT subscriber_id, subscriber_mdn, last_update_time FROM subscriber_info")
            subcriber_info = cur_subcriber_info.fetchall()

            items = [["ICCID", subcriber_info[0][0]], ["Phone_Number", subcriber_info[0][1]], ["Date", src.util.cocoa_date_to_human_date(subcriber_info[0][2])]]

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table simcards (Key text, Value text)")
                cur.executemany("insert into simcards values (?, ?)", items)
                conn.commit()
                conn.close()
                message = ("[AUTO] Sim Card Artifacts Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(20)
            except :
                print("[AUTO] Sim Card Artifacts Analyze Fail")
                pass
        except :
            print("[AUTO] Sim Card Artifacts Analyze Fail")
            pass

        # Bluetooth Artifact
        try :
            path = extract_path + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Preferences/com.apple.MobileBluetooth.devices.plist"
            with open(path, 'rb') as fp :
                bluetooth_device = plistlib.loads(fp.read())
            # bluetooth_device = plistlib.readPlist(extract_path + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Preferences/com.apple.MobileBluetooth.devices.plist")
            bluetooth_device_mac_address = []
            for i in bluetooth_device :
                bluetooth_device_mac_address.append(i)
            bluetooth = []
            for i in range(len(bluetooth_device)) :
                Mac = bluetooth_device_mac_address[i]
                if (bluetooth_device[str(bluetooth_device_mac_address[i])].get("Name", "NULL")) == "NULL" :
                    Name = "NULL"
                else :
                    Name = bluetooth_device[str(bluetooth_device_mac_address[i])]["Name"]
                    if (bluetooth_device[str(bluetooth_device_mac_address[i])].get("LastSeenTime", "NULL")) == "NULL" :
                        LastSeenTime = "NULL"
                    else :
                        LastSeenTime = src.util.unix_date_to_human_date(bluetooth_device[str(bluetooth_device_mac_address[i])]["LastSeenTime"])
                        if (bluetooth_device[str(bluetooth_device_mac_address[i])].get("DefaultName", "NULL")) == "NULL" :
                            DefaultName = "NULL"
                        else :
                            DefaultName = bluetooth_device[str(bluetooth_device_mac_address[i])]["DefaultName"]
                bluetooth.append([Mac, Name, LastSeenTime, DefaultName])

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table bluetooth (Mac text, Name text, LastSeenTime text, DefaultName text)")
                cur.executemany("insert into bluetooth values (?, ?, ?, ?)", bluetooth)
                conn.commit()
                conn.close()
                message = ("[AUTO] Bluetooth Artifacts Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(30)
            except :
                print("[AUTO] Bluetooth Artifacts Analyze Fail")
                pass
        except :
            print("[AUTO] Bluetooth Artifacts Analyze Fail")
            pass

        # Bluetooth devices that have been shown Artifact
        try :
            bluetooth_that_have_been_shown_location = pathlib.Path(extract_path + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Database/com.apple.MobileBluetooth.ledevices.other.db")
            conn = sqlite3.connect(bluetooth_that_have_been_shown_location)
            cur_otherdevices = conn.cursor()
            cur_otherdevices.execute("SELECT Uuid, Name, Address FROM OtherDevices")
            otherdevices = cur_otherdevices.fetchall()

            for i in range(len(otherdevices)) :
                otherdevices[i] = list(otherdevices[i])
            
            for i in range(len(otherdevices)) :
                if otherdevices[i][1] == "" :
                    otherdevices[i][1] = "NULL"

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table bluetooth_that_have_been_shown (UUID text, Name text, Address text)")
                cur.executemany("insert into bluetooth_that_have_been_shown values (?, ?, ?)", otherdevices)
                conn.commit()
                conn.close()
                message = ("[AUTO] Bluetooth devices that have been shown Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(40)
            except :
                print("[AUTO] Bluetooth devices that have been shown Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] Bluetooth devices that have been shown Artifact Analyze Fail")
            pass

        # App Permision (TCC) Artifact
        try :
            tcc_location = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/TCC/TCC.db")
            conn = sqlite3.connect(tcc_location)
            cur_tcc = conn.cursor()
            cur_tcc.execute("SELECT service, client FROM access")
            tcc = cur_tcc.fetchall()

            for i in range(len(tcc)) :
                tcc[i] = list(tcc[i])

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table TCC (Service text, Client text)")
                cur.executemany("insert into TCC values (?, ?)", tcc)
                conn.commit()
                conn.close()
                message = ("[AUTO] App Permision (TCC) Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(50)
            except :
                print("[AUTO] App Permision (TCC) Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] App Permision (TCC) Artifact Analyze Fail")
            pass

        # Wallet Pass Artifact
        try :
            wallet_pass_path = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/Passes/Cards")
            wallet_pass_list = os.listdir(wallet_pass_path)
            wallet_list = []

            # Extract only .pkpass folder
            for i in wallet_pass_list :
                if i[28:] == ".pkpass" :
                    wallet_list.append(i)

            # Each Wallet Pass Pass.json
            wallet_list_json = []
            for i in range(len(wallet_list)) :
                json_location = pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/Passes/Cards/" + str(wallet_list[i]) + "/pass.json")
                wallet_list_json.append(json_location)

            # Export Json Data
            import json
            pass_detail = []
            for i in range(len(wallet_list_json)) :
                with open(wallet_list_json[i], 'r') as f:
                    json_data = json.load(f)

                organizationName = json_data['organizationName']
                description = json_data['description']
                serialNumber = json_data['serialNumber']
                secondaryFields_value = json_data['storeCard']["secondaryFields"]
                secondaryFields_value_Name = secondaryFields_value[0]['value']
                secondaryFields_value_Card_Number = secondaryFields_value[1]['value']

                pass_detail.append([organizationName, description, serialNumber, secondaryFields_value_Name, secondaryFields_value_Card_Number])

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table wallet_pass (OrganizationName text, Description text, SerialNumber text, Value_Name text, Value_Card_Number text)")
                cur.executemany("insert into wallet_pass values (?, ?, ?, ?, ?)", pass_detail)
                conn.commit()
                conn.close()
                message = ("[AUTO] Wallet Pass Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(60)
            except :
                print("[AUTO] Wallet Pass Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] Wallet Pass Artifact Analyze Fail")
            pass

        # Owner Information Artifact
        try :
            homesharing_path = extract_path + "/extract_file/HomeDomain/Library/Preferences/com.apple.homesharing.plist"
            purplebuddy_path = extract_path + "/extract_file/HomeDomain/Library/Preferences/com.apple.purplebuddy.plist"
            systemConfiguration_preferences_path = extract_path + "/extract_file/SystemPreferencesDomain/SystemConfiguration/preferences.plist"
            with open(homesharing_path, 'rb') as fp :
                homesharing = plistlib.loads(fp.read())
            with open(purplebuddy_path, 'rb') as fp :
                purplebuddy = plistlib.loads(fp.read())
            with open(systemConfiguration_preferences_path, 'rb') as fp :
                systemConfiguration_preferences = plistlib.loads(fp.read())
            # homesharing = plistlib.readPlist(extract_path + "/extract_file/HomeDomain/Library/Preferences/com.apple.homesharing.plist")
            # purplebuddy = plistlib.readPlist(extract_path + "/extract_file/HomeDomain/Library/Preferences/com.apple.purplebuddy.plist")
            # systemConfiguration_preferences = plistlib.readPlist(extract_path + "/extract_file/SystemPreferencesDomain/SystemConfiguration/preferences.plist")
            device_name = systemConfiguration_preferences["System"]["System"]["HostName"]
            apple_id = homesharing["homeSharingAppleID"]
            install_date = purplebuddy["SetupLastExit"]
            install_type = purplebuddy["SetupState"]

            owner_information = [["device_name", device_name], ["apple_id", apple_id], ["install_date", install_date], ["install_type", install_type]]

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table owner_information (Key text, Value text)")
                cur.executemany("insert into owner_information values (?, ?)", owner_information)
                conn.commit()
                conn.close()
                message = ("[AUTO] Owner Information Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(70)
            except :
                print("[AUTO] Owner Information Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] Owner Information Artifact Analyze Fail")
            pass

        # Calendar Event Artifact
        try :
            calendar_location = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/Calendar/Calendar.sqlitedb")
            
            conn = sqlite3.connect(calendar_location)
            cur_calendaritem = conn.cursor()
            cur_calendaritem.execute("SELECT summary, start_date, end_date FROM CalendarItem")
            calendaritem = cur_calendaritem.fetchall()
            calendar = []
            
            for i in range(len(calendaritem)) :
                value = [calendaritem[i][0], src.util.cocoa_date_to_human_date(calendaritem[i][1]), src.util.cocoa_date_to_human_date(calendaritem[i][2])]
                calendar.append(value)

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table calendar (Calendar_Item text, Start_Date text, End_Date text)")
                cur.executemany("insert into calendar values (?, ?, ?)", calendar)
                conn.commit()
                conn.close()
                message = ("[AUTO] Calendar Event Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(80)
            except :
                print("[AUTO] Calendar Event Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] Calendar Event Artifact Analyze Fail")
            pass

        # Address Book Artifact
        try :
            addressbook_location = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/AddressBook/AddressBook.sqlitedb")
            conn = sqlite3.connect(addressbook_location)

            cur_ABPerson = conn.cursor()
            cur_ABPerson.execute("SELECT ROWID, First, Last FROM ABPerson")
            ABPerson = cur_ABPerson.fetchall()

            cur_ABMultiValue = conn.cursor()
            cur_ABMultiValue.execute("SELECT record_id, value FROM ABMultiValue")
            ABMultiValue = cur_ABMultiValue.fetchall()

            addressbook = []

            for i in range(len(ABPerson)):
                for j in range(len(ABPerson)):
                    if ABMultiValue[i][0] == ABPerson[j][0] :
                        if str(ABPerson[j][2]) == str(None) :
                            name = ABPerson[j][1]
                        else :
                            name = str(ABPerson[j][2]) + str(ABPerson[j][1])
                        value = [name, ABMultiValue[i][1]]
                        addressbook.append(value)
            conn.close()

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table addressbook (Name text, Value text)")
                cur.executemany("insert into addressbook values (?, ?)", addressbook)
                conn.commit()
                conn.close()
                message = ("[AUTO] Address Book Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(90)
            except :
                print("[AUTO] Address Book Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] Address Book Artifact Analyze Fail")
            pass

        # Install Application Artifact
        try :
            installed_application_location = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/FrontBoard/applicationState.db")
            
            conn = sqlite3.connect(installed_application_location)
            cur_application_identifier_tab = conn.cursor()
            cur_application_identifier_tab.execute("SELECT id, application_identifier FROM application_identifier_tab")
            application_identifier_tab = cur_application_identifier_tab.fetchall()

            installed_application = []
            for i in range(len(application_identifier_tab)) :
                installed_application.append(["Value",application_identifier_tab[i][1]])
            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table installed_application (Key text, Value text)")
                cur.executemany("insert into installed_application values (?, ?)", installed_application)
                conn.commit()
                conn.close()
                message = ("[AUTO] Install Application Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(95)
            except :
                print("[AUTO] Install Application Artifact Analyze Fail")
                pass
        except :
            print("[AUTO] Install Application Artifact Analyze Fail")
            pass

        # SMS Artifact
        try :
            sms_location = pathlib.Path(extract_path + "/extract_file/HomeDomain/Library/SMS/sms.db")
            conn = sqlite3.connect(sms_location)

            cur_message = conn.cursor()
            cur_message.execute("SELECT text, account_guid, handle_id, date, date_read, date_delivered, service FROM message")
            message_items = cur_message.fetchall()

            cur_caller_id = conn.cursor()
            cur_caller_id.execute("SELECT destination_caller_id FROM message")
            caller_id = cur_caller_id.fetchall()
            caller_id = str(caller_id[0])
            caller_id= caller_id.replace("('",'').replace("',)",'')

            cur_handle = conn.cursor()
            cur_handle.execute("SELECT ROWID, id, service FROM handle")
            handle_items = cur_handle.fetchall()

            for i in range(len(message_items)) :
                message_items[i] = list(message_items[i])
            for i in range(len(handle_items)) :
                handle_items[i] = list(handle_items[i])

            message_list = []
            
            for i in range(len(message_items)) :
                for j in range(len(handle_items)) :
                    if message_items[i][2] == 0 :
                        Phone_Number = caller_id
                        Message = message_items[i][0]
                        Message_Type = message_items[i][6]
                        Date = src.util.cocoa_date_to_human_date_nano(message_items[i][3])
                        if message_items[i][4] == 0 :
                            Read_Date = 0
                        else :
                            Read_Date = src.util.cocoa_date_to_human_date_nano(message_items[i][4])
                        if message_items[i][5] == 0 :
                            Delivered_Date = 0
                        else :
                            Delivered_Date = src.util.cocoa_date_to_human_date_nano(message_items[i][5])
                        message_list.append([Phone_Number, Message, Message_Type, Date, Read_Date, Delivered_Date])
                        break
                    elif message_items[i][2] == handle_items[j][0] :
                        Phone_Number = handle_items[j][1]
                        Message = message_items[i][0]
                        Message_Type = message_items[i][6]
                        Date = src.util.cocoa_date_to_human_date_nano(message_items[i][3])
                        if message_items[i][4] == 0 :
                            Read_Date = 0
                        else :
                            Read_Date = src.util.cocoa_date_to_human_date_nano(message_items[i][4])
                        if message_items[i][5] == 0 :
                            Delivered_Date = 0
                        else :
                            Delivered_Date = src.util.cocoa_date_to_human_date_nano(message_items[i][5])
                        message_list.append([Phone_Number, Message, Message_Type, Date, Read_Date, Delivered_Date])
                        break

            try :
                conn = sqlite3.connect("analyze.db")
                cur = conn.cursor()
                cur.execute("create table SMS (Phone_Number text, Message text, Message_Type text, Date text, Read_Date text, Delivered_Date text)")
                cur.executemany("insert into SMS values (?, ?, ?, ?, ?, ?)", message_list)
                conn.commit()
                conn.close()
                message = ("[AUTO] SMS Artifact Analyze Success")
                print(message)
                self.processing_label.setText(message)
                self.progressBar.setValue(100)
            except :
                print("[AUTO] SMS Artifact Analyze Fail")
                pass
            self.processing_label.setText("AUTO ANALYZE SUCCESS")
            print("[AUTO] ANALYZE SUCCESS")
        except :
            print("[AUTO] SMS Artifact Analyze Fail")
            pass
    except :
        print("[AUTO] ANALYZE FAIL")
        