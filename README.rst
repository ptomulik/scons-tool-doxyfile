scons-tool-doxyfile
===================

.. image:: https://badge.fury.io/py/scons-tool-doxyfile.svg
    :target: https://badge.fury.io/py/scons-tool-doxyfile
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-doxyfile.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-doxyfile
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-doxyfile?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-doxyfile

SCons_ tool to generate Doxyfile for Doxygen_. The generated Doxyfile may be
further used by scons_doxygen_ tool.


Installation
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add doxyfile tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-doxyfile

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-doxyfile

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-doxyfile = "*"


The tool will be installed as a namespaced package ``sconstool.doxyfile``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-doxyfile`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-doxyfile.git site_scons/site_tools/doxyfile

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.doxyfile`` (this may be required by other tools).

Usage example
-------------

Git-based projects
^^^^^^^^^^^^^^^^^^

#. Copy doxygen template to ``src/``, for example::

      mkdir src && cp site_scons/site_tools/doxyfile/Doxyfile.in src/

#. Create some source files, for example ``src/test.hpp``:

   .. code-block:: cpp

      // src/test.hpp
      /**
       * @brief Test class
       */
      class TestClass { };

#. Write ``SConstruct`` file:

   .. code-block:: python

      # SConstruct
      env = Environment(tools=['doxyfile', 'doxygen'])
      SConscript('src/SConscript', exports=['env'], variant_dir='build', duplicate=0)

#. Write ``src/SConscript``:

   .. code-block:: python

      # src/SConscript
      Import(['env'])
      doxyfile = env.Doxyfile( INPUT = '.', RECURSIVE = True)
      env.Doxygen(doxyfile)

#. Try it out::

      scons

   This shall create documentation under ``build`` directory.

#. Check the generated documentation (it should contain docs for ``TestClass``
   under ``Classes`` tab)::

      firefox build/html/index.html

Details
-------

Module contents and description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The **scons-tool-doxyfile** contains these crucial files:

* ``__init__.py``, ``doxyoptions.py`` and ``about.py`` files,
* ``Doxyfile.in`` template,
* ``SConstruct`` script, and
* this ``README.rst``

The tool provides a ``Doxyfile()`` builder which generates ``Doxyfile``
configuration file from ``Doxyfile.in`` template. It accepts several *options*
to customize the generated ``Doxyfile``. The options are passed as keyword
arguments to ``Doxyfile``:

.. code-block:: python

   env.Doxyfile(INPUT='.', RECURSIVE=True, STRIP_FROM_INC_PATH='.', ...)

Same template may be used to generate documentation for several sub-projects by
using different sets of options (and variant builds, if necessary).
You may also use your own template file, instead of default ``Doxyfile.in``
shipped along with this tool.

Option types
^^^^^^^^^^^^

The options ``Doxyfile()`` builder accepts are categorized into several types:

+---------------+--------------------------+----------------------------+----------------------------+
| Type          | Note                     | Example value in SConscript| Example output to Doxyfile |
+===============+==========================+============================+============================+
| *int*         | integer                  | 3                          | 3                          |
+---------------+--------------------------+----------------------------+----------------------------+
| *str*         | string                   | 'str1' or 'str 2'          | str1 or "str 2"            |
+---------------+--------------------------+----------------------------+----------------------------+
| *list*        | list                     | ['a b', False, 3]          | "a b" False 3              |
+---------------+--------------------------+----------------------------+----------------------------+
| *dict*        | dictionary               | {'a' : 'A', 'b' : 'B'}     | a=A b=B                    |
+---------------+--------------------------+----------------------------+----------------------------+
| *bool*        | boolean                  | True or False              | YES or NO                  |
+---------------+--------------------------+----------------------------+----------------------------+
| *entry*       | ref to file or directory | 'foo'                      | /tmp/prj/build/foo         |
+---------------+--------------------------+----------------------------+----------------------------+
| *file*        | ref to file              | 'bar.txt'                  | /tmp/prj/build/bar.txt     |
+---------------+--------------------------+----------------------------+----------------------------+
| *dir*         | ref to directory         | '.'                        | /tmp/prj/build             |
+---------------+--------------------------+----------------------------+----------------------------+
| *srcentry*    | ref to source file or dir| 'foo'                      | /tmp/prj/src/foo           |
+---------------+--------------------------+----------------------------+----------------------------+
| *srcfile*     | ref to source file       | 'foo.txt'                  | /tmp/prj/src/foo.txt       |
+---------------+--------------------------+----------------------------+----------------------------+
| *srcdir*      | ref to source directory  | '.'                        | /tmp/prj/src               |
+---------------+--------------------------+----------------------------+----------------------------+
| *dualentry*   | ref to entry + its source| 'foo'                      | | /tmp/prj/build/foo \\    |
|               |                          |                            | | /tmp/prj/src/foo         |
+---------------+--------------------------+----------------------------+----------------------------+
| *dualfile*    | ref to file + its source | 'foo.txt'                  | | /tmp/prj/build/foo.txt \\|
|               |                          |                            | | /tmp/prj/src/foo.txt     |
+---------------+--------------------------+----------------------------+----------------------------+
| *dualdir*     | ref to dir + its source  | '.'                        | | /tmp/prj/build \\        |
|               |                          |                            | | /tmp/prj/src             |
+---------------+--------------------------+----------------------------+----------------------------+
| *entries*     | list of entries          | ['foo', 'bar/gez']         | | /tmp/prj/build/foo \\    |
|               |                          |                            | | /tmp/prj/build/bar/geez  |
+---------------+--------------------------+----------------------------+----------------------------+
| *files*       | list of files            | ['foo', 'bar.txt']         | | /tmp/prj/build/foo \\    |
|               |                          |                            | | /tmp/prj/build/bar.txt   |
+---------------+--------------------------+----------------------------+----------------------------+
| *dirs*        | list of directories      | ['.', 'foo']               | | /tmp/prj/build \\        |
|               |                          |                            | | /tmp/prj/build/foo       |
+---------------+--------------------------+----------------------------+----------------------------+
| *srcentries*  | list of source entries   | ['.', 'foo']               | | /tmp/prj/src \\          |
|               |                          |                            | | /tmp/prj/src/foo         |
+---------------+--------------------------+----------------------------+----------------------------+
| *srcfiles*    | list of source files     | ['a.txt', 'b.txt']         | | /tmp/prj/src/a.txt \\    |
|               |                          |                            | | /tmp/prj/src/b.txt       |
+---------------+--------------------------+----------------------------+----------------------------+
| *srcdirs*     | list of source dirs      | ['.', 'foo']               | | /tmp/prj/src \\          |
|               |                          |                            | | /tmp/prj/src/foo         |
+---------------+--------------------------+----------------------------+----------------------------+
| *dualentries* | list of dual entries     | ['.', 'foo']               | | /tmp/prj/build \\        |
|               |                          |                            | | /tmp/prj/src \\          |
|               |                          |                            | | /tmp/prj/build/foo \\    |
|               |                          |                            | | /tmp/prj/src/foo         |
+---------------+--------------------------+----------------------------+----------------------------+
| *dualfiles*   | list of dual files       | ['a.txt', 'b.txt']         | | /tmp/prj/build/a.txt \\  |
|               |                          |                            | | /tmp/prj/src/a.txt \\    |
|               |                          |                            | | /tmp/prj/build/b.txt \\  |
|               |                          |                            | | /tmp/prj/src/b.txt       |
+---------------+--------------------------+----------------------------+----------------------------+
| *dualdirs*    | list of dual directories | ['.', 'foo']               | | /tmp/prj/build \\        |
|               |                          |                            | | /tmp/prj/src \\          |
|               |                          |                            | | /tmp/prj/build/foo \\    |
|               |                          |                            | | /tmp/prj/src/foo         |
+---------------+--------------------------+----------------------------+----------------------------+

An *entry* is a path to file or directory (undecided). For each value of type
*entry*, *file* or *dir* a single path is outputted to Doxyfile. If
relative paths are provided by user, they are assumed to be relative to a
directory containing the calling ``SConscript``. Note, that ``SCons`` will
write absolute paths to Doxyfile, so you should consider using
``STRIP_FROM_PATH``, ``STRIP_FROM_INC_PATH`` and similar options.

In variant builds, the *entry*, *file* and *directory*, if given as
relative paths,  will point to a file or subdirectory of build dir.

A *srcentry*, *srcfile*, or *srcdir* will generate a path pointing to a
source file or directory corresponding to given file. This, of course, becomes
relevant when variant builds are used.

Dual entry, file (or directory) results with a single path or two
paths being emitted to Doxyfile. For variant builds, pair of paths is written
to Doxyfile: the first one in build dir and the second pointing to a
corresponding source file or dir.

The values written to Doxyfile are automatically quoted if they contain
white spaces. For example, the hash ``{'a' : 'be ce'}`` will result with
``a="be ce"``.

Values being assigned to Doxyfile options are subject of simple validation.

Supported options
^^^^^^^^^^^^^^^^^

The supported options are summarized in the following table:

======================== ========== =====================================
Option                   Type       Default
======================== ========== =====================================
ABBREVIATE_BRIEF_        str
ALIASES_                 str
ALLEXTERNALS_            bool       NO
ALPHABETICAL_INDEX_      bool       YES
ALWAYS_DETAILED_SEC_     bool       NO
AUTOLINK_SUPPORT_        bool       YES
BINARY_TOC_              bool       NO
BRIEF_MEMBER_DESC_       bool       YES
BUILTIN_STL_SUPPORT_     bool       NO
CALLER_GRAPH_            bool       NO
CALL_GRAPH_              bool       NO
CASE_SENSE_NAMES_        bool       *OS specific*
CHM_FILE_                srcfile
CHM_INDEX_ENCODING_      str
CITE_BIB_FILES_          files
CLANG_ASSISTED_PARSING_  bool       NO
CLANG_OPTIONS_           str
CLASS_DIAGRAMS_          bool       YES
CLASS_GRAPH_             bool       YES
COLLABORATION_GRAPH_     bool       YES
COLS_IN_ALPHA_INDEX_     str
COMPACT_LATEX_           bool       NO
COMPACT_RTF_             bool       NO
CPP_CLI_SUPPORT_         bool       NO
CREATE_SUBDIRS_          bool       NO
DIRECTORY_GRAPH_         bool       YES
DISABLE_INDEX_           bool       NO
DISTRIBUTE_GROUP_DOC_    bool       NO
DOCBOOK_OUTPUT_          dir
DOCSET_BUNDLE_ID_        str        org.doxygen.Project
DOCSET_FEEDNAME_         str        "Doxygen generated docs"
DOCSET_PUBLISHER_ID_     str        org.doxygen.Publisher
DOCSET_PUBLISHER_NAME_   str        Publisher
DOTFILE_DIRS_            srcdirs
DOT_CLEANUP_             bool       YES
DOT_FONTNAME_            str        Helvetica
DOT_FONTPATH_            srcdir
DOT_FONTSIZE_            int        10
DOT_GRAPH_MAX_NODES_     int        50
DOT_IMAGE_FORMAT_        str        png
DOT_MULTI_TARGETS_       bool       NO
DOT_NUM_THREADS_         int        0
DOT_PATH_                str
DOT_TRANSPARENT_         bool       NO
DOXYFILE_ENCODING_       str        UTF-8
ECLIPSE_DOC_ID_          str        org.doxygen.Project
ENABLED_SECTIONS_        str
ENABLE_PREPROCESSING_    bool       YES
ENUM_VALUES_PER_LINE_    int        4
EXAMPLE_PATH_            srcdirs
EXAMPLE_PATTERNS_        str
EXAMPLE_RECURSIVE_       bool       NO
EXCLUDE_                 srcdirs
EXCLUDE_PATTERNS_        str
EXCLUDE_SYMBOLS_         str
EXCLUDE_SYMLINKS_        bool       NO
EXPAND_AS_DEFINED_       list
EXPAND_ONLY_PREDEF_      bool       NO
EXTENSION_MAPPING_       str
EXTERNAL_GROUPS_         bool       YES
EXTERNAL_PAGES_          bool       YES
EXTERNAL_SEARCH_         bool       NO
EXTERNAL_SEARCH_ID_      str
EXTRACT_ALL_             bool       NO
EXTRACT_ANON_NSPACES_    bool       NO
EXTRACT_LOCAL_CLASSES_   bool       YES
EXTRACT_LOCAL_METHODS_   bool       NO
EXTRACT_PACKAGE_         bool       NO
EXTRACT_PRIVATE_         bool       NO
EXTRACT_STATIC_          bool       NO
EXTRA_PACKAGES_          str
EXTRA_SEARCH_MAPPINGS_   str
EXT_LINKS_IN_WINDOW_     bool       NO
FILE_PATTERNS_           str
FILE_VERSION_FILTER_     str
FILTER_PATTERNS_         dict
FILTER_SOURCE_FILES_     bool       NO
FILTER_SOURCE_PATTERNS_  dict
FORCE_LOCAL_INCLUDES_    bool       NO
FORMULA_FONTSIZE_        int        10
FORMULA_TRANSPARENT_     bool       YES
FULL_PATH_NAMES_         bool       YES
GENERATE_AUTOGEN_DEF_    bool       NO
GENERATE_BUGLIST_        bool       YES
GENERATE_CHI_            bool       NO
GENERATE_DEPRECATEDLIST_ bool       YES
GENERATE_DOCBOOK_        bool       NO
GENERATE_DOCSET_         bool       NO
GENERATE_ECLIPSEHELP_    bool       NO
GENERATE_HTML_           bool       YES
GENERATE_HTMLHELP_       bool       NO
GENERATE_LATEX_          bool       YES
GENERATE_LEGEND_         bool       YES
GENERATE_MAN_            bool       NO
GENERATE_PERLMOD_        bool       NO
GENERATE_QHP_            bool       NO
GENERATE_RTF_            bool       NO
GENERATE_TAGFILE_        file
GENERATE_TESTLIST_       bool       YES
GENERATE_TODOLIST_       bool       YES
GENERATE_TREEVIEW_       bool       NO
GENERATE_XML_            bool       NO
GRAPHICAL_HIERARCHY_     bool       YES
GROUP_GRAPHS_            bool       YES
HAVE_DOT_                bool       NO
HHC_LOCATION_            str
HIDE_FRIEND_COMPOUNDS_   bool       NO
HIDE_IN_BODY_DOCS_       bool       NO
HIDE_SCOPE_NAMES_        bool       NO
HIDE_UNDOC_CLASSES_      bool       NO
HIDE_UNDOC_MEMBERS_      bool       NO
HIDE_UNDOC_RELATIONS_    bool       YES
HTML_COLORSTYLE_GAMMA_   int        80
HTML_COLORSTYLE_HUE_     int        220
HTML_COLORSTYLE_SAT_     int        100
HTML_DYNAMIC_SECTIONS_   bool       NO
HTML_EXTRA_FILES_        srcfiles
HTML_EXTRA_STYLESHEET_   srcfile
HTML_FILE_EXTENSION_     str        .html
HTML_FOOTER_             srcfile
HTML_HEADER_             srcfile
HTML_INDEX_NUM_ENTRIES_  int        100
HTML_OUTPUT_             str        html
HTML_STYLESHEET_         srcfile
HTML_TIMESTAMP_          bool       YES
IDL_PROPERTY_SUPPORT_    bool       YES
IGNORE_PREFIX_           str
IMAGE_PATH_              srcdirs
INCLUDED_BY_GRAPH_       bool       YES
INCLUDE_FILE_PATTERNS_   str
INCLUDE_GRAPH_           bool       YES
INCLUDE_PATH_            srcdirs
INHERIT_DOCS_            bool       YES
INLINE_GROUPED_CLASSES_  bool       NO
INLINE_INFO_             bool       YES
INLINE_INHERITED_MEMB_   bool       NO
INLINE_SIMPLE_STRUCTS_   bool       NO
INLINE_SOURCES_          bool       NO
INPUT_                   srcentries
INPUT_ENCODING_          str        UTF-8
INPUT_FILTER_            str
INTERACTIVE_SVG_         bool       NO
INTERNAL_DOCS_           bool       NO
JAVADOC_AUTOBRIEF_       bool       NO
LATEX_BATCHMODE_         bool       NO
LATEX_BIB_STYLE_         str
LATEX_CMD_NAME_          str        latex
LATEX_EXTRA_FILES_       srcfiles
LATEX_FOOTER_            srcfile
LATEX_HEADER_            srcfile
LATEX_HIDE_INDICES_      bool       NO
LATEX_OUTPUT_            str        latex
LATEX_SOURCE_CODE_       bool       NO
LAYOUT_FILE_             srcfile
LOOKUP_CACHE_SIZE_       int        0
MACRO_EXPANSION_         bool       NO
MAKEINDEX_CMD_NAME_      str        makeindex
MAN_EXTENSION_           str        .3
MAN_LINKS_               bool       NO
MAN_OUTPUT_              str        man
MARKDOWN_SUPPORT_        bool       YES
MATHJAX_CODEFILE_        srcfile
MATHJAX_EXTENSIONS_      str
MATHJAX_FORMAT_          str        HTML-CSS
MATHJAX_RELPATH_         str        http://cdn.mathjax.org/mathjax/latest
MAX_DOT_GRAPH_DEPTH_     int        0
MAX_INITIALIZER_LINES_   int        30
MSCFILE_DIRS_            dirs
MSCGEN_PATH_             str
MULTILINE_CPP_IS_BRIEF_  bool       NO
OPTIMIZE_FOR_FORTRAN_    bool       NO
OPTIMIZE_OUTPUT_FOR_C_   bool       NO
OPTIMIZE_OUTPUT_JAVA_    bool       NO
OPTIMIZE_OUTPUT_VHDL_    bool       NO
OUTPUT_DIRECTORY_        dir
OUTPUT_LANGUAGE_         str        English
PAPER_TYPE_              str        a4
PDF_HYPERLINKS_          bool       YES
PERLMOD_LATEX_           bool       NO
PERLMOD_MAKEVAR_PREFIX_  str
PERLMOD_PRETTY_          bool       YES
PERL_PATH_               str        /usr/bin/perl
PREDEFINED_              list
PROJECT_BRIEF_           str
PROJECT_LOGO_            str
PROJECT_NAME_            str        "My Project"
PROJECT_NUMBER_          str
QCH_FILE_                str
QHG_LOCATION_            str
QHP_CUST_FILTER_ATTRS_   str
QHP_CUST_FILTER_NAME_    str
QHP_NAMESPACE_           str
QHP_SECT_FILTER_ATTRS_   str
QHP_VIRTUAL_FOLDER_      str        doc
QT_AUTOBRIEF_            bool       NO
QUIET_                   bool       NO
RECURSIVE_               bool       NO
REFERENCED_BY_RELATION_  bool       NO
REFERENCES_LINK_SOURCE_  bool       YES
REFERENCES_RELATION_     bool       NO
REPEAT_BRIEF_            bool       YES
RTF_EXTENSIONS_FILE_     file
RTF_HYPERLINKS_          bool       NO
RTF_OUTPUT_              str        rtf
RTF_STYLESHEET_FILE_     file
SEARCHDATA_FILE_         str        searchdata.xml
SEARCHENGINE_            bool       YES
SEARCHENGINE_URL_        str
SEARCH_INCLUDES_         bool       YES
SEPARATE_MEMBER_PAGES_   bool       NO
SERVER_BASED_SEARCH_     bool       NO
SHORT_NAMES_             bool       NO
SHOW_FILES_              bool       YES
SHOW_INCLUDE_FILES_      bool       YES
SHOW_NAMESPACES_         bool       YES
SHOW_USED_FILES_         bool       YES
SIP_SUPPORT_             bool       NO
SKIP_FUNCTION_MACROS_    bool       YES
SORT_BRIEF_DOCS_         bool       NO
SORT_BY_SCOPE_NAME_      bool       NO
SORT_GROUP_NAMES_        bool       NO
SORT_MEMBERS_CTORS_1ST_  bool       NO
SORT_MEMBER_DOCS_        bool       YES
SOURCE_BROWSER_          bool       NO
SOURCE_TOOLTIPS_         bool       YES
STRICT_PROTO_MATCHING_   bool       NO
STRIP_CODE_COMMENTS_     bool       YES
STRIP_FROM_INC_PATH_     srcdirs
STRIP_FROM_PATH_         srcdirs
SUBGROUPING_             bool       YES
TAB_SIZE_                int        4
TAGFILES_                str
TCL_SUBST_               str
TEMPLATE_RELATIONS_      bool       NO
TOC_EXPAND_              bool       NO
TREEVIEW_WIDTH_          int        250
TYPEDEF_HIDES_STRUCT_    bool       NO
UML_LIMIT_NUM_FIELDS_    int        10
UML_LOOK_                bool       NO
USE_HTAGS_               bool       NO
USE_MATHJAX_             bool       NO
USE_MDFILE_AS_MAINPAGE_  srcfile
USE_PDFLATEX_            bool       YES
VERBATIM_HEADERS_        bool       YES
WARNINGS_                bool       YES
WARN_FORMAT_             str        "$file:$line: $text"
WARN_IF_DOC_ERROR_       bool       YES
WARN_IF_UNDOCUMENTED_    bool       YES
WARN_LOGFILE_            file
WARN_NO_PARAMDOC_        bool       NO
XML_DTD_                 str
XML_OUTPUT_              str        xml
XML_PROGRAMLISTING_      bool       YES
XML_SCHEMA_              str
======================== ========== =====================================

.. _ABBREVIATE_BRIEF: http://doxygen.org/manual/config.html#cfg_abbreviate_brief
.. _ALIASES: http://doxygen.org/manual/config.html#cfg_aliases
.. _ALLEXTERNALS: http://doxygen.org/manual/config.html#cfg_allexternals
.. _ALPHABETICAL_INDEX: http://doxygen.org/manual/config.html#cfg_alphabetical_index
.. _ALWAYS_DETAILED_SEC: http://doxygen.org/manual/config.html#cfg_always_detailed_sec
.. _AUTOLINK_SUPPORT: http://doxygen.org/manual/config.html#cfg_autolink_support
.. _BINARY_TOC: http://doxygen.org/manual/config.html#cfg_binary_toc
.. _BRIEF_MEMBER_DESC: http://doxygen.org/manual/config.html#cfg_brief_member_desc
.. _BUILTIN_STL_SUPPORT: http://doxygen.org/manual/config.html#cfg_builtin_stl_support
.. _CALLER_GRAPH: http://doxygen.org/manual/config.html#cfg_caller_graph
.. _CALL_GRAPH: http://doxygen.org/manual/config.html#cfg_call_graph
.. _CASE_SENSE_NAMES: http://doxygen.org/manual/config.html#cfg_case_sense_names
.. _CHM_FILE: http://doxygen.org/manual/config.html#cfg_chm_file
.. _CHM_INDEX_ENCODING: http://doxygen.org/manual/config.html#cfg_chm_index_encoding
.. _CITE_BIB_FILES: http://doxygen.org/manual/config.html#cfg_cite_bib_files
.. _CLANG_ASSISTED_PARSING: http://doxygen.org/manual/config.html#cfg_clang_assisted_parsing
.. _CLANG_OPTIONS: http://doxygen.org/manual/config.html#cfg_clang_options
.. _CLASS_DIAGRAMS: http://doxygen.org/manual/config.html#cfg_class_diagrams
.. _CLASS_GRAPH: http://doxygen.org/manual/config.html#cfg_class_graph
.. _COLLABORATION_GRAPH: http://doxygen.org/manual/config.html#cfg_collaboration_graph
.. _COLS_IN_ALPHA_INDEX: http://doxygen.org/manual/config.html#cfg_cols_in_alpha_index
.. _COMPACT_LATEX: http://doxygen.org/manual/config.html#cfg_compact_latex
.. _COMPACT_RTF: http://doxygen.org/manual/config.html#cfg_compact_rtf
.. _CPP_CLI_SUPPORT: http://doxygen.org/manual/config.html#cfg_cpp_cli_support
.. _CREATE_SUBDIRS: http://doxygen.org/manual/config.html#cfg_create_subdirs
.. _DIRECTORY_GRAPH: http://doxygen.org/manual/config.html#cfg_directory_graph
.. _DISABLE_INDEX: http://doxygen.org/manual/config.html#cfg_disable_index
.. _DISTRIBUTE_GROUP_DOC: http://doxygen.org/manual/config.html#cfg_distribute_group_doc
.. _DOCBOOK_OUTPUT: http://doxygen.org/manual/config.html#cfg_docbook_output
.. _DOCSET_BUNDLE_ID: http://doxygen.org/manual/config.html#cfg_docset_bundle_id
.. _DOCSET_FEEDNAME: http://doxygen.org/manual/config.html#cfg_docset_feedname
.. _DOCSET_PUBLISHER_ID: http://doxygen.org/manual/config.html#cfg_docset_publisher_id
.. _DOCSET_PUBLISHER_NAME: http://doxygen.org/manual/config.html#cfg_docset_publisher_name
.. _DOTFILE_DIRS: http://doxygen.org/manual/config.html#cfg_dotfile_dirs
.. _DOT_CLEANUP: http://doxygen.org/manual/config.html#cfg_dot_cleanup
.. _DOT_FONTNAME: http://doxygen.org/manual/config.html#cfg_dot_fontname
.. _DOT_FONTPATH: http://doxygen.org/manual/config.html#cfg_dot_fontpath
.. _DOT_FONTSIZE: http://doxygen.org/manual/config.html#cfg_dot_fontsize
.. _DOT_GRAPH_MAX_NODES: http://doxygen.org/manual/config.html#cfg_dot_graph_max_nodes
.. _DOT_IMAGE_FORMAT: http://doxygen.org/manual/config.html#cfg_dot_image_format
.. _DOT_MULTI_TARGETS: http://doxygen.org/manual/config.html#cfg_dot_multi_targets
.. _DOT_NUM_THREADS: http://doxygen.org/manual/config.html#cfg_dot_num_threads
.. _DOT_PATH: http://doxygen.org/manual/config.html#cfg_dot_path
.. _DOT_TRANSPARENT: http://doxygen.org/manual/config.html#cfg_dot_transparent
.. _DOXYFILE_ENCODING: http://doxygen.org/manual/config.html#cfg_doxyfile_encoding
.. _ECLIPSE_DOC_ID: http://doxygen.org/manual/config.html#cfg_eclipse_doc_id
.. _ENABLED_SECTIONS: http://doxygen.org/manual/config.html#cfg_enabled_sections
.. _ENABLE_PREPROCESSING: http://doxygen.org/manual/config.html#cfg_enable_preprocessing
.. _ENUM_VALUES_PER_LINE: http://doxygen.org/manual/config.html#cfg_enum_values_per_line
.. _EXAMPLE_PATH: http://doxygen.org/manual/config.html#cfg_example_path
.. _EXAMPLE_PATTERNS: http://doxygen.org/manual/config.html#cfg_example_patterns
.. _EXAMPLE_RECURSIVE: http://doxygen.org/manual/config.html#cfg_example_recursive
.. _EXCLUDE: http://doxygen.org/manual/config.html#cfg_exclude
.. _EXCLUDE_PATTERNS: http://doxygen.org/manual/config.html#cfg_exclude_patterns
.. _EXCLUDE_SYMBOLS: http://doxygen.org/manual/config.html#cfg_exclude_symbols
.. _EXCLUDE_SYMLINKS: http://doxygen.org/manual/config.html#cfg_exclude_symlinks
.. _EXPAND_AS_DEFINED: http://doxygen.org/manual/config.html#cfg_expand_as_defined
.. _EXPAND_ONLY_PREDEF: http://doxygen.org/manual/config.html#cfg_expand_only_predef
.. _EXTENSION_MAPPING: http://doxygen.org/manual/config.html#cfg_extension_mapping
.. _EXTERNAL_GROUPS: http://doxygen.org/manual/config.html#cfg_external_groups
.. _EXTERNAL_PAGES: http://doxygen.org/manual/config.html#cfg_external_pages
.. _EXTERNAL_SEARCH: http://doxygen.org/manual/config.html#cfg_external_search
.. _EXTERNAL_SEARCH_ID: http://doxygen.org/manual/config.html#cfg_external_search_id
.. _EXTRACT_ALL: http://doxygen.org/manual/config.html#cfg_extract_all
.. _EXTRACT_ANON_NSPACES: http://doxygen.org/manual/config.html#cfg_extract_anon_nspaces
.. _EXTRACT_LOCAL_CLASSES: http://doxygen.org/manual/config.html#cfg_extract_local_classes
.. _EXTRACT_LOCAL_METHODS: http://doxygen.org/manual/config.html#cfg_extract_local_methods
.. _EXTRACT_PACKAGE: http://doxygen.org/manual/config.html#cfg_extract_package
.. _EXTRACT_PRIVATE: http://doxygen.org/manual/config.html#cfg_extract_private
.. _EXTRACT_STATIC: http://doxygen.org/manual/config.html#cfg_extract_static
.. _EXTRA_PACKAGES: http://doxygen.org/manual/config.html#cfg_extra_packages
.. _EXTRA_SEARCH_MAPPINGS: http://doxygen.org/manual/config.html#cfg_extra_search_mappings
.. _EXT_LINKS_IN_WINDOW: http://doxygen.org/manual/config.html#cfg_ext_links_in_window
.. _FILE_PATTERNS: http://doxygen.org/manual/config.html#cfg_file_patterns
.. _FILE_VERSION_FILTER: http://doxygen.org/manual/config.html#cfg_file_version_filter
.. _FILTER_PATTERNS: http://doxygen.org/manual/config.html#cfg_filter_patterns
.. _FILTER_SOURCE_FILES: http://doxygen.org/manual/config.html#cfg_filter_source_files
.. _FILTER_SOURCE_PATTERNS: http://doxygen.org/manual/config.html#cfg_filter_source_patterns
.. _FORCE_LOCAL_INCLUDES: http://doxygen.org/manual/config.html#cfg_force_local_includes
.. _FORMULA_FONTSIZE: http://doxygen.org/manual/config.html#cfg_formula_fontsize
.. _FORMULA_TRANSPARENT: http://doxygen.org/manual/config.html#cfg_formula_transparent
.. _FULL_PATH_NAMES: http://doxygen.org/manual/config.html#cfg_full_path_names
.. _GENERATE_AUTOGEN_DEF: http://doxygen.org/manual/config.html#cfg_generate_autogen_def
.. _GENERATE_BUGLIST: http://doxygen.org/manual/config.html#cfg_generate_buglist
.. _GENERATE_CHI: http://doxygen.org/manual/config.html#cfg_generate_chi
.. _GENERATE_DEPRECATEDLIST: http://doxygen.org/manual/config.html#cfg_generate_deprecatedlist
.. _GENERATE_DOCBOOK: http://doxygen.org/manual/config.html#cfg_generate_docbook
.. _GENERATE_DOCSET: http://doxygen.org/manual/config.html#cfg_generate_docset
.. _GENERATE_ECLIPSEHELP: http://doxygen.org/manual/config.html#cfg_generate_eclipsehelp
.. _GENERATE_HTML: http://doxygen.org/manual/config.html#cfg_generate_html
.. _GENERATE_HTMLHELP: http://doxygen.org/manual/config.html#cfg_generate_htmlhelp
.. _GENERATE_LATEX: http://doxygen.org/manual/config.html#cfg_generate_latex
.. _GENERATE_LEGEND: http://doxygen.org/manual/config.html#cfg_generate_legend
.. _GENERATE_MAN: http://doxygen.org/manual/config.html#cfg_generate_man
.. _GENERATE_PERLMOD: http://doxygen.org/manual/config.html#cfg_generate_perlmod
.. _GENERATE_QHP: http://doxygen.org/manual/config.html#cfg_generate_qhp
.. _GENERATE_RTF: http://doxygen.org/manual/config.html#cfg_generate_rtf
.. _GENERATE_TAGFILE: http://doxygen.org/manual/config.html#cfg_generate_tagfile
.. _GENERATE_TESTLIST: http://doxygen.org/manual/config.html#cfg_generate_testlist
.. _GENERATE_TODOLIST: http://doxygen.org/manual/config.html#cfg_generate_todolist
.. _GENERATE_TREEVIEW: http://doxygen.org/manual/config.html#cfg_generate_treeview
.. _GENERATE_XML: http://doxygen.org/manual/config.html#cfg_generate_xml
.. _GRAPHICAL_HIERARCHY: http://doxygen.org/manual/config.html#cfg_graphical_hierarchy
.. _GROUP_GRAPHS: http://doxygen.org/manual/config.html#cfg_group_graphs
.. _HAVE_DOT: http://doxygen.org/manual/config.html#cfg_have_dot
.. _HHC_LOCATION: http://doxygen.org/manual/config.html#cfg_hhc_location
.. _HIDE_FRIEND_COMPOUNDS: http://doxygen.org/manual/config.html#cfg_hide_friend_compounds
.. _HIDE_IN_BODY_DOCS: http://doxygen.org/manual/config.html#cfg_hide_in_body_docs
.. _HIDE_SCOPE_NAMES: http://doxygen.org/manual/config.html#cfg_hide_scope_names
.. _HIDE_UNDOC_CLASSES: http://doxygen.org/manual/config.html#cfg_hide_undoc_classes
.. _HIDE_UNDOC_MEMBERS: http://doxygen.org/manual/config.html#cfg_hide_undoc_members
.. _HIDE_UNDOC_RELATIONS: http://doxygen.org/manual/config.html#cfg_hide_undoc_relations
.. _HTML_COLORSTYLE_GAMMA: http://doxygen.org/manual/config.html#cfg_html_colorstyle_gamma
.. _HTML_COLORSTYLE_HUE: http://doxygen.org/manual/config.html#cfg_html_colorstyle_hue
.. _HTML_COLORSTYLE_SAT: http://doxygen.org/manual/config.html#cfg_html_colorstyle_sat
.. _HTML_DYNAMIC_SECTIONS: http://doxygen.org/manual/config.html#cfg_html_dynamic_sections
.. _HTML_EXTRA_FILES: http://doxygen.org/manual/config.html#cfg_html_extra_files
.. _HTML_EXTRA_STYLESHEET: http://doxygen.org/manual/config.html#cfg_html_extra_stylesheet
.. _HTML_FILE_EXTENSION: http://doxygen.org/manual/config.html#cfg_html_file_extension
.. _HTML_FOOTER: http://doxygen.org/manual/config.html#cfg_html_footer
.. _HTML_HEADER: http://doxygen.org/manual/config.html#cfg_html_header
.. _HTML_INDEX_NUM_ENTRIES: http://doxygen.org/manual/config.html#cfg_html_index_num_entries
.. _HTML_OUTPUT: http://doxygen.org/manual/config.html#cfg_html_output
.. _HTML_STYLESHEET: http://doxygen.org/manual/config.html#cfg_html_stylesheet
.. _HTML_TIMESTAMP: http://doxygen.org/manual/config.html#cfg_html_timestamp
.. _IDL_PROPERTY_SUPPORT: http://doxygen.org/manual/config.html#cfg_idl_property_support
.. _IGNORE_PREFIX: http://doxygen.org/manual/config.html#cfg_ignore_prefix
.. _IMAGE_PATH: http://doxygen.org/manual/config.html#cfg_image_path
.. _INCLUDED_BY_GRAPH: http://doxygen.org/manual/config.html#cfg_included_by_graph
.. _INCLUDE_FILE_PATTERNS: http://doxygen.org/manual/config.html#cfg_include_file_patterns
.. _INCLUDE_GRAPH: http://doxygen.org/manual/config.html#cfg_include_graph
.. _INCLUDE_PATH: http://doxygen.org/manual/config.html#cfg_include_path
.. _INHERIT_DOCS: http://doxygen.org/manual/config.html#cfg_inherit_docs
.. _INLINE_GROUPED_CLASSES: http://doxygen.org/manual/config.html#cfg_inline_grouped_classes
.. _INLINE_INFO: http://doxygen.org/manual/config.html#cfg_inline_info
.. _INLINE_INHERITED_MEMB: http://doxygen.org/manual/config.html#cfg_inline_inherited_memb
.. _INLINE_SIMPLE_STRUCTS: http://doxygen.org/manual/config.html#cfg_inline_simple_structs
.. _INLINE_SOURCES: http://doxygen.org/manual/config.html#cfg_inline_sources
.. _INPUT: http://doxygen.org/manual/config.html#cfg_input
.. _INPUT_ENCODING: http://doxygen.org/manual/config.html#cfg_input_encoding
.. _INPUT_FILTER: http://doxygen.org/manual/config.html#cfg_input_filter
.. _INTERACTIVE_SVG: http://doxygen.org/manual/config.html#cfg_interactive_svg
.. _INTERNAL_DOCS: http://doxygen.org/manual/config.html#cfg_internal_docs
.. _JAVADOC_AUTOBRIEF: http://doxygen.org/manual/config.html#cfg_javadoc_autobrief
.. _LATEX_BATCHMODE: http://doxygen.org/manual/config.html#cfg_latex_batchmode
.. _LATEX_BIB_STYLE: http://doxygen.org/manual/config.html#cfg_latex_bib_style
.. _LATEX_CMD_NAME: http://doxygen.org/manual/config.html#cfg_latex_cmd_name
.. _LATEX_EXTRA_FILES: http://doxygen.org/manual/config.html#cfg_latex_extra_files
.. _LATEX_FOOTER: http://doxygen.org/manual/config.html#cfg_latex_footer
.. _LATEX_HEADER: http://doxygen.org/manual/config.html#cfg_latex_header
.. _LATEX_HIDE_INDICES: http://doxygen.org/manual/config.html#cfg_latex_hide_indices
.. _LATEX_OUTPUT: http://doxygen.org/manual/config.html#cfg_latex_output
.. _LATEX_SOURCE_CODE: http://doxygen.org/manual/config.html#cfg_latex_source_code
.. _LAYOUT_FILE: http://doxygen.org/manual/config.html#cfg_layout_file
.. _LOOKUP_CACHE_SIZE: http://doxygen.org/manual/config.html#cfg_lookup_cache_size
.. _MACRO_EXPANSION: http://doxygen.org/manual/config.html#cfg_macro_expansion
.. _MAKEINDEX_CMD_NAME: http://doxygen.org/manual/config.html#cfg_makeindex_cmd_name
.. _MAN_EXTENSION: http://doxygen.org/manual/config.html#cfg_man_extension
.. _MAN_LINKS: http://doxygen.org/manual/config.html#cfg_man_links
.. _MAN_OUTPUT: http://doxygen.org/manual/config.html#cfg_man_output
.. _MARKDOWN_SUPPORT: http://doxygen.org/manual/config.html#cfg_markdown_support
.. _MATHJAX_CODEFILE: http://doxygen.org/manual/config.html#cfg_mathjax_codefile
.. _MATHJAX_EXTENSIONS: http://doxygen.org/manual/config.html#cfg_mathjax_extensions
.. _MATHJAX_FORMAT: http://doxygen.org/manual/config.html#cfg_mathjax_format
.. _MATHJAX_RELPATH: http://doxygen.org/manual/config.html#cfg_mathjax_relpath
.. _MAX_DOT_GRAPH_DEPTH: http://doxygen.org/manual/config.html#cfg_max_dot_graph_depth
.. _MAX_INITIALIZER_LINES: http://doxygen.org/manual/config.html#cfg_max_initializer_lines
.. _MSCFILE_DIRS: http://doxygen.org/manual/config.html#cfg_mscfile_dirs
.. _MSCGEN_PATH: http://doxygen.org/manual/config.html#cfg_mscgen_path
.. _MULTILINE_CPP_IS_BRIEF: http://doxygen.org/manual/config.html#cfg_multiline_cpp_is_brief
.. _OPTIMIZE_FOR_FORTRAN: http://doxygen.org/manual/config.html#cfg_optimize_for_fortran
.. _OPTIMIZE_OUTPUT_FOR_C: http://doxygen.org/manual/config.html#cfg_optimize_output_for_c
.. _OPTIMIZE_OUTPUT_JAVA: http://doxygen.org/manual/config.html#cfg_optimize_output_java
.. _OPTIMIZE_OUTPUT_VHDL: http://doxygen.org/manual/config.html#cfg_optimize_output_vhdl
.. _OUTPUT_DIRECTORY: http://doxygen.org/manual/config.html#cfg_output_directory
.. _OUTPUT_LANGUAGE: http://doxygen.org/manual/config.html#cfg_output_language
.. _PAPER_TYPE: http://doxygen.org/manual/config.html#cfg_paper_type
.. _PDF_HYPERLINKS: http://doxygen.org/manual/config.html#cfg_pdf_hyperlinks
.. _PERLMOD_LATEX: http://doxygen.org/manual/config.html#cfg_perlmod_latex
.. _PERLMOD_MAKEVAR_PREFIX: http://doxygen.org/manual/config.html#cfg_perlmod_makevar_prefix
.. _PERLMOD_PRETTY: http://doxygen.org/manual/config.html#cfg_perlmod_pretty
.. _PERL_PATH: http://doxygen.org/manual/config.html#cfg_perl_path
.. _PREDEFINED: http://doxygen.org/manual/config.html#cfg_predefined
.. _PROJECT_BRIEF: http://doxygen.org/manual/config.html#cfg_project_brief
.. _PROJECT_LOGO: http://doxygen.org/manual/config.html#cfg_project_logo
.. _PROJECT_NAME: http://doxygen.org/manual/config.html#cfg_project_name
.. _PROJECT_NUMBER: http://doxygen.org/manual/config.html#cfg_project_number
.. _QCH_FILE: http://doxygen.org/manual/config.html#cfg_qch_file
.. _QHG_LOCATION: http://doxygen.org/manual/config.html#cfg_qhg_location
.. _QHP_CUST_FILTER_ATTRS: http://doxygen.org/manual/config.html#cfg_qhp_cust_filter_attrs
.. _QHP_CUST_FILTER_NAME: http://doxygen.org/manual/config.html#cfg_qhp_cust_filter_name
.. _QHP_NAMESPACE: http://doxygen.org/manual/config.html#cfg_qhp_namespace
.. _QHP_SECT_FILTER_ATTRS: http://doxygen.org/manual/config.html#cfg_qhp_sect_filter_attrs
.. _QHP_VIRTUAL_FOLDER: http://doxygen.org/manual/config.html#cfg_qhp_virtual_folder
.. _QT_AUTOBRIEF: http://doxygen.org/manual/config.html#cfg_qt_autobrief
.. _QUIET: http://doxygen.org/manual/config.html#cfg_quiet
.. _RECURSIVE: http://doxygen.org/manual/config.html#cfg_recursive
.. _REFERENCED_BY_RELATION: http://doxygen.org/manual/config.html#cfg_referenced_by_relation
.. _REFERENCES_LINK_SOURCE: http://doxygen.org/manual/config.html#cfg_references_link_source
.. _REFERENCES_RELATION: http://doxygen.org/manual/config.html#cfg_references_relation
.. _REPEAT_BRIEF: http://doxygen.org/manual/config.html#cfg_repeat_brief
.. _RTF_EXTENSIONS_FILE: http://doxygen.org/manual/config.html#cfg_rtf_extensions_file
.. _RTF_HYPERLINKS: http://doxygen.org/manual/config.html#cfg_rtf_hyperlinks
.. _RTF_OUTPUT: http://doxygen.org/manual/config.html#cfg_rtf_output
.. _RTF_STYLESHEET_FILE: http://doxygen.org/manual/config.html#cfg_rtf_stylesheet_file
.. _SEARCHDATA_FILE: http://doxygen.org/manual/config.html#cfg_searchdata_file
.. _SEARCHENGINE: http://doxygen.org/manual/config.html#cfg_searchengine
.. _SEARCHENGINE_URL: http://doxygen.org/manual/config.html#cfg_searchengine_url
.. _SEARCH_INCLUDES: http://doxygen.org/manual/config.html#cfg_search_includes
.. _SEPARATE_MEMBER_PAGES: http://doxygen.org/manual/config.html#cfg_separate_member_pages
.. _SERVER_BASED_SEARCH: http://doxygen.org/manual/config.html#cfg_server_based_search
.. _SHORT_NAMES: http://doxygen.org/manual/config.html#cfg_short_names
.. _SHOW_FILES: http://doxygen.org/manual/config.html#cfg_show_files
.. _SHOW_INCLUDE_FILES: http://doxygen.org/manual/config.html#cfg_show_include_files
.. _SHOW_NAMESPACES: http://doxygen.org/manual/config.html#cfg_show_namespaces
.. _SHOW_USED_FILES: http://doxygen.org/manual/config.html#cfg_show_used_files
.. _SIP_SUPPORT: http://doxygen.org/manual/config.html#cfg_sip_support
.. _SKIP_FUNCTION_MACROS: http://doxygen.org/manual/config.html#cfg_skip_function_macros
.. _SORT_BRIEF_DOCS: http://doxygen.org/manual/config.html#cfg_sort_brief_docs
.. _SORT_BY_SCOPE_NAME: http://doxygen.org/manual/config.html#cfg_sort_by_scope_name
.. _SORT_GROUP_NAMES: http://doxygen.org/manual/config.html#cfg_sort_group_names
.. _SORT_MEMBERS_CTORS_1ST: http://doxygen.org/manual/config.html#cfg_sort_members_ctors_1st
.. _SORT_MEMBER_DOCS: http://doxygen.org/manual/config.html#cfg_sort_member_docs
.. _SOURCE_BROWSER: http://doxygen.org/manual/config.html#cfg_source_browser
.. _SOURCE_TOOLTIPS: http://doxygen.org/manual/config.html#cfg_source_tooltips
.. _STRICT_PROTO_MATCHING: http://doxygen.org/manual/config.html#cfg_strict_proto_matching
.. _STRIP_CODE_COMMENTS: http://doxygen.org/manual/config.html#cfg_strip_code_comments
.. _STRIP_FROM_INC_PATH: http://doxygen.org/manual/config.html#cfg_strip_from_inc_path
.. _STRIP_FROM_PATH: http://doxygen.org/manual/config.html#cfg_strip_from_path
.. _SUBGROUPING: http://doxygen.org/manual/config.html#cfg_subgrouping
.. _TAB_SIZE: http://doxygen.org/manual/config.html#cfg_tab_size
.. _TAGFILES: http://doxygen.org/manual/config.html#cfg_tagfiles
.. _TCL_SUBST: http://doxygen.org/manual/config.html#cfg_tcl_subst
.. _TEMPLATE_RELATIONS: http://doxygen.org/manual/config.html#cfg_template_relations
.. _TOC_EXPAND: http://doxygen.org/manual/config.html#cfg_toc_expand
.. _TREEVIEW_WIDTH: http://doxygen.org/manual/config.html#cfg_treeview_width
.. _TYPEDEF_HIDES_STRUCT: http://doxygen.org/manual/config.html#cfg_typedef_hides_struct
.. _UML_LIMIT_NUM_FIELDS: http://doxygen.org/manual/config.html#cfg_uml_limit_num_fields
.. _UML_LOOK: http://doxygen.org/manual/config.html#cfg_uml_look
.. _USE_HTAGS: http://doxygen.org/manual/config.html#cfg_use_htags
.. _USE_MATHJAX: http://doxygen.org/manual/config.html#cfg_use_mathjax
.. _USE_MDFILE_AS_MAINPAGE: http://doxygen.org/manual/config.html#cfg_use_mdfile_as_mainpage
.. _USE_PDFLATEX: http://doxygen.org/manual/config.html#cfg_use_pdflatex
.. _VERBATIM_HEADERS: http://doxygen.org/manual/config.html#cfg_verbatim_headers
.. _WARNINGS: http://doxygen.org/manual/config.html#cfg_warnings
.. _WARN_FORMAT: http://doxygen.org/manual/config.html#cfg_warn_format
.. _WARN_IF_DOC_ERROR: http://doxygen.org/manual/config.html#cfg_warn_if_doc_error
.. _WARN_IF_UNDOCUMENTED: http://doxygen.org/manual/config.html#cfg_warn_if_undocumented
.. _WARN_LOGFILE: http://doxygen.org/manual/config.html#cfg_warn_logfile
.. _WARN_NO_PARAMDOC: http://doxygen.org/manual/config.html#cfg_warn_no_paramdoc
.. _XML_DTD: http://doxygen.org/manual/config.html#cfg_xml_dtd
.. _XML_OUTPUT: http://doxygen.org/manual/config.html#cfg_xml_output
.. _XML_PROGRAMLISTING: http://doxygen.org/manual/config.html#cfg_xml_programlisting
.. _XML_SCHEMA: http://doxygen.org/manual/config.html#cfg_xml_schema

.. <!-- Other links -->
.. _SCons: http://scons.org
.. _Doxygen: http://doxygen.org
.. _scons_doxygen: https://bitbucket.org/russel/scons_doxygen
.. _scons-doxygen-template: https://github.com/ptomulik/scons-doxygen-template
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/

Notes to developers
-------------------

Regenerating documentation for options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you change some options in ``doxyoptions.py``, then you should regenerate
option's documentation in ``README.rst``. New documentation may be generated by
running::

    scons -Q doc-options

After that, copy-paste the output of the above command to an appropriate place
in this ``README.rst`` (note, just skip scons messages).

LICENSE
-------

Copyright (c) 2013-2018 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. <!--- vim: set expandtab tabstop=2 shiftwidth=2 syntax=rst: -->
