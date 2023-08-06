# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ppepiot/src/hgview/hgviewlib/qt4/fileviewer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(481, 438)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 33, 481, 405))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tableView_revisions = RevisionsTableView(self.splitter)
        self.tableView_revisions.setAlternatingRowColors(True)
        self.tableView_revisions.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_revisions.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_revisions.setShowGrid(False)
        self.tableView_revisions.setGridStyle(QtCore.Qt.NoPen)
        self.tableView_revisions.setObjectName(_fromUtf8("tableView_revisions"))
        self.textView = HgFileView(self.splitter)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar_edit = QtGui.QToolBar(MainWindow)
        self.toolBar_edit.setGeometry(QtCore.QRect(0, 0, 481, 33))
        self.toolBar_edit.setObjectName(_fromUtf8("toolBar_edit"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_edit)
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionReload = QtGui.QAction(MainWindow)
        self.actionReload.setObjectName(_fromUtf8("actionReload"))
        self.toolBar_edit.addAction(self.actionReload)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "hgview filelog", None))
        self.toolBar_edit.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionReload.setText(_translate("MainWindow", "Reload", None))
        self.actionReload.setShortcut(_translate("MainWindow", "Ctrl+R", None))

from hgfileview import HgFileView
from revisions_table import RevisionsTableView
