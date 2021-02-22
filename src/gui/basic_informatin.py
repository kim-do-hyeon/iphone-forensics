from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import plistlib

def iphone_information(self, manifest_location, info_location):
    try :
        with open(manifest_location, 'rb') as fp :
            manifest = plistlib.loads(fp.read())
        with open(info_location, 'rb') as fp :
            info = plistlib.loads(fp.read())
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
        
        items = [["Device Name", str(device_name)],
        ["Display Name", display_name],
        ["Build Version", str(build_version)],
        ["GUID", str(GUID)],
        ["ICCID", str(ICCID)],
        ["IMEI", str(IMEI)],
        ["Last Backup Date", str(Last_Backup_Date)],
        ["Phone Number", str(phone_number)],
        ["Product Name", str(product_name)],
        ["Product Type", str(product_type)],
        ["Product Version", str(product_version)],
        ["Serial Number", str(serial_number)],
        ["Target Identifier", str(target_identifier)],
        ["Target Type", str(target_type)]]


        _translate = QCoreApplication.translate
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(14)
        for i in range(14):
            item = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        for i in range(2):
            item = QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        item = QTableWidgetItem()
        for i in range(14):
            for j in range(2):
                self.tableWidget.setItem(i, j, item)
                item = QTableWidgetItem()
        for i in range(14) :
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("iphone_forensics", str(i)))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("iphone_forensics", "Key"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("iphone_forensics", "Value"))
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
            
        for i in range(14):
            for j in range(2):
                item = self.tableWidget.item(i, j)
                item.setText(_translate("iphone_forensics", str(items[i][j])))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.progressBar.setValue(100)
    except :
        QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

def backup_information(self, manifest_location, info_location) :
    try :
        with open(manifest_location, 'rb') as fp :
            manifest = plistlib.loads(fp.read())
        with open(info_location, 'rb') as fp :
            info = plistlib.loads(fp.read())
        isencrypted = manifest["IsEncrypted"]
        backup_version = manifest["Version"]
        backup_date = manifest["Date"]
        backup_system_domains_version = manifest["SystemDomainsVersion"]
        backup_iphone_password_exsit = manifest["WasPasscodeSet"]
        items = [["IsEncrypted", isencrypted],
        ["Backup Version", backup_version],
        ["Backup Date", backup_date],
        ["Backup System Domains Version", backup_system_domains_version],
        ["Backup iPhone Password Exsit", backup_iphone_password_exsit]]

        _translate = QCoreApplication.translate
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(5)
        for i in range(5):
            item = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        for i in range(2):
            item = QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
        item = QTableWidgetItem()
        for i in range(5):
            for j in range(2):
                self.tableWidget.setItem(i, j, item)
                item = QTableWidgetItem()
        for i in range(5) :
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("iphone_forensics", str(i)))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("iphone_forensics", "Key"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("iphone_forensics", "Value"))
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
            
        for i in range(5):
            for j in range(2):
                item = self.tableWidget.item(i, j)
                item.setText(_translate("iphone_forensics", str(items[i][j])))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.progressBar.setValue(100)
    except :
        QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)