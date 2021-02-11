import plistlib
import src.util

def iphone_information(manifest, info) :
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
    print("\n========== IPHONE INFORMATIONS ==========")
    print("Device Name : ", device_name)
    print("Display Name : ", display_name)
    print("Build Version : ", build_version)
    print("GUID : ", GUID)
    print("ICCID : ", ICCID)
    print("IMEI : ", IMEI)
    print("Last Backup Date : ", Last_Backup_Date)
    print("Phone Number : ", phone_number)
    print("Product Name : ", product_name)
    print("Product Type : ", product_type)
    print("Product Version : ", product_version)
    print("Serial Number : ", serial_number)
    print("Target Identifier : ", target_identifier)
    print("Target Type : ", target_type)
    print("========================================\n")

def iphone_backup_information(manifest, info) :
    manifest = plistlib.readPlist(manifest)
    info = plistlib.readPlist(info)
    isencrypted = manifest["IsEncrypted"]
    backup_version = manifest["Version"]
    backup_date = manifest["Date"]
    backup_system_domains_version = manifest["SystemDomainsVersion"]
    backup_iphone_password_exsit = manifest["WasPasscodeSet"]
    print("\n========== IPHONE BACKUP FILE INFOMRATIONS ==========")
    print("Backupfile encrypted? : ", isencrypted)
    print("Backup Version (iTunes) : ", backup_version)
    print("Backup Date : ", backup_date)
    print("Backup System Domains Version : ", backup_system_domains_version)
    print("Iphone Password Exsit? : ", backup_iphone_password_exsit)
    print("====================================================\n")

def iphone_accessibility_information(manifest, info) :
    manifest = plistlib.readPlist(manifest)
    info = plistlib.readPlist(info)
    mono_audio = manifest["Lockdown"]["com.apple.Accessibility"]["MonoAudioEnabledByiTunes"]
    voice_over_touch = manifest["Lockdown"]["com.apple.Accessibility"]["VoiceOverTouchEnabledByiTunes"]
    closed_captioning = manifest["Lockdown"]["com.apple.Accessibility"]["ClosedCaptioningEnabledByiTunes"]
    speak_auto_corrections = manifest["Lockdown"]["com.apple.Accessibility"]["SpeakAutoCorrectionsEnabledByiTunes"]
    invert_display = manifest["Lockdown"]["com.apple.Accessibility"]["InvertDisplayEnabledByiTunes"]
    zoom_touch = manifest["Lockdown"]["com.apple.Accessibility"]["ZoomTouchEnabledByiTunes"]
    print("\n========== IPHONE ACCESSIBILITY INFORMATIONS ==========")
    print("MonoAudio Enabled : ", mono_audio)
    print("VoiceOverTouch Enabled : ", voice_over_touch)
    print("ClosedCaptioning Enabled : ", closed_captioning)
    print("SpeakAutoCorrections Enabled : ", speak_auto_corrections)
    print("InvertDisplay Enabled : ", invert_display)
    print("ZoomTouch Enabled : ", zoom_touch)
    print("======================================================\n")

def installed_Application(manifest, info) :
    manifest = plistlib.readPlist(manifest)
    info = plistlib.readPlist(info)
    installed_application_list = info["Installed Applications"]
    installed_application_count = 0
    for key in installed_application_list :
        installed_application_count += 1
    print("\n========== INSTALLED APPLICATION INFORMATIONS ==========")
    print("Installed Applications Count : ", installed_application_count)
    for key in installed_application_list :
        print(key)
    print("========================================================\n")