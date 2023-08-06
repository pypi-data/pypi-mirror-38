..
    Copyright (c) 2018 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno:

Welcome to cogeno's documentation!
##################################

For some repetitive or parameterized coding tasks, it's convenient to
use a code generating tool to build code fragments, instead of writing
(or editing) that source code by hand.

Cogeno, the inline code generation tool, processes Python or Jinja2 "snippets"
inlined in your source files. It can also access CMake build
parameters and device tree information to generate source code automatically
tailored and tuned to a specific project configuration.

Cogeno can be used, for example, to generate source code that creates
and fills data structures, adapts programming logic, creates
configuration-specific code fragments, and more.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   invocation
   functions
   modules
   templates
   build
   principle


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
