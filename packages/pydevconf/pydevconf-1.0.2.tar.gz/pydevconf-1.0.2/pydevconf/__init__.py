import getopt
import os
import sys
import sysconfig

pyver = sysconfig.get_config_var('VERSION')
getvar = sysconfig.get_config_var

def prefix():
    return sysconfig.get_config_var('prefix')

def exec_prefix():
    return sysconfig.get_config_var('exec_prefix')

def includes():
    return ['-I' + sysconfig.get_path('include'),
            '-I' + sysconfig.get_path('platinclude')]

def cflags():
    flags = includes()
    flags.extend(getvar('CFLAGS').split())
    return flags

def libs():
    flags = ['-lpython' + pyver + sys.abiflags]
    flags += getvar('LIBS').split()
    flags += getvar('SYSLIBS').split()
    return flags

def ldflags():
    flags = libs()
    if not getvar('Py_ENALBLE_SHARED'):
        flags.insert(0, '-L' + getvar('LIBPL'))
    if not getvar('PYTHONFRAMEWORK'):
        libs.extend(getvar('LINKFORSHARED').split())
    return flags

def extension_suffix():
    return sysconfig.get_config_var('EXT_SUFFIX')

def abiflags():
    return sys.abiflags

def configdir():
    return sysconfig.get_config_var('LIBPL')
