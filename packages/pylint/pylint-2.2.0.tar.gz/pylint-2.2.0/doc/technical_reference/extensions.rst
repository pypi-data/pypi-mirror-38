Optional Pylint checkers in the extensions module
=================================================

Pylint provides the following optional plugins:

- :ref:`pylint.extensions.bad_builtin`
- :ref:`pylint.extensions.check_elif`
- :ref:`pylint.extensions.comparetozero`
- :ref:`pylint.extensions.docparams`
- :ref:`pylint.extensions.docstyle`
- :ref:`pylint.extensions.emptystring`
- :ref:`pylint.extensions.mccabe`
- :ref:`pylint.extensions.overlapping_exceptions`
- :ref:`pylint.extensions.redefined_variable_type`

You can activate any or all of these extensions by adding a ``load-plugins`` line to the ``MASTER`` section of your ``.pylintrc``, for example::

    load-plugins=pylint.extensions.docparams,pylint.extensions.docstyle

.. _pylint.extensions.bad_builtin:

Deprecated Builtins checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.bad_builtin``.
Verbatim name of the checker is ``deprecated_builtins``.

Deprecated Builtins checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This used to be the ``bad-builtin`` core checker, but it was moved to
an extension instead. It can be used for finding prohibited used builtins,
such as ``map`` or ``filter``, for which other alternatives exists.

If you want to control for what builtins the checker should warn about,
you can use the ``bad-functions`` option::

    $ pylint a.py --load-plugins=pylint.extensions.bad_builtin --bad-functions=apply,reduce
    ...

Deprecated Builtins checker Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-functions:
  List of builtins function names that should not be used, separated by a comma

  Default: ``map,filter``

Deprecated Builtins checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-builtin (W0141): *Used builtin function %s*
  Used when a black listed builtin function is used (see the bad-function
  option). Usual black listed functions are the ones like map, or filter , where
  Python offers now some cleaner alternative like list comprehension.


.. _pylint.extensions.check_elif:

Else If Used checker
~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.check_elif``.
Verbatim name of the checker is ``else_if_used``.

Else If Used checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:else-if-used (R5501): *Consider using "elif" instead of "else if"*
  Used when an else statement is immediately followed by an if statement and
  does not contain statements that would be unrelated to it.


.. _pylint.extensions.comparetozero:

Compare-To-Zero checker
~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.comparetozero``.
Verbatim name of the checker is ``compare-to-zero``.

Compare-To-Zero checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:compare-to-zero (C2001): *Avoid comparisons to zero*
  Used when Pylint detects comparison to a 0 constant.


.. _pylint.extensions.docparams:

Parameter Documentation checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.docparams``.
Verbatim name of the checker is ``parameter_documentation``.

