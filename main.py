#!/usr/bin/env python3

from ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

class MainDialog(QMainWindow):
        def __init__(self, parent=None):
            super(MainDialog, self).__init__()

            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.wireupUi()

            self.main_file = ""
            self.item_file = ""
            self.template_file = ""
            self.output_dir = ""

        def wireupUi(self):
            self.ui.errorBox.hide()
            self.ui.mainSelectButton.clicked.connect(self.selectMainFile)
            self.ui.itemSelectButton.clicked.connect(self.selectItemFile)
            self.ui.templateSelectButton.clicked.connect(self.selectTemplate)
            self.ui.saveSelectButton.clicked.connect(self.selectOutputDir)

        def selectMainFile(self):
            sender = self.sender()
            main_file = self.openFile("Select a main file")
            if main_file:
                self.main_file = main_file
            self.ui.mainSelectText.setText(self.main_file)

        def selectItemFile(self):
            sender = self.sender()
            item_file = self.openFile("Select an item file")
            if item_file:
                self.item_file = item_file
            self.ui.itemSelectText.setText(self.item_file)

        def selectTemplate(self):
            sender = self.sender()
            template = QFileDialog.getOpenFileName(self, "Select a template file", "", "HTML Files (*.html);;All Files (*)")[0]
            if template:
                self.template_dir = template
            self.ui.templateSelectText.setText(self.template_dir)

        def selectOutputDir(self):
            sender = self.sender()
            output = self.openDirectory("Select an output folder")
            if output:
                self.output_file = output
            self.ui.saveSelectText.setText(self.output_file)

        def openFile(self, reason):
            return QFileDialog.getOpenFileName(self, reason, "", "CSV Files (*.csv);;All Files (*)")[0]

        def openDirectory(self, reason):
            return QFileDialog.getExistingDirectory(self, reason, "", options=QFileDialog.ShowDirsOnly)

if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = MainDialog()
        win.show()
        sys.exit(app.exec_())
