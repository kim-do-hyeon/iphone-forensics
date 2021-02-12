import os
import pathlib
import sqlite3
import plistlib
import src.util

def apple_accounts():

    # Apple Accounts Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\HomeDomain\Library\Accounts\Accounts3.sqlite

    apple_accounts_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/Accounts")) + "\\Accounts3.sqlite")
    
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

    print("\n========== PRINT_TYPE ==========")
    print("'USERNAME' , 'IDENTIFIER', 'DATE', 'ACCOUNT_DESCRIPTION', 'ACCOUNT_TYPE', 'ACCOUNT_TYPE_DESCRIPTION', 'CREDENTIAL_TYPE'")
    print("================================\n")
    
    for i in range(len(apple_account)) :
        apple_account[i][2] = src.util.cocoa_date_to_human_date(apple_account[i][2])
        print(apple_account[i])

def sim_card():

    # SIM Card Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\WirelessDomain\Library\Databases\CellularUsage.db

    sim_card_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/WirelessDomain/Library/Databases")) + "\\CellularUsage.db")
    
    conn = sqlite3.connect(sim_card_location)
    cur_subcriber_info = conn.cursor()
    cur_subcriber_info.execute("SELECT subscriber_id, subscriber_mdn, last_update_time FROM subscriber_info")
    subcriber_info = cur_subcriber_info.fetchall()
    
    print("\n========== PRINT_TYPE ==========")
    print("'ICCID' , 'Phone Number', 'DATE'")
    print("================================\n")

    sim_card = []
    for i in range(3) :
        sim_card.append(subcriber_info[0][i])

    sim_card[2] = src.util.cocoa_date_to_human_date(sim_card[2])

    print("ICCID : ", sim_card[0])
    print("Phone Number : ", sim_card[1])
    print("Last Update Time : ", sim_card[2])

def bluetooth() :

    # Bluetooth Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\SysSharedContainerDomain-systemgroup.com.apple.bluetooth\Library\Preferences\com.apple.MobileBluetooth.devices.plist

    bluetooth_device = plistlib.readPlist(str(pathlib.Path(os.getcwd() + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Preferences/com.apple.MobileBluetooth.devices.plist")))
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
    
    print("\n========== PRINT_TYPE ==========")
    print("'MAC Address' , 'Name', 'Last Seen Time', 'Device Type'")
    print("================================\n")

    for i in bluetooth :
        print(i)

def bluetooth_that_have_been_shown() :

    # Bluetooth Bluetooth devices that have been shown Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\SysSharedContainerDomain-systemgroup.com.apple.bluetooth\Library\Database\com.apple.MobileBluetooth.ledevices.other.db

    bluetooth_that_have_been_shown_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/SysSharedContainerDomain-systemgroup.com.apple.bluetooth/Library/Database")) + "\\com.apple.MobileBluetooth.ledevices.other.db")
    conn = sqlite3.connect(bluetooth_that_have_been_shown_location)
    cur_otherdevices = conn.cursor()
    cur_otherdevices.execute("SELECT Uuid, Name, Address FROM OtherDevices")
    otherdevices = cur_otherdevices.fetchall()

    for i in range(len(otherdevices)) :
        otherdevices[i] = list(otherdevices[i])
    
    for i in range(len(otherdevices)) :
        if otherdevices[i][1] == "" :
            otherdevices[i][1] = "NULL"

    print("\n========== PRINT_TYPE ==========")
    print("'UUID' , 'Name', 'Address'")
    print("================================\n")

    for i in range(len(otherdevices)) :
            print(otherdevices[i])

def app_permission():

    # App Permision (TCC) Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\HomeDomain\Library\TCC\TCC.db

    tcc_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/TCC")) + "\\TCC.db")
    conn = sqlite3.connect(tcc_location)
    cur_tcc = conn.cursor()
    cur_tcc.execute("SELECT service, client FROM access")
    tcc = cur_tcc.fetchall()

    print("\n========== PRINT_TYPE ==========")
    print("'Service' , 'Client'")
    print("================================\n")

    for i in range(len(tcc)) :
        tcc[i] = list(tcc[i])
        print(tcc[i])

def wallet_pass() :

    # Wallet Pass Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\HomeDomain\Library\Passes\Cards\*.pkpass\pass.json

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

    print("\n========== PRINT_TYPE ==========")
    print("'Organization Name' , 'Description', 'Serial Number', 'Name', 'Card Number'")
    print("================================\n")

    for i in pass_detail :
        print(i)