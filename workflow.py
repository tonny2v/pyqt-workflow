#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: add keyPressEvent that auto execute when press enter key
# TODO: add "add a new command and save to the json by default"
# TODO: load json from remote file
# TODO: add a mission to system login
# TODO: set a schedule for a mission

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import json



class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            if len(self.listdata) != 0:
                return QtCore.QVariant(list(self.listdata)[index.row()])
        else:
            return QtCore.QVariant()

    def setAllData(self, newdata):
        """ replace all data with new data """
        self.beginResetModel()
        self.listdata = newdata
        self.resetInternalData()
        self.endResetModel()
        # import ipdb; ipdb.set_trace() #XXX BREAKPOINT

class MyWidget(QtWidgets.QWidget):
    # define a sigal
    on_executed = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MyWidget, self).__init__()
        # load workflow file
        self.workflow = json.load(open('workflow.json'))
        self.initGui()
        # declare what happens if the signal is invoked self.on_executed.connect(self.lbl.setText) def text_changed_handler(self):
        keys = [str(k) for k,v in self.workflow.items() if str(self.le.text()) in k]

    def text_changed_handler(self):
        keys = [str(k) for k,v in self.workflow.items() if str(self.le.text()) in k]
        print(keys)
        self.lm.setAllData(keys)
        self.lv.setCurrentIndex(self.lv.model().index(0,0))

    def lv_handler(self, s):
        print (s)

    def run(self):
        print(self.lv.selectionModel().selectedIndexes()[0].data())
        text = self.lv.selectionModel().selectedIndexes()[0].data()
        try:
            res = os.popen(self.workflow[str(text)])
            self.on_executed.emit('succeed! ' + res.readline())
        except:
            self.on_executed.emit('failed! ')

    def stop(self):
        pass

    def initGui(self):
        # widgets
        self.le = QtWidgets.QLineEdit("", self)
        self.le.textChanged[str].connect(self.text_changed_handler)
        self.lbl = QtWidgets.QLabel("result")
        self.lbl.setWordWrap(True)
        self.lv = QtWidgets.QListView(self)
        self.lm = MyListModel(self.workflow.keys(), self)
        self.lv.setModel(self.lm)

        runButton = QtWidgets.QPushButton("Run")
        stopButton = QtWidgets.QPushButton("Stop")
        runButton.clicked.connect(self.run)
        stopButton.clicked.connect(self.stop)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.le)
        hbox.addWidget(runButton)
        hbox.addWidget(stopButton)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.lv)
        vbox.addWidget(self.lbl)
        # vbox.addStretch(1)
        self.setLayout(vbox)

class MyMainWindow(QtWidgets.QMainWindow):

    def __init__(self, widget):
        """docstring for __init__"""
        super(MyMainWindow, self).__init__()
        self.widget = widget
        self.initGui()

    def initGui(self):
        """docstring for iniGui"""
        self.setCentralWidget(self.widget)
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('Tools')
        self.show()
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    win = MyMainWindow(widget)
    sys.exit(app.exec_())
