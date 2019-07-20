from fractions import Fraction
from random import randint
import math
import os
import json
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import main_gui
import about_gui

'''
【分数题目类】
封装了生成题目的整个流程，是整个程序的核心部分
'''
class Frac():
    def __init__(self, **kwargs):
        self.amount = int(kwargs["amount"])
        self.low_range = int(kwargs["low_range"])
        self.high_range = int(kwargs["high_range"])
        self.ui = kwargs["ui"]
        self.get_calc_symbol()
        self.problems = {}

    def get_calc_symbol(self):
        self.symbol = []
        if self.ui.checkBox_5.isChecked():
            self.symbol.append("+")
        if self.ui.checkBox_6.isChecked():
            self.symbol.append("-")
        if self.ui.checkBox_7.isChecked():
            self.symbol.append("*")
        if self.ui.checkBox_8.isChecked():
            self.symbol.append("/")

    def gen(self):
        cnt = 1
        sector = 99 / len(self.symbol)
        while cnt <= self.amount:
            rand_num = randint(0, 99)
            for item in range(len(self.symbol)):
                if rand_num > math.floor(item * sector):
                    selected_symbol = self.symbol[item]
            numerator_A = randint(self.low_range,self.high_range)
            denominator_A = randint(self.low_range,self.high_range)
            numerator_B = randint(self.low_range,self.high_range)
            denominator_B = randint(self.low_range,self.high_range)
            result = eval(f"Fraction(numerator_A, denominator_A) {selected_symbol} Fraction(numerator_B, denominator_B)")
            numerator_Ans = result.numerator
            denominator_Ans = result.denominator
            self.problems[cnt] = {}
            self.problems[cnt]["symbol"] = selected_symbol
            self.problems[cnt]["numerator_A"] = numerator_A
            self.problems[cnt]["denominator_A"] = denominator_A
            self.problems[cnt]["numerator_B"] = numerator_B
            self.problems[cnt]["denominator_B"] = denominator_B
            self.problems[cnt]["numerator_Ans"] = numerator_Ans
            self.problems[cnt]["denominator_Ans"] = denominator_Ans
            cnt += 1

    def output(self):
        if self.ui.checkBox.isChecked():
            self.output_tex()
        if self.ui.checkBox_2.isChecked():
            self.output_pdf()
        if self.ui.checkBox_3.isChecked():
            self.output_txt()
        if self.ui.checkBox_4.isChecked():
            self.output_ans_txt()

    # txt格式输出题目
    def output_txt(self):
        with open ("problems.txt", "w") as f:
            cnt = 1
            while cnt <= self.amount:
                linebreak = 0
                while linebreak < 5:
                    f.write(f"{self.problems[cnt]['numerator_A']}/{self.problems[cnt]['denominator_A']} {self.problems[cnt]['symbol']} {self.problems[cnt]['numerator_B']}/{self.problems[cnt]['denominator_B']} = \t\t")
                    cnt += 1
                    linebreak += 1
                f.write("\n")

    # tex格式输出题目
    def output_tex(self):
        with open ("problems.tex", "w") as f:
            f.write("\\documentclass[fleqn, 12pt]{extarticle}\n")
            f.write("\\usepackage[left=2cm, right=5cm, top=2cm]{geometry}\n")
            f.write("\\usepackage{mathtools}\n")
            f.write("\\begin{document}\n")
            f.write("\\begin{alignat*}{5}\n")
            cnt = 1
            while cnt <= self.amount:
                if self.problems[cnt]['symbol'] == "*":
                    converted_symbol = "\\times"
                elif self.problems[cnt]['symbol'] == "/":
                    converted_symbol = "\\div"
                else:
                    converted_symbol = self.problems[cnt]['symbol']
                f.write(f"&\\frac{{{self.problems[cnt]['numerator_A']}}}{{{self.problems[cnt]['denominator_A']}}} {converted_symbol} \\frac{{{self.problems[cnt]['numerator_B']}}}{{{self.problems[cnt]['denominator_B']}}} = \\qquad \\qquad")
                if cnt % 5 == 0:
                    f.write("\\\\\n")
                else:
                    f.write("\n")
                cnt += 1
            f.write("\\end{alignat*}\n")
            f.write("\\end{document}\n")
    
    # 将tex文件转换成pdf（如果没有安装LaTeX，将无法转换，这里使用的是latexmk）
    def output_pdf(self):
        if os.path.exists("problems.tex"):
            os.system("latexmk -pdf problems.tex")
        else:
            self.output_tex()
            os.system("latexmk -pdf problems.tex")

    # txt格式输出答案
    def output_ans_txt(self):
        with open ("answer.txt", "w") as f:
            cnt = 1
            while cnt <= self.amount:
                f.write(f"{self.problems[cnt]['numerator_Ans']} / {self.problems[cnt]['denominator_Ans']}")
                if cnt % 5 == 0:
                    f.write("\n")
                else:
                    f.write("\t\t")
                cnt += 1
    
    # 用于清理中间生成的文件
    def cleanup(self):
        file_list = ["problems.aux",
                     "problems.fdb_latexmk",
                     "problems.fls",
                     "problems.log"]
        cnt = 0
        while cnt < len(file_list):
            if os.path.exists(file_list[cnt]):
                os.remove(file_list[cnt])
            cnt += 1

