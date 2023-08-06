# coding:utf-8
import colorama
import sys
from colorama import Fore, Back, Style

wr = sys.stdout.write


def init(autoreset: bool = False, convert=None, strip=None, wrap=True):
    colorama.init(autoreset=autoreset, convert=convert, strip=strip, wrap=wrap)


def fi(inline: bool = True):
    if inline:
        wr(Style.RESET_ALL)
    else:
        print(Style.RESET_ALL)
    sys.stdout.flush()


def step():
    wr(Fore.LIGHTBLACK_EX + '>')
    fi()


def success(s: str, inline: bool = False):
    wr(Fore.GREEN + s)
    fi(inline)


def error(s: str, inline: bool = False):
    wr(Fore.LIGHTRED_EX + s)
    fi(inline)


def value(s, inline: bool = False):
    wr(Fore.LIGHTCYAN_EX + s)
    fi(inline)


def job(s, inline: bool = False):
    wr(Back.BLUE + Fore.LIGHTWHITE_EX + '\n - {} - '.format(s))
    fi(inline)


def about_to(left, value=None, right=None, inline: bool = False, no_dot: bool = False):
    wr(Fore.LIGHTBLACK_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + left)
    if value: wr(Fore.LIGHTCYAN_EX + ' {}'.format(value))
    if right: wr(Fore.LIGHTYELLOW_EX + ' {}'.format(right))
    if not no_dot:
        if inline: wr(Fore.LIGHTBLACK_EX + '... ')
    fi(inline)


def about_t(left, value=None, right=None, no_dot: bool = False):
    about_to(left=left, value=value, right=right, inline=True, no_dot=no_dot)


def getting(s, inline: bool = True):
    wr(Fore.LIGHTBLACK_EX + '> ')
    wr(Fore.LIGHTYELLOW_EX + s)
    wr(Fore.LIGHTBLACK_EX + ' > ')
    fi(inline)
