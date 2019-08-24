# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(429, 284)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(9, 9, 221, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(9, 48, 411, 231))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "关于"))
        self.label.setText(_translate("Dialog", "Fraction-Calc V1.0"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>这是一个可以生成各种分数练习题的软件，目前本软件已经开发完成，之后可能会添加新功能。</p><p>本软件使用PyQt5制作，GUI设计使用了Qt Designer。</p><p>本软件的开源协议是GNU v3。</p><p>软件作者：oscarcx123</p><p>项目地址：<a href=\"https://github.com/oscarcx123/fraction-calc\"><span style=\" text-decoration: underline; color:#0057ae;\">https://github.com/oscarcx123/fraction-calc</span></a></p><p><br/></p></body></html>"))
