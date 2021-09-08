#!/usr/bin/env python3

from ui import Ui_MainWindow
from renderer import TemplateRenderer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import re
import os.path as path

class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.wireupUi()

        self.main_file = ""
        self.item_file = ""
        self.item_name = ""
        self.template_file = ""
        self.output_dir = ""

    def wireupUi(self):
        self.ui.errorBox.hide()
        self.ui.mainSelectButton.clicked.connect(self.selectMainFile)
        self.ui.itemSelectButton.clicked.connect(self.selectItemFile)
        self.ui.itemName.textChanged.connect(self.updateItemName)
        self.ui.templateSelectButton.clicked.connect(self.selectTemplate)
        self.ui.saveSelectButton.clicked.connect(self.selectOutputDir)
        self.ui.runButton.clicked.connect(self.runRender)
        self.ui.runButton.setEnabled(True) # TODO: Replace with handling of filled fields

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
            self.item_name = path.splitext(path.basename(self.item_file))[0]
            self.ui.itemName.setEnabled(True)
            self.ui.itemName.setText(self.item_name)
            self.ui.itemSelectText.setText(self.item_file)

    def selectTemplate(self):
        sender = self.sender()
        template = QFileDialog.getOpenFileName(self, "Select a template file", "", "HTML Files (*.html);;All Files (*)")[0]
        if template:
            self.template_file = template
            self.ui.templateSelectText.setText(self.template_file)

    def selectOutputDir(self):
        sender = self.sender()
        output = self.openDirectory("Select an output folder")
        if output:
            self.output_dir = output
            self.ui.saveSelectText.setText(self.output_dir)

    def updateItemName(self, text):
        print("Changed", text)
        self.item_name = text

    def openFile(self, reason):
        return QFileDialog.getOpenFileName(self, reason, "", "CSV Files (*.csv);;All Files (*)")[0]

    def openDirectory(self, reason):
        return QFileDialog.getExistingDirectory(self, reason, "", options=QFileDialog.ShowDirsOnly)

    def runRender(self):
        self.ui.runButton.setEnabled(False)
        try:
            with open(self.template_file, 'r', errors='replace', encoding='utf-8') as f:
                template = f.read()
            main_data = open(self.main_file, 'r', errors='replace', encoding='utf-8')
            item_data = open(self.item_file, 'r', errors='replace', encoding='utf-8')
            self.renderer = TemplateRenderer(template, main_data, {self.item_name : item_data})
            out_files = self.renderer.render()
            main_data.close()
            item_data.close()

            for filename, contents in out_files.items():
                filename = re.sub(r'[\<\>\:\"\/\\\|\?\*\.]', '_', filename.encode('ascii', 'ignore').decode('ascii'))
                filename = re.sub(r'^\s+|\s+$', '', filename)
                with open(self.output_dir + '/' + filename + '.html', 'w', encoding='utf-8') as f:
                    f.write(contents)
        except Exception as e:
            self.appendMessage(e.__str__(), True)
        self.ui.runButton.setEnabled(True)

    def appendMessage(self, message: str, is_error=False):
        self.ui.errorBox.setText(message)
        self.ui.errorBox.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainDialog()
    win.show()
    sys.exit(app.exec_())
