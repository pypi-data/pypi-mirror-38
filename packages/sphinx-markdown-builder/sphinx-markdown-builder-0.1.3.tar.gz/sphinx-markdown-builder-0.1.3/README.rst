sphinx-markdown-builder
=======================

`PyPI <https://pypi.org/project/sphinx-markdown-builder>`__ `PyPI -
Downloads <https://pypi.org/project/sphinx-markdown-builder>`__ `PyPI -
Python Version <https://pypi.org/project/sphinx-markdown-builder>`__
`GitHub
stars <https://github.com/codejamninja/sphinx-markdown-builder>`__

   sphinx builder that outputs markdown files

Please ★ this repo if you found it useful ★ ★ ★

Features
--------

-  Generates markdown

Installation
------------

.. code:: sh

   pip3 install sphinx-markdown-builder

Dependencies
------------

-  `Python 3 <https://www.python.org>`__

Usage
-----

Load extension in configuration.

*conf.py*

.. code:: py

   extensions = [
       'sphinx_markdown_builder'
   ]

If using `recommonmark <https://github.com/rtfd/recommonmark>`__, make
sure you explicitly ignore the build files as they will conflict with
the system.

*conf.py*

.. code:: py

   exclude_patterns = [
       'build/*'
   ]

Build markdown files with Makefile

.. code:: sh

   make markdown

Build markdown files with ``sphinx-build`` command

.. code:: sh

   cd docs
   sphinx-build -M markdown ./ build

Support
-------

Submit an
`issue <https://github.com/codejamninja/sphinx-markdown-builder/issues/new>`__

Screenshots
-----------

`Contribute <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/CONTRIBUTING.md>`__
a screenshot

Contributing
------------

Review the `guidelines for
contributing <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/CONTRIBUTING.md>`__

License
-------

`MIT
License <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/LICENSE>`__

`Jam Risser <https://codejam.ninja>`__ © 2018

Changelog
---------

Review the
`changelog <https://github.com/codejamninja/sphinx-markdown-builder/blob/master/CHANGELOG.md>`__

Credits
-------

-  `Jam Risser <https://codejam.ninja>`__ - Author
-  `Matthew
   Brett <https://github.com/matthew-brett/nb2plots/blob/master/nb2plots/doctree2md.py>`__
   - doctree2md

Support on Liberapay
--------------------

A ridiculous amount of coffee ☕ ☕ ☕ was consumed in the process of
building this project.

`Add some fuel <https://liberapay.com/codejamninja/donate>`__ if you’d
like to keep me going!

`Liberapay receiving <https://liberapay.com/codejamninja/donate>`__
`Liberapay patrons <https://liberapay.com/codejamninja/donate>`__
