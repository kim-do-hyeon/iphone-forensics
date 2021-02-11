import os
import pathlib
import src.init_plugin
import src.mobile_plugin
import src.os_plugin
import src.chat

print("    ____      __                        ___                __                     ")
print("   /  _/___  / /_  ____  ____  ___     /   |  ____  ____ _/ /_  ______  ___  _____")
print("   / // __ \/ __ \/ __ \/ __ \/ _ \   / /| | / __ \/ __ `/ / / / /_  / / _ \/ ___/")
print(" _/ // /_/ / / / / /_/ / / / /  __/  / ___ |/ / / / /_/ / / /_/ / / /_/  __/ /    ")
print("/___/ .___/_/ /_/\____/_/ /_/\___/  /_/  |_/_/ /_/\__,_/_/\__, / /___/\___/_/     ")
print("   /_/                                                   /____/                   ")
print("                                                                                  ")

log_file = open('log.txt', 'w', -1, 'utf-8')
def log(message):
    message = src.util.timestamp() + ' > ' + message
    print(message, file=log_file)
log("Start")

# Get iPhone Backup File Path (%appdata%\Roaming\Apple Computer\MobileSynce\Backup)
try :
    appdata_path = os.getenv('APPDATA')
    log("Appdata Path : " + str(appdata_path))
    backup_file_path = pathlib.Path(os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup")
    log("Backup File Path : " + str(backup_file_path))
    backup_file_list = os.listdir(backup_file_path)
    log("Backup File List : " + str(backup_file_list))

    print("\nList of backup files currently stored on your computer.\nWhen you select a backup file, the file is automatically extracted.")

    # Backup File List
    for i in range(len(backup_file_list)) :
        print("[{0}] : ".format(i), backup_file_list[i])

except :
    print("The backup file could not be found. Does it exist in a different location?")
    backup_file_path = str(input("Please enter the location of the backup file : "))
    backup_file_path = pathlib.Path(backup_file_path)
    log("Custom Backup File Path : " + str(backup_file_path))
    backup_file_list = os.listdir(backup_file_path)
    log("Custom Backup File List : ", + str(backup_file_list))
    
    for i in range(len(backup_file_list)) :
        print("[{0}] : ".format(i), backup_file_list[i])

temp = int(input("Selected Number : "))
log("Selected Number : " + str(temp))
if temp == "" :
    print("Something Wrong. Please Retry")
    log("Something Wrong. Please Retry")
    quit()
elif temp > len(backup_file_list) :
    print("Out of range. Please Retry")
    log("Out of range. Please Retry")
    quit()
else :
    print("\n============================================================")
    # Selected Backup File Path
    print("Selected Backup File : ", backup_file_list[temp])
    log("Selected Backup File : " + str(backup_file_list[temp]))
    backup_file_location = pathlib.Path(str(backup_file_path) + "/" + backup_file_list[temp])
    print("Backup File Path : ", backup_file_location)
    log("Selected Backup File Location : " + str(backup_file_location))

    # Selected Manifest & info plist
    backup_file_manifest = str(backup_file_location) + "/Manifest.plist"
    backup_file_info = str(backup_file_location) + "/info.plist"
    log("Manifest : " + str(backup_file_manifest))
    log("Info : " + str(backup_file_info))
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
    log("Selected Options : " + str(num))
    # Call Plugins
    if num == 1 :
        log("Selected iPhone Information")
        src.init_plugin.iphone_information(backup_file_manifest, backup_file_info)
    elif num == 2 :
        log("Selected iPhone Backup Information")
        src.init_plugin.iphone_backup_information(backup_file_manifest, backup_file_info)
    elif num == 3 :
        log("Selected iPhone Accessibility Information")
        src.init_plugin.iphone_accessibility_information(backup_file_manifest, backup_file_info)
    elif num == 4 :
        log("Selected Installed Application")
        src.init_plugin.installed_Application(backup_file_manifest, backup_file_info)
    elif num == 5 :
        log("Selected Extract Backup File")
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
        print("7. SMS List\n")
        
        artifacts = float(input("Number : "))
        log("Selected Artifacts : " + str(artifacts))
        if artifacts == 0 :
            log("Select Owner Information Artifact")
            src.mobile_plugin.owner_infomation_artifact()
        elif artifacts == 1 :
            log("Selected AddressBook Artifact")
            src.mobile_plugin.addressbook_artifact()
        elif artifacts == 2 :
            log("Selected Calendar Event Artifact")
            src.mobile_plugin.calendar_event_artifact()
        elif artifacts == 3 :
            log("Selected Installed Application Artifact")
            src.mobile_plugin.installed_application()
        elif artifacts == 4 :
            log("Selected Apple Accounts Artifact")
            src.os_plugin.apple_accounts()
        elif artifacts == 5 :
            log("Selected Sim Card Artifact")
            src.os_plugin.sim_card()
        elif artifacts == 6 :
            log("Selected Bluetooth Artifact")
            src.os_plugin.bluetooth()
        elif artifacts == 6.1 :
            log("Selected Bluetooth That Have Been Shown Artifact")
            src.os_plugin.bluetooth_that_have_been_shown()
        elif artifacts == 7 :
            log("Selected SMS Artifact")
            src.chat.sms()
        else :
            print("\nError, Wrong Number. Please Check Your Number.\n")
            log("Error, Wrong Number. Please Check Your Number.")
            break
    elif num == 0 :
        print("Bye!")
        log("Bye!")
        break
    else :
        print("\nError, Wrong Number. Please Check Your Number.\n")
        break