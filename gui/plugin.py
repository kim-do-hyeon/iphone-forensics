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
def iphone_information(self, manifest_location, info_location):
    try :
        manifest = plistlib.readPlist(manifest_location)
        info = plistlib.readPlist(info_location)
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
        items = "\n==== iPhone Information ====\n\n" + "Device Name : " + device_name + "\n" + "Display Name : " + display_name + "\n" + "Build Version : \
            " + build_version + "\n"+ "GUID : " + GUID + "\n" + "ICCID : " + ICCID + " \n" + "IMEI : \
            " + IMEI + "\n" + "Last Backup Date : " + str(Last_Backup_Date)+ "\n" + "Phone Number : \
            " + phone_number + "\n" + "Product Type : " + product_type + "\n" + "Product Type : \
            " + product_type + "\n" + "Serial Number : " + serial_number + "\n" + "Target Identifier : \
            " + target_identifier + "\n" + "Targey Type : " + target_type
        self.txt_result.setText(items)
        self.progressBar.setValue(100)
    except :
        QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

def backup_information(self, manifest_location, info_location) :
    try :
        manifest = plistlib.readPlist(manifest_location)
        info = plistlib.readPlist(info_location)
        isencrypted = manifest["IsEncrypted"]
        backup_version = manifest["Version"]
        backup_date = manifest["Date"]
        backup_system_domains_version = manifest["SystemDomainsVersion"]
        backup_iphone_password_exsit = manifest["WasPasscodeSet"]
        items = "\n==== Backup Information ====\n\n" +" IsEncrypted : " + str(isencrypted) + "\n" + "Version : \
            " + backup_version + "\n" + "Backup Date : \
            " + str(backup_date) + "\n" + "Backup System Domains Version : \
            " + str(backup_system_domains_version) + "\n" + "Backup iPhone Password Exsit : \
            " + str(backup_iphone_password_exsit)
        self.txt_result.setText(items)
        self.progressBar.setValue(100)
    except :
        QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

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