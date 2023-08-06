..
    mynotes builds indexes and converts to HTML a tree of notes written in
    Markdown.
    Copyright (C) 2018 Yorick Brunet <mynotes@yok.ch>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Welcome to *mynotes* !
======================

*mynotes* builds indexes and converts to HTML a tree of notes written in
Markdown.

The index building phase creates new index files (still in Markdown)
that contains links to files and subfolders of the local folder.

As example, index files for the tree

* A/
    * a1.md
    * a2.md
* B/
    * BB/
        * bb1.md
    * b1.md
* c.md

are generated as following

* A/
    * index.md (with links to a1.md and a2.md)
    * a1.md
    * a2.md
* B/
    * index.md (with links to BB/index.md and b1.md)
    * BB/
        * index.md (with link to bb1.md)
        * bb1.md
    * b1.md
* c.md
* index.md (with links to A/index.md, B/index.md and c.md)

The html generation phase creates HTML files from Markdown files (including
ToC and links to upper/top index).

Additional files that are not strictly part of the notes (thus files not with
Markdown format) can be placed in folders ``_files``. These folders are by
default ignored when building the indexes and generating HTML files.

Installation
------------

Python 3.6+ is required to run *mynotes*.

The package can be installed directly from PyPi using pip:

.. code-block:: shell

    pip install mynotes

or downloaded from the release/tags page and then installed using pip:

.. code-block:: shell

   pip install mynotes-xxx.tar.gz

Excecution
----------

*mynotes* package contains two scripts for command line interaction.

* ``mynotes-build`` builds the index files.

.. code-block:: python

    usage: mynotes-build [-h] [--verbose] [--config CONFIG]

    Build index files for notes tree.

    optional arguments:
    -h, --help            show this help message and exit
    --verbose, -v         Increase verbosity
    --config CONFIG, -c CONFIG
                            Configuration file

* ``mynotes-genhtml`` generates HTML files into a dedicated folder.

.. code-block:: python

    usage: mynotes-genhtml [-h] [--verbose] [--config CONFIG]

    Generate HTML files for markdown files.

    optional arguments:
    -h, --help            show this help message and exit
    --verbose, -v         Increase verbosity
    --config CONFIG, -c CONFIG
                            Configuration file

Configuration
-------------

*mynotes* writes the its configuration in a configuration file
(``.mynotes.ini``). This file is created automatically if it does not exist
and default configuration values are used.

*mynotes* takes only into account section ``[mynotes]`` thus the configuration
could be written in common file, e.g. ``setup.cfg``.

The configuration keys are:

+------------------+----------------------------------------------------------+
| Key              | Purpose                                                  |
+==================+==========================================================+
| ``index``        | Name of index files (with markdown extension)            |
+------------------+----------------------------------------------------------+
| ``home``         | Main file of a directory (comes on top of the index list |
|                  | and is included in index HTML files.                     |
+------------------+----------------------------------------------------------+
| ``excl_dirs``    | Directories to exclude, independent from path.           |
+------------------+----------------------------------------------------------+
| ``excl_files``   | Files to exclude, independent from path. The index file  |
|                  | is not ignore when generating HTML files.                |
+------------------+----------------------------------------------------------+
| ``md_ext``       | Extension for Markdown files, must be used for ``index`` |
|                  | and ``home`` keys.                                       |
+------------------+----------------------------------------------------------+
| ``plugins_html`` | Activated plugins for HTML generation:                   |
|                  |                                                          |
|                  | * ``links-index``: Generate links to upper/top index     |
|                  | * ``toc``: Generate toc                                  |
+------------------+----------------------------------------------------------+

Example of configuration file:

.. code-block:: text

    [mynotes]
    index = index.md
    home = home.md
    excl_dirs = .git _files _html
    excl_files = .gitignore .python-version index.md Makefile .mynotes.ini
    md_ext = .md
    plugins_html = links-index toc

License
--------

*mynotes* is licensed under the `GNU General Public License version 3
<https://www.gnu.org/licenses/quick-guide-gplv3.html>`_.

See `LICENSE <LICENSE>`_.
