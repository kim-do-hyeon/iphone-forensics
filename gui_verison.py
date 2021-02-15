import os
import sys
import pathlib
import sqlite3
import datetime
import src.util
import gui.plugin
import gui.auto_db
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

ui = uic.loadUiType('gui/main.ui')[0] # Call ui file

def log(message): # LOG
            message = src.util.timestamp() + ' > ' + message
            print(message, file=log_file)

log_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '.txt'
log_file = open(log_name, 'w', -1, 'utf-8')
log("Start")

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

        # Button - Artifacts Analyze Button
        self.analyze_btn.clicked.connect(self.auto_analyze)

        # Button - iPhone Information Buttons
        self.iphone_information_btn.clicked.connect(self.iphone_information)
        self.backup_information_btn.clicked.connect(self.backup_information)

        # Button - Artifacts
        self.sms_btn.clicked.connect(self.sms)
        self.addressbook_btn.clicked.connect(self.addressbook)
        self.wallet_pass_btn.clicked.connect(self.wallet_pass)
        self.appleaccount_btn.clicked.connect(self.apple_accounts)
        self.calendar_btn.clicked.connect(self.calendar)
        self.bluetooth_btn.clicked.connect(self.bluetooth)
        self.bluetooth_all_btn.clicked.connect(self.bluetooth_all)
        self.simcard_btn.clicked.connect(self.simcard)
        self.application_btn.clicked.connect(self.application)
        self.tcc_btn.clicked.connect(self.tcc)

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
        log("Folder Path > " + str(folder_path))

    def auto_path_select(self) :
        appdata_path = os.getenv('APPDATA')
        backup_file_path = os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup"
        backup_file_list = os.listdir(backup_file_path)
        backup_file_location = str(backup_file_path) + "\\" + backup_file_list[0]
        self.folder_path_line.setText(backup_file_location)
        self.folder_path_global(backup_file_location) # Global Variable Settings
        log("Folder Path > " + str(folder_path))

    def db_path_select(self) :
        global db_path
        db_filter = 'DataBase File (*.db) ;; All files (*.*)'
        db_path = QFileDialog.getOpenFileName(self, 'Select DB', filter=db_filter)
        db_path = db_path[0]
        self.db_path_line.setText(db_path)
        log("DB Path > " + str(db_path))

    def extract_path_select(self) :
        global extract_path
        dialog = QFileDialog()
        extract_path = dialog.getExistingDirectory(None, "Select Folder")
        self.extract_path_line.setText(extract_path)
        log("Extract Path > " + str(extract_path))
        
    def folder_path_global(self, path) :
        global folder_path
        folder_path = str(path)
        self.requirement_file()

    def requirement_file(self) :
        global manifest_location
        global info_location
        manifest_location = str(folder_path) + "\\Manifest.plist"
        info_location = str(folder_path) + "\\Info.plist"
        log("Manifest Path > " + str(manifest_location))
        log("Info Path > " + str(info_location))
        
    # Extract
    def extract(self) :
        try :
            try :
                log("Extract Start")
                self.extract_backupfile(folder_path, extract_path)
                log("Extract Success")
            except :
                log("Extract Fail")
                QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
        except :
            log("Extract Fail")
            QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
        
    def extract_backupfile(self, backupfile_location, extract_location) :
        log_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '_error.txt'
        err_log_file = open(log_name, 'w', -1, 'utf-8')
        print("========== Extract ERROR LOG ==========", file = err_log_file)
        targetdir = backupfile_location
        Manifest_location = pathlib.Path(str(backupfile_location) + "\\Manifest.db")
        def filepath(target):
            folder = target[:2]
            return pathlib.Path(str(targetdir) + r"\\" + folder + r"\\" + target)

        conn = sqlite3.connect(Manifest_location)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Files")
        r = cur.fetchall()
        total_count = len(r)
        progressbar_count = 0
        progressbar_progress = 100 / total_count
        for i in range(total_count) :
            self.progressBar.setValue(round(progressbar_count))
            value = (src.util.printProgress(i, total_count, 'Progress:', 'Complete', 1, 50))
            target = r[i][0]
            if int(r[i][3]) == 1 :
                file_path = filepath(target)
                realativePath = pathlib.Path(r[i][2])
                file_new_name = realativePath.parts[-1]
                destination_path = r[i][1] + "/" + r[i][2]
                destination_path = list(pathlib.Path(destination_path).parts)
                destination_path.pop()
                destination_path = '/'.join(destination_path)
                if os.path.isdir(destination_path) : pass
                else :
                    try :
                        cwd = extract_location + "/extract_file/" + destination_path
                        cwd = pathlib.Path(cwd)
                        os.makedirs(cwd)
                    except : pass
                try :
                    destination_path = extract_location + "/extract_file/" + destination_path
                    destination_path = pathlib.Path(destination_path)
                    shutil.copyfile(file_path, os.path.join(destination_path, file_new_name))
                except :
                    print("Copy Fail > " + str(destination_path) + " > " + str(file_new_name), file = err_log_file)
                    pass
            progressbar_count += progressbar_progress
        print("\n")
        print("========== Success Extract Files ==========", file = err_log_file)
        conn.close()
        self.progressBar.setValue(100)

    def auto_analyze(self) :
        # Check DB File Exsit
        db = extract_path + '/analyze.db'
        if os.path.isfile(db) == True :
            log("DB File Exsits")
            reply = QMessageBox.question(self, 'DB Exists', 'The database file exists. Do you want it to be overwritten?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                log("DB File Exsits > N")
                return
            else : 
                log("DB File Exsits > Y > Remove DB File")
                os.remove(db)
        try :
            log("Auto Analyzing Start")
            gui.auto_db.auto(self, extract_path)
            log("Auto Analyzing End")
        except :
            log("Auto Analyzing Fail")
            QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

    # Information
    def iphone_information(self) :
        self.progressBar.setValue(0)
        try :
            gui.plugin.iphone_information(self, manifest_location, info_location)
            log("Information > iPhone Information > Success")
        except :
            log("Information > iPhone Information > Fail")
            QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)
    
    def backup_information(self) :
        self.progressBar.setValue(0)
        try :
            gui.plugin.backup_information(self, manifest_location, info_location)
            log("Information > backup Information > Success")
        except :
            log("Information > iPhone Information > Fail")
            QMessageBox.warning(self, 'Error', 'Something Wrong...', QMessageBox.Ok, QMessageBox.Ok)

    # Artifacts
    def sms(self):
        self.progressBar.setValue(0)
        try :
            gui.plugin.sms(self, db_path)
            log("Artifacts > SMS > Success")
        except :
            log("Artifacts > SMS > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)
        
    def addressbook(self):
        self.progressBar.setValue(0)
        try :
            gui.plugin.addressbook(self, db_path)
            log("Artifacts > AddressBook > Success")
        except :
            log("Artifacts > AddressBook > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)
    
    def wallet_pass(self):
        try :
            gui.plugin.wallet_pass(self, db_path)
            log("Artifacts > Wallet Pass > Success")
        except :
            log("Artifacts > Wallet Pass > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

    def apple_accounts(self):
        try :
            gui.plugin.apple_accounts(self, db_path)
            log("Artifacts > Apple Accounts > Success")
        except :
            log("Artifacts > Apple Accounts > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

    def calendar(self):
        try :
            gui.plugin.calendar(self, db_path)
            log("Artifacts > Calendar > Success")
        except :
            log("Artifacts > Calendar > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

    def bluetooth(self):
        try :
            gui.plugin.bluetooth(self, db_path)
            log("Artifacts > Bluetooth > Success")
        except :
            log("Artifacts > Bluetooth > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

    def bluetooth_all(self):
        try :
            gui.plugin.bluetooth_all(self, db_path)
            log("Artifacts > Bluetooth All > Success")
        except :
            log("Artifacts > Bluetooth All > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

    def simcard(self):
        try :
            gui.plugin.simcard(self, db_path)
            log("Artifacts > SIM Card > Success")
        except :
            log("Artifacts > SIM Card > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)
    
    def application(self):
        try :
            gui.plugin.application(self, db_path)
            log("Artifacts > Applicaton List > Success")
        except :
            log("Artifacts > Applicaton List > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)
    
    def tcc(self):
        try :
            gui.plugin.tcc(self, db_path)
            log("Artifacts > App Permission (TCC) > Success")
        except :
            log("Artifacts > App Permission (TCC) > Fail")
            QMessageBox.warning(self, 'Error', 'Please Select Database File!', QMessageBox.Ok, QMessageBox.Ok)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()