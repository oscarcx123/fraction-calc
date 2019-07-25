from fractions import Fraction
from random import randint
import math
import os
import json
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import main_gui
import about_gui
import help_gui

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
        self.additional_rules = False
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

    # 未启用的函数
    def check_additional_rules(self):
        checkbox_num = [9, 10, 11, 12, 13]
        for num in checkbox_num:
            eval(f"if self.ui.checkBox_{num}.isChecked(): self.additional_rules = True")

    '''
    分解质因数算法
    来自：StackOverflow - Algorithm to find Largest prime factor of a number
    '''
    def factorization(self, n):
        factors = []
        d = 2
        while n > 1:
            while n % d == 0:
                factors.append(d)
                n /= d
            d = d + 1
            if d*d > n:
                if n > 1: factors.append(n)
                break
        return factors

    def gen(self):
        cnt = 1
        while cnt <= self.amount:
            selected_symbol = self.symbol[randint(0, len(self.symbol) - 1)]
            if selected_symbol == "+":
                generated_num = self.addition()
            if selected_symbol == "-":
                generated_num = self.subtraction()
            if selected_symbol == "*":
                generated_num = self.multiplication()
            if selected_symbol == "/":
                generated_num = self.division()
            numerator_A = generated_num["numerator_A"]
            numerator_B = generated_num["numerator_B"]
            denominator_A = generated_num["denominator_A"]
            denominator_B = generated_num["denominator_B"]
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

    def addition(self):
        denominator_A = 0
        denominator_B = 0
        numerator_A = 0
        numerator_B = 0
        # 勾选1可以作为分母
        if not self.ui.checkBox_13.isChecked() and self.low_range == 1:
            denominator_A = randint(2, self.high_range)
        else:
            denominator_A = randint(self.low_range, self.high_range)
        # 勾选同分母运算
        if self.ui.checkBox_9.isChecked():
            denominator_B = denominator_A
        # 勾选分母有公因数
        if self.ui.checkBox_10.isChecked():
            # 对第一个分数的分母进行分解质因数
            factors = self.factorization(denominator_A)
            # factors为空，说明分母为1，此时无视“分母有公因数”这条规则
            if factors == []:
                denominator_B = randint(self.low_range,self.high_range)
            else:
                # 随机选择一个因子，计算出该因子可达的最大倍数，从而得出分母
                selected_factor = factors[randint(0, len(factors) - 1)]
                multiple = self.high_range // selected_factor
                denominator_B = int(randint(1 , multiple) * selected_factor)
        if denominator_B == 0:
            denominator_B = randint(self.low_range,self.high_range)
        # 勾选运算项均为真分数或1
        if self.ui.checkBox_12.isChecked():
            # 勾选答案不大于1（此时为“运算项均为真分数”的一个子情况）
            if self.ui.checkBox_11.isChecked():
                numerator_A = randint(1, math.floor(denominator_A / 2))
                B_max_value = 1 - Fraction(numerator_A, denominator_A)
                numerator_B_max = math.floor(denominator_B * B_max_value.numerator / B_max_value.denominator)
                numerator_B = randint(1 , numerator_B_max)
            else:
                numerator_A = randint(self.low_range, denominator_A)
                numerator_B = randint(self.low_range, denominator_B)
        if numerator_A == 0:
            numerator_A = randint(self.low_range,self.high_range)
        if numerator_B == 0:
            numerator_B = randint(self.low_range,self.high_range)
        return {"numerator_A": numerator_A,
                "numerator_B": numerator_B,
                "denominator_A": denominator_A,
                "denominator_B": denominator_B}

    def subtraction(self):
        denominator_A = 0
        denominator_B = 0
        numerator_A = 0
        numerator_B = 0
        # 勾选1可以作为分母
        if not self.ui.checkBox_20.isChecked() and self.low_range == 1:
            denominator_A = randint(2, self.high_range)
        else:
            denominator_A = randint(self.low_range, self.high_range)
        # 勾选同分母运算
        if self.ui.checkBox_16.isChecked():
            denominator_B = denominator_A
        # 勾选分母有公因数
        if self.ui.checkBox_17.isChecked():
            # 对第一个分数的分母进行分解质因数
            factors = self.factorization(denominator_A)
            # factors为空，说明分母为1，此时无视“分母有公因数”这条规则
            if factors == []:
                denominator_B = randint(self.low_range,self.high_range)
            else:
                # 随机选择一个因子，计算出该因子可达的最大倍数，从而得出分母
                selected_factor = factors[randint(0, len(factors) - 1)]
                multiple = self.high_range // selected_factor
                denominator_B = int(randint(1 , multiple) * selected_factor)
        if denominator_B == 0:
            denominator_B = randint(self.low_range,self.high_range)
        # 勾选运算项均为真分数或1
        if self.ui.checkBox_19.isChecked():
            numerator_A = randint(self.low_range, denominator_A)
            numerator_B = randint(self.low_range, denominator_B)
        if numerator_A == 0:
            numerator_A = randint(self.low_range,self.high_range)
        if numerator_B == 0:
            numerator_B = randint(self.low_range,self.high_range)
        # 勾选答案答案不为负数
        if self.ui.checkBox_18.isChecked():
            if Fraction(numerator_A, denominator_A) - Fraction(numerator_B, denominator_B) < 0:
                numerator_A, numerator_B = numerator_B, numerator_A
                denominator_A, denominator_B = denominator_B, denominator_A
        return {"numerator_A": numerator_A,
                "numerator_B": numerator_B,
                "denominator_A": denominator_A,
                "denominator_B": denominator_B}

    def multiplication(self):
        denominator_A = 0
        denominator_B = 0
        numerator_A = 0
        numerator_B = 0
        # 勾选1可以作为分母
        if not self.ui.checkBox_23.isChecked() and self.low_range == 1:
            denominator_A = randint(2, self.high_range)
        else:
            denominator_A = randint(self.low_range, self.high_range)
        # 结果可以约分
        if self.ui.checkBox_14.isChecked():
            # 对第一个分数的分母进行分解质因数
            factors = self.factorization(denominator_A)
            # factors为空，说明分母为1，此时分母B无视“分母可以为1”这条规则
            if factors == []:
                if self.low_range == 1:
                    denominator_B = randint(2,self.high_range)
                else:
                    denominator_B = randint(self.low_range,self.high_range)
                factors_B = self.factorization(denominator_B)
                selected_factor = factors_B[randint(0, len(factors_B) - 1)]
                multiple = self.high_range // selected_factor
                numerator_A = int(randint(1 , multiple) * selected_factor)
            else:
                # 随机选择一个因子，计算出该因子可达的最大倍数，从而得出可以约分的数字
                selected_factor = factors[randint(0, len(factors) - 1)]
                multiple = self.high_range // selected_factor
                numerator_B = int(randint(1 , multiple) * selected_factor)
                denominator_B = randint(self.low_range,self.high_range)
                # 对第二个分数的分母进行分解质因数
                factors_B = self.factorization(denominator_B)
                if factors_B != []:
                    selected_factor = factors_B[randint(0, len(factors_B) - 1)]
                    multiple = self.high_range // selected_factor
                    numerator_A = int(randint(1 , multiple) * selected_factor)
        if denominator_B == 0:
            denominator_B = randint(self.low_range,self.high_range)
        if numerator_A == 0:
            numerator_A = randint(self.low_range,self.high_range)
        if numerator_B == 0:
            numerator_B = randint(self.low_range,self.high_range)
        return {"numerator_A": numerator_A,
                "numerator_B": numerator_B,
                "denominator_A": denominator_A,
                "denominator_B": denominator_B}

    def division(self):
        denominator_A = 0
        denominator_B = 0
        numerator_A = 0
        numerator_B = 0
        # 勾选1可以作为分母
        if not self.ui.checkBox_24.isChecked() and self.low_range == 1:
            denominator_A = randint(2, self.high_range)
        else:
            denominator_A = randint(self.low_range, self.high_range)
        # 结果可以约分
        if self.ui.checkBox_21.isChecked():
            # 对第一个分数的分母进行分解质因数
            factors = self.factorization(denominator_A)
            # factors为空，说明分母为1，此时分母B无视“分母可以为1”这条规则
            if factors == []:
                if self.low_range == 1:
                    numerator_B = randint(2,self.high_range)
                else:
                    numerator_B = randint(self.low_range,self.high_range)
                factors_B = self.factorization(numerator_B)
                selected_factor = factors_B[randint(0, len(factors_B) - 1)]
                multiple = self.high_range // selected_factor
                numerator_A = int(randint(1 , multiple) * selected_factor)
            else:
                # 随机选择一个因子，计算出该因子可达的最大倍数，从而得出可以约分的数字
                selected_factor = factors[randint(0, len(factors) - 1)]
                multiple = self.high_range // selected_factor
                denominator_B = int(randint(1 , multiple) * selected_factor)
                numerator_B = randint(self.low_range,self.high_range)
                # 对第二个分数的分母进行分解质因数
                factors_B = self.factorization(numerator_B)
                if factors_B != []:
                    selected_factor = factors_B[randint(0, len(factors_B) - 1)]
                    multiple = self.high_range // selected_factor
                    numerator_A = int(randint(1 , multiple) * selected_factor)
        if denominator_B == 0:
            denominator_B = randint(self.low_range,self.high_range)
        if numerator_A == 0:
            numerator_A = randint(self.low_range,self.high_range)
        if numerator_B == 0:
            numerator_B = randint(self.low_range,self.high_range)
        return {"numerator_A": numerator_A,
                "numerator_B": numerator_B,
                "denominator_A": denominator_A,
                "denominator_B": denominator_B}

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
        self.help_window = Help()


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
        self.ui.action.triggered.connect(self.help_window.show_window)


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
        # 基础题型设置 > 加法设置 > 同分母运算
        self.ui.checkBox_9.setChecked(conf["addition_same_denominator"])
        # 基础题型设置 > 加法设置 > 分母有公因数
        self.ui.checkBox_10.setChecked(conf["addition_denominator_has_common_factor"])
        # 基础题型设置 > 加法设置 > 答案不大于1
        self.ui.checkBox_11.setChecked(conf["addition_answer_within_one"])
        # 基础题型设置 > 加法设置 > 运算项均为真分数或1
        self.ui.checkBox_12.setChecked(conf["addition_proper_fraction"])
        # 基础题型设置 > 加法设置 > 1可以作为分母
        self.ui.checkBox_13.setChecked(conf["addition_one_as_denominator"])
        # 基础题型设置 > 乘法设置 > 结果可以约分
        self.ui.checkBox_14.setChecked(conf["multiplication_fraction_reduction"])
        # 基础题型设置 > 减法设置 > 同分母运算
        self.ui.checkBox_16.setChecked(conf["subtraction_same_denominator"])
        # 基础题型设置 > 减法设置 > 分母有公因数
        self.ui.checkBox_17.setChecked(conf["subtraction_denominator_has_common_factor"])
        # 基础题型设置 > 减法设置 > 答案不为负数
        self.ui.checkBox_18.setChecked(conf["subtraction_positive_answer"])
        # 基础题型设置 > 减法设置 > 运算项均为真分数或1
        self.ui.checkBox_19.setChecked(conf["subtraction_proper_fraction"])
        # 基础题型设置 > 减法设置 > 1可以作为分母
        self.ui.checkBox_20.setChecked(conf["subtraction_one_as_denominator"])
        # 基础题型设置 > 除法设置 > 结果可以约分
        self.ui.checkBox_21.setChecked(conf["division_fraction_reduction"])
        # 基础题型设置 > 乘法设置 > 1可以作为分母
        self.ui.checkBox_23.setChecked(conf["multiplication_one_as_denominator"])
        # 基础题型设置 > 除法设置 > 1可以作为分母
        self.ui.checkBox_24.setChecked(conf["division_one_as_denominator"])

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
        checkbox_dict = {
            "checkBox": "output_tex",
            "checkBox_2": "output_pdf",
            "checkBox_3": "output_txt",
            "checkBox_4": "output_ans_txt",
            "checkBox_5": "symbol_addition",
            "checkBox_6": "symbol_subtraction",
            "checkBox_7": "symbol_multiplication",
            "checkBox_8": "symbol_division",
            "checkBox_9": "addition_same_denominator",
            "checkBox_10": "addition_denominator_has_common_factor",
            "checkBox_11": "addition_answer_within_one",
            "checkBox_12": "addition_proper_fraction",
            "checkBox_13": "addition_one_as_denominator",
            "checkBox_14": "multiplication_fraction_reduction",
            "checkBox_16": "subtraction_same_denominator",
            "checkBox_17": "subtraction_denominator_has_common_factor",
            "checkBox_18": "subtraction_positive_answer",
            "checkBox_19": "subtraction_proper_fraction",
            "checkBox_20": "subtraction_one_as_denominator",
            "checkBox_21": "division_fraction_reduction",
            "checkBox_23": "multiplication_one_as_denominator",
            "checkBox_24": "division_one_as_denominator",
        }

        for box in checkbox_dict:
            checkbox_command = (
                f"if self.ui.{box}.isChecked():\n"
                f"    conf['{checkbox_dict[box]}'] = True\n"
                f"else:\n"
                f"    conf['{checkbox_dict[box]}'] = False"
            )
            loc = locals()
            exec(checkbox_command)
            conf = loc['conf']
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


# “使用帮助”窗口
class Help(SubWin):
    def ui_init(self):
        self.ui = help_gui.Ui_Dialog()

if __name__ == '__main__':
    window = MainWin()