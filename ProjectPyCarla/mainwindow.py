# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QSystemTrayIcon, QMenu, QPushButton
from PySide6.QtCore import QFile, Slot, Signal, QObject, QThreadPool
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction, QIcon, QTextCursor
from PySide6.QtDesigner import QDesignerFormWindowCursorInterface

import PySide6.QtCore as QtCore

import speech_recognition
import pyttsx3

from CarlaListener import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.carlaThread = QThreadPool()

#load ui#
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)
    #_load ui_#

#Bindings#
        self.ui.pushButton.released.connect(self.pushButtonReleased)

    #_Bindings_#

#Minimize to tray#
        self.closing = False

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.initClose)

        trayIconMenu = QMenu(self)
        trayIconMenu.addAction(exitAction)

        sysTrayIcon = QSystemTrayIcon(self)
        sysTrayIcon.setContextMenu(trayIconMenu)
        sysTrayIcon.setIcon(QIcon("ai.ico"))
        sysTrayIcon.show()
        sysTrayIcon.activated.connect(self.trayIconClicked)

    def initClose(self):
        self.closing = True
        self.close()

    def trayIconClicked(self, reason):
        if (reason == QSystemTrayIcon.Trigger):
            if(self.isVisible()):
                self.hide()
            else:
                self.show()
                self.activateWindow()

    def closeEvent(self, event):
        if(self.closing):
            event.accept()
        else:
            self.hide()
            event.ignore()
    #_Minimize to tray_#

#Slots#
    def handleProcess(self, processID):
        if processID == 1:
            self.ui.pushButton.setText("Listening...")
            self.ui.pushButton.setEnabled(0)
        elif processID == 2:
            self.ui.pushButton.setText("Ready")
            self.ui.pushButton.setEnabled(1)
        elif processID == 3:
            self.appendTextToTextEdit("Some error occured")
            self.ui.pushButton.setText("Ready")
            self.ui.pushButton.setEnabled(1)
        elif processID == 4:
            self.pushButtonReleased()

    def updateGUI(self, text):
        self.appendTextToTextEdit(text)

    def pushButtonReleased(self):
        self.carlaListener = CarlaListener()
        self.carlaListener.signals.result.connect(self.updateGUI)
        self.carlaListener.signals.process.connect(self.handleProcess)
        self.carlaThread.start(self.carlaListener)
        print("Max Thread count: %d\n Active Thread count: %d" % (self.carlaThread.maxThreadCount(), self.carlaThread.activeThreadCount()))

    #_Slots_#

    def appendTextToTextEdit(self, text):
        self.ui.textEdit.moveCursor(QTextCursor.End);
        self.ui.textEdit.insertPlainText(text);
        self.ui.textEdit.insertPlainText("\n");
        self.ui.textEdit.moveCursor(QTextCursor.End);


class MyClass():
    def __init__(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
