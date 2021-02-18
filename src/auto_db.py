import os
import pathlib
import sqlite3
import plistlib
import src.util

def auto(manifest, info) :
    if src.util.db_exsit() == True :
        try :
            try : # iPhone Information
                manifest = plistlib.readPlist(manifest)
                info = plistlib.readPlist(info)
                device_name = info["Device Name"]
                display_name = info["Display Name"]
                build_version = info["Build Version"]
                GUID = info["GUID"]
                ICCID = info["ICCID"]
                IMEI = info["IMEI"]
                Last_Backup_Date = info["Last Backup Date"]
                phone_number = info["Phone Number"]
                product_name = info["Product Name"]
                product_type = info["Product Type"]
                product_version = info["Product Version"]
                serial_number = info["Serial Number"]
                target_identifier = info["Target Identifier"]
                target_type = info["Target Type"]

                items = [["Device_Name", device_name], ["Display_Name", display_name], ["Build_Version", build_version],
                ["GUID", GUID], ["ICCID", ICCID], ["IMEI", IMEI], ["Last_Backup_Date", Last_Backup_Date], ["Phone_Number", phone_number],
                ["Product_Name", product_name], ["Product_Type", product_type], ["Prodct_Version", product_version], ["Serial_Number", serial_number],
                ["Target_Identifier", target_identifier], ["Target_Type", target_type]]
                
                try :
                    conn = sqlite3.connect("analyze.db")
                    cur = conn.cursor()
                    cur.execute("create table Information (Key text, Value text)")
                    cur.executemany("insert into Information values (?, ?)", items)
                    conn.commit()
                    conn.close()
                    print("[Auto] iPhone Information Success")
                except :
                    print("[Auto] iPhone Information Fail")
                    pass
            except :
                print("[Auto] iPhone Information Fail")
                pass

            try : # Backup Information
                isencrypted = manifest["IsEncrypted"]
                backup_version = manifest["Version"]
                backup_date = manifest["Date"]
                backup_system_domains_version = manifest["SystemDomainsVersion"]
                backup_iphone_password_exsit = manifest["WasPasscodeSet"]

                items = [["IsEncrypted", isencrypted], ["Version", backup_version],
                ["Backup_Date", backup_date], ["Backup_System_Domains_Version", backup_system_domains_version],
                ["Backup_iPhone_Password_Exsit", backup_iphone_password_exsit]]

                try :
                    conn = sqlite3.connect("analyze.db")
                    cur = conn.cursor()
                    cur.execute("create table Backup_Information (Key text, Value text)")
                    cur.executemany("insert into Backup_Information values (?, ?)", items)
                    conn.commit()
                    conn.close()
                    print("[AUTO] Backup Information Success")
                except :
                    print("[AUTO] Backup Information Fail")
                    pass
            except :
                print("[AUTO] Backup Information Fail")
                pass

            try : # Iphone_Accessibility_Information
                mono_audio = manifest["Lockdown"]["com.apple.Accessibility"]["MonoAudioEnabledByiTunes"]
                voice_over_touch = manifest["Lockdown"]["com.apple.Accessibility"]["VoiceOverTouchEnabledByiTunes"]
                closed_captioning = manifest["Lockdown"]["com.apple.Accessibility"]["ClosedCaptioningEnabledByiTunes"]
                speak_auto_corrections = manifest["Lockdown"]["com.apple.Accessibility"]["SpeakAutoCorrectionsEnabledByiTunes"]
                invert_display = manifest["Lockdown"]["com.apple.Accessibility"]["InvertDisplayEnabledByiTunes"]
                zoom_touch = manifest["Lockdown"]["com.apple.Accessibility"]["ZoomTouchEnabledByiTunes"]

                items = [["Mono_Audio", mono_audio], ["Voice_Over_Touch", voice_over_touch], ["Closed_Captioning", closed_captioning],
                ["Speak_Auto_Corrections", speak_auto_corrections], ["Invert_Display", invert_display], ["Zoom_Touch", zoom_touch]]

                try :
                    conn = sqlite3.connect("analyze.db")
                    cur = conn.cursor()
                    cur.execute("create table Iphone_Accessibility_Information (Key text, Value text)")
                    cur.executemany("insert into Iphone_Accessibility_Information values (?, ?)", items)
                    conn.commit()
                    conn.close()
                    print("[AUTO] Iphone Accessibility Information Success")
                except :
                    print("[AUTO] Iphone Accessibility Information Fail")
                    pass
            except :
                print("[AUTO] Iphone Accessibility Information Fail")
                pass

            try : # Apple Accounts Artifact
                apple_accounts_location = pathlib.Path((os.getcwd() + "/extract_file/HomeDomain/Library/Accounts") + "\\Accounts3.sqlite")
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
                    print("[AUTO] Apple Accounts Artifact Success")
                except :
                    print("[AUTO] Apple Accounts Artifact Fail")
                    pass
            except :
                print("[AUTO] Apple Accounts Artifact Fail")
                pass

            try : # SIM Card Artifact
                sim_card_location = pathlib.Path((os.getcwd() + "/extract_file/WirelessDomain/Library/Databases") + "\\CellularUsage.db")
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
                    print("[AUTO] SIM Card Artifact Success")
                except :
                    print("[AUTO] SIM Card Artifact Fail")
                    pass
            except :
                print("[AUTO] SIM Card Artifact Fail")
                pass

            try : # Bluetooth Artifact
                bluetooth_device = plistlib.readPlist(os.getcwd() + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Preferences/com.apple.MobileBluetooth.devices.plist")
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
                    print("[AUTO] Bluetooth Artifact Success")
                except :
                    print("[AUTO] Bluetooth Artifact Fail")
                    pass
            except :
                print("[AUTO] Bluetooth Artifact Fail")
                pass

            try : # Bluetooth Bluetooth devices that have been shown Artifact
                bluetooth_that_have_been_shown_location = pathlib.Path((os.getcwd() + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Database") + "\\com.apple.MobileBluetooth.ledevices.other.db")
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
                    print("[AUTO] Bluetooth Bluetooth devices that have been shown Artifact Success")
                except :
                    print("[AUTO] Bluetooth Bluetooth devices that have been shown Artifact Fail")
                    pass
            except :
                print("[AUTO] Bluetooth Bluetooth devices that have been shown Artifact Fail")
                pass

            try : # App Permision (TCC) Artifact
                tcc_location = pathlib.Path((os.getcwd() + "/extract_file/HomeDomain/Library/TCC") + "\\TCC.db")
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
                    print("[AUTO] App Permision (TCC) Artifact Success")
                except :
                    print("[AUTO] App Permision (TCC) Artifact Fail")
                    pass
            except :
                print("[AUTO] App Permision (TCC) Artifact Fail")
                pass

            try : # Wallet Pass Artifact
                wallet_pass_path = pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/Passes/Cards")
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
                    print("[AUTO] Wallet Pass Artifact Success")
                except :
                    print("[AUTO] Wallet Pass Artifact Fail")
                    pass
            except :
                print("[AUTO] Wallet Pass Artifact Fail")
                pass

            try : # Owner Information Artifact
                homesharing = plistlib.readPlist(os.getcwd() + "/extract_file/HomeDomain/Library/Preferences/com.apple.homesharing.plist")
                purplebuddy = plistlib.readPlist(os.getcwd() + "/extract_file/HomeDomain/Library/Preferences/com.apple.purplebuddy.plist")
                systemConfiguration_preferences = plistlib.readPlist(os.getcwd() + "/extract_file/SystemPreferencesDomain/SystemConfiguration/preferences.plist")
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
                    print("[AUTO] Owner Information Artifact Success")
                except :
                    print("[AUTO] Owner Information Artifact Fail")
                    pass
            except :
                print("[AUTO] Owner Information Artifact Fail")
                pass

            try : # Calendar Event Artifact
                calendar_location = pathlib.Path((os.getcwd() + "/extract_file/HomeDomain/Library/Calendar") + "\\Calendar.sqlitedb")
                
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
                    print("[AUTO] Calendar Event Artifact Success")
                except :
                    print("[AUTO] Calendar Event Artifact Fail")
                    pass
            except :
                print("[AUTO] Calendar Event Artifact Fail")
                pass

            try : # Address Book Artifact
                addressbook_location = pathlib.Path((os.getcwd() + "/extract_file/HomeDomain/Library/AddressBook") + "\\AddressBook.sqlitedb")
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
                    print("[AUTO] Address Book Artifact Success")
                except :
                    print("[AUTO] Address Book Artifact Fail")
                    pass
            except :
                print("[AUTO] Address Book Artifact Fail")
                pass

            try : # Install Application Artifact
                installed_application_location = pathlib.Path((os.getcwd() + "/extract_file/HomeDomain/Library/FrontBoard") + "\\applicationState.db")
                
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
                    print("[AUTO] Install Application Artifact Success")
                except :
                    print("[AUTO] Install Application Artifact Fail")
                    pass
            except :
                print("[AUTO] Install Application Artifact Fail")
                pass


            try : # SMS Artifact
                sms_location = pathlib.Path((os.getcwd() + "/extract_file/HomeDomain/Library/SMS") + "\\sms.db")
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
                    print("[AUTO] SMS Artifact Success")
                except :
                    print("[AUTO] SMS Artifact Fail")
                    pass
            except :
                print("[AUTO] SMS Artifact Fail")
                pass
            print("AUTO ANALYZE SUCCESS")
        except :
            print("AUTO ANALYZE FAIL")
    else :
        print("Return to the first screen.")