Parameter Documentation checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you document the parameters of your functions, methods and constructors and
their types systematically in your code this optional component might
be useful for you. Sphinx style, Google style, and Numpy style are supported.
(For some examples, see https://pypi.python.org/pypi/sphinxcontrib-napoleon .)

You can activate this checker by adding the line::

    load-plugins=pylint.extensions.docparams

to the ``MASTER`` section of your ``.pylintrc``.

This checker verifies that all function, method, and constructor docstrings
include documentation of the

* parameters and their types
* return value and its type
* exceptions raised

and can handle docstrings in

* Sphinx style (``param``, ``type``, ``return``, ``rtype``,
  ``raise`` / ``except``)::

   def function_foo(x, y, z):
       '''function foo ...

       :param x: bla x
       :type x: int

       :param y: bla y
       :type y: float

       :param int z: bla z

       :return: sum
       :rtype: float

       :raises OSError: bla
       '''
       return x + y + z

* or the Google style (``Args:``, ``Returns:``, ``Raises:``)::

   def function_foo(x, y, z):
       '''function foo ...

       Args:
           x (int): bla x
           y (float): bla y

           z (int): bla z

       Returns:
           float: sum

       Raises:
           OSError: bla
       '''
       return x + y + z

* or the Numpy style (``Parameters``, ``Returns``, ``Raises``)::

   def function_foo(x, y, z):
       '''function foo ...

       Parameters
       ----------
       x: int
           bla x
       y: float
           bla y

       z: int
           bla z

       Returns
       -------
       float
           sum

       Raises
       ------
       OSError
           bla
       '''
       return x + y + z


You'll be notified of **missing parameter documentation** but also of
**naming inconsistencies** between the signature and the documentation which
often arise when parameters are renamed automatically in the code, but not in
the documentation.

Constructor parameters can be documented in either the class docstring or
the ``__init__`` docstring, but not both::

    class ClassFoo(object):
        '''Sphinx style docstring foo

        :param float x: bla x

        :param y: bla y
        :type y: int
        '''
        def __init__(self, x, y):
            pass

    class ClassBar(object):
        def __init__(self, x, y):
            '''Google style docstring bar

            Args:
                x (float): bla x
                y (int): bla y
            '''
            pass

In some cases, having to document all parameters is a nuisance, for instance if
many of your functions or methods just follow a **common interface**. To remove
this burden, the checker accepts missing parameter documentation if one of the
following phrases is found in the docstring:

* For the other parameters, see
* For the parameters, see

(with arbitrary whitespace between the words). Please add a link to the
docstring defining the interface, e.g. a superclass method, after "see"::

   def callback(x, y, z):
       '''Sphinx style docstring for callback ...

       :param x: bla x
       :type x: int

       For the other parameters, see
       :class:`MyFrameworkUsingAndDefiningCallback`
       '''
       return x + y + z

   def callback(x, y, z):
       '''Google style docstring for callback ...

       Args:
           x (int): bla x

       For the other parameters, see
       :class:`MyFrameworkUsingAndDefiningCallback`
       '''
       return x + y + z

Naming inconsistencies in existing parameter and their type documentations are
still detected.

Parameter Documentation checker Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:accept-no-param-doc:
  Whether to accept totally missing parameter documentation in the docstring of
  a function that has parameters.

  Default: ``yes``
:accept-no-raise-doc:
  Whether to accept totally missing raises documentation in the docstring of a
  function that raises an exception.

  Default: ``yes``
:accept-no-return-doc:
  Whether to accept totally missing return documentation in the docstring of a
  function that returns a statement.

  Default: ``yes``
:accept-no-yields-doc:
  Whether to accept totally missing yields documentation in the docstring of a
  generator.

  Default: ``yes``
:default-docstring-type:
  If the docstring type cannot be guessed the specified docstring type will be
  used.

  Default: ``default``

Parameter Documentation checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:differing-param-doc (W9017): *"%s" differing in parameter documentation*
  Please check parameter names in declarations.
:differing-type-doc (W9018): *"%s" differing in parameter type documentation*
  Please check parameter names in type declarations.
:multiple-constructor-doc (W9005): *"%s" has constructor parameters documented in class and __init__*
  Please remove parameter declarations in the class or constructor.
:missing-param-doc (W9015): *"%s" missing in parameter documentation*
  Please add parameter declarations for all parameters.
:missing-type-doc (W9016): *"%s" missing in parameter type documentation*
  Please add parameter type declarations for all parameters.
:missing-raises-doc (W9006): *"%s" not documented as being raised*
  Please document exceptions for all raised exception types.
:missing-return-doc (W9011): *Missing return documentation*
  Please add documentation about what this method returns.
:missing-return-type-doc (W9012): *Missing return type documentation*
  Please document the type returned by this method.
:missing-yield-doc (W9013): *Missing yield documentation*
  Please add documentation about what this generator yields.
:missing-yield-type-doc (W9014): *Missing yield type documentation*
  Please document the type yielded by this method.
:redundant-returns-doc (W9008): *Redundant returns documentation*
  Please remove the return/rtype documentation from this method.
:redundant-yields-doc (W9010): *Redundant yields documentation*
  Please remove the yields documentation from this method.


.. _pylint.extensions.docstyle:

Docstyle checker
~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.docstyle``.
Verbatim name of the checker is ``docstyle``.

Docstyle checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^
:bad-docstring-quotes (C0198): *Bad docstring quotes in %s, expected """, given %s*
  Used when a docstring does not have triple double quotes.
:docstring-first-line-empty (C0199): *First line empty in %s docstring*
  Used when a blank line is found at the beginning of a docstring.


.. _pylint.extensions.emptystring:

Compare-To-Empty-String checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.emptystring``.
Verbatim name of the checker is ``compare-to-empty-string``.

Compare-To-Empty-String checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:compare-to-empty-string (C1901): *Avoid comparisons to empty string*
  Used when Pylint detects comparison to an empty string constant.


.. _pylint.extensions.mccabe:

Design checker
~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.mccabe``.
Verbatim name of the checker is ``design``.

Design checker Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can now use this plugin for finding complexity issues in your code base.

Activate it through ``pylint --load-plugins=pylint.extensions.mccabe``. It introduces
a new warning, ``too-complex``, which is emitted when a code block has a complexity
higher than a preestablished value, which can be controlled through the
``max-complexity`` option, such as in this example::

    $ cat a.py
    def f10():
        """McCabe rating: 11"""
        myint = 2
        if myint == 5:
            return myint
        elif myint == 6:
            return myint
        elif myint == 7:
            return myint
        elif myint == 8:
            return myint
        elif myint == 9:
            return myint
        elif myint == 10:
            if myint == 8:
                while True:
                    return True
            elif myint == 8:
                with myint:
                    return 8
        else:
            if myint == 2:
                return myint
            return myint
        return myint
    $ pylint a.py --load-plugins=pylint.extensions.mccabe
    R:1: 'f10' is too complex. The McCabe rating is 11 (too-complex)
    $ pylint a.py --load-plugins=pylint.extensions.mccabe --max-complexity=50
    $

Design checker Options
^^^^^^^^^^^^^^^^^^^^^^
:max-complexity:
  McCabe complexity cyclomatic threshold

  Default: ``10``

Design checker Messages
^^^^^^^^^^^^^^^^^^^^^^^
:too-complex (R1260): *%s is too complex. The McCabe rating is %d*
  Used when a method or function is too complex based on McCabe Complexity
  Cyclomatic


.. _pylint.extensions.overlapping_exceptions:

Overlap-Except checker
~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.overlapping_exceptions``.
Verbatim name of the checker is ``overlap-except``.

Overlap-Except checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:overlapping-except (W0714): *Overlapping exceptions (%s)*
  Used when exceptions in handler overlap or are identical


.. _pylint.extensions.redefined_variable_type:

Multiple Types checker
~~~~~~~~~~~~~~~~~~~~~~

This checker is provided by ``pylint.extensions.redefined_variable_type``.
Verbatim name of the checker is ``multiple_types``.

Multiple Types checker Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:redefined-variable-type (R0204): *Redefinition of %s type from %s to %s*
  Used when the type of a variable changes inside a method or a function.


