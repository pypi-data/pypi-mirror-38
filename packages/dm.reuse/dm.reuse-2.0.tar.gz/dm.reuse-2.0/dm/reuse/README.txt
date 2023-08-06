dm.reuse
========

Utilities to reuse (slightly modified) objects in new contexts.

Currently, there is a single utility: `rebindFunction`.
It allows to reuse the code of a function while changing name, globals,
default arguments, properties and/or names used.

Lets look at a trivial example. Function `f` accesses global variables
`i` and `j`.

Examples
--------

>>> i = 1; j = 2
>>> def f(): return i, j
...
>>> f()
(1, 2)

We want to derive a new function `g` which binds `i` to `-1`:

>>> from dm.reuse import rebindFunction
>>> g=rebindFunction(f, i=-1)
>>> g()
(-1, 2)

We can specify the rebinds not only via keyword arguments but via
a dictionary as well:

>>> g=rebindFunction(f, dict(i=-1, j=-2))
>>> g()
(-1, -2)

Usually, the function name is taken over from the original function,
but it can be changed:

>>> f.__name__
'f'
>>> g.__name__
'f'
>>> g=rebindFunction(f, dict(i=-1, j=-2), funcName='g')
>>> g.__name__
'g'
>>> g()
(-1, -2)

The originals function docstring is taken over, too -- unless
overridden:

>>> f.func_doc = 'some documentation'
>>> g=rebindFunction(f, dict(i=-1, j=-2))
>>> f.__doc__ is g.__doc__
True
>>> g=rebindFunction(f, dict(i=-1, j=-2), funcDoc='some new documentation')
>>> g.__doc__
'some new documentation'

Default values for arguments can be added, removed or changed.
Unknown arguments are recognized:

>>> def f(a1, a2=2): return a1, a2
...
>>> g=rebindFunction(f, argRebindDir=dict(a1=1))
>>> g()
(1, 2)

>>> from dm.reuse import REQUIRED
>>> g=rebindFunction(f, argRebindDir=dict(a2=REQUIRED))
>>> g(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
  ...
TypeError: f() takes exactly 2 arguments (1 given)

>>> g=rebindFunction(f, argRebindDir=dict(a2=10))
>>> g(1)
(1, 10)

>>> g=rebindFunction(f, argRebindDir=dict(a3=10))
Traceback (most recent call last):
  ...
ValueError: unknown arguments in `argRebindDir`: a3

Finally, function properties can be rebound with `propRebindDir`.
We are careful, to give the new function a separate new property dict.

>>> f.prop='p'
>>> g=rebindFunction(f)
>>> g.prop
'p'
>>> g=rebindFunction(f, propRebindDir=dict(prop='P', prop2='p2'))
>>> g.prop, g.prop2
('P', 'p2')
>>> f.__dict__
{'prop': 'p'}

Occationally, functions use local imports which are not adequate
in the new context. In order to provide control over them, names
used inside the function code can be changed.

>>> def f(a): import codecs; return codecs, a
...
>>> g=rebindFunction(f, nameRebindDir=dict(codecs='urllib'))
>>> r = g(1)
>>> r[0].__name__, r[1]
('urllib', 1)

This way, references to global variables can be changed as well.

>>> i1, i2 = 1, 2
>>> def f(): return i1
... 
>>> g=rebindFunction(f, nameRebindDir=dict(i1='i2'))
>>> g()
2



History
-------

2.0
  added partial support for Python 3 (keyword only arguments and
  annotations are not yet supported)

  dropped support for Python before 2.7

1.1
  ``nameRebindDir`` support added
