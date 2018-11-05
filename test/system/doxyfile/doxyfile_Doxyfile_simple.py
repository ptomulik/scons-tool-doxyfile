# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (c) 2018 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import TestSCons
import sys
import os

if sys.platform == 'win32':
    test = TestSCons.TestSCons(program='scons.bat', interpreter=None)
else:
    test = TestSCons.TestSCons()

test.subdir('src')
test.subdir('site_scons')
test.subdir(['site_scons', 'site_tools'])
test.subdir(['site_scons', 'site_tools', 'doxyfile'])

test.file_fixture('../../../__init__.py', 'site_scons/site_tools/doxyfile/__init__.py')
test.file_fixture('../../../doxyoptions.py', 'site_scons/site_tools/doxyfile/doxyoptions.py')
test.file_fixture('../../../about.py', 'site_scons/site_tools/doxyfile/about.py')
test.file_fixture('../../../Doxyfile.in', 'src/Doxyfile.in')

test.write('src/test.hpp', r"""\
// src/test.hpp
/**
 * @brief Test class
 */
class TestClass { };
""")

test.write('SConstruct', r"""\
# SConstruct
import sconstool.loader
sconstool.loader.extend_toolpath(transparent=True)
env = Environment(tools=['doxyfile'])
SConscript('src/SConscript', exports=['env'], variant_dir='build', duplicate=0)
""")

test.write('src/SConscript', r"""\
# src/SConscript
Import(['env'])
doxyfile = env.Doxyfile(INPUT='.', RECURSIVE=True)
""")

test.run()  # nothing should happen .. but it happens unfortunatelly
test.must_not_exist('src/Doxyfile')
test.must_exist('build/Doxyfile')
test.must_contain('build/Doxyfile', '"My Project"')


test.run(['-c'])
test.must_not_exist('build/Doxyfile')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
