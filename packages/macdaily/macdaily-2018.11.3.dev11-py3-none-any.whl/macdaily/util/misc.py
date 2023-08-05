# -*- coding: utf-8 -*-

import contextlib
import datetime
import functools
import getpass
import os
import platform
import re
import shutil
import sys
import traceback

import ptyng

from macdaily.util.const import (SHELL, USER, blue, bold, dim, grey, program,
                                 purple, python, red, reset)
from macdaily.util.error import UnsupportedOS

try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def beholder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != 'Darwin':
            raise UnsupportedOS('macdaily: error: script runs only on macOS')
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('macdaily: {}error{}: operation interrupted'.format(red, reset), file=sys.stderr)
            sys.stdout.write(reset)
            sys.tracebacklimit = 0
            raise
        except Exception as error:
            print('macdaily: {}error{}: {!s}'.format(red, reset, error), file=sys.stderr)
            sys.stdout.write(reset)
            sys.tracebacklimit = 0
            raise
    return wrapper


def date():
    now = datetime.datetime.now()
    txt = datetime.datetime.strftime(now, '%+')
    return txt


def get_pass(askpass):
    if sys.stdout.isatty():
        return getpass.getpass(prompt='Password:')
    try:
        password = subprocess.check_output([askpass, '🔑 Enter your password for {}.'.format(USER)])
    except subprocess.CalledProcessError:
        raise
    return password.strip().decode()


def make_context(devnull, redirect=False):
    if redirect:
        return contextlib.redirect_stdout(devnull)
    return contextlib.nullcontext()


def make_description(command):
    def desc(singular):
        if singular:
            return command.desc[0]
        else:
            return command.desc[1]
    return desc


def print_info(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}|💼|{} {}{}{}'.format(bold, blue, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|💼| {}'.format(context))


def print_misc(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}|📌|{} {}{}{}'.format(bold, grey, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📌| {}'.format(context))


def print_scpt(text, file, redirect=False):
    if not isinstance(text, str):
        text = ' '.join(text)
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}|📜|{} {}{}{}'.format(bold, purple, reset, bold, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write('|📜| {}'.format(context))


