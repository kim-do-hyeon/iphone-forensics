import os
import pathlib
import sqlite3
import plistlib
import src.util

def owner_infomation_artifact():
    try : # Owner Information Artifact
        homesharing_location = os.getcwd() + "/extract_file/HomeDomain/Library/Preferences/com.apple.homesharing.plist"
        purplebuddy_location = os.getcwd() + "/extract_file/HomeDomain/Library/Preferences/com.apple.purplebuddy.plist"
        systemConfiguration_preferences_location = os.getcwd() + "/extract_file/SystemPreferencesDomain/SystemConfiguration/preferences.plist"
        with open(homesharing_location, 'rb') as fp :
                homesharing = plistlib.loads(fp.read())
        with open(purplebuddy_location, 'rb') as fp :
                purplebuddy = plistlib.loads(fp.read())
        with open(systemConfiguration_preferences_location, 'rb') as fp :
                systemConfiguration_preferences = plistlib.loads(fp.read())
        device_name = systemConfiguration_preferences["System"]["System"]["HostName"]
        apple_id = homesharing["homeSharingAppleID"]
        install_date = purplebuddy["SetupLastExit"]
        install_type = purplebuddy["SetupState"]

        owner_information = [device_name, apple_id, install_date, install_type]
        print("\n")
        print("Device Name : ", device_name)
        print("Apple ID : ", apple_id)
        print("Install Date : ", install_date)
        print("Instal Type : ", install_type)
    except :
        print("Something Wrong.")

def calendar_event_artifact():

    try : # Calendar Event Artifact
        calendar_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/Calendar")) + "\\Calendar.sqlitedb")
        
        conn = sqlite3.connect(calendar_location)
        cur_calendaritem = conn.cursor()
        cur_calendaritem.execute("SELECT summary, start_date, end_date FROM CalendarItem")
        calendaritem = cur_calendaritem.fetchall()
        calendar = []

        print("\n========== PRINT_TYPE ==========")
        print("'Calendar Item' , 'Start Date & Time', 'End Date & Time'")
        print("================================\n")
        
        for i in range(len(calendaritem)) :
            value = [calendaritem[i][0], src.util.cocoa_date_to_human_date(calendaritem[i][1]), src.util.cocoa_date_to_human_date(calendaritem[i][2])]
            print(value)
            calendar.append(value)
    except :
        print("Something Wrong.")

def addressbook_artifact():
    try : # Address Book Artifact
        addressbook_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/AddressBook")) + "\\AddressBook.sqlitedb")
        conn = sqlite3.connect(addressbook_location)

        cur_ABPerson = conn.cursor()
        cur_ABPerson.execute("SELECT ROWID, First, Last FROM ABPerson")
        ABPerson = cur_ABPerson.fetchall()

        cur_ABMultiValue = conn.cursor()
        cur_ABMultiValue.execute("SELECT record_id, value FROM ABMultiValue")
        ABMultiValue = cur_ABMultiValue.fetchall()

        addressbook = []

        print("\n========== PRINT_TYPE ==========")
        print("'Name' , 'Value'")
        print("================================\n")

        for i in range(len(ABPerson)):
            for j in range(len(ABPerson)):
                if ABMultiValue[i][0] == ABPerson[j][0] :
                    if str(ABPerson[j][2]) == str(None) :
                        name = ABPerson[j][1]
                    else :
                        name = str(ABPerson[j][2]) + str(ABPerson[j][1])
                    value = [name, ABMultiValue[i][1]]
                    print(value)
                    addressbook.append(value)
        conn.close()
    except :
        print("Something Wrong.")

def installed_application() :
    try : # Install Application Artifact
        installed_application_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/FrontBoard")) + "\\applicationState.db")
        
        conn = sqlite3.connect(installed_application_location)
        cur_application_identifier_tab = conn.cursor()
        cur_application_identifier_tab.execute("SELECT id, application_identifier FROM application_identifier_tab")
        application_identifier_tab = cur_application_identifier_tab.fetchall()

        installed_application = []
        for i in range(len(application_identifier_tab)) :
            installed_application.append(application_identifier_tab[i][1])
            print(application_identifier_tab[i][1])
    except :
        print("Something Wrong.")