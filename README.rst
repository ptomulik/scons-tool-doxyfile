scons-tool-doxyfile
===================

SCons_ tool to generate Doxyfile for Doxygen_. The generated Doxyfile may be
further used by scons_doxygen_ tool.

Usage example
-------------

Git-based projects
^^^^^^^^^^^^^^^^^^

#. Create new git repository::

      mkdir /tmp/prj && cd /tmp/prj
      touch README.md
      git init

#. Add scons_doxygen_ as submodule (here we use git mirror of scons_doxygen_)::

      git submodule add git://github.com/ptomulik/scons_doxygen.git site_scons/site_tools/doxygen

#. Add scons-tool-doxyfile as submodule::

      git submodule add git://github.com/ptomulik/scons-tool-doxyfile.git site_scons/site_tools/doxyfile

#. Copy doxygen template to ``src/``::

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
      env = Environment(tools = [ 'doxyfile', 'doxygen'])
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

The scons-tool-doxyfile consists of two files:

* ``__init__.py`` file, and
* ``Doxyfile.in`` template.

The tool provides a ``Doxyfile`` builder which generates ``Doxyfile`` from
``Doxyfile.in`` template. It accepts several *options* to customize the
generated ``Doxyfile``. The options are passed as keyword arguments to
``Doxyfile``:

.. code-block:: python

   env.Doxyfile(INPUT = '.', RECURSIVE = True, STRIP_FROM_INC_PATH = '.', ...)

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
DISTRIBUTE_GROUP_DOC_    bool       NO
MAN_LINKS_               bool       NO
GENERATE_BUGLIST_        bool       YES
USE_HTAGS_               bool       NO
BINARY_TOC_              bool       NO
DIRECTORY_GRAPH_         bool       YES
DOT_FONTSIZE_            int        10
DOT_NUM_THREADS_         int        0
ALLEXTERNALS_            bool       NO
EXCLUDE_SYMLINKS_        bool       NO
SOURCE_BROWSER_          bool       NO
EXPAND_AS_DEFINED_       str
DOCBOOK_OUTPUT_          dir
AUTOLINK_SUPPORT_        bool       YES
SEARCHDATA_FILE_         str        searchdata.xml
FILE_VERSION_FILTER_     str
EXTRACT_ANON_NSPACES_    bool       NO
COMPACT_LATEX_           bool       NO
SOURCE_TOOLTIPS_         bool       YES
TEMPLATE_RELATIONS_      bool       NO
OPTIMIZE_FOR_FORTRAN_    bool       NO
OUTPUT_DIRECTORY_        dir
OPTIMIZE_OUTPUT_FOR_C_   bool       NO
HTML_COLORSTYLE_GAMMA_   int        80
ABBREVIATE_BRIEF_        str
HTML_EXTRA_FILES_        srcfiles
LATEX_BATCHMODE_         bool       NO
HIDE_UNDOC_RELATIONS_    bool       YES
DOCSET_BUNDLE_ID_        str        org.doxygen.Project
HTML_FILE_EXTENSION_     str        .html
OUTPUT_LANGUAGE_         str        English
INLINE_GROUPED_CLASSES_  bool       NO
EXTRACT_STATIC_          bool       NO
INCLUDE_GRAPH_           bool       YES
PDF_HYPERLINKS_          bool       YES
GENERATE_DOCBOOK_        bool       NO
EXTRA_SEARCH_MAPPINGS_   str
COLS_IN_ALPHA_INDEX_     str
HIDE_SCOPE_NAMES_        bool       NO
CITE_BIB_FILES_          files
TCL_SUBST_               str
LAYOUT_FILE_             srcfile
OPTIMIZE_OUTPUT_JAVA_    bool       NO
STRIP_FROM_INC_PATH_     srcdirs
EXAMPLE_PATH_            srcdirs
DOT_TRANSPARENT_         bool       NO
HIDE_UNDOC_CLASSES_      bool       NO
TREEVIEW_WIDTH_          int        250
RECURSIVE_               bool       NO
PAPER_TYPE_              str        a4
QHP_CUST_FILTER_NAME_    str
TAB_SIZE_                int        4
HTML_OUTPUT_             str        html
INPUT_                   srcentries
PROJECT_LOGO_            str
INLINE_INHERITED_MEMB_   bool       NO
MAX_INITIALIZER_LINES_   int        30
MAN_OUTPUT_              str        man
IMAGE_PATH_              srcdirs
HTML_FOOTER_             srcfile
INLINE_INFO_             bool       YES
PERLMOD_MAKEVAR_PREFIX_  str
CLASS_DIAGRAMS_          bool       YES
GENERATE_TODOLIST_       bool       YES
MAX_DOT_GRAPH_DEPTH_     int        0
DOCSET_FEEDNAME_         str        "Doxygen generated docs"
GENERATE_PERLMOD_        bool       NO
DOTFILE_DIRS_            srcdirs
CHM_INDEX_ENCODING_      str
RTF_HYPERLINKS_          bool       NO
DOXYFILE_ENCODING_       str        UTF-8
MARKDOWN_SUPPORT_        bool       YES
EXT_LINKS_IN_WINDOW_     bool       NO
QUIET_                   bool       NO
SORT_BRIEF_DOCS_         bool       NO
LATEX_FOOTER_            srcfile
INCLUDED_BY_GRAPH_       bool       YES
XML_OUTPUT_              str        xml
MATHJAX_RELPATH_         str        http://cdn.mathjax.org/mathjax/latest
SEARCHENGINE_URL_        str
GENERATE_LATEX_          bool       YES
XML_SCHEMA_              str
CREATE_SUBDIRS_          bool       NO
GENERATE_DOCSET_         bool       NO
LATEX_SOURCE_CODE_       bool       NO
EXTRACT_PRIVATE_         bool       NO
FILE_PATTERNS_           str
BUILTIN_STL_SUPPORT_     bool       NO
GENERATE_TREEVIEW_       bool       NO
PROJECT_BRIEF_           str
EXTRACT_PACKAGE_         bool       NO
USE_MDFILE_AS_MAINPAGE_  srcfile
QT_AUTOBRIEF_            bool       NO
HIDE_IN_BODY_DOCS_       bool       NO
DOT_MULTI_TARGETS_       bool       NO
VERBATIM_HEADERS_        bool       YES
CALLER_GRAPH_            bool       NO
IGNORE_PREFIX_           str
HIDE_FRIEND_COMPOUNDS_   bool       NO
FILTER_SOURCE_FILES_     bool       NO
EXAMPLE_PATTERNS_        str
ALPHABETICAL_INDEX_      bool       YES
EXAMPLE_RECURSIVE_       bool       NO
UML_LOOK_                bool       NO
GENERATE_QHP_            bool       NO
INCLUDE_FILE_PATTERNS_   str
STRICT_PROTO_MATCHING_   bool       NO
PERL_PATH_               str        /usr/bin/perl
PROJECT_NAME_            str        "My Project"
SEARCH_INCLUDES_         bool       YES
GENERATE_TAGFILE_        file
EXCLUDE_                 srcdirs
LOOKUP_CACHE_SIZE_       int        0
MSCFILE_DIRS_            dirs
DOT_FONTNAME_            str        Helvetica
MAKEINDEX_CMD_NAME_      str        makeindex
BRIEF_MEMBER_DESC_       bool       YES
REFERENCES_RELATION_     bool       NO
MAN_EXTENSION_           str        .3
WARN_IF_UNDOCUMENTED_    bool       YES
INPUT_FILTER_            str
XML_DTD_                 str
LATEX_BIB_STYLE_         str
MATHJAX_CODEFILE_        srcfile
INTERNAL_DOCS_           bool       NO
QCH_FILE_                str
OPTIMIZE_OUTPUT_VHDL_    bool       NO
RTF_OUTPUT_              str        rtf
HHC_LOCATION_            str
MULTILINE_CPP_IS_BRIEF_  bool       NO
HTML_TIMESTAMP_          bool       YES
HTML_HEADER_             srcfile
CASE_SENSE_NAMES_        bool       *OS dependent*
LATEX_HEADER_            srcfile
EXTERNAL_PAGES_          bool       YES
GENERATE_HTMLHELP_       bool       NO
GENERATE_ECLIPSEHELP_    bool       NO
EXTERNAL_GROUPS_         bool       YES
FILTER_PATTERNS_         str
HTML_STYLESHEET_         srcfile
SUBGROUPING_             bool       YES
SORT_MEMBERS_CTORS_1ST_  bool       NO
TAGFILES_                str
PREDEFINED_              str
USE_PDFLATEX_            bool       YES
DOT_GRAPH_MAX_NODES_     int        50
ENUM_VALUES_PER_LINE_    int        4
SORT_GROUP_NAMES_        bool       NO
DOT_IMAGE_FORMAT_        str        png
EXTRACT_LOCAL_METHODS_   bool       NO
DOCSET_PUBLISHER_ID_     str        org.doxygen.Publisher
HTML_DYNAMIC_SECTIONS_   bool       NO
UML_LIMIT_NUM_FIELDS_    int        10
HTML_COLORSTYLE_HUE_     int        220
GENERATE_XML_            bool       NO
CPP_CLI_SUPPORT_         bool       NO
QHP_SECT_FILTER_ATTRS_   str
GROUP_GRAPHS_            bool       YES
SEPARATE_MEMBER_PAGES_   bool       NO
PERLMOD_LATEX_           bool       NO
FORMULA_FONTSIZE_        int        10
ALWAYS_DETAILED_SEC_     bool       NO
EXCLUDE_PATTERNS_        str
EXTERNAL_SEARCH_ID_      str
RTF_EXTENSIONS_FILE_     file
LATEX_EXTRA_FILES_       srcfiles
COMPACT_RTF_             bool       NO
ENABLED_SECTIONS_        str
LATEX_HIDE_INDICES_      bool       NO
SHOW_USED_FILES_         bool       YES
ECLIPSE_DOC_ID_          str        org.doxygen.Project
GRAPHICAL_HIERARCHY_     bool       YES
ALIASES_                 str
HTML_COLORSTYLE_SAT_     int        100
WARN_IF_DOC_ERROR_       bool       YES
GENERATE_RTF_            bool       NO
SERVER_BASED_SEARCH_     bool       NO
CHM_FILE_                srcfile
LATEX_CMD_NAME_          str        latex
QHP_NAMESPACE_           str
FORMULA_TRANSPARENT_     bool       YES
INTERACTIVE_SVG_         bool       NO
XML_PROGRAMLISTING_      bool       YES
GENERATE_CHI_            bool       NO
REFERENCES_LINK_SOURCE_  bool       YES
WARN_LOGFILE_            file
FILTER_SOURCE_PATTERNS_  str
TOC_EXPAND_              bool       NO
GENERATE_LEGEND_         bool       YES
PROJECT_NUMBER_          str
HTML_EXTRA_STYLESHEET_   srcfile
SKIP_FUNCTION_MACROS_    bool       YES
SHOW_FILES_              bool       YES
CLASS_GRAPH_             bool       YES
LATEX_OUTPUT_            str        latex
GENERATE_MAN_            bool       NO
SORT_BY_SCOPE_NAME_      bool       NO
CLANG_OPTIONS_           str
INCLUDE_PATH_            srcdirs
MSCGEN_PATH_             str
DOT_CLEANUP_             bool       YES
MATHJAX_FORMAT_          str        HTML-CSS
INPUT_ENCODING_          str        UTF-8
IDL_PROPERTY_SUPPORT_    bool       YES
FULL_PATH_NAMES_         bool       YES
DISABLE_INDEX_           bool       NO
SIP_SUPPORT_             bool       NO
MACRO_EXPANSION_         bool       NO
EXTRACT_ALL_             bool       NO
WARNINGS_                bool       YES
EXTRACT_LOCAL_CLASSES_   bool       YES
REPEAT_BRIEF_            bool       YES
INLINE_SOURCES_          bool       NO
USE_MATHJAX_             bool       NO
EXTENSION_MAPPING_       str
SHORT_NAMES_             bool       NO
DOT_PATH_                str
RTF_STYLESHEET_FILE_     file
TYPEDEF_HIDES_STRUCT_    bool       NO
PERLMOD_PRETTY_          bool       YES
ENABLE_PREPROCESSING_    bool       YES
JAVADOC_AUTOBRIEF_       bool       NO
STRIP_FROM_PATH_         srcdirs
EXCLUDE_SYMBOLS_         str
HTML_INDEX_NUM_ENTRIES_  int        100
GENERATE_AUTOGEN_DEF_    bool       NO
CLANG_ASSISTED_PARSING_  bool       NO
COLLABORATION_GRAPH_     bool       YES
DOCSET_PUBLISHER_NAME_   str        Publisher
QHP_CUST_FILTER_ATTRS_   str
GENERATE_HTML_           bool       YES
CALL_GRAPH_              bool       NO
GENERATE_DEPRECATEDLIST_ bool       YES
SORT_MEMBER_DOCS_        bool       YES
SHOW_INCLUDE_FILES_      bool       YES
WARN_FORMAT_             str        "$file:$line: $text"
WARN_NO_PARAMDOC_        bool       NO
MATHJAX_EXTENSIONS_      str
EXTERNAL_SEARCH_         bool       NO
GENERATE_TESTLIST_       bool       YES
INLINE_SIMPLE_STRUCTS_   bool       NO
DOT_FONTPATH_            srcdir
REFERENCED_BY_RELATION_  bool       NO
HAVE_DOT_                bool       NO
INHERIT_DOCS_            bool       YES
EXTRA_PACKAGES_          str
HIDE_UNDOC_MEMBERS_      bool       NO
FORCE_LOCAL_INCLUDES_    bool       NO
SHOW_NAMESPACES_         bool       YES
QHP_VIRTUAL_FOLDER_      str        doc
EXPAND_ONLY_PREDEF_      bool       NO
SEARCHENGINE_            bool       YES
STRIP_CODE_COMMENTS_     bool       YES
QHG_LOCATION_            str
======================== ========== =====================================

