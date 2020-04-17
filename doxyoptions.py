# -*- coding: utf-8 -*-
"""`doxyoptions`
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
# Factory method

try:
    _int_types = (int, long)
except NameError:
    _int_types = (int,)

def DoxyVal(env, val, kind=None, **kw):
    import SCons.Util
    import SCons.Errors
    _class_map = {
        'int'           : DoxyValInt,
        'str'           : DoxyValStr,
        'list'          : DoxyValList,
        'dict'          : DoxyValDict,
        'bool'          : DoxyValBool,
        'entry'         : DoxyValEntry,
        'file'          : DoxyValFile,
        'dir'           : DoxyValDir,
        'srcentry'      : DoxyValSrcEntry,
        'srcfile'       : DoxyValSrcFile,
        'srcdir'        : DoxyValSrcDir,
        'dualentry'     : DoxyValDualEntry,
        'dualfile'      : DoxyValDualFile,
        'dualdir'       : DoxyValDualDir,
        'entries'       : DoxyValEntries,
        'files'         : DoxyValFiles,
        'dirs'          : DoxyValDirs,
        'srcentries'    : DoxyValSrcEntries,
        'srcfiles'      : DoxyValSrcFiles,
        'srcdirs'       : DoxyValSrcDirs,
        'dualentries'   : DoxyValDualEntries,
        'dualfiles'     : DoxyValDualFiles,
        'dualdirs'      : DoxyValDualDirs,
    }
    if kind is None:
        kind = type(val).__name__.lower()
    if kind is None:
        raise SCons.Errors.UserError("can not create doxygen option with no type")
    if not SCons.Util.is_String(kind):
        kind = kind.__name__.lower()
    try:
        klass = _class_map[kind]
    except KeyError:
        raise SCons.Errors.UserError("can not create doxygen option of type %s" % kind)
    return klass(env,val,**kw)


class DoxyValBase(object):
    def __init__(self, env, value=None, **kw):
        self._env = env
        self._kw = { 'ssep' : self.default_ssep(),
                     'dsep' : self.default_dsep(),
                     'quot' : self.default_quot() }
        self._kw.update(kw)
        self.assign(value)

    @classmethod
    def default_ssep(cls):
        return ' '
    @classmethod
    def default_dsep(cls):
        return '='
    @classmethod
    def default_quot(cls):
        return lambda s :  "\"%s\"" % s
    @classmethod
    def kind(cls):
        import re
        return re.sub(r'^DoxyVal', '', cls.__name__).lower()
    def assign(self, val):
        if val is None: self._value = val
        else: self._assign(val)
    def _assign(self, val):
        raise NotImplementedError
    def __str__(self):
        return ('' if self._value is None else self._str())
    def _str(self):
        raise NotImplementedError

class DoxyValStr(DoxyValBase):
    def _assign(self,val):
        import SCons.Util
        import SCons.Errors
        if not SCons.Util.is_String(val):
            raise SCons.Errors.UserError("can not set doxygen option of string type to %r" % val)
        self._value = val
    def _str(self):
        return  self._str_str("%s" % self._value)
    def _str_str(self,s):
        import re
        return (self._kw['quot'](s) if re.search(r'\s',s) else s)

class DoxyValInt(DoxyValBase):
    def _assign(self, val):
        import SCons.Util
        import SCons.Errors
        global _int_types
        if not isinstance(val, _int_types):
            raise SCons.Errors.UserError("can not set doxygen option of type int to %r" % val)
        self._value = val
    def _str(self):
        return "%s" % self._value

class DoxyValBool(DoxyValBase):
    def _assign(self, val):
        import SCons.Errors
        if val == 'YES': val = True
        elif val == 'NO': val = False
        if not isinstance(val, bool) and not isinstance(val, _int_types):
            raise SCons.Errors.UserError("can not set doxygen option of type bool to %r" % val)
        self._value = bool(val)
    def _str(self):
        return ('YES' if self._value else 'NO')

class DoxyValSeq(DoxyValBase):
    def _str_seq(self,seq):
        return self._kw['ssep'].join([('' if x is None else "%s" % x) for x in seq])

class DoxyValList(DoxyValSeq):
    def _assign(self, val):
        import SCons.Util
        if SCons.Util.is_Sequence(val):
            pass
        elif SCons.Util.is_Scalar(val):
            val = [val]
        else:
            raise SCons.Errors.UserError("can not set doxygen option of type list to %r" % val)
        self._value = [DoxyVal(self._env, v, self.item_kind(), **self._kw) for v in val]
    @classmethod
    def item_kind(cls):
        return None # deduce type ...
    def _str(self):
        return super(DoxyValList,self)._str_seq(self._value)

class DoxyValDict(DoxyValSeq):
    def _assign(self, val):
        import SCons.Util
        import SCons.Errors
        if not isinstance(val, dict):
            raise SCons.Errors.UserError("can not set doxygen option of type int to %r" % val)
        self._value = dict([(k,DoxyVal(self._env, v, **self._kw)) for k,v in val.items()])
    def _str(self):
        f = lambda k,v : "%s%s%s" % (k, self._kw['dsep'], ('' if v is None else v))
        items = [f(k,v) for (k,v) in self._value.items()]
        return super(DoxyValDict,self)._str_seq(items)

class DoxyValFsList(DoxyValList):
    @classmethod
    def default_ssep(cls):
        return " \\\n"
    @classmethod
    def item_kind(cls):
        raise NotImplementedError # force subclasses to show their item types

class DoxyValFsBase(DoxyValStr):
    def _assign(self, val):
        import SCons.Util
        import SCons.Errors
        import SCons.Node.FS
        if isinstance(val, SCons.Node.FS.Base):
            self._fs_assign(val)
        elif SCons.Util.is_String(val):
            self._fs_assign(self._fs_create(val))
        else:
            raise SCons.Errors.UserError("can not set doxygen option of type %s to %r" % (self.kind(),val))
    def _str(self):
        import sys
        if sys.platform == 'win32':
            return self._str_str(self._value.get_abspath().replace('\\', '\\\\'))
        else:
            return self._str_str(self._value.get_abspath())
    def _fs_assign(self,val):
        self._value = val
    def _fs_create(self,val):
        raise NotImplementedError

class DoxyValFsSrcBase(DoxyValFsBase):
    def _fs_assign(self, val):
        self._value = val.srcnode()

class DoxyValFsDualBase(DoxyValFsList):
    def _assign(self, val):
        import SCons.Util
        import SCons.Node.FS
        if isinstance(val,SCons.Node.FS.Base):
            pass
        elif SCons.Util.is_String(val):
            val = self._fs_create(val)
        else:
            raise SCons.Errors.UserError("can not set doxygen option of type %s to %r" % (self.kind(),val))
        self._fs_assign(val)
    def _fs_assign(self,val):
        src = val.srcnode()
        ik = self.item_kind()
        vals = [ DoxyVal(self._env, val, ik, **self._kw) ]
        if val != src:
            vals.append(DoxyVal(self._env, src, ik, **self._kw))
        self._value = vals

class DoxyValEntry(DoxyValFsBase):
    def _fs_create(self,val):
        return self._env.Entry(val)

class DoxyValFile(DoxyValFsBase):
    def _fs_create(self,val):
        return self._env.File(val)

class DoxyValDir(DoxyValFsBase):
    def _fs_create(self,val):
        return self._env.Dir(val)

class DoxyValSrcEntry(DoxyValFsSrcBase):
    def _fs_create(self,val):
        return self._env.Entry(val).srcnode()

class DoxyValSrcFile(DoxyValFsSrcBase):
    def _fs_create(self,val):
        return self._env.File(val).srcnode()

class DoxyValSrcDir(DoxyValFsSrcBase):
    def _fs_create(self,val):
        return self._env.Dir(val).srcnode()

class DoxyValDualEntry(DoxyValFsDualBase):
    @classmethod
    def item_kind(cls):
        return 'entry'
    def _fs_create(self,val):
        return self._env.Entry(val)

class DoxyValDualFile(DoxyValFsDualBase):
    @classmethod
    def item_kind(cls):
        return 'file'
    def _fs_create(self,val):
        return self._env.File(val)

class DoxyValDualDir(DoxyValFsDualBase):
    @classmethod
    def item_kind(cls):
        return 'dir'
    def _fs_create(self,val):
        return self._env.Dir(val)

class DoxyValEntries(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'entry'

class DoxyValFiles(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'file'

class DoxyValDirs(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'dir'

class DoxyValSrcEntries(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'srcentry'

class DoxyValSrcFiles(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'srcfile'

class DoxyValSrcDirs(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'srcdir'

class DoxyValDualEntries(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'dualentry'

class DoxyValDualFiles(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'dualfile'

class DoxyValDualDirs(DoxyValFsList):
    @classmethod
    def item_kind(cls):
        return 'dualdir'

def doxyoptions(env):
    import os;
    # NOTE: this may sometimes give wrong result, but I have no better idea how
    # to determine case sensitiveness, some people say, that this gives wrong
    # answer on Mac OS for example (I don't have one to test it)
    #
    # See also:
    # http://stackoverflow.com/questions/7870041/check-if-file-system-is-case-insensitive-in-python
    case_sense_names = (os.path.normcase('A') != os.path.normcase('a'))
    opts = {
        'ABBREVIATE_BRIEF'          : DoxyVal(env, ''),
        'ALIASES'                   : DoxyVal(env, ''),
        'ALLEXTERNALS'              : DoxyVal(env, False),
        'ALPHABETICAL_INDEX'        : DoxyVal(env, True),
        'ALWAYS_DETAILED_SEC'       : DoxyVal(env, False),
        'AUTOLINK_SUPPORT'          : DoxyVal(env, True),
        'BINARY_TOC'                : DoxyVal(env, False),
        'BRIEF_MEMBER_DESC'         : DoxyVal(env, True),
        'BUILTIN_STL_SUPPORT'       : DoxyVal(env, False),
        'CALLER_GRAPH'              : DoxyVal(env, False),
        'CALL_GRAPH'                : DoxyVal(env, False),
        'CASE_SENSE_NAMES'          : DoxyVal(env, case_sense_names),
        'CHM_FILE'                  : DoxyVal(env, None, 'file'),
        'CHM_FILE'                  : DoxyVal(env, None, 'srcfile'),
        'CHM_INDEX_ENCODING'        : DoxyVal(env, ''),
        'CITE_BIB_FILES'            : DoxyVal(env, None, 'files'),
        'CLANG_ASSISTED_PARSING'    : DoxyVal(env, False),
        'CLANG_OPTIONS'             : DoxyVal(env, ''),
        'CLASS_DIAGRAMS'            : DoxyVal(env, True),
        'CLASS_GRAPH'               : DoxyVal(env, True),
        'COLLABORATION_GRAPH'       : DoxyVal(env, True),
        'COLS_IN_ALPHA_INDEX'       : DoxyVal(env, ''),
        'COMPACT_LATEX'             : DoxyVal(env, False),
        'COMPACT_RTF'               : DoxyVal(env, False),
        'CPP_CLI_SUPPORT'           : DoxyVal(env, False),
        'CREATE_SUBDIRS'            : DoxyVal(env, False),
        'DIRECTORY_GRAPH'           : DoxyVal(env, True),
        'DISABLE_INDEX'             : DoxyVal(env, False),
        'DISTRIBUTE_GROUP_DOC'      : DoxyVal(env, False),
        'DOCBOOK_OUTPUT'            : DoxyVal(env, None, 'dir'),
        'DOCSET_BUNDLE_ID'          : DoxyVal(env, 'org.doxygen.Project'),
        'DOCSET_FEEDNAME'           : DoxyVal(env, 'Doxygen generated docs'),
        'DOCSET_PUBLISHER_ID'       : DoxyVal(env, 'org.doxygen.Publisher'),
        'DOCSET_PUBLISHER_NAME'     : DoxyVal(env, 'Publisher'),
        'DOTFILE_DIRS'              : DoxyVal(env, None, 'srcdirs'),
        'DOT_CLEANUP'               : DoxyVal(env, True),
        'DOT_FONTNAME'              : DoxyVal(env, 'Helvetica'),
        'DOT_FONTPATH'              : DoxyVal(env, None, 'srcdir'),
        'DOT_FONTSIZE'              : DoxyVal(env, 10),
        'DOT_GRAPH_MAX_NODES'       : DoxyVal(env, 50),
        'DOT_IMAGE_FORMAT'          : DoxyVal(env, 'png'),
        'DOT_MULTI_TARGETS'         : DoxyVal(env, False),
        'DOT_NUM_THREADS'           : DoxyVal(env, 0),
        'DOT_PATH'                  : DoxyVal(env, ''),
        'DOT_TRANSPARENT'           : DoxyVal(env, False),
        'DOXYFILE_ENCODING'         : DoxyVal(env, 'UTF-8'),
        'ECLIPSE_DOC_ID'            : DoxyVal(env, 'org.doxygen.Project'),
        'ENABLED_SECTIONS'          : DoxyVal(env, ''),
        'ENABLE_PREPROCESSING'      : DoxyVal(env, True),
        'ENUM_VALUES_PER_LINE'      : DoxyVal(env, 4),
        'EXAMPLE_PATH'              : DoxyVal(env, None, 'srcdirs'),
        'EXAMPLE_PATTERNS'          : DoxyVal(env, ''),
        'EXAMPLE_RECURSIVE'         : DoxyVal(env, False),
        'EXCLUDE'                   : DoxyVal(env, None, 'srcdirs'),
        'EXCLUDE_PATTERNS'          : DoxyVal(env, ''),
        'EXCLUDE_SYMBOLS'           : DoxyVal(env, ''),
        'EXCLUDE_SYMLINKS'          : DoxyVal(env, False),
        'EXPAND_AS_DEFINED'         : DoxyVal(env, []),
        'EXPAND_ONLY_PREDEF'        : DoxyVal(env, False),
        'EXTENSION_MAPPING'         : DoxyVal(env, ''),
        'EXTERNAL_GROUPS'           : DoxyVal(env, True),
        'EXTERNAL_PAGES'            : DoxyVal(env, True),
        'EXTERNAL_SEARCH'           : DoxyVal(env, False),
        'EXTERNAL_SEARCH_ID'        : DoxyVal(env, ''),
        'EXTRACT_ALL'               : DoxyVal(env, False),
        'EXTRACT_ANON_NSPACES'      : DoxyVal(env, False),
        'EXTRACT_LOCAL_CLASSES'     : DoxyVal(env, True),
        'EXTRACT_LOCAL_METHODS'     : DoxyVal(env, False),
        'EXTRACT_PACKAGE'           : DoxyVal(env, False),
        'EXTRACT_PRIVATE'           : DoxyVal(env, False),
        'EXTRACT_STATIC'            : DoxyVal(env, False),
        'EXTRA_PACKAGES'            : DoxyVal(env, ''),
        'EXTRA_SEARCH_MAPPINGS'     : DoxyVal(env, ''),
        'EXT_LINKS_IN_WINDOW'       : DoxyVal(env, False),
        'FILE_PATTERNS'             : DoxyVal(env, ''),
        'FILE_VERSION_FILTER'       : DoxyVal(env, ''),
        'FILTER_PATTERNS'           : DoxyVal(env, {}),
        'FILTER_SOURCE_FILES'       : DoxyVal(env, False),
        'FILTER_SOURCE_PATTERNS'    : DoxyVal(env, {}),
        'FORCE_LOCAL_INCLUDES'      : DoxyVal(env, False),
        'FORMULA_FONTSIZE'          : DoxyVal(env, 10),
        'FORMULA_TRANSPARENT'       : DoxyVal(env, True),
        'FULL_PATH_NAMES'           : DoxyVal(env, True),
        'GENERATE_AUTOGEN_DEF'      : DoxyVal(env, False),
        'GENERATE_BUGLIST'          : DoxyVal(env, True),
        'GENERATE_CHI'              : DoxyVal(env, False),
        'GENERATE_DEPRECATEDLIST'   : DoxyVal(env, True),
        'GENERATE_DOCBOOK'          : DoxyVal(env, False),
        'GENERATE_DOCSET'           : DoxyVal(env, False),
        'GENERATE_ECLIPSEHELP'      : DoxyVal(env, False),
        'GENERATE_HTML'             : DoxyVal(env, True),
        'GENERATE_HTMLHELP'         : DoxyVal(env, False),
        'GENERATE_LATEX'            : DoxyVal(env, True),
        'GENERATE_LEGEND'           : DoxyVal(env, True),
        'GENERATE_MAN'              : DoxyVal(env, False),
        'GENERATE_PERLMOD'          : DoxyVal(env, False),
        'GENERATE_QHP'              : DoxyVal(env, False),
        'GENERATE_RTF'              : DoxyVal(env, False),
        'GENERATE_TAGFILE'          : DoxyVal(env, None, 'file'),
        'GENERATE_TESTLIST'         : DoxyVal(env, True),
        'GENERATE_TODOLIST'         : DoxyVal(env, True),
        'GENERATE_TREEVIEW'         : DoxyVal(env, False),
        'GENERATE_XML'              : DoxyVal(env, False),
        'GRAPHICAL_HIERARCHY'       : DoxyVal(env, True),
        'GROUP_GRAPHS'              : DoxyVal(env, True),
        'HAVE_DOT'                  : DoxyVal(env, False),
        'HHC_LOCATION'              : DoxyVal(env, ''),
        'HIDE_FRIEND_COMPOUNDS'     : DoxyVal(env, False),
        'HIDE_IN_BODY_DOCS'         : DoxyVal(env, False),
        'HIDE_SCOPE_NAMES'          : DoxyVal(env, False),
        'HIDE_UNDOC_CLASSES'        : DoxyVal(env, False),
        'HIDE_UNDOC_MEMBERS'        : DoxyVal(env, False),
        'HIDE_UNDOC_RELATIONS'      : DoxyVal(env, True),
        'HTML_COLORSTYLE_GAMMA'     : DoxyVal(env, 80),
        'HTML_COLORSTYLE_HUE'       : DoxyVal(env, 220),
        'HTML_COLORSTYLE_SAT'       : DoxyVal(env, 100),
        'HTML_DYNAMIC_SECTIONS'     : DoxyVal(env, False),
        'HTML_EXTRA_FILES'          : DoxyVal(env, None, 'srcfiles'),
        'HTML_EXTRA_STYLESHEET'     : DoxyVal(env, None, 'srcfile'),
        'HTML_FILE_EXTENSION'       : DoxyVal(env, '.html'),
        'HTML_FOOTER'               : DoxyVal(env, None, 'srcfile'),
        'HTML_HEADER'               : DoxyVal(env, None, 'srcfile'),
        'HTML_INDEX_NUM_ENTRIES'    : DoxyVal(env, 100),
        'HTML_OUTPUT'               : DoxyVal(env, 'html'),
        'HTML_STYLESHEET'           : DoxyVal(env, None, 'srcfile'),
        'HTML_TIMESTAMP'            : DoxyVal(env, True),
        'IDL_PROPERTY_SUPPORT'      : DoxyVal(env, True),
        'IGNORE_PREFIX'             : DoxyVal(env, ''),
        'IMAGE_PATH'                : DoxyVal(env, None, 'srcdirs'),
        'INCLUDED_BY_GRAPH'         : DoxyVal(env, True),
        'INCLUDE_FILE_PATTERNS'     : DoxyVal(env, ''),
        'INCLUDE_GRAPH'             : DoxyVal(env, True),
        'INCLUDE_PATH'              : DoxyVal(env, None, 'srcdirs'),
        'INHERIT_DOCS'              : DoxyVal(env, True),
        'INLINE_GROUPED_CLASSES'    : DoxyVal(env, False),
        'INLINE_INFO'               : DoxyVal(env, True),
        'INLINE_INHERITED_MEMB'     : DoxyVal(env, False),
        'INLINE_SIMPLE_STRUCTS'     : DoxyVal(env, False),
        'INLINE_SOURCES'            : DoxyVal(env, False),
        'INPUT'                     : DoxyVal(env, None, 'srcentries'),
        'INPUT_ENCODING'            : DoxyVal(env, 'UTF-8'),
        'INPUT_FILTER'              : DoxyVal(env, ''),
        'INTERACTIVE_SVG'           : DoxyVal(env, False),
        'INTERNAL_DOCS'             : DoxyVal(env, False),
        'JAVADOC_AUTOBRIEF'         : DoxyVal(env, False),
        'LATEX_BATCHMODE'           : DoxyVal(env, False),
        'LATEX_BIB_STYLE'           : DoxyVal(env, ''),
        'LATEX_CMD_NAME'            : DoxyVal(env, 'latex'),
        'LATEX_EXTRA_FILES'         : DoxyVal(env, None, 'srcfiles'),
        'LATEX_FOOTER'              : DoxyVal(env, None, 'srcfile'),
        'LATEX_HEADER'              : DoxyVal(env, None, 'srcfile'),
        'LATEX_HIDE_INDICES'        : DoxyVal(env, False),
        'LATEX_OUTPUT'              : DoxyVal(env, 'latex'),
        'LATEX_SOURCE_CODE'         : DoxyVal(env, False),
        'LAYOUT_FILE'               : DoxyVal(env, None, 'srcfile'),
        'LOOKUP_CACHE_SIZE'         : DoxyVal(env, 0),
        'MACRO_EXPANSION'           : DoxyVal(env, False),
        'MAKEINDEX_CMD_NAME'        : DoxyVal(env, 'makeindex'),
        'MAN_EXTENSION'             : DoxyVal(env, '.3'),
        'MAN_LINKS'                 : DoxyVal(env, False),
        'MAN_OUTPUT'                : DoxyVal(env, 'man'),
        'MARKDOWN_SUPPORT'          : DoxyVal(env, True),
        'MATHJAX_CODEFILE'          : DoxyVal(env, None, 'srcfile'),
        'MATHJAX_EXTENSIONS'        : DoxyVal(env, ''),
        'MATHJAX_FORMAT'            : DoxyVal(env, 'HTML-CSS'),
        'MATHJAX_RELPATH'           : DoxyVal(env, 'http://cdn.mathjax.org/mathjax/latest'),
        'MAX_DOT_GRAPH_DEPTH'       : DoxyVal(env, 0),
        'MAX_INITIALIZER_LINES'     : DoxyVal(env, 30),
        'MSCFILE_DIRS'              : DoxyVal(env, None, 'dirs'),
        'MSCGEN_PATH'               : DoxyVal(env, ''),
        'MULTILINE_CPP_IS_BRIEF'    : DoxyVal(env, False),
        'OPTIMIZE_FOR_FORTRAN'      : DoxyVal(env, False),
        'OPTIMIZE_OUTPUT_FOR_C'     : DoxyVal(env, False),
        'OPTIMIZE_OUTPUT_JAVA'      : DoxyVal(env, False),
        'OPTIMIZE_OUTPUT_VHDL'      : DoxyVal(env, False),
        'OUTPUT_DIRECTORY'          : DoxyVal(env, None, 'dir'),
        'OUTPUT_LANGUAGE'           : DoxyVal(env, 'English'),
        'PAPER_TYPE'                : DoxyVal(env, 'a4'),
        'PDF_HYPERLINKS'            : DoxyVal(env, True),
        'PERLMOD_LATEX'             : DoxyVal(env, False),
        'PERLMOD_MAKEVAR_PREFIX'    : DoxyVal(env, ''),
        'PERLMOD_PRETTY'            : DoxyVal(env, True),
        'PERL_PATH'                 : DoxyVal(env, '/usr/bin/perl'),
        'PREDEFINED'                : DoxyVal(env, []),
        'PROJECT_BRIEF'             : DoxyVal(env, ''),
        'PROJECT_LOGO'              : DoxyVal(env, ''),
        'PROJECT_NAME'              : DoxyVal(env, 'My Project'),
        'PROJECT_NUMBER'            : DoxyVal(env, ''),
        'QCH_FILE'                  : DoxyVal(env, ''),
        'QHG_LOCATION'              : DoxyVal(env, ''),
        'QHP_CUST_FILTER_ATTRS'     : DoxyVal(env, ''),
        'QHP_CUST_FILTER_NAME'      : DoxyVal(env, ''),
        'QHP_NAMESPACE'             : DoxyVal(env, ''),
        'QHP_SECT_FILTER_ATTRS'     : DoxyVal(env, ''),
        'QHP_VIRTUAL_FOLDER'        : DoxyVal(env, 'doc'),
        'QT_AUTOBRIEF'              : DoxyVal(env, False),
        'QUIET'                     : DoxyVal(env, False),
        'RECURSIVE'                 : DoxyVal(env, False),
        'REFERENCED_BY_RELATION'    : DoxyVal(env, False),
        'REFERENCES_LINK_SOURCE'    : DoxyVal(env, True),
        'REFERENCES_RELATION'       : DoxyVal(env, False),
        'REPEAT_BRIEF'              : DoxyVal(env, True),
        'RTF_EXTENSIONS_FILE'       : DoxyVal(env, None, 'file'),
        'RTF_HYPERLINKS'            : DoxyVal(env, False),
        'RTF_OUTPUT'                : DoxyVal(env, 'rtf'),
        'RTF_STYLESHEET_FILE'       : DoxyVal(env, None, 'file'),
        'SEARCHDATA_FILE'           : DoxyVal(env, 'searchdata.xml'),
        'SEARCHENGINE'              : DoxyVal(env, True),
        'SEARCHENGINE_URL'          : DoxyVal(env, ''),
        'SEARCH_INCLUDES'           : DoxyVal(env, True),
        'SEPARATE_MEMBER_PAGES'     : DoxyVal(env, False),
        'SERVER_BASED_SEARCH'       : DoxyVal(env, False),
        'SHORT_NAMES'               : DoxyVal(env, False),
        'SHOW_FILES'                : DoxyVal(env, True),
        'SHOW_INCLUDE_FILES'        : DoxyVal(env, True),
        'SHOW_NAMESPACES'           : DoxyVal(env, True),
        'SHOW_USED_FILES'           : DoxyVal(env, True),
        'SIP_SUPPORT'               : DoxyVal(env, False),
        'SKIP_FUNCTION_MACROS'      : DoxyVal(env, True),
        'SORT_BRIEF_DOCS'           : DoxyVal(env, False),
        'SORT_BY_SCOPE_NAME'        : DoxyVal(env, False),
        'SORT_GROUP_NAMES'          : DoxyVal(env, False),
        'SORT_MEMBERS_CTORS_1ST'    : DoxyVal(env, False),
        'SORT_MEMBER_DOCS'          : DoxyVal(env, True),
        'SOURCE_BROWSER'            : DoxyVal(env, False),
        'SOURCE_TOOLTIPS'           : DoxyVal(env, True),
        'STRICT_PROTO_MATCHING'     : DoxyVal(env, False),
        'STRIP_CODE_COMMENTS'       : DoxyVal(env, True),
        'STRIP_FROM_INC_PATH'       : DoxyVal(env, None, 'srcdirs'),
        'STRIP_FROM_PATH'           : DoxyVal(env, None, 'srcdirs'),
        'SUBGROUPING'               : DoxyVal(env, True),
        'TAB_SIZE'                  : DoxyVal(env, 4),
        'TAGFILES'                  : DoxyVal(env, ''),
        'TCL_SUBST'                 : DoxyVal(env, ''),
        'TEMPLATE_RELATIONS'        : DoxyVal(env, False),
        'TOC_EXPAND'                : DoxyVal(env, False),
        'TREEVIEW_WIDTH'            : DoxyVal(env, 250),
        'TYPEDEF_HIDES_STRUCT'      : DoxyVal(env, False),
        'UML_LIMIT_NUM_FIELDS'      : DoxyVal(env, 10),
        'UML_LOOK'                  : DoxyVal(env, False),
        'USE_HTAGS'                 : DoxyVal(env, False),
        'USE_MATHJAX'               : DoxyVal(env, False),
        'USE_MDFILE_AS_MAINPAGE'    : DoxyVal(env, None, 'srcfile'),
        'USE_PDFLATEX'              : DoxyVal(env, True),
        'VERBATIM_HEADERS'          : DoxyVal(env, True),
        'WARNINGS'                  : DoxyVal(env, True),
        'WARN_FORMAT'               : DoxyVal(env, '$file:$line: $text'),
        'WARN_IF_DOC_ERROR'         : DoxyVal(env, True),
        'WARN_IF_UNDOCUMENTED'      : DoxyVal(env, True),
        'WARN_LOGFILE'              : DoxyVal(env, None, 'file'),
        'WARN_NO_PARAMDOC'          : DoxyVal(env, False),
        'XML_DTD'                   : DoxyVal(env, ''),
        'XML_OUTPUT'                : DoxyVal(env, 'xml'),
        'XML_PROGRAMLISTING'        : DoxyVal(env, True),
        'XML_SCHEMA'                : DoxyVal(env, ''),
    }
    return opts

def generate_doc(env):
    opts = doxyoptions(env)
    table = [ [key, opts[key].kind(), "%s" % opts[key]] for key in sorted(opts.keys())]
    width = lambda n : max([len(r[n]) for r in table])
    widths = [width(i) for i in range(0,3)]
    widths[0] += 1
    fmt = "%%-%ds %%-%ds %%-%ds " % (widths[0],widths[1],widths[2])
    hdr = fmt % tuple('=' * widths[i] for i in range(0,3))
    doc = []
    doc.append(hdr)
    doc.append(fmt % ("Option", "Type", "Default"))
    doc.append(hdr)
    for row in table:
        doc.append(fmt % (row[0] + '_', row[1], row[2]))
    doc.append(hdr)
    doc.append('')
    url = 'http://doxygen.org/manual/config.html#cfg_'
    for row in table:
        doc.append(".. _%s: %s" % (row[0], url+row[0].lower()))
    return "\n".join(doc)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4 nospell:
