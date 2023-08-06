"""
使用python3.7编写一些自己常用的python包
create by swm 20181120
"""
from sys import platform


def hello_swm():
    print("Hi, I am october, thanks for using this packages!")


def the_system() -> str:
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'OSX'
    elif platform == "win32":
        return 'windows'