.. _DISTRIBUTE_GROUP_DOC: http://doxygen.org/manual/config.html#cfg_distribute_group_doc
.. _MAN_LINKS: http://doxygen.org/manual/config.html#cfg_man_links
.. _GENERATE_BUGLIST: http://doxygen.org/manual/config.html#cfg_generate_buglist
.. _USE_HTAGS: http://doxygen.org/manual/config.html#cfg_use_htags
.. _BINARY_TOC: http://doxygen.org/manual/config.html#cfg_binary_toc
.. _DIRECTORY_GRAPH: http://doxygen.org/manual/config.html#cfg_directory_graph
.. _DOT_FONTSIZE: http://doxygen.org/manual/config.html#cfg_dot_fontsize
.. _DOT_NUM_THREADS: http://doxygen.org/manual/config.html#cfg_dot_num_threads
.. _ALLEXTERNALS: http://doxygen.org/manual/config.html#cfg_allexternals
.. _EXCLUDE_SYMLINKS: http://doxygen.org/manual/config.html#cfg_exclude_symlinks
.. _SOURCE_BROWSER: http://doxygen.org/manual/config.html#cfg_source_browser
.. _EXPAND_AS_DEFINED: http://doxygen.org/manual/config.html#cfg_expand_as_defined
.. _DOCBOOK_OUTPUT: http://doxygen.org/manual/config.html#cfg_docbook_output
.. _AUTOLINK_SUPPORT: http://doxygen.org/manual/config.html#cfg_autolink_support
.. _SEARCHDATA_FILE: http://doxygen.org/manual/config.html#cfg_searchdata_file
.. _FILE_VERSION_FILTER: http://doxygen.org/manual/config.html#cfg_file_version_filter
.. _EXTRACT_ANON_NSPACES: http://doxygen.org/manual/config.html#cfg_extract_anon_nspaces
.. _COMPACT_LATEX: http://doxygen.org/manual/config.html#cfg_compact_latex
.. _SOURCE_TOOLTIPS: http://doxygen.org/manual/config.html#cfg_source_tooltips
.. _TEMPLATE_RELATIONS: http://doxygen.org/manual/config.html#cfg_template_relations
.. _OPTIMIZE_FOR_FORTRAN: http://doxygen.org/manual/config.html#cfg_optimize_for_fortran
.. _OUTPUT_DIRECTORY: http://doxygen.org/manual/config.html#cfg_output_directory
.. _OPTIMIZE_OUTPUT_FOR_C: http://doxygen.org/manual/config.html#cfg_optimize_output_for_c
.. _HTML_COLORSTYLE_GAMMA: http://doxygen.org/manual/config.html#cfg_html_colorstyle_gamma
.. _ABBREVIATE_BRIEF: http://doxygen.org/manual/config.html#cfg_abbreviate_brief
.. _HTML_EXTRA_FILES: http://doxygen.org/manual/config.html#cfg_html_extra_files
.. _LATEX_BATCHMODE: http://doxygen.org/manual/config.html#cfg_latex_batchmode
.. _HIDE_UNDOC_RELATIONS: http://doxygen.org/manual/config.html#cfg_hide_undoc_relations
.. _DOCSET_BUNDLE_ID: http://doxygen.org/manual/config.html#cfg_docset_bundle_id
.. _HTML_FILE_EXTENSION: http://doxygen.org/manual/config.html#cfg_html_file_extension
.. _OUTPUT_LANGUAGE: http://doxygen.org/manual/config.html#cfg_output_language
.. _INLINE_GROUPED_CLASSES: http://doxygen.org/manual/config.html#cfg_inline_grouped_classes
.. _EXTRACT_STATIC: http://doxygen.org/manual/config.html#cfg_extract_static
.. _INCLUDE_GRAPH: http://doxygen.org/manual/config.html#cfg_include_graph
.. _PDF_HYPERLINKS: http://doxygen.org/manual/config.html#cfg_pdf_hyperlinks
.. _GENERATE_DOCBOOK: http://doxygen.org/manual/config.html#cfg_generate_docbook
.. _EXTRA_SEARCH_MAPPINGS: http://doxygen.org/manual/config.html#cfg_extra_search_mappings
.. _COLS_IN_ALPHA_INDEX: http://doxygen.org/manual/config.html#cfg_cols_in_alpha_index
.. _HIDE_SCOPE_NAMES: http://doxygen.org/manual/config.html#cfg_hide_scope_names
.. _CITE_BIB_FILES: http://doxygen.org/manual/config.html#cfg_cite_bib_files
.. _TCL_SUBST: http://doxygen.org/manual/config.html#cfg_tcl_subst
.. _LAYOUT_FILE: http://doxygen.org/manual/config.html#cfg_layout_file
.. _OPTIMIZE_OUTPUT_JAVA: http://doxygen.org/manual/config.html#cfg_optimize_output_java
.. _STRIP_FROM_INC_PATH: http://doxygen.org/manual/config.html#cfg_strip_from_inc_path
.. _EXAMPLE_PATH: http://doxygen.org/manual/config.html#cfg_example_path
.. _DOT_TRANSPARENT: http://doxygen.org/manual/config.html#cfg_dot_transparent
.. _HIDE_UNDOC_CLASSES: http://doxygen.org/manual/config.html#cfg_hide_undoc_classes
.. _TREEVIEW_WIDTH: http://doxygen.org/manual/config.html#cfg_treeview_width
.. _RECURSIVE: http://doxygen.org/manual/config.html#cfg_recursive
.. _PAPER_TYPE: http://doxygen.org/manual/config.html#cfg_paper_type
.. _QHP_CUST_FILTER_NAME: http://doxygen.org/manual/config.html#cfg_qhp_cust_filter_name
.. _TAB_SIZE: http://doxygen.org/manual/config.html#cfg_tab_size
.. _HTML_OUTPUT: http://doxygen.org/manual/config.html#cfg_html_output
.. _INPUT: http://doxygen.org/manual/config.html#cfg_input
.. _PROJECT_LOGO: http://doxygen.org/manual/config.html#cfg_project_logo
.. _INLINE_INHERITED_MEMB: http://doxygen.org/manual/config.html#cfg_inline_inherited_memb
.. _MAX_INITIALIZER_LINES: http://doxygen.org/manual/config.html#cfg_max_initializer_lines
.. _MAN_OUTPUT: http://doxygen.org/manual/config.html#cfg_man_output
.. _IMAGE_PATH: http://doxygen.org/manual/config.html#cfg_image_path
.. _HTML_FOOTER: http://doxygen.org/manual/config.html#cfg_html_footer
.. _INLINE_INFO: http://doxygen.org/manual/config.html#cfg_inline_info
.. _PERLMOD_MAKEVAR_PREFIX: http://doxygen.org/manual/config.html#cfg_perlmod_makevar_prefix
.. _CLASS_DIAGRAMS: http://doxygen.org/manual/config.html#cfg_class_diagrams
.. _GENERATE_TODOLIST: http://doxygen.org/manual/config.html#cfg_generate_todolist
.. _MAX_DOT_GRAPH_DEPTH: http://doxygen.org/manual/config.html#cfg_max_dot_graph_depth
.. _DOCSET_FEEDNAME: http://doxygen.org/manual/config.html#cfg_docset_feedname
.. _GENERATE_PERLMOD: http://doxygen.org/manual/config.html#cfg_generate_perlmod
.. _DOTFILE_DIRS: http://doxygen.org/manual/config.html#cfg_dotfile_dirs
.. _CHM_INDEX_ENCODING: http://doxygen.org/manual/config.html#cfg_chm_index_encoding
.. _RTF_HYPERLINKS: http://doxygen.org/manual/config.html#cfg_rtf_hyperlinks
.. _DOXYFILE_ENCODING: http://doxygen.org/manual/config.html#cfg_doxyfile_encoding
.. _MARKDOWN_SUPPORT: http://doxygen.org/manual/config.html#cfg_markdown_support
.. _EXT_LINKS_IN_WINDOW: http://doxygen.org/manual/config.html#cfg_ext_links_in_window
.. _QUIET: http://doxygen.org/manual/config.html#cfg_quiet
.. _SORT_BRIEF_DOCS: http://doxygen.org/manual/config.html#cfg_sort_brief_docs
.. _LATEX_FOOTER: http://doxygen.org/manual/config.html#cfg_latex_footer
.. _INCLUDED_BY_GRAPH: http://doxygen.org/manual/config.html#cfg_included_by_graph
.. _XML_OUTPUT: http://doxygen.org/manual/config.html#cfg_xml_output
.. _MATHJAX_RELPATH: http://doxygen.org/manual/config.html#cfg_mathjax_relpath
.. _SEARCHENGINE_URL: http://doxygen.org/manual/config.html#cfg_searchengine_url
.. _GENERATE_LATEX: http://doxygen.org/manual/config.html#cfg_generate_latex
.. _XML_SCHEMA: http://doxygen.org/manual/config.html#cfg_xml_schema
.. _CREATE_SUBDIRS: http://doxygen.org/manual/config.html#cfg_create_subdirs
.. _GENERATE_DOCSET: http://doxygen.org/manual/config.html#cfg_generate_docset
.. _LATEX_SOURCE_CODE: http://doxygen.org/manual/config.html#cfg_latex_source_code
.. _EXTRACT_PRIVATE: http://doxygen.org/manual/config.html#cfg_extract_private
.. _FILE_PATTERNS: http://doxygen.org/manual/config.html#cfg_file_patterns
.. _BUILTIN_STL_SUPPORT: http://doxygen.org/manual/config.html#cfg_builtin_stl_support
.. _GENERATE_TREEVIEW: http://doxygen.org/manual/config.html#cfg_generate_treeview
.. _PROJECT_BRIEF: http://doxygen.org/manual/config.html#cfg_project_brief
.. _EXTRACT_PACKAGE: http://doxygen.org/manual/config.html#cfg_extract_package
.. _USE_MDFILE_AS_MAINPAGE: http://doxygen.org/manual/config.html#cfg_use_mdfile_as_mainpage
.. _QT_AUTOBRIEF: http://doxygen.org/manual/config.html#cfg_qt_autobrief
.. _HIDE_IN_BODY_DOCS: http://doxygen.org/manual/config.html#cfg_hide_in_body_docs
.. _DOT_MULTI_TARGETS: http://doxygen.org/manual/config.html#cfg_dot_multi_targets
.. _VERBATIM_HEADERS: http://doxygen.org/manual/config.html#cfg_verbatim_headers
.. _CALLER_GRAPH: http://doxygen.org/manual/config.html#cfg_caller_graph
.. _IGNORE_PREFIX: http://doxygen.org/manual/config.html#cfg_ignore_prefix
.. _HIDE_FRIEND_COMPOUNDS: http://doxygen.org/manual/config.html#cfg_hide_friend_compounds
.. _FILTER_SOURCE_FILES: http://doxygen.org/manual/config.html#cfg_filter_source_files
.. _EXAMPLE_PATTERNS: http://doxygen.org/manual/config.html#cfg_example_patterns
.. _ALPHABETICAL_INDEX: http://doxygen.org/manual/config.html#cfg_alphabetical_index
.. _EXAMPLE_RECURSIVE: http://doxygen.org/manual/config.html#cfg_example_recursive
.. _UML_LOOK: http://doxygen.org/manual/config.html#cfg_uml_look
.. _GENERATE_QHP: http://doxygen.org/manual/config.html#cfg_generate_qhp
.. _INCLUDE_FILE_PATTERNS: http://doxygen.org/manual/config.html#cfg_include_file_patterns
.. _STRICT_PROTO_MATCHING: http://doxygen.org/manual/config.html#cfg_strict_proto_matching
.. _PERL_PATH: http://doxygen.org/manual/config.html#cfg_perl_path
.. _PROJECT_NAME: http://doxygen.org/manual/config.html#cfg_project_name
.. _SEARCH_INCLUDES: http://doxygen.org/manual/config.html#cfg_search_includes
.. _GENERATE_TAGFILE: http://doxygen.org/manual/config.html#cfg_generate_tagfile
.. _EXCLUDE: http://doxygen.org/manual/config.html#cfg_exclude
.. _LOOKUP_CACHE_SIZE: http://doxygen.org/manual/config.html#cfg_lookup_cache_size
.. _MSCFILE_DIRS: http://doxygen.org/manual/config.html#cfg_mscfile_dirs
.. _DOT_FONTNAME: http://doxygen.org/manual/config.html#cfg_dot_fontname
.. _MAKEINDEX_CMD_NAME: http://doxygen.org/manual/config.html#cfg_makeindex_cmd_name
.. _BRIEF_MEMBER_DESC: http://doxygen.org/manual/config.html#cfg_brief_member_desc
.. _REFERENCES_RELATION: http://doxygen.org/manual/config.html#cfg_references_relation
.. _MAN_EXTENSION: http://doxygen.org/manual/config.html#cfg_man_extension
.. _WARN_IF_UNDOCUMENTED: http://doxygen.org/manual/config.html#cfg_warn_if_undocumented
.. _INPUT_FILTER: http://doxygen.org/manual/config.html#cfg_input_filter
.. _XML_DTD: http://doxygen.org/manual/config.html#cfg_xml_dtd
.. _LATEX_BIB_STYLE: http://doxygen.org/manual/config.html#cfg_latex_bib_style
.. _MATHJAX_CODEFILE: http://doxygen.org/manual/config.html#cfg_mathjax_codefile
.. _INTERNAL_DOCS: http://doxygen.org/manual/config.html#cfg_internal_docs
.. _QCH_FILE: http://doxygen.org/manual/config.html#cfg_qch_file
.. _OPTIMIZE_OUTPUT_VHDL: http://doxygen.org/manual/config.html#cfg_optimize_output_vhdl
.. _RTF_OUTPUT: http://doxygen.org/manual/config.html#cfg_rtf_output
.. _HHC_LOCATION: http://doxygen.org/manual/config.html#cfg_hhc_location
.. _MULTILINE_CPP_IS_BRIEF: http://doxygen.org/manual/config.html#cfg_multiline_cpp_is_brief
.. _HTML_TIMESTAMP: http://doxygen.org/manual/config.html#cfg_html_timestamp
.. _HTML_HEADER: http://doxygen.org/manual/config.html#cfg_html_header
.. _CASE_SENSE_NAMES: http://doxygen.org/manual/config.html#cfg_case_sense_names
.. _LATEX_HEADER: http://doxygen.org/manual/config.html#cfg_latex_header
.. _EXTERNAL_PAGES: http://doxygen.org/manual/config.html#cfg_external_pages
.. _GENERATE_HTMLHELP: http://doxygen.org/manual/config.html#cfg_generate_htmlhelp
.. _GENERATE_ECLIPSEHELP: http://doxygen.org/manual/config.html#cfg_generate_eclipsehelp
.. _EXTERNAL_GROUPS: http://doxygen.org/manual/config.html#cfg_external_groups
.. _FILTER_PATTERNS: http://doxygen.org/manual/config.html#cfg_filter_patterns
.. _HTML_STYLESHEET: http://doxygen.org/manual/config.html#cfg_html_stylesheet
.. _SUBGROUPING: http://doxygen.org/manual/config.html#cfg_subgrouping
.. _SORT_MEMBERS_CTORS_1ST: http://doxygen.org/manual/config.html#cfg_sort_members_ctors_1st
.. _TAGFILES: http://doxygen.org/manual/config.html#cfg_tagfiles
.. _PREDEFINED: http://doxygen.org/manual/config.html#cfg_predefined
.. _USE_PDFLATEX: http://doxygen.org/manual/config.html#cfg_use_pdflatex
.. _DOT_GRAPH_MAX_NODES: http://doxygen.org/manual/config.html#cfg_dot_graph_max_nodes
.. _ENUM_VALUES_PER_LINE: http://doxygen.org/manual/config.html#cfg_enum_values_per_line
.. _SORT_GROUP_NAMES: http://doxygen.org/manual/config.html#cfg_sort_group_names
.. _DOT_IMAGE_FORMAT: http://doxygen.org/manual/config.html#cfg_dot_image_format
.. _EXTRACT_LOCAL_METHODS: http://doxygen.org/manual/config.html#cfg_extract_local_methods
.. _DOCSET_PUBLISHER_ID: http://doxygen.org/manual/config.html#cfg_docset_publisher_id
.. _HTML_DYNAMIC_SECTIONS: http://doxygen.org/manual/config.html#cfg_html_dynamic_sections
.. _UML_LIMIT_NUM_FIELDS: http://doxygen.org/manual/config.html#cfg_uml_limit_num_fields
.. _HTML_COLORSTYLE_HUE: http://doxygen.org/manual/config.html#cfg_html_colorstyle_hue
.. _GENERATE_XML: http://doxygen.org/manual/config.html#cfg_generate_xml
.. _CPP_CLI_SUPPORT: http://doxygen.org/manual/config.html#cfg_cpp_cli_support
.. _QHP_SECT_FILTER_ATTRS: http://doxygen.org/manual/config.html#cfg_qhp_sect_filter_attrs
.. _GROUP_GRAPHS: http://doxygen.org/manual/config.html#cfg_group_graphs
.. _SEPARATE_MEMBER_PAGES: http://doxygen.org/manual/config.html#cfg_separate_member_pages
.. _PERLMOD_LATEX: http://doxygen.org/manual/config.html#cfg_perlmod_latex
.. _FORMULA_FONTSIZE: http://doxygen.org/manual/config.html#cfg_formula_fontsize
.. _ALWAYS_DETAILED_SEC: http://doxygen.org/manual/config.html#cfg_always_detailed_sec
.. _EXCLUDE_PATTERNS: http://doxygen.org/manual/config.html#cfg_exclude_patterns
.. _EXTERNAL_SEARCH_ID: http://doxygen.org/manual/config.html#cfg_external_search_id
.. _RTF_EXTENSIONS_FILE: http://doxygen.org/manual/config.html#cfg_rtf_extensions_file
.. _LATEX_EXTRA_FILES: http://doxygen.org/manual/config.html#cfg_latex_extra_files
.. _COMPACT_RTF: http://doxygen.org/manual/config.html#cfg_compact_rtf
.. _ENABLED_SECTIONS: http://doxygen.org/manual/config.html#cfg_enabled_sections
.. _LATEX_HIDE_INDICES: http://doxygen.org/manual/config.html#cfg_latex_hide_indices
.. _SHOW_USED_FILES: http://doxygen.org/manual/config.html#cfg_show_used_files
.. _ECLIPSE_DOC_ID: http://doxygen.org/manual/config.html#cfg_eclipse_doc_id
.. _GRAPHICAL_HIERARCHY: http://doxygen.org/manual/config.html#cfg_graphical_hierarchy
.. _ALIASES: http://doxygen.org/manual/config.html#cfg_aliases
.. _HTML_COLORSTYLE_SAT: http://doxygen.org/manual/config.html#cfg_html_colorstyle_sat
.. _WARN_IF_DOC_ERROR: http://doxygen.org/manual/config.html#cfg_warn_if_doc_error
.. _GENERATE_RTF: http://doxygen.org/manual/config.html#cfg_generate_rtf
.. _SERVER_BASED_SEARCH: http://doxygen.org/manual/config.html#cfg_server_based_search
.. _CHM_FILE: http://doxygen.org/manual/config.html#cfg_chm_file
.. _LATEX_CMD_NAME: http://doxygen.org/manual/config.html#cfg_latex_cmd_name
.. _QHP_NAMESPACE: http://doxygen.org/manual/config.html#cfg_qhp_namespace
.. _FORMULA_TRANSPARENT: http://doxygen.org/manual/config.html#cfg_formula_transparent
.. _INTERACTIVE_SVG: http://doxygen.org/manual/config.html#cfg_interactive_svg
.. _XML_PROGRAMLISTING: http://doxygen.org/manual/config.html#cfg_xml_programlisting
.. _GENERATE_CHI: http://doxygen.org/manual/config.html#cfg_generate_chi
.. _REFERENCES_LINK_SOURCE: http://doxygen.org/manual/config.html#cfg_references_link_source
.. _WARN_LOGFILE: http://doxygen.org/manual/config.html#cfg_warn_logfile
.. _FILTER_SOURCE_PATTERNS: http://doxygen.org/manual/config.html#cfg_filter_source_patterns
.. _TOC_EXPAND: http://doxygen.org/manual/config.html#cfg_toc_expand
.. _GENERATE_LEGEND: http://doxygen.org/manual/config.html#cfg_generate_legend
.. _PROJECT_NUMBER: http://doxygen.org/manual/config.html#cfg_project_number
.. _HTML_EXTRA_STYLESHEET: http://doxygen.org/manual/config.html#cfg_html_extra_stylesheet
.. _SKIP_FUNCTION_MACROS: http://doxygen.org/manual/config.html#cfg_skip_function_macros
.. _SHOW_FILES: http://doxygen.org/manual/config.html#cfg_show_files
.. _CLASS_GRAPH: http://doxygen.org/manual/config.html#cfg_class_graph
.. _LATEX_OUTPUT: http://doxygen.org/manual/config.html#cfg_latex_output
.. _GENERATE_MAN: http://doxygen.org/manual/config.html#cfg_generate_man
.. _SORT_BY_SCOPE_NAME: http://doxygen.org/manual/config.html#cfg_sort_by_scope_name
.. _CLANG_OPTIONS: http://doxygen.org/manual/config.html#cfg_clang_options
.. _INCLUDE_PATH: http://doxygen.org/manual/config.html#cfg_include_path
.. _MSCGEN_PATH: http://doxygen.org/manual/config.html#cfg_mscgen_path
.. _DOT_CLEANUP: http://doxygen.org/manual/config.html#cfg_dot_cleanup
.. _MATHJAX_FORMAT: http://doxygen.org/manual/config.html#cfg_mathjax_format
.. _INPUT_ENCODING: http://doxygen.org/manual/config.html#cfg_input_encoding
.. _IDL_PROPERTY_SUPPORT: http://doxygen.org/manual/config.html#cfg_idl_property_support
.. _FULL_PATH_NAMES: http://doxygen.org/manual/config.html#cfg_full_path_names
.. _DISABLE_INDEX: http://doxygen.org/manual/config.html#cfg_disable_index
.. _SIP_SUPPORT: http://doxygen.org/manual/config.html#cfg_sip_support
.. _MACRO_EXPANSION: http://doxygen.org/manual/config.html#cfg_macro_expansion
.. _EXTRACT_ALL: http://doxygen.org/manual/config.html#cfg_extract_all
.. _WARNINGS: http://doxygen.org/manual/config.html#cfg_warnings
.. _EXTRACT_LOCAL_CLASSES: http://doxygen.org/manual/config.html#cfg_extract_local_classes
.. _REPEAT_BRIEF: http://doxygen.org/manual/config.html#cfg_repeat_brief
.. _INLINE_SOURCES: http://doxygen.org/manual/config.html#cfg_inline_sources
.. _USE_MATHJAX: http://doxygen.org/manual/config.html#cfg_use_mathjax
.. _EXTENSION_MAPPING: http://doxygen.org/manual/config.html#cfg_extension_mapping
.. _SHORT_NAMES: http://doxygen.org/manual/config.html#cfg_short_names
.. _DOT_PATH: http://doxygen.org/manual/config.html#cfg_dot_path
.. _RTF_STYLESHEET_FILE: http://doxygen.org/manual/config.html#cfg_rtf_stylesheet_file
.. _TYPEDEF_HIDES_STRUCT: http://doxygen.org/manual/config.html#cfg_typedef_hides_struct
.. _PERLMOD_PRETTY: http://doxygen.org/manual/config.html#cfg_perlmod_pretty
.. _ENABLE_PREPROCESSING: http://doxygen.org/manual/config.html#cfg_enable_preprocessing
.. _JAVADOC_AUTOBRIEF: http://doxygen.org/manual/config.html#cfg_javadoc_autobrief
.. _STRIP_FROM_PATH: http://doxygen.org/manual/config.html#cfg_strip_from_path
.. _EXCLUDE_SYMBOLS: http://doxygen.org/manual/config.html#cfg_exclude_symbols
.. _HTML_INDEX_NUM_ENTRIES: http://doxygen.org/manual/config.html#cfg_html_index_num_entries
.. _GENERATE_AUTOGEN_DEF: http://doxygen.org/manual/config.html#cfg_generate_autogen_def
.. _CLANG_ASSISTED_PARSING: http://doxygen.org/manual/config.html#cfg_clang_assisted_parsing
.. _COLLABORATION_GRAPH: http://doxygen.org/manual/config.html#cfg_collaboration_graph
.. _DOCSET_PUBLISHER_NAME: http://doxygen.org/manual/config.html#cfg_docset_publisher_name
.. _QHP_CUST_FILTER_ATTRS: http://doxygen.org/manual/config.html#cfg_qhp_cust_filter_attrs
.. _GENERATE_HTML: http://doxygen.org/manual/config.html#cfg_generate_html
.. _CALL_GRAPH: http://doxygen.org/manual/config.html#cfg_call_graph
.. _GENERATE_DEPRECATEDLIST: http://doxygen.org/manual/config.html#cfg_generate_deprecatedlist
.. _SORT_MEMBER_DOCS: http://doxygen.org/manual/config.html#cfg_sort_member_docs
.. _SHOW_INCLUDE_FILES: http://doxygen.org/manual/config.html#cfg_show_include_files
.. _WARN_FORMAT: http://doxygen.org/manual/config.html#cfg_warn_format
.. _WARN_NO_PARAMDOC: http://doxygen.org/manual/config.html#cfg_warn_no_paramdoc
.. _MATHJAX_EXTENSIONS: http://doxygen.org/manual/config.html#cfg_mathjax_extensions
.. _EXTERNAL_SEARCH: http://doxygen.org/manual/config.html#cfg_external_search
.. _GENERATE_TESTLIST: http://doxygen.org/manual/config.html#cfg_generate_testlist
.. _INLINE_SIMPLE_STRUCTS: http://doxygen.org/manual/config.html#cfg_inline_simple_structs
.. _DOT_FONTPATH: http://doxygen.org/manual/config.html#cfg_dot_fontpath
.. _REFERENCED_BY_RELATION: http://doxygen.org/manual/config.html#cfg_referenced_by_relation
.. _HAVE_DOT: http://doxygen.org/manual/config.html#cfg_have_dot
.. _INHERIT_DOCS: http://doxygen.org/manual/config.html#cfg_inherit_docs
.. _EXTRA_PACKAGES: http://doxygen.org/manual/config.html#cfg_extra_packages
.. _HIDE_UNDOC_MEMBERS: http://doxygen.org/manual/config.html#cfg_hide_undoc_members
.. _FORCE_LOCAL_INCLUDES: http://doxygen.org/manual/config.html#cfg_force_local_includes
.. _SHOW_NAMESPACES: http://doxygen.org/manual/config.html#cfg_show_namespaces
.. _QHP_VIRTUAL_FOLDER: http://doxygen.org/manual/config.html#cfg_qhp_virtual_folder
.. _EXPAND_ONLY_PREDEF: http://doxygen.org/manual/config.html#cfg_expand_only_predef
.. _SEARCHENGINE: http://doxygen.org/manual/config.html#cfg_searchengine
.. _STRIP_CODE_COMMENTS: http://doxygen.org/manual/config.html#cfg_strip_code_comments
.. _QHG_LOCATION: http://doxygen.org/manual/config.html#cfg_qhg_location

.. <!-- Other links -->
.. _SCons: http://scons.org
.. _Doxygen: http://doxygen.org
.. _scons_doxygen: https://bitbucket.org/russel/scons_doxygen
.. _scons-doxygen-template: https://github.com/ptomulik/scons-doxygen-template

LICENSE
-------

Copyright (c) 2013 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>

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
