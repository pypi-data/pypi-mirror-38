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


def error(s: str, inline: bool = False):
    if inline:
        stdout.write(Fore.LIGHTRED_EX + s)
    else:
        print(Fore.LIGHTRED_EX + s)


def value(s, inline: bool = False):
    if inline:
        stdout.write(Fore.LIGHTCYAN_EX + s)
    else:
        print(Fore.LIGHTCYAN_EX + s)


def step():
    stdout.write(Fore.LIGHTBLACK_EX + '>')


def job(s):
    stdout.write(Back.BLUE + '\n - {} - '.format(s))


def about_t(left, value=None, right=None):
    about_to(left=left, value=value, right=right, inline=True)


def about_to(left, value=None, right=None, inline: bool = False):
    stdout.write(Fore.LIGHTBLACK_EX + '> ')
    stdout.write(Fore.LIGHTYELLOW_EX + left)
    if value: stdout.write(Fore.LIGHTCYAN_EX + ' {}'.format(value))
    if right: stdout.write(Fore.LIGHTYELLOW_EX + ' {}'.format(right))
    if inline:
        stdout.write(Fore.LIGHTBLACK_EX + '... ')
    else:
        print()


def getting(s):
    stdout.write(Fore.LIGHTYELLOW_EX + s)
    stdout.write(Fore.LIGHTBLACK_EX + ' > ')
