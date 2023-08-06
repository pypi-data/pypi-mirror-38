import os
from ctypes import *
import inspect, re

class c_long_p(object):
    @classmethod
    def from_param(self, param):
        assert param.typecode == 'l'
        return cast(param.buffer_info()[0], POINTER(c_long))

class c_int_p(object):
    @classmethod
    def from_param(self, param):
        assert param.typecode == 'i'
        return cast(param.buffer_info()[0], POINTER(c_int))

class c_double_p(object):
    @classmethod
    def from_param(self, param):
        assert param.typecode == 'd'
        return cast(param.buffer_info()[0], POINTER(c_double))

def mtime(fn):
    try:
        return os.stat(fn)[8]
    except OSError:
        return -1

def cfile(fns,cflags='',ldflags=''):

    if isinstance(fns,str):
        fns=(fns,)

    frm=inspect.currentframe().f_back
    d=os.path.dirname(frm.f_code.co_filename)

    fbase=fns[0][:-2]
    la='lib'+fbase+'.la'
    so=os.path.join(d, 'lib'+fbase+'.so.0.0.0')
    ltso=os.path.join('.libs', 'lib'+fbase+'.so.0.0.0')

    # Allow modules to be install without source
    for fn in fns:
        if os.path.exists(fn):
            break
    else:
        for f in os.listdir(d):
            if f.startswith('lib'+fbase+'.'):
                installed_so = os.path.join(d, f)
                if os.path.exists(installed_so):
                    return CDLL(installed_so)

    # Recompiled changed files
    link=False
    los=''
    for i,fn in enumerate(fns):
        assert fn[-2:]=='.c'
        fbase=fn[:-2]
        lo=os.path.join(d, fbase+'.lo')
        los+=lo+" "
        c =os.path.join(d, fbase+'.c')

        if mtime(lo) <= mtime(c):
            ret=os.system('libtool --mode=compile gcc -o '+lo+' '+cflags+
                          ' -c '+c)
            if ret!=0:
                if os.path.exists(c):
                    raise ImportError("Compilation of "+c+" failed.")
                continue
            link=True

        if link:
            ret=os.system('libtool --mode=link gcc -o '+la+' '+los+' '+ldflags+
                          ' -version-info 0:0:0 -rpath /usr/lib/')
            try:
                os.unlink(so)
            except OSError:
                pass
            os.link(ltso, so)
            if ret!=0: raise ImportError("Linking of "+c+" failed.")

    return CDLL(so)
