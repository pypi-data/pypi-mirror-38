#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Michel Mooij, michel.mooij7@gmail.com

import os
import platform

import waflib
from waflib import Scripting, Errors, Logs, Utils, Context

import wtools

def options(opt):
    opt.add_option('--debug', dest='debug', default=False, action='store_true', help='debug build')
    opt.add_option('--eroot', dest='eroot', default=None, help='base path to external dependencies')
    opt.add_option('--sysroot', dest='sysroot', default=None, help='cross-compile toolchain sysroot')
    opt.load('compiler_c')
    opt.load('compiler_cxx')
    opt.load('eclipse_waf', tooldir=wtools.location) #TODO: merge changes into waf/waflib/Tools/extras/eclipse?
    opt.load('eclipse_make', tooldir=wtools.location)
    opt.load('make', tooldir=wtools.location)
    opt.load('indent', tooldir=wtools.location)
    opt.load('tree', tooldir=wtools.location)
    opt.load('pkg', tooldir=wtools.location)
    opt.load('bundle', tooldir=wtools.location)


def configure(conf):
    conf.check_waf_version(mini='1.9.9')
    conf.load('compiler_c')
    conf.load('compiler_cxx')
    conf.load('eclipse_waf')
    conf.load('eclipse_make')
    conf.load('make')
    conf.load('indent')
    conf.load('tree')
    conf.load('pkg')
    conf.load('bundle')
    
    eroot = os.getenv('EROOT')
    if conf.options.eroot:
        eroot = conf.options.eroot
    if eroot and os.path.exists(eroot):
        conf.env.EROOT = os.path.abspath(eroot)

    sysroot = os.getenv('SYSROOT')
    if conf.options.sysroot:
        sysroot = conf.options.sysroot
    if sysroot and os.path.exists(sysroot):
        conf.env.SYSROOT = os.path.abspath(sysroot)

    configure_cc(conf)
    configure_defines(conf)
    configure_includes(conf)
    configure_libdirs(conf)


def configure_cc(conf):
    if conf.env.CC_NAME == 'gcc':
        cflags = ['-Wall', '-pthread']
        if conf.options.debug:
            cflags.extend(['-g', '-ggdb'])
        else:
            cflags.extend(['-O3'])
    
        for cc in ('CFLAGS', 'CXXFLAGS'):
            for cflag in cflags:
                conf.env.append_unique(cc, cflag)


def configure_defines(conf):
    if conf.options.debug:
        defines = []
    else:
        defines = ['NDEBUG']

    for define in defines:
        conf.env.append_unique('DEFINES', define)


def configure_includes(conf):
    includes = []
    conf.env.append_unique('INCLUDES', os.path.join(conf.env.PREFIX, 'include'))

    if conf.env.EROOT:
        includes.append(os.path.join(conf.env.EROOT,'include'))

    for include in includes:
        if os.path.exists(include):
            conf.env.prepend_value('INCLUDES', include)


def configure_libdirs(conf):
    libdirs = []

    for root in (conf.env.SYSROOT, conf.env.EROOT):
        if not root:
            continue
        for lib in ('lib64', 'lib'):
            for path in (lib, os.path.join('usr', lib), os.path.join('usr', 'local', lib)):
                libdirs.append(os.path.join(root, path))

    for libdir in libdirs:
        if os.path.exists(libdir):
            conf.env.prepend_value('LIBPATH', libdir)
    

def post(bld):
    if bld.env.DEST_CPU != platform.machine():
        return

    if 'linux' not in bld.env.DEST_OS:
        return

    if bld.cmd != "install":
        return

    try:
        bld.exec_command('/sbin/ldconfig')
    except:
        pass