def print_term(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print(text, end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def print_text(text, file, redirect=False):
    flag = text.endswith(os.linesep)
    if not redirect:
        end = str() if flag else os.linesep
        print('{}{}{}'.format(dim, text, reset), end=end)
    with open(file, 'a') as fd:
        context = re.sub(r'(\033\[[0-9][0-9;]*m)|(\^D\x08\x08)', r'',
                         (text if flag else '{}{}'.format(text, os.linesep)), flags=re.IGNORECASE)
        fd.write(context)


def record(file, args, today, config, redirect=False):
    # record program arguments
    print_misc('{} {}'.format(python, program), file, redirect)
    with open(file, 'a') as log:
        log.writelines(['TIME: {!s}\n'.format(today), 'FILE: {}\n'.format(file)])

    # record parsed arguments
    print_misc('Parsing command line arguments'.format(), file, redirect)
    with open(file, 'a') as log:
        for key, value in vars(args).items():
            if isinstance(value, dict):
                for k, v, in value.items():
                    log.write('ARG: {} -> {} = {}\n'.format(key, k, v))
            else:
                log.write('ARG: {} = {}\n'.format(key, value))

    # record parsed configuration
    print_misc('Parsing configuration file '
               '{!r}'.format(os.path.expanduser("~/.dailyrc")), file, redirect)
    with open(file, 'a') as log:
        for key, value in config.items():
            for k, v, in value.items():
                log.write('CFG: {} -> {} = {}\n'.format(key, k, v))


def run(argv, file, *, redirect=False, password=None, yes=None, shell=False,
        prefix=None, timeout=None, executable=SHELL, verbose=False):
    suffix = '> /dev/null' if redirect else None
    return script(argv, file, password=password, yes=yes, redirect=(not verbose), shell=shell,
                  executable=executable, timeout=timeout, prefix=prefix, suffix=suffix)


def _merge(argv):
    if isinstance(argv, str):
        return argv
    return ' '.join(argv)


def _script(argv=SHELL, file='typescript', password=None, yes=None,
            shell=False, executable=SHELL, prefix=None, suffix=None, timeout=None):
    if suffix is not None:
        argv = '{} {}'.format(_merge(argv), suffix)
    if prefix is not None:
        argv = '{} {}'.format(prefix, _merge(argv))
    if shell:
        argv = [executable, '-c', _merge(argv)]

    if password is not None:
        bpwd = password.encode()
    bdim = dim.encode()
    repl = rb'\1' + bdim
    # test = bytes()

    def master_read_ng(fd, replace=None):
        data = os.read(fd, 1024).replace(b'^D\x08\x08', b'')
        if replace is not None:
            data = data.replace(replace, b'')
        if password is not None:
            data = data.replace(bpwd, b'********')
        data = data.replace(b'Password:', b'Password:\r\n')
        text = re.sub(rb'\033\[[0-9][0-9;]*m', rb'', data, flags=re.IGNORECASE)
        typescript.write(text)
        byte = bdim + re.sub(rb'(\033\[[0-9][0-9;]*m)', repl, data, flags=re.IGNORECASE)
        # nonlocal test
        # test = byte
        return byte

    if yes is None:
        def master_read(fd):
            return master_read_ng(fd)

        def stdin_read(fd):
            return os.read(fd, 1024)
    else:
        if isinstance(yes, str):
            yes = yes.encode()
        txt = re.sub(rb'[\r\n]*$', rb'', yes)
        old = txt + b'\r\n'
        exp = txt + b'\n'

        def master_read(fd):
            return master_read_ng(fd, replace=old)

        def stdin_read(fd):
            return exp

    with open(file, 'ab') as typescript:
        returncode = ptyng.spawn(argv, master_read, stdin_read, timeout=timeout)
    # if not test.decode().endswith(os.linesep):
    #     sys.stdout.write(os.linesep)
    return returncode


def _unbuffer(argv=SHELL, file='typescript', password=None, yes=None,
              redirect=False, executable=SHELL, prefix=None, suffix=None, timeout=None):
    def replace(password):
        if password is None:
            return ''
        return (".replace({!r}, '********')".format(password))

    def ansi2text(password):
        return ('{} -c "'
                'import re, sys; '
                "data = sys.stdin.read().strip().replace('^D\x08\x08', ''); "
                "temp = re.sub(r'\x1b\\[[0-9][0-9;]*m', r'', data, flags=re.IGNORECASE); "
                "text = temp.replace('Password:', 'Password:\\r\\n'){}; "
                "print(text.strip())"
                '"'.format(sys.executable, replace(password)))

    def text2dim(password):
        return ('{} -c "'
                'import re, sys; '
                "data = sys.stdin.read().strip().replace('^D\x08\x08', ''); "
                "temp = {!r} + re.sub(r'(\x1b\\[[0-9][0-9;]*m)', r'\\1{}', data, flags=re.IGNORECASE); "
                "text = temp.replace('Password:', 'Password:\\r\\n'){}; "
                "print(text.strip())"
                '"'.format(sys.executable, dim, dim, replace(password)))

    if suffix is not None:
        argv = '{} {}'.format(_merge(argv), suffix)
    argv = 'unbuffer -p {} | tee -a >(col -b | {} >> {}) | {}'.format(_merge(argv), ansi2text(password), file, text2dim(password))
    # argv = f'unbuffer -p {_merge(argv)} | {text2dim(password)} | tee -a >(col -b | {ansi2text(password)} >> {file})'
    if yes is not None:
        argv = 'yes {} | {}'.format(yes, argv)
    if prefix is not None:
        argv = '{} {}'.format(prefix, _merge(argv))
    # argv = f'set -x; {argv}'

    try:
        returncode = subprocess.check_call(argv, shell=True, executable=SHELL, timeout=timeout)
    except subprocess.SubprocessError as error:
        text = traceback.format_exc()
        if password is not None:
            text = text.replace(password, '********')
        print_text(text, file, redirect=redirect)
        returncode = getattr(error, 'returncode', 1)
    # if password is not None:
    #     with contextlib.suppress(subprocess.SubprocessError):
    #         subprocess.run(['chown', getpass.getuser(), file], stdout=subprocess.DEVNULL)
    return returncode


def script(argv=SHELL, file='typescript', *, password=None, yes=None, prefix=None,
           redirect=False, timeout=None, shell=False, executable=SHELL, suffix=None):
    if isinstance(argv, str):
        argv = [argv]
    else:
        argv = list(argv)

    with open(file, 'a') as typescript:
        args = " ".join(argv)
        if password is not None:
            args = args.replace(password, '********')
        typescript.write('Script started on {}\n'.format(date()))
        typescript.write('command: {!r}\n'.format(args))

    if shutil.which('unbuffer') is None:
        returncode = _script(argv, file, password, yes, shell, executable, prefix, suffix, timeout)
    else:
        returncode = _unbuffer(argv, file, password, yes, redirect, executable, prefix, suffix, timeout)

    with open(file, 'a') as typescript:
        # print('Before:', typescript.tell())
        typescript.write('Script done on {}\n'.format(date()))
        # print('After:', typescript.tell())
    sys.stdout.write(reset)
    return returncode


def sudo(argv, file, password, *, askpass=None, sethome=False, yes=None,
         redirect=False, verbose=False, timeout=None, executable=SHELL):
    def make_prefix(argv, askpass, sethome):
        if not isinstance(argv, str):
            argv = ' '.join(argv)
        if getpass.getuser() == 'root':
            return argv
        sudo_argv = 'echo {!r} | sudo --stdin --validate --prompt="Password:\n" &&'.format(password)
        if yes is not None:
            sudo_argv = '{} yes {} |'.format(sudo_argv, yes)
        sudo_argv = '{} sudo'.format(sudo_argv)
        if sethome:
            sudo_argv = '{} --set-home'.format(sudo_argv)
        if askpass is not None:
            sudo_argv = 'SUDO_ASKPASS={!r} {} --askpass --prompt="🔑 Enter your password for {}."'.format(askpass, sudo_argv, USER)
        return sudo_argv
    return run(argv, file, password=password, redirect=redirect, timeout=timeout, shell=True,
               prefix=make_prefix(argv, askpass, sethome), executable=executable, verbose=verbose)
