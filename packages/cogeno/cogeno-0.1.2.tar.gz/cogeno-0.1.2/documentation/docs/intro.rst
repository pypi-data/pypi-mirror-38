..
    Copyright (c) 2004-2015 Ned Batchelder
    SPDX-License-Identifier: MIT
    Copyright (c) 2018 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_intro:

Introduction
############

Script snippets that are inlined in a source file are used as code generators.
The tool to scan the source file for the Python snippets and process them is
cogeno. Cogeno and part of this documentation is based on
`Cog <https://nedbatchelder.com/code/cog/index.html>`_ from Ned Batchelder.

The inlined Python snippets can contain any Python code, they are regular
Python scripts. All Python snippets in a source file and all Python snippets of
included template files are treated as a python script with a common set of
global Python variables. Global data created in one snippet can be used in
another snippet that is processed later on. This feature could be used, for
example, to customize included template files.

An inlined Python snippet can always access the cogeno module. The cogeno
module encapsulates and provides all the functions to retrieve information
(options, device tree properties, CMake variables, config properties) and to
output the generated code.

Cogeno transforms files in a very simple way: it finds chunks of script code
embedded in them, executes the script code, and places its output combined with
the original file into the generated file. The original file can contain
whatever text you like around the script code. It will usually be source code.

For example, if you run this file through cogeno:

::

    /* This is my C file. */
    ...
    /**
     * @code{.cogeno.py}
     * fnames = ['DoSomething', 'DoAnotherThing', 'DoLastThing']
     * for fn in fnames:
     *     cogeno.outl("void %s();" % fn)
     * @endcode{.cogeno.py}
     */
    /** @code{.cogeno.ins}@endcode */
    ...

it will come out like this:

::

    /* This is my C file. */
    ...
    /**
     * @code{.cogeno.py}
     * fnames = ['DoSomething', 'DoAnotherThing', 'DoLastThing']
     * for fn in fnames:
     *     cogeno.outl("void %s();" % fn)
     * @endcode{.cogeno.py}
     */
    void DoSomething();
    void DoAnotherThing();
    void DoLastThing();
    /** @code{.cogeno.ns}@endcode */
    ...

Lines with ``@code{.cogeno.py}`` or ``@code{.cogeno.ins}@endcode`` are marker lines.
The lines between ``@code{.cogeno.py}`` and ``@endcode{.cogeno.py}`` are the
generator Python code. The lines between ``@endcode{.cogeno.py}`` and
``@code{.cogeno.ins}@endcode`` are the output from the generator.

When cogeno runs, it discards the last generated Python output, executes the
generator Python code, and writes its generated output into the file. All text
lines outside of the special markers are passed through unchanged.

The cogeno marker lines can contain any text in addition to the marker tokens.
This makes it possible to hide the generator Python code from the source file.

In the sample above, the entire chunk of Python code is a C comment, so the
Python code can be left in place while the file is treated as C code.


