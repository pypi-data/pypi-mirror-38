# coding:utf-8
import sys
import colorama


def init(autoreset: bool = True):
    colorama.init(autoreset=autoreset)


def success(s: str, inline: bool = False):
    if inline:
        sys.stdout.write(colorama.Fore.GREEN + s)
    else:
        print(colorama.Fore.GREEN + s)
    return


def error(s: str, inline: bool = False):
    if inline:
        sys.stdout.write(colorama.Fore.LIGHTRED_EX + s)
    else:
        print(colorama.Fore.LIGHTRED_EX + s)
    return


def value(s, inline: bool = False):
    if inline:
        sys.stdout.write(colorama.Fore.LIGHTCYAN_EX + s)
    else:
        print(colorama.Fore.LIGHTCYAN_EX + s)
    return


def step():
    sys.stdout.write(colorama.Fore.LIGHTBLACK_EX + '>')
    return


def job(start, value=None, end=None, inline: bool = False):
    sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX + start)
    if value: sys.stdout.write(colorama.Fore.LIGHTCYAN_EX + value)
    if end: sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX + end)
    if not inline: print()
    return


def getting(s):
    sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX + s)
    sys.stdout.write(colorama.Fore.LIGHTBLACK_EX + ' > ')
    return
