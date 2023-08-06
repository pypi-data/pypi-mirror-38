..
    Copyright (c) 2018 Bobby Noelte
    SPDX-License-Identifier: Apache-2.0

.. _cogeno_build:

Integration into the build process
##################################

Code generation has to be invoked as part of the build process of a project.

.. contents::
   :depth: 2
   :local:
   :backlinks: top

CMake
-----

Projects that use `CMake <https://cmake.org/>`_ to manage building the project
can add the following CMake code to the CMake scripts.

By this a file that contains inline code generation can be added to the project
using the `target_sources_cogeno` command in the respective :file:`CMakeList.txt` file.

.. function:: target_sources_cogeno(file [COGENO_DEFINES defines..] [DEPENDS target.. file..])

.. code::

    # Copyright (c) 2018 Bobby Noelte.
    #
    # SPDX-License-Identifier: Apache-2.0

    function(target_sources_cogeno
        target          # The CMake target that depends on the generated file
        )

        set(options)
        set(oneValueArgs)
        set(multiValueArgs COGENO_DEFINES DEPENDS)
        cmake_parse_arguments(COGENO "${options}" "${oneValueArgs}"
                              "${multiValueArgs}" ${ARGN})
        # prepend -D to all defines
        string(REGEX REPLACE "([^;]+)" "-D;\\1"
                COGENO_COGENO_DEFINES "${COGENO_COGENO_DEFINES}")

        message(STATUS "Will generate for target ${target}")
        # Generated file must be generated to the current binary directory.
        # Otherwise this would trigger CMake issue #14633:
        # https://gitlab.kitware.com/cmake/cmake/issues/14633
        foreach(arg ${COGENO_UNPARSED_ARGUMENTS})
            if(IS_ABSOLUTE ${arg})
                set(template_file ${arg})
                get_filename_component(generated_file_name ${arg} NAME)
                set(generated_file ${CMAKE_CURRENT_BINARY_DIR}/${generated_file_name})
            else()
                set(template_file ${CMAKE_CURRENT_SOURCE_DIR}/${arg})
                set(generated_file ${CMAKE_CURRENT_BINARY_DIR}/${arg})
            endif()
            get_filename_component(template_dir ${template_file} DIRECTORY)
            get_filename_component(generated_dir ${generated_file} DIRECTORY)

            if(IS_DIRECTORY ${template_file})
                message(FATAL_ERROR "target_sources_cogeno() was called on a directory")
            endif()

            # Generate file from template
            message(STATUS " from '${template_file}'")
            message(STATUS " to   '${generated_file}'")
            add_custom_command(
                COMMENT "cogeno ${generated_file}"
                OUTPUT ${generated_file}
                MAIN_DEPENDENCY ${template_file}
                DEPENDS
                ${COGENO_DEPENDS}
                COMMAND
                ${PYTHON_EXECUTABLE}
                cogeno.py
                ${COGENO_COGENO_DEFINES}
                -D "\"BOARD=${BOARD}\""
                -D "\"APPLICATION_SOURCE_DIR=${APPLICATION_SOURCE_DIR}\""
                -D "\"APPLICATION_BINARY_DIR=${APPLICATION_BINARY_DIR}\""
                -D "\"PROJECT_NAME=${PROJECT_NAME}\""
                -D "\"PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}\""
                -D "\"PROJECT_BINARY_DIR=${PROJECT_BINARY_DIR}\""
                -D "\"CMAKE_SOURCE_DIR=${CMAKE_SOURCE_DIR}\""
                -D "\"CMAKE_BINARY_DIR=${CMAKE_BINARY_DIR}\""
                -D "\"CMAKE_CURRENT_SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}\""
                -D "\"CMAKE_CURRENT_BINARY_DIR=${CMAKE_CURRENT_BINARY_DIR}\""
                -D "\"CMAKE_CURRENT_LIST_DIR=${CMAKE_CURRENT_LIST_DIR}\""
                -D "\"CMAKE_FILES_DIRECTORY=${CMAKE_FILES_DIRECTORY}\""
                -D "\"CMAKE_PROJECT_NAME=${CMAKE_PROJECT_NAME}\""
                -D "\"CMAKE_SYSTEM=${CMAKE_SYSTEM}\""
                -D "\"CMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}\""
                -D "\"CMAKE_SYSTEM_VERSION=${CMAKE_SYSTEM_VERSION}\""
                -D "\"CMAKE_SYSTEM_PROCESSOR=${CMAKE_SYSTEM_PROCESSOR}\""
                -D "\"CMAKE_C_COMPILER=${CMAKE_C_COMPILER}\""
                -D "\"CMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}\""
                -D "\"CMAKE_COMPILER_IS_GNUCC=${CMAKE_COMPILER_IS_GNUCC}\""
                -D "\"CMAKE_COMPILER_IS_GNUCXX=${CMAKE_COMPILER_IS_GNUCXX}\""
                --config "${PROJECT_BINARY_DIR}/.config"
                --cmakecache "${CMAKE_BINARY_DIR}/CMakeCache.txt"
                --dts "${PROJECT_BINARY_DIR}/${BOARD}.dts_compiled"
                --bindings "${DTS_APP_BINDINGS}" "${PROJECT_SOURCE_DIR}/dts/bindings"
                --edts "${PROJECT_BINARY_DIR}/edts.json"
                --modules "${APPLICATION_SOURCE_DIR}/templates" "${PROJECT_SOURCE_DIR}/templates"
                --templates "${APPLICATION_SOURCE_DIR}/templates" "${PROJECT_SOURCE_DIR}/templates"
                --input "${template_file}"
                --output "${generated_file}"
                --log "${CMAKE_BINARY_DIR}/${CMAKE_FILES_DIRECTORY}/cogeno.log"
                --lock "${CMAKE_BINARY_DIR}/${CMAKE_FILES_DIRECTORY}/cogeno.lock"
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            )
            target_sources(${target} PRIVATE ${generated_file})
            # Add template directory to include path to allow includes with
            # relative path in generated file to work
            target_include_directories(${target} PRIVATE ${template_dir})
            # Add directory of generated file to include path to allow includes
            # of generated header file with relative path.
            target_include_directories(${target} PRIVATE ${generated_dir})
        endforeach()
    endfunction()


