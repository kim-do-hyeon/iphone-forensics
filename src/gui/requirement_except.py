from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

ui = uic.loadUiType('src/gui/requirement_except.ui')[0] # Call ui file

class ExceptWindow(QDialog, ui):
    except_manifest = QtCore.pyqtSignal(str)
    except_info = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('src/gui/icon.ico'))
        self.show()

        # File Management Buttons
        self.manifest_select_btn.clicked.connect(self.manifest_select)
        self.info_select_btn.clicked.connect(self.info_select)
        self.return_btn.clicked.connect(self.return_select)

    def manifest_select(self) :
        try :
            global manifest_path
            file_filter = 'Plist File (*.plist) ;; All files (*.*)'
            manifest_path = QFileDialog.getOpenFileName(self, 'Select Manifest File', filter=file_filter)
            manifest_path = manifest_path[0]
            self.manifest_path_line.setText(manifest_path)
            self.except_manifest.emit(manifest_path)
        except :
            QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)
        
    def info_select(self) :
        try :
            global info_path
            file_filter = 'Plist File (*.plist) ;; All files (*.*)'
            info_path = QFileDialog.getOpenFileName(self, 'Select Info File', filter=file_filter)
            info_path = info_path[0]
            self.info_path_line.setText(info_path)
            self.except_info.emit(info_path)
        except :
            QMessageBox.warning(self, 'Error', 'Something Wrong', QMessageBox.Ok, QMessageBox.Ok)

    def return_select(self) :
        self.close()