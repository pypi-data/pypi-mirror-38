# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ppepiot/src/hgview/hgviewlib/qt4/filediffviewer.ui'
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
        MainWindow.resize(620, 546)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 33, 620, 513))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableView_revisions_left = RevisionsTableView(self.layoutWidget)
        self.tableView_revisions_left.setAlternatingRowColors(True)
        self.tableView_revisions_left.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_revisions_left.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_revisions_left.setShowGrid(False)
        self.tableView_revisions_left.setObjectName(_fromUtf8("tableView_revisions_left"))
        self.horizontalLayout.addWidget(self.tableView_revisions_left)
        self.tableView_revisions_right = RevisionsTableView(self.layoutWidget)
        self.tableView_revisions_right.setAlternatingRowColors(True)
        self.tableView_revisions_right.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_revisions_right.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_revisions_right.setShowGrid(False)
        self.tableView_revisions_right.setObjectName(_fromUtf8("tableView_revisions_right"))
        self.horizontalLayout.addWidget(self.tableView_revisions_right)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtGui.QFrame(self.layoutWidget1)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setGeometry(QtCore.QRect(0, 0, 121, 33))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.toolBar_edit = QtGui.QToolBar(MainWindow)
        self.toolBar_edit.setGeometry(QtCore.QRect(121, 0, 499, 33))
        self.toolBar_edit.setObjectName(_fromUtf8("toolBar_edit"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_edit)
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionReload = QtGui.QAction(MainWindow)
        self.actionReload.setObjectName(_fromUtf8("actionReload"))
        self.toolBar.addAction(self.actionReload)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tableView_revisions_left, self.tableView_revisions_right)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "hgview diff", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBar_edit.setWindowTitle(_translate("MainWindow", "toolBar_2", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionReload.setText(_translate("MainWindow", "Reload", None))
        self.actionReload.setShortcut(_translate("MainWindow", "Ctrl+R", None))

from revisions_table import RevisionsTableView