Zephyr
------

Cogeno can be integrated into `Zephyr <https://github.com/zephyrproject-rtos/zephyr>`_ by
applying the `codegen pull request <https://github.com/zephyrproject-rtos/zephyr/pull/10885>`_.

Within Zephyr cogeno is referenced as codegen. This was the name the development started with.
It had to be changed because codegen was already used by several open source project.

In Zephyr the processing of source files is controlled by the CMake extension functions:
``zephyr_sources_codegen(..)`` or ``zephyr_library_sources_codegen(..)``. The generated
source files are added to the Zephyr sources. During build the source files are
processed by cogeno and the generated source files are written to the CMake
binary directory. Zephyr uses `CMake <https://cmake.org/>`_ as the tool to manage building
the project. A file that contains inline code generation has to be added to the project
by one of the following commands in a :file:`CMakeList.txt` file:

.. function:: zephyr_sources_cogdeen(file [CODEGEN_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_sources_codegen_ifdef(ifguard file [CODEGEN_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_library_sources_codegen(file [CODEGEN_DEFINES defines..] [DEPENDS target.. file..])

.. function:: zephyr_library_sources_codegen_ifdef(ifguard file [CODEGEN_DEFINES defines..] [DEPENDS target.. file..])

The arguments given by the ``COGDEGEN_DEFINES`` keyword have to be of the form
``define_name=define_value``. The arguments become globals in the python
snippets and can be accessed by ``define_name``.

Dependencies given by the ``DEPENDS`` key word are added to the dependencies
of the generated file.