'''
【主窗口类】
主窗口类继承自QMainWindow类。
图形程序绝大部分交互都在这里。
'''
class MainWin(QMainWindow):
    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        QMainWindow.__init__(self, parent)
        self.ui = main_gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_subwindow()
        self.init_interface()
        self.init_signal()
        self.show()
        sys.exit(self.app.exec_())


    # 子窗口初始化（在这里创建实例，从而规避子窗口多开问题）
    def init_subwindow(self):
        self.about_window = About()


    # 图形界面数值的初始化
    def init_interface(self):
        # 初始化“生成器”页面的进度条为0%
        self.ui.progressBar.setValue(0)
        # 设置题目上限（目前没解决多页问题，因此限定100题）
        self.ui.spinBox_3.setMaximum(100)
        #【基础设置】初始化
        if os.path.exists("conf.json"):
            self.load_conf()
        else:
            self.load_default_conf()


    # 信号和槽（绑定事件）初始化
    def init_signal(self):
        # 绑定“生成器”页面的“生成”按钮到generate函数
        self.ui.pushButton.clicked.connect(self.generate)
        self.ui.action_2.triggered.connect(self.about_window.show_window)


    # 在有配置文件的情况下，读取上次使用时的配置
    def load_conf(self):
        with open("conf.json") as f:
            conf = json.load(f)
        # 设置“最小数值范围“
        self.ui.spinBox.setValue(int(conf["low_range"]))
        # 设置”最大数值范围“
        self.ui.spinBox_2.setValue(int(conf["high_range"]))
        # 设置”题目数量“
        self.ui.spinBox_3.setValue(int(conf["amount"]))
        # 设置tex格式输出题目
        self.ui.checkBox.setChecked(conf["output_tex"])
        # 设置pdf格式输出题目
        self.ui.checkBox_2.setChecked(conf["output_pdf"])
        # 设置txt格式输出题目
        self.ui.checkBox_3.setChecked(conf["output_txt"])
        # 设置txt格式输出答案
        self.ui.checkBox_4.setChecked(conf["output_ans_txt"])
        # 设置“出现加法运算”
        self.ui.checkBox_5.setChecked(conf["symbol_addition"])
        # 设置“出现减法运算”
        self.ui.checkBox_6.setChecked(conf["symbol_subtraction"])
        # 设置“出现乘法运算”
        self.ui.checkBox_7.setChecked(conf["symbol_multiplication"])
        # 设置“出现除法运算”
        self.ui.checkBox_8.setChecked(conf["symbol_division"])

    # 如果是初次运行，会加载默认配置
    def load_default_conf(self):
        # 默认“最小数值范围“是2
        self.ui.spinBox.setValue(2)
        # 默认”最大数值范围“是15
        self.ui.spinBox_2.setValue(9)
        # 默认”题目数量“是100
        self.ui.spinBox_3.setValue(100)
        # 设置tex格式输出题目
        self.ui.checkBox.setChecked(True)
        # 设置pdf格式输出题目
        self.ui.checkBox_2.setChecked(True)
        # 设置txt格式输出题目
        self.ui.checkBox_3.setChecked(True)
        # 设置txt格式输出答案
        self.ui.checkBox_4.setChecked(True)
        # 设置“出现加法运算”
        self.ui.checkBox_5.setChecked(True)
        # 设置“出现减法运算”
        self.ui.checkBox_6.setChecked(True)
        # 设置“出现乘法运算”
        self.ui.checkBox_7.setChecked(True)
        # 设置“出现除法运算”
        self.ui.checkBox_8.setChecked(True)

    # 点击“生成”后，会保存当前使用的配置
    def save_conf(self):
        conf = {}
        conf["low_range"] = self.ui.spinBox.text()
        conf["high_range"] = self.ui.spinBox_2.text()
        conf["amount"] = self.ui.spinBox_3.text()
        if self.ui.checkBox.isChecked():
            conf["output_tex"] = True
        else:
            conf["output_tex"] = False
        if self.ui.checkBox_2.isChecked():
            conf["output_pdf"] = True
        else:
            conf["output_pdf"] = False
        if self.ui.checkBox_3.isChecked():
            conf["output_txt"] = True
        else:
            conf["output_txt"] = False
        if self.ui.checkBox_4.isChecked():
            conf["output_ans_txt"] = True
        else:
            conf["output_ans_txt"] = False
        if self.ui.checkBox_5.isChecked():
            conf["symbol_addition"] = True
        else:
            conf["symbol_addition"] = False
        if self.ui.checkBox_6.isChecked():
            conf["symbol_subtraction"] = True
        else:
            conf["symbol_subtraction"] = False
        if self.ui.checkBox_7.isChecked():
            conf["symbol_multiplication"] = True
        else:
            conf["symbol_multiplication"] = False
        if self.ui.checkBox_8.isChecked():
            conf["symbol_division"] = True
        else:
            conf["symbol_division"] = False
        with open(("conf.json"), "w") as f:
            json.dump(conf, f)

    def generate(self):
        low_range = self.ui.spinBox.text()
        high_range = self.ui.spinBox_2.text()
        amount = self.ui.spinBox_3.text()
        self.save_conf()
        Practice = Frac(amount=amount, low_range=low_range, high_range=high_range, ui=self.ui)
        Practice.gen()
        Practice.output()
        Practice.cleanup()


'''
【子窗口基类】
需要继承并复写ui_init函数才能使用。
使用时需要在MainWin类的init_subwindow函数中注册。
每次显示窗口就只调用show方法而不是重新实例化，这样可以防止子窗口多开。
'''
class SubWin(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui_init()
        self.ui.setupUi(self)

    # 此函数留白，用于在继承子窗口基类时复写
    # 复写格式为 self.ui = gui_file.ui_type()
    # 例子：self.ui = about_gui.Ui_Dialog()
    def ui_init(self):
        pass

    # 显示窗口
    def show_window(self):
        self.show()
        self.raise_()

# “关于”窗口
class About(SubWin):
    def ui_init(self):
        self.ui = about_gui.Ui_Dialog()

if __name__ == '__main__':
    window = MainWin()