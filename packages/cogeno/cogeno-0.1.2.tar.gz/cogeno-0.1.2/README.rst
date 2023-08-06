Cogeno
======

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

Download
********

Cogeno is available from `<https://gitlab.com/b0661/cogeno>`_. It can be
installed by::

    git clone https://gitlab.com/b0661/cogeno.git
    pip3 install -e cogeno

Documentation
*************

The source of the documentation is in the ``documentation`` folder.
You can build it by::

    cd cogeno/documentation
    make html

Requirements
************

Development is currently done with:

- Python 3.6.3
- Sphinx 1.7.5

Questions & issues
******************

Please post questions and issues as `GitLab issues <https://gitlab.com/b0661/cogeno/issues>`_.

Alternatives
************

- `Cog <https://nedbatchelder.com/code/cog/index.html>`_

Credits
*******

Cogeno development started as a `pull request <https://github.com/zephyrproject-rtos/zephyr/pull/10885>`_
to the `Zephyr <https://github.com/zephyrproject-rtos/zephyr>`_ project.
Several people invested quite a time in commenting and improving the pull request and it's spin-offs.
Please see the pull requests.

The cogeno code base started from the `Cog <https://nedbatchelder.com/code/cog/index.html>`_
source code. Ned Batchelder provides this wonderful tool.



