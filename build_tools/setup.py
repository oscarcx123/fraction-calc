from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Compiler import Options

# 使用"embed"选项
Options.embed = "main"

ext_modules = [
    Extension("main",  ["main.py"]),
    Extension("main_gui",  ["main_gui.py"]),
    Extension("about_gui",  ["about_gui.py"]),
    Extension("help_gui",  ["help_gui.py"]),
]

setup(
    name = 'Fraction-Calc',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)