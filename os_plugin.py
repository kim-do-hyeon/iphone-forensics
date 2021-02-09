import os
import pathlib
import sqlite3
import plistlib
import util

# def apple_note():

#     # Apple Note Artifact
#     # C:\Users\pental\Desktop\iphone-forensics\extract_file\AppDomainGroup-group.com.apple.notes\NoteStore.sqlite

#     apple_note_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/AppDomainGroup-group.com.apple.notes")) + "\\NoteStore.sqlite")
    
#     conn = sqlite3.connect(apple_note_location)
#     cur_calendaritem = conn.cursor()
#     cur_calendaritem.execute("SELECT summary, start_date, end_date FROM CalendarItem")
#     calendaritem = cur_calendaritem.fetchall()
#     calendar = []

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

    print("========== PRINT_TYPE ==========")
    print("'USERNAME' , 'IDENTIFIER', 'DATE', 'ACCOUNT_DESCRIPTION', 'ACCOUNT_TYPE', 'ACCOUNT_TYPE_DESCRIPTION', 'CREDENTIAL_TYPE'")
    print("================================")
    
    for i in range(len(apple_account)) :
        apple_account[i][2] = util.cocoa_date_to_human_date(apple_account[i][2])
        print(apple_account[i])