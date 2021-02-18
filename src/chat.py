import os
import pathlib
import plistlib
import sqlite3
import src.util

def sms():
    try :
        # SMS Artifact
        # C:\Users\pental\Desktop\iphone-forensics\extract_file\HomeDomain\Library\SMS\sms.db

        sms_location = pathlib.Path(str(pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/SMS")) + "\\sms.db")
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
                    message_list.append([Phone_Number, Message, Date, Read_Date, Delivered_Date])
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

        print("\n========== PRINT_TYPE ==========")
        print("'Phone Number' , 'Message', 'Message_Type', 'Date', 'Read_Date', 'Delivered_Date'")
        print("================================\n")

        for i in message_list :
            print(i)
    except :
        print("Something Wrong. SMS Artifact does not work. Please retry")