#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ctypes import CDLL, c_char_p, c_long
from subprocess import *
import platform

def pipe_through_prog(prog, text):
    p1 = Popen(prog.split(), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    [result, err] = p1.communicate(input=text.encode('utf-8'))
    return [p1.returncode, result.decode('utf-8'), err]

def use_library(lib, text):
    textbytes = text.encode('utf-8')
    textlen = len(textbytes)
    return [0, lib(textbytes, textlen).decode('utf-8'), '']

class CMark:
    def __init__(self, prog=None, library_dir=None):
        self.prog = prog
        if prog:
            self.to_html = lambda x: pipe_through_prog(prog, x)
        else:
            sysname = platform.system()
            libname = "libcmark"
            if sysname == 'Darwin':
                libname += ".dylib"
            elif sysname == 'Windows':
                libname = "cmark.dll"
            else:
                libname += ".so"
            if library_dir:
                libpath = library_dir + "/" + libname
            else:
                libpath = "build/src/" + libname
            cmark = CDLL(libpath)
            markdown = cmark.cmark_markdown_to_html
            markdown.restype = c_char_p
            markdown.argtypes = [c_char_p, c_long]
            self.to_html = lambda x: use_library(markdown, x)
