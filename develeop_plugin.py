def addressbook_artifact():
    # Address Book Artifact
    # C:\Users\pental\Desktop\iphone-forensics\extract_file\HomeDomain\Library\AddressBook\AddressBook.sqlitedb
    import os
    import pathlib
    import sqlite3
    addressbook_path = pathlib.Path(os.getcwd() + "/extract_file/HomeDomain/Library/AddressBook")
    addressbook_location = pathlib.Path(str(addressbook_path) + "\\AddressBook.sqlitedb")
    conn = sqlite3.connect(addressbook_location)
    cur_ABPerson = conn.cursor()
    cur_ABPerson.execute("SELECT ROWID, First, Last FROM ABPerson")
    ABPerson = cur_ABPerson.fetchall()
    cur_ABMultiValue = conn.cursor()
    cur_ABMultiValue.execute("SELECT record_id, value FROM ABMultiValue")
    ABMultiValue = cur_ABMultiValue.fetchall()
    address = []
    for i in range(len(ABPerson)):
        for j in range(len(ABPerson)):
            if ABMultiValue[i][0] == ABPerson[j][0] :
                if str(ABPerson[j][2]) == str(None) :
                    name = ABPerson[j][1]
                else :
                    name = str(ABPerson[j][2]) + str(ABPerson[j][1])
                print([name, ABMultiValue[i][1]])
                address.append([name, ABMultiValue[i][1]])
    conn.close()

    # connect_analyze_database = sqlite3.connect("analyze.db")
    # cur_analyze_database = connect_analyze_database.cursor()
    # cur_analyze_database.execute("create table Address (Name text, value text)")

    # cur_analyze_database.executemany("insert into Address values (?, ?)", address)
    # connect_analyze_database.commit()

    # connect_analyze_database.close()