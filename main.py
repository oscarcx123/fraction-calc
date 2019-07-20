from fractions import Fraction
from random import randint
from pylatex import Document
import os
import json

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


import main_gui
import about_gui

class Frac():
    def __init__(self, **kwargs):
        self.amount = int(kwargs["amount"])
        self.low_range = int(kwargs["low_range"])
        self.high_range = int(kwargs["high_range"])
        self.problems = {}

    def gen(self):
        cnt = 1
        while cnt <= self.amount:
            numerator_A = randint(self.low_range,self.high_range)
            denominator_A = randint(self.low_range,self.high_range)
            numerator_B = randint(self.low_range,self.high_range)
            denominator_B = randint(self.low_range,self.high_range)
            result = Fraction(numerator_A, denominator_A) + Fraction(numerator_B, denominator_B)
            numerator_Ans = result.numerator
            denominator_Ans = result.denominator
            self.problems[cnt] = {}
            self.problems[cnt]["numerator_A"] = numerator_A
            self.problems[cnt]["denominator_A"] = denominator_A
            self.problems[cnt]["numerator_B"] = numerator_B
            self.problems[cnt]["denominator_B"] = denominator_B
            self.problems[cnt]["numerator_Ans"] = numerator_Ans
            self.problems[cnt]["denominator_Ans"] = denominator_Ans
            cnt += 1

    def output(self):
        if ui.checkBox.isChecked():
            self.output_tex()
        if ui.checkBox_2.isChecked():
            self.output_pdf()
        if ui.checkBox_3.isChecked():
            self.output_txt()
        if ui.checkBox_4.isChecked():
            self.output_ans_txt()

    # txt格式输出题目
    def output_txt(self):
        with open ("problems.txt", "w") as f:
            cnt = 1
            while cnt <= self.amount:
                linebreak = 0
                while linebreak < 5:
                    f.write(f"{self.problems[cnt]['numerator_A']}/{self.problems[cnt]['denominator_A']} + {self.problems[cnt]['numerator_B']}/{self.problems[cnt]['denominator_B']} = \t\t")
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
                f.write(f"&\\frac{{{self.problems[cnt]['numerator_A']}}}{{{self.problems[cnt]['denominator_A']}}} + \\frac{{{self.problems[cnt]['numerator_B']}}}{{{self.problems[cnt]['denominator_B']}}} = \\qquad \\qquad")
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



# GUI默认数值的初始化
def init_ui():
    # 绑定“生成器”页面的“生成”按钮到generate函数
    ui.pushButton.clicked.connect(generate)
    # 初始化“生成器”页面的进度条为0%
    ui.progressBar.setValue(0)
    # 设置题目上限（目前没解决多页问题，因此限定100题）
    ui.spinBox_3.setMaximum(100)
    #【基础设置】
    if os.path.exists("conf.json"):
        load_conf()
    else:
        load_default_conf()

# 在有配置文件的情况下，读取上次使用时的配置
def load_conf():
    with open("conf.json") as f:
        conf = json.load(f)
    # 设置“最小数值范围“
    ui.spinBox.setValue(int(conf["low_range"]))
    # 设置”最大数值范围“
    ui.spinBox_2.setValue(int(conf["high_range"]))
    # 设置”题目数量“
    ui.spinBox_3.setValue(int(conf["amount"]))
    # 设置tex格式输出题目
    ui.checkBox.setChecked(conf["output_tex"])
    # 设置pdf格式输出题目
    ui.checkBox_2.setChecked(conf["output_pdf"])
    # 设置txt格式输出题目
    ui.checkBox_3.setChecked(conf["output_txt"])
    # 设置txt格式输出答案
    ui.checkBox_4.setChecked(conf["output_ans_txt"])

# 如果是初次运行，会加载默认配置
def load_default_conf():
    # 默认“最小数值范围“是2
    ui.spinBox.setValue(2)
    # 默认”最大数值范围“是15
    ui.spinBox_2.setValue(9)
    # 默认”题目数量“是100
    ui.spinBox_3.setValue(100)
    # 设置tex格式输出题目
    ui.checkBox.setChecked(True)
    # 设置pdf格式输出题目
    ui.checkBox_2.setChecked(True)
    # 设置txt格式输出题目
    ui.checkBox_3.setChecked(True)
    # 设置txt格式输出答案
    ui.checkBox_4.setChecked(True)

# 点击“生成”后，会保存当前使用的配置
def save_conf():
    conf = {}
    conf["low_range"] = ui.spinBox.text()
    conf["high_range"] = ui.spinBox_2.text()
    conf["amount"] = ui.spinBox_3.text()
    if ui.checkBox.isChecked():
        conf["output_tex"] = True
    else:
        conf["output_tex"] = False
    if ui.checkBox_2.isChecked():
        conf["output_pdf"] = True
    else:
        conf["output_pdf"] = False
    if ui.checkBox_3.isChecked():
        conf["output_txt"] = True
    else:
        conf["output_txt"] = False
    if ui.checkBox_4.isChecked():
        conf["output_ans_txt"] = True
    else:
        conf["output_ans_txt"] = False
    with open(("conf.json"), "w") as f:
        json.dump(conf, f)

def generate():
    low_range = ui.spinBox.text()
    high_range = ui.spinBox_2.text()
    amount = ui.spinBox_3.text()
    save_conf()
    Practice = Frac(amount=amount, low_range=low_range, high_range=high_range)
    Practice.gen()
    Practice.output()
    Practice.cleanup()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = main_gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    init_ui()  
    MainWindow.show()
    sys.exit(app.exec_())