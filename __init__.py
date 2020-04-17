# -*- coding: utf-8 -*-
"""`doxyfile`

Tool specific initialization for doxyfile.
"""

#
# Copyright (c) 2013-2020 by Paweł Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

from .about import __version__
from .doxyoptions import *

def Doxyfile(env, target='Doxyfile', *args, **kw):
    import SCons.Util
    import copy
    # build subst-dict
    sd = {}
    for key,val in doxyoptions(env).items():
        placeholder = '@%s@' % key
        sd[placeholder] = copy.copy(val)
        try: sd[placeholder].assign(kw[key])
        except KeyError: pass
    # use builder
    return env.Substfile(target, *args, SUBST_DICT = sd)

def generate(env):
    try:
        env['BUILDERS']['Substfile']
    except KeyError:
        env.Tool('textfile')
    env.AddMethod(Doxyfile,'Doxyfile')

def exists(env):
    return 1

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4 nospell:
