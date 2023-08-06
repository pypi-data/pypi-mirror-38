# coding:utf-8
import colorama
from sys import stdout
from colorama import Fore, Back, Style


def init(autoreset: bool = True, convert=None, strip=None, wrap=True):
    colorama.init(autoreset=autoreset, convert=convert, strip=strip, wrap=wrap)


def success(s: str, inline: bool = False):
    if inline:
        stdout.write(Fore.GREEN + s)
    else:
        print(Fore.GREEN + s)
    return


def error(s: str, inline: bool = False):
    if inline:
        stdout.write(Fore.LIGHTRED_EX + s)
    else:
        print(Fore.LIGHTRED_EX + s)
    return


def value(s, inline: bool = False):
    if inline:
        stdout.write(Fore.LIGHTCYAN_EX + s)
    else:
        print(Fore.LIGHTCYAN_EX + s)
    return


def step():
    stdout.write(Fore.LIGHTBLACK_EX + '>')
    return


def job(s):
    stdout.write(Back.BLUE + '\n - {} - '.format(s))
    return


def about_to(left, value=None, right=None, inline: bool = True):
    stdout.write(Fore.LIGHTYELLOW_EX + '> {}'.format(left))
    if value: stdout.write(Fore.LIGHTCYAN_EX + ' {}'.format(value))
    if right: stdout.write(Fore.LIGHTYELLOW_EX + ' {}'.format(right))
    if inline:
        stdout.write(Fore.LIGHTBLACK_EX + '... ')
    else:
        print()
    return


def getting(s):
    stdout.write(Fore.LIGHTYELLOW_EX + s)
    stdout.write(Fore.LIGHTBLACK_EX + ' > ')
    return
