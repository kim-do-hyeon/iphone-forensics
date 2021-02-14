import os
import sys
import pathlib
import plistlib
import sqlite3
import gui.plugin
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

ui = uic.loadUiType('gui/main.ui')[0] # Call ui file

defualt_message = "* iPhone Forensics Tool * \n\
    \n Sourced By PENTAL \n \
    \n First, Mount the location of the iPhone backup file.\n\
    \n Second, press the analysis button to proceed with automatic analysis.\n\
    \n Third, enter the database file and proceed with artifact analysis."

class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('gui/icon.ico'))

        # File Management Buttons
        self.folder_select_btn.clicked.connect(self.folder_path_select)
        self.extract_select_btn.clicked.connect(self.extract_path_select)
        self.db_path_select_btn.clicked.connect(self.db_path_select)
        self.auto_select_btn.clicked.connect(self.auto_path_select)

        # Button - Extract Button
        self.extract_btn.clicked.connect(self.extract)

        # Button - iPhone Information Buttons
        self.iphone_information_btn.clicked.connect(self.iphone_information)
        self.backup_information_btn.clicked.connect(self.backup_information)

        # Button - Artifacts
        self.sms_btn.clicked.connect(self.sms)
        self.addressbook_btn.clicked.connect(self.addressbook)
        self.wallet_pass_btn.clicked.connect(self.wallet_pass)

        # Text Result
        self.txt_result.setText(defualt_message)

        # ProgrssBar Setting
        self.progressBar.setValue(0)

    # Path Select 
    def folder_path_select(self) :
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.folder_path_line.setText(folder_path)
        self.folder_path_global(folder_path) # Global Variable Settings

    def auto_path_select(self) :
        appdata_path = os.getenv('APPDATA')
        backup_file_path = os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup"
        backup_file_list = os.listdir(backup_file_path)
        backup_file_location = str(backup_file_path) + "\\" + backup_file_list[0]
        self.folder_path_line.setText(backup_file_location)
        self.folder_path_global(backup_file_location) # Global Variable Settings

    def db_path_select(self) :
        global db_path
        db_filter = 'DataBase File (*.db) ;; All files (*.*)'
        db_path = QFileDialog.getOpenFileName(self, 'Select DB', filter=db_filter)
        db_path = db_path[0]
        self.db_path_line.setText(db_path)

    def extract_path_select(self) :
        global extract_path
        dialog = QFileDialog()
        extract_path = dialog.getExistingDirectory(None, "Select Folder")
        self.extract_path_line.setText(extract_path)

    def folder_path_global(self, path) :
        global folder_path
        folder_path = str(path)
        self.requirement_file()

    def requirement_file(self) :
        global manifest_location
        global info_location
        manifest_location = str(folder_path) + "\\Manifest.plist"
        info_location = str(folder_path) + "\\Info.plist"

    # Extract
    def extract(self) :
        try :
            import gui.extract
            try :
                gui.extract.extract_backupfile(folder_path, extract_path)
            except :
                QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
        except :
            QMessageBox.warning(self, 'Error', 'File Error\ngui/extract.py does exsit?', QMessageBox.Ok, QMessageBox.Ok)
    
    # Information
    def iphone_information(self) :
        self.progressBar.setValue(0)
        try :
            gui.plugin.iphone_information(self, manifest_location, info_location)
        except :
            QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)
    
    def backup_information(self) :
        self.progressBar.setValue(0)
        try :
            gui.plugin.backup_information(self, manifest_location, info_location)
        except :
            QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

    # Artifacts
    def sms(self):
        self.progressBar.setValue(0)
        try :
            gui.plugin.sms(self, db_path)
        except :
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)
        
    def addressbook(self):
        self.progressBar.setValue(0)
        try :
            gui.plugin.addressbook(self, db_path)
        except :
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)
    
    def wallet_pass(self):
        try :
            gui.plugin.wallet_pass(self, db_path)
        except :
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()