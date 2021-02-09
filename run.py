import os
import pathlib
import src.init_plugin
import src.mobile_plugin
import src.os_plugin

print("    ____      __                        ___                __                     ")
print("   /  _/___  / /_  ____  ____  ___     /   |  ____  ____ _/ /_  ______  ___  _____")
print("   / // __ \/ __ \/ __ \/ __ \/ _ \   / /| | / __ \/ __ `/ / / / /_  / / _ \/ ___/")
print(" _/ // /_/ / / / / /_/ / / / /  __/  / ___ |/ / / / /_/ / / /_/ / / /_/  __/ /    ")
print("/___/ .___/_/ /_/\____/_/ /_/\___/  /_/  |_/_/ /_/\__,_/_/\__, / /___/\___/_/     ")
print("   /_/                                                   /____/                   ")
print("                                                                                  ")

# Get iPhone Backup File Path (%appdata%\Roaming\Apple Computer\MobileSynce\Backup)
try :
    appdata_path = os.getenv('APPDATA')
    backup_file_path = pathlib.Path(os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup")
    backup_file_list = os.listdir(backup_file_path)

    print("\nList of backup files currently stored on your computer.\nWhen you select a backup file, the file is automatically extracted.")

    # Backup File List
    for i in range(len(backup_file_list)) :
        print("[{0}] : ".format(i), backup_file_list[i])

except :
    print("The backup file could not be found. Does it exist in a different location?")
    quit()

temp = int(input("Selected Number : "))

if temp == "" :
    print("Something Wrong. Please Retry")
    quit()
elif temp > len(backup_file_list) :
    print("Out of range. Please Retry")
    quit()
else :
    print("\n============================================================")
    # Selected Backup File Path
    print("Selected Backup File : ", backup_file_list[temp])
    backup_file_location = pathlib.Path(str(backup_file_path) + "/" + backup_file_list[temp])
    print("Backup File Path : ", backup_file_location)

    # Selected Manifest & info plist
    backup_file_manifest = str(backup_file_location) + "/Manifest.plist"
    backup_file_info = str(backup_file_location) + "/info.plist"

    print("Manifest : ", backup_file_manifest)
    print("Info : ", backup_file_info)
    print("============================================================\n")

while True :
    print("\n========== Select Options ==========\n")
    print("1. iPhone Information \n")
    print("2. iPhone Backup File Information \n")
    print("3. iPhone Accessibility Information \n")
    print("4. Installed Application Information \n")
    print("5. Extract File (iPhone Backup File)\n")
    print("9. Artifacts\n")
    print("0. Exit \n")

    num = int(input("Number : "))

    # Call Plugins
    if num == 1 :
        src.init_plugin.iphone_information(backup_file_manifest, backup_file_info)
    elif num == 2 :
        src.init_plugin.iphone_backup_information(backup_file_manifest, backup_file_info)
    elif num == 3 :
        src.init_plugin.iphone_accessibility_information(backup_file_manifest, backup_file_info)
    elif num == 4 :     
        src.init_plugin.installed_Application(backup_file_manifest, backup_file_info)
    elif num == 5 :
        src.init_plugin.extract_backupfile(backup_file_location)
    elif num == 9 :
        print("\nThis can only be used if extracted using this tool!!\n")
        print("0. Owner Information\n")
        print("1. AddressBook\n")
        print("2. Calendar Event\n")
        print("3. Installed Application\n")
        print("4. Apple Accounts\n")
        print("5. Sim Card Information\n")
        print("6. Bluetooth Device\n")
        print("\t 6.1 Bluetooth That Have Been Shown\n")
        artifacts = float(input("Number : "))
        
        if artifacts == 0 :
            src.mobile_plugin.owner_infomation_artifact()
        elif artifacts == 1 :
            src.mobile_plugin.addressbook_artifact()
        elif artifacts == 2 :
            src.mobile_plugin.calendar_event_artifact()
        elif artifacts == 3 :
            src.mobile_plugin.installed_application()
        elif artifacts == 4 :
            src.os_plugin.apple_accounts()
        elif artifacts == 5 :
            src.os_plugin.sim_card()
        elif artifacts == 6 :
            src.os_plugin.bluetooth()
        elif artifacts == 6.1 :
            src.os_plugin.bluetooth_that_have_been_shown()
        else : 
            print("\nError, Wrong Number. Please Check Your Number.\n")
            break
    elif num == 0 :
        print("Bye!")
        break
    else :
        print("\nError, Wrong Number. Please Check Your Number.\n")
        break