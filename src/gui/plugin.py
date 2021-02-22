import os
import pathlib
import plistlib
import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

# iPhone Information
# def iphone_information(self, manifest_location, info_location):
#     # try :
#     with open(manifest_location, 'rb') as fp :
#         manifest = plistlib.loads(fp.read())
#     with open(info_location, 'rb') as fp :
#         info = plistlib.loads(fp.read())
#     device_name = info["Device Name"]
#     display_name = info["Display Name"]
#     build_version = info["Build Version"]
#     GUID = info["GUID"]
#     ICCID = info["ICCID"]
#     IMEI = info["IMEI"]
#     Last_Backup_Date = info["Last Backup Date"]
#     phone_number = info["Phone Number"]
#     product_name = info["Product Name"]
#     product_type = info["Product Type"]
#     product_version = info["Product Version"]
#     serial_number = info["Serial Number"]
#     target_identifier = info["Target Identifier"]
#     target_type = info["Target Type"]
#     items = "\n==== iPhone Information ====\n\n" + "Device Name : " + device_name + "\n" + "Display Name : " + display_name + "\n" + "Build Version : \
#         " + build_version + "\n"+ "GUID : " + GUID + "\n" + "ICCID : " + ICCID + " \n" + "IMEI : \
#         " + IMEI + "\n" + "Last Backup Date : " + str(Last_Backup_Date)+ "\n" + "Phone Number : \
#         " + phone_number + "\n" + "Product Type : " + product_type + "\n" + "Product Type : \
#         " + product_type + "\n" + "Serial Number : " + serial_number + "\n" + "Target Identifier : \
#         " + target_identifier + "\n" + "Targey Type : " + target_type
#     self.txt_result.setText(items)
#     self.progressBar.setValue(100)
#     # except :
#     #     QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

# def backup_information(self, manifest_location, info_location) :
#     # try :
#     with open(manifest_location, 'rb') as fp :
#         manifest = plistlib.loads(fp.read())
#     with open(info_location, 'rb') as fp :
#         info = plistlib.loads(fp.read())
#     isencrypted = manifest["IsEncrypted"]
#     backup_version = manifest["Version"]
#     backup_date = manifest["Date"]
#     backup_system_domains_version = manifest["SystemDomainsVersion"]
#     backup_iphone_password_exsit = manifest["WasPasscodeSet"]
#     items = "\n==== Backup Information ====\n\n" +" IsEncrypted : " + str(isencrypted) + "\n" + "Version : \
#         " + backup_version + "\n" + "Backup Date : \
#         " + str(backup_date) + "\n" + "Backup System Domains Version : \
#         " + str(backup_system_domains_version) + "\n" + "Backup iPhone Password Exsit : \
#         " + str(backup_iphone_password_exsit)
#     self.txt_result.setText(items)
#     self.progressBar.setValue(100)
#     # except :
#     #     QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

