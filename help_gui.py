# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(746, 454)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(9, 9, 223, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(9, 48, 731, 401))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "帮助"))
        self.label.setText(_translate("Dialog", "Fraction-Calc 帮助"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>Q：软件如何使用？</p><p>A：选择对应的运算符号以及相关的题目特征，点击生成即可，题目文件名为problems，答案文件名为answer，这些文件都能在软件运行目录下找到。</p><p>Q：为什么无法生成PDF格式的题目？</p><p>A：PDF需要使用latexmk渲染，目前可以选择生成tex格式然后自行使用软件渲染；或者你可以使用txt格式输出，坏处就是无法展示自然书写的分数。后期可能会陆续支持更多格式。</p><p>Q：这个软件只能生成分数练习题吗？</p><p>A：是的，如果需要普通的整数四则运算，可以去看看另一个开源项目oralcalc，那个是一个很棒的口算题生成器，并且提供在线demo使用。</p><p>P.S. 本人是计算机业余爱好者，编程能力有限，出错在所难免，如果有问题可以去项目地址提issue，有能力修复的可以直接提Pull Request。</p><p>软件作者：oscarcx123</p><p>项目地址：<a href=\"https://github.com/oscarcx123/fraction-calc\"><span style=\" text-decoration: underline; color:#0057ae;\">https://github.com/oscarcx123/fraction-calc</span></a></p></body></html>"))
