scons-tool-dvipdfm
==================

.. image:: https://badge.fury.io/py/scons-tool-dvipdfm.svg
    :target: https://badge.fury.io/py/scons-tool-dvipdfm
    :alt: PyPi package version

.. image:: https://travis-ci.org/ptomulik/scons-tool-dvipdfm.svg?branch=master
    :target: https://travis-ci.org/ptomulik/scons-tool-dvipdfm
    :alt: Travis CI build status

.. image:: https://ci.appveyor.com/api/projects/status/github/ptomulik/scons-tool-dvipdfm?svg=true
    :target: https://ci.appveyor.com/project/ptomulik/scons-tool-dvipdfm

This is dvipdfm tool for `SCons`_. It is derived from the ``dvipdf`` tool
present in `SCons`_ core. The code has been adapted to enable usage of
`dvipdfm`_ program.

Installation
------------

There are few ways to install this tool for your project.

From pypi_
^^^^^^^^^^

This method may be preferable if you build your project under a virtualenv. To
add dvipdfm tool from pypi_, type (within your wirtualenv):

.. code-block:: shell

   pip install scons-tool-loader scons-tool-dvipdfm

or, if your project uses pipenv_:

.. code-block:: shell

   pipenv install --dev scons-tool-loader scons-tool-dvipdfm

Alternatively, you may add this to your ``Pipfile``

.. code-block::

   [dev-packages]
   scons-tool-loader = "*"
   scons-tool-dvipdfm = "*"


The tool will be installed as a namespaced package ``sconstool.dvipdfm``
in project's virtual environment. You may further use scons-tool-loader_
to load the tool.

As a git submodule
^^^^^^^^^^^^^^^^^^

#. Create new git repository:

   .. code-block:: shell

      mkdir /tmp/prj && cd /tmp/prj
      touch README.rst
      git init

#. Add the `scons-tool-dvipdfm`_ as a submodule:

   .. code-block:: shell

      git submodule add git://github.com/ptomulik/scons-tool-dvipdfm.git site_scons/site_tools/dvipdfm

#. For python 2.x create ``__init__.py`` in ``site_tools`` directory:

   .. code-block:: shell

      touch site_scons/site_tools/__init__.py

   this will allow to directly import ``site_tools.dvipdfm`` (this may be required by other tools).


Usage examples
--------------

Converting existing ``*.dvi`` file to ``*.pdf``:

.. code-block:: python

    # SConstruct
    env = Environment(tools=['dvipdfm'])
    env.DVIPDFM('foo.dvi')

Compiling ``LaTeX`` document to ``*.dvi`` and generating ``*.pdf`` file with
the ``DVIPDFM`` builder (note, the ``tex`` or ``default`` tool(s) must be
loaded):

.. code-block:: python

    # SConstruct
    env = Environment(tools=['tex', 'dvipdfm'])
    env.DVIPDFM('foo.tex')

Construction variables
----------------------

The following construction variables may be used to configure the ``DVIPDFM``
builder:

============================== ==============================================
        Variable                                Description
============================== ==============================================
 ``DVIPDFM``                    the ``dvipdfm`` executable
------------------------------ ----------------------------------------------
 ``DVIPDFMFLAGS``               additional flags to ``dvipdfm``
------------------------------ ----------------------------------------------
 ``DVIPDFMCOM``                 complete commandline for ``dvipdfm``
------------------------------ ----------------------------------------------
 ``DVIPDFMSUFFIX``              suffix for target files, by default ``.pdf``
============================== ==============================================


LICENSE
-------
Copyright (c) 2013-2018 by Paweł Tomulik

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

.. _SCons: http://scons.org
.. _SCons test framework: https://bitbucket.org/dirkbaechle/scons_test_framework
.. _scons-tool-dvipdfm: https://github.com/ptomulik/scons-tool-dvipdfm
.. _scons-tool-loader: https://github.com/ptomulik/scons-tool-loader
.. _mercurial: http://mercurial.selenic.com/
.. _dvipdfm: http://gaspra.kettering.edu/dvipdfm/
.. _pipenv: https://pipenv.readthedocs.io/
.. _pypi: https://pypi.org/