# SMS
def sms(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from sms')
            sms_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setRowCount(len(sms_list))
            for i in range(len(sms_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(6):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(sms_list)):
                for j in range(6):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(sms_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Phone Number"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Message"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("iphone_forensics", "Type"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("iphone_forensics", "Date"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("iphone_forensics", "Read Date"))
            item = self.tableWidget.horizontalHeaderItem(5)
            item.setText(_translate("iphone_forensics", "Delivered Date"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)

            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)
                
            for i in range(len(sms_list)):
                for j in range(6):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(sms_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def addressbook(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from addressbook')
            addressbook_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(addressbook_list))
            for i in range(len(addressbook_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(2):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(addressbook_list)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(addressbook_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Name"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Phone Number"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)

            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            for i in range(len(addressbook_list)):
                for j in range(2):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(addressbook_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def wallet_pass(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from wallet_pass')
            wallet_pass_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setRowCount(len(wallet_pass_list))
            for i in range(len(wallet_pass_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(5):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(wallet_pass_list)):
                for j in range(5):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(wallet_pass_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Organization Name"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Description"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("iphone_forensics", "Serial Number"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("iphone_forensics", "Card Owner Name"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("iphone_forensics", "Card Number"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(wallet_pass_list)):
                for j in range(5):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(wallet_pass_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def apple_accounts(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from AppleAccounts')
            apple_accounts_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setRowCount(len(apple_accounts_list))
            for i in range(len(apple_accounts_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(7):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(apple_accounts_list)):
                for j in range(7):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(apple_accounts_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "UserName"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Identifier"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("iphone_forensics", "Date"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("iphone_forensics", "Account Info"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("iphone_forensics", "Account Type"))
            item = self.tableWidget.horizontalHeaderItem(5)
            item.setText(_translate("iphone_forensics", "Account Type Info"))
            item = self.tableWidget.horizontalHeaderItem(6)
            item.setText(_translate("iphone_forensics", "Credential type"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(apple_accounts_list)):
                for j in range(7):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(apple_accounts_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def calendar(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from calendar')
            calendar_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(len(calendar_list))
            for i in range(len(calendar_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(3):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(calendar_list)):
                for j in range(3):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(calendar_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Item"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Start Date"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("iphone_forensics", "End Date"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(calendar_list)):
                for j in range(3):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(calendar_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def bluetooth(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from bluetooth')
            bluetooth_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setRowCount(len(bluetooth_list))
            for i in range(len(bluetooth_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(4):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(bluetooth_list)):
                for j in range(4):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(bluetooth_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "MAC"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Name"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("iphone_forensics", "Last Seen Time"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("iphone_forensics", "Default Name"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(bluetooth_list)):
                for j in range(4):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(bluetooth_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def simcard(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from simcards')
            simcard_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(simcard_list))
            for i in range(len(simcard_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(2):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(simcard_list)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(simcard_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Key"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Value"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(simcard_list)):
                for j in range(2):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(simcard_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def bluetooth_all(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from bluetooth_that_have_been_shown')
            bluetooth_all_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(len(bluetooth_all_list))
            for i in range(len(bluetooth_all_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(3):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(bluetooth_all_list)):
                for j in range(3):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(bluetooth_all_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "UUID"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Name"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("iphone_forensics", "Address"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(bluetooth_all_list)):
                for j in range(3):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(bluetooth_all_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def application(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from installed_application')
            application_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(application_list))
            for i in range(len(application_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(2):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(application_list)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(application_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Key"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Value"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(application_list)):
                for j in range(2):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(application_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def tcc(self, db_path) :
    try :
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try :
            cur.execute('select * from TCC')
            tcc_list = cur.fetchall()
            _translate = QCoreApplication.translate
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(tcc_list))
            for i in range(len(tcc_list)):
                item = QTableWidgetItem()
                self.tableWidget.setVerticalHeaderItem(i, item)
            for i in range(2):
                item = QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i, item)
            item = QTableWidgetItem()
            for i in range(len(tcc_list)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, item)
                    item = QTableWidgetItem()
            for i in range(len(tcc_list)) :
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("iphone_forensics", str(i)))
            
            # Column Width Auto Manage
            header = self.tableWidget.horizontalHeader()
            twidth = header.width()
            width = []
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                width.append(header.sectionSize(column))
            
            wfactor = twidth / sum(width)
            for column in range(header.count()):
                header.setSectionResizeMode(column, QHeaderView.Interactive)
                header.resizeSection(column, width[column]*wfactor)

            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("iphone_forensics", "Service"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("iphone_forensics", "Client"))
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            for i in range(len(tcc_list)):
                for j in range(2):
                    item = self.tableWidget.item(i, j)
                    item.setText(_translate("iphone_forensics", str(tcc_list[i][j])))
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            self.progressBar.setValue(100)
        except :
            QMessageBox.warning(self, 'Error', 'Database Error! \nIs It True Database?', QMessageBox.Ok, QMessageBox.Ok)
    except :
        QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)