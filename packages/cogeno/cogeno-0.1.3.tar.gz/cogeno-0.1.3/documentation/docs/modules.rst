..
    Copyright (c) 2018 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_modules:

Code generation modules
#######################

Code generation modules provide supporting functions for code generation.

Modules have to be imported to gain access to the module's functions
and variables.

 ::

    /* This file uses modules. */
    ...
    /**
     * @code{.cogeno.py}
     * cogeno.import_module('my_special_module')
     * my_special_module.do_everything():
     * @endcode{.cogeno.py}
     */
    /** @code{.cogeno.ins}@endcode */
    ...

.. contents::
   :depth: 2
   :local:
   :backlinks: top

Generic modules
***************

Extended device tree specification (EDTS) database
==================================================

The EDTS database module is the exception from the import rule for modules.
It is always imported for cogeno inline code generation. There is also a
convenience function :func:`cogeno.edts()` to get the database.

In case you want to use the extended device tree database in another Python
project import it by:

::

    import cogeno.modules.edtsdatabase
