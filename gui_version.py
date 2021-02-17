import os
import sys
import pathlib
import sqlite3
import shutil
import datetime
import src.util
import gui.plugin
import gui.auto_db

from gui.requirement_except import ExceptWindow

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

        # Thread
        self.th_extract = ExtractThread(self)
        self.th_extract.evt_result_append.connect(self.th_extract_result_handler)
        self.th_extract.evt_result_bar_append.connect(self.th_extract_result_bar_handler)
        self.th_extract.evt_extract_finished.connect(self.th_extract_finish_handler)

    # Path Select 
    def folder_path_select(self) :
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.folder_path_line.setText(folder_path)
        self.folder_path_global(folder_path) # Global Variable Settings
        log("Folder Path > " + str(folder_path))

    def auto_path_select(self) :
        try :
            appdata_path = os.getenv('APPDATA')
            backup_file_path = os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup"
            backup_file_list = os.listdir(backup_file_path)
            backup_file_location = str(backup_file_path) + "\\" + backup_file_list[0]
            self.folder_path_line.setText(backup_file_location)
            self.folder_path_global(backup_file_location) # Global Variable Settings
            log("Auto Folder Path > " + str(folder_path))
        except :
            log("Auto Folder Path > FAIL")
            QMessageBox.warning(self, 'Error', 'Backup Folder Not Found.\nVerify that the files are in that folder', QMessageBox.Ok, QMessageBox.Ok)

    def db_path_select(self) :
        try :
            global db_path
            db_filter = 'DataBase File (*.db) ;; All files (*.*)'
            db_path = QFileDialog.getOpenFileName(self, 'Select DB', filter=db_filter)
            db_path = db_path[0]
            self.db_path_line.setText(db_path)
            log("DB Path > " + str(db_path))
        except :
            log("DB Path > FAIL")
            QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)

    def extract_path_select(self) :
        try :
            global extract_path
            dialog = QFileDialog()
            extract_path = dialog.getExistingDirectory(None, "Select Folder")
            self.extract_path_line.setText(extract_path)
            log("Extract Path > " + str(extract_path))
        except :
            log("Extract Path > FAIL")
            QMessageBox.warning(self, 'Error', 'Something Wrong\nVerify that the files are in that folder', QMessageBox.Ok, QMessageBox.Ok)
        
    def folder_path_global(self, path) :
        global folder_path
        folder_path = str(path)
        self.requirement_file()

    def requirement_file(self) :
        try :
            global manifest_location
            global info_location
            manifest_location = str(folder_path) + "\\Manifest.plist"
            info_location = str(folder_path) + "\\Info.plist"
            log("Manifest Path > " + str(manifest_location))
            log("Info Path > " + str(info_location))
        except :
            log("Manifest, Info File > FAIL")
            QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
    
    # Except Process
    def except_file(self) :
        self.except_process = ExceptWindow()
        self.except_process.except_manifest.connect(self.except_manifest_path)
        self.except_process.except_info.connect(self.except_info_path)

    def except_manifest_path(self, value) :
        global manifest_location
        manifest_location = value
        log("Except Manifest Path > " + str(manifest_location))

    def except_info_path(self, value) :
        global info_location
        info_location = value
        log("Except Info Path > " + str(info_location))
        
    # Extract
    def extract(self) :
        try :
            log("Extract Start")
            extract_exsit_path = extract_path + '/extract_file'
            if os.path.isdir(extract_exsit_path) == True :
                log("Extract Folder Exsits")
                reply = QMessageBox.question(self, 'Extract Folder Exists', 'The Extract folder exists. Do you want it to be overwritten?\nIt may take some time.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    log("Extract Folder Exsits > N")
                    return
                else : 
                    log("Extract Folder > Y > Remove Extract Folder")
                    shutil.rmtree(extract_exsit_path)
            try :
                self.processing_label.setText("Extract Start")
                self.set_enabled(False)
                self.th_extract.start()
                self.progressBar.setValue(100)
                self.processing_label.setText("Extract Success")
            except :
                log("Extract Fail")
                QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
        except :
            log("Extract Fail")
            QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
    
    # Thread Hanlder
    def th_extract_result_handler(self, message):
        self.processing_label.setText(message)
    
    def th_extract_result_bar_handler(self, count):
        self.progressBar.setValue(round(float(count)))

    def th_extract_finish_handler(self):
        self.set_enabled(True)
        log("Extract Success")
        QMessageBox.information(self, 'Finished', 'Extract finished!', QMessageBox.Ok, QMessageBox.Ok)

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

        db = os.getcwd() + '/analyze.db'
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
            reply = QMessageBox.question(self, 'Error', 'Perhaps Manifest.plist does not exist.\nDo you want to choose yourself?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                log("Except Select File > N")
                return
            else :
                log("Except Select File > Y")
                self.except_file()
    
    def backup_information(self) :
        self.progressBar.setValue(0)
        try :
            gui.plugin.backup_information(self, manifest_location, info_location)
            log("Information > backup Information > Success")
        except :
            log("Information > iPhone Information > Fail")
            reply = QMessageBox.question(self, 'Error', 'Perhaps Info.plist does not exist.\nDo you want to choose yourself?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                log("Except Select File > N")
                return
            else :
                log("Except Select File > Y")
                self.except_file()

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
        
    def set_enabled(self, enabled):
        self.folder_select_btn.setEnabled(enabled)
        self.auto_select_btn.setEnabled(enabled)
        self.extract_select_btn.setEnabled(enabled)
        self.extract_btn.setEnabled(enabled)
        self.db_path_select_btn.setEnabled(enabled)
        self.analyze_btn.setEnabled(enabled)
        self.iphone_information_btn.setEnabled(enabled)
        self.backup_information_btn.setEnabled(enabled)
        self.sms_btn.setEnabled(enabled)
        self.wallet_pass_btn.setEnabled(enabled)
        self.appleaccount_btn.setEnabled(enabled)
        self.addressbook_btn.setEnabled(enabled)
        self.calendar_btn.setEnabled(enabled)
        self.bluetooth_btn.setEnabled(enabled)
        self.bluetooth_all_btn.setEnabled(enabled)
        self.simcard_btn.setEnabled(enabled)
        self.application_btn.setEnabled(enabled)
        self.tcc_btn.setEnabled(enabled)

class ExtractThread(QThread):
    evt_result_append = pyqtSignal(str)
    evt_result_bar_append = pyqtSignal(str)
    evt_extract_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent

    def run(self) :
        log_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '_error.txt'
        err_log_file = open(log_name, 'w', -1, 'utf-8')
        print("========== Extract ERROR LOG ==========", file = err_log_file)
        targetdir = folder_path
        Manifest_location = pathlib.Path(str(folder_path) + "\\Manifest.db")
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
            value = src.util.printProgress_gui(i, total_count, 'Progress:', 'Complete', 1, 50)
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
                        cwd = extract_path + "/extract_file/" + destination_path
                        cwd = pathlib.Path(cwd)
                        os.makedirs(cwd)
                    except : pass
                try :
                    destination_path = extract_path + "/extract_file/" + destination_path
                    destination_path = pathlib.Path(destination_path)
                    shutil.copyfile(file_path, os.path.join(destination_path, file_new_name))
                except :
                    print("Copy Fail > " + str(destination_path) + " > " + str(file_new_name), file = err_log_file)
                    pass
            progressbar_count += progressbar_progress
            self.evt_result_append.emit(value)
            self.evt_result_bar_append.emit(str(progressbar_count))
        print("\n")
        print("========== Success Extract Files ==========", file = err_log_file)
        conn.close() 
        self.evt_extract_finished.emit()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()