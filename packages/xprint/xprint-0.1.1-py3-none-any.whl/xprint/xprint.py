# coding:utf-8
import sys
import colorama
from colorama import Fore, Back, Style


def init(autoreset: bool = True, convert=None, strip=None, wrap=True):
    colorama.init(autoreset=autoreset, convert=convert, strip=strip, wrap=wrap)


def success(s: str, inline: bool = False):
    if inline:
        sys.stdout.write(Fore.GREEN + s)
    else:
        print(Fore.GREEN + s)
    return


def error(s: str, inline: bool = False):
    if inline:
        sys.stdout.write(Fore.LIGHTRED_EX + s)
    else:
        print(Fore.LIGHTRED_EX + s)
    return


def value(s, inline: bool = False):
    if inline:
        sys.stdout.write(Fore.LIGHTCYAN_EX + s)
    else:
        print(Fore.LIGHTCYAN_EX + s)
    return


def step():
    sys.stdout.write(Fore.LIGHTBLACK_EX + '>')
    return


def job(start, value=None, end=None, inline: bool = False):
    sys.stdout.write(Fore.LIGHTYELLOW_EX + start)
    if value: sys.stdout.write(Fore.LIGHTCYAN_EX + value)
    if end: sys.stdout.write(Fore.LIGHTYELLOW_EX + end)
    if not inline: print()
    return


def getting(s):
    sys.stdout.write(Fore.LIGHTYELLOW_EX + s)
    sys.stdout.write(Fore.LIGHTBLACK_EX + ' > ')
    return
