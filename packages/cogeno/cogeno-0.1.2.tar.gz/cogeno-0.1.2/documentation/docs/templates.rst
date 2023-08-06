..
    Copyright (c) 2018 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_templates:

Code Generation Templates
#########################

Code generation templates provide sophisticated code generation functions.

Templates are simply text files. They may be hierarchical organized.
There is always one top level template. All the other templates have
to be included to gain access to the template's functions and variables.

A template file usually contains normal text and templating commands
intermixed. A bound sequence of templating commands is called a script
snippet. As a special case a template file may be a scripte snippet
as a whole.

Cogeno supports two flavours of script snippets: Python and Jinja2.
A script snippet has to be written in one of the two scripting
languages. Within a template file snippets of different language can
coexist.

.. contents::
   :depth: 2
   :local:
   :backlinks: top


Template Snippets
*****************


 ::

    /* This file uses templates. */
    ...
    /**
     * @code{.cogen}
     * template_in_var = 1
     * cogeno.out_include('templates/template_tmpl.c')
     * if template_out_var not None:
     *     cogeno.outl("int x = %s;" % template_out_var)
     * @endcode{.cogen}
     */
    /** @code{.codeins}@endcode */
    ...

Device drivers
**************

Pin controller drivers
----------------------

::

    cogeno.out_include('templates/drivers/pinctrl_tmpl.c')

The template generates the most part of a pinctrl driver including driver
instantiation.

 The template expects the following globals to be set:

.. attribute:: compatible

    The compatible string of the driver (e.g. 'st,stm32-pinctrl')

.. attribute:: config_get

    C function name of device config_get function.

.. attribute:: mux_free

    C function name of device mux_free function.

.. attribute:: mux_get

    C function name of device mux_get function.

.. attribute:: mux_set

    C function name of device mux_set function.

.. attribute:: device_init

    C function name of device init function

.. attribute:: data_info

    device data type definition (e.g. 'struct pinctrl_stm32_data')

Usage example:

::

    /**
     * @code{.cogen}
     * compatible = 'st,stm32-pinctrl'
     * config_get = 'pinctrl_stm32_config_get'
     * config_set = 'pinctrl_stm32_config_set'
     * mux_get = 'pinctrl_stm32_mux_get'
     * mux_set = 'pinctrl_stm32_mux_set'
     * device_init = 'pinctrl_stm32_device_init'
     * data_info = 'struct pinctrl_stm32_data'
     * cogeno.out_include('templates/drivers/pinctrl_tmpl.c')
     * @endcode{.cogen}
     */
    /** @code{.codeins}@endcode */




