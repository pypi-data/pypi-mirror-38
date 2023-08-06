Short description
=================

Function converts recursively an object of standard (im-)mutable types into
strictly immutable ones.


Long description
================

In Python sometimes it is useful to have a "static" struct to be shared across
functions and classes and to guarantee it can not be changed accidentally
by some code.

In addition to standard immutable simple types (like int, str etc.), there are
two complex types: `frozenset` and `tuple`. Unfortunately years ago (2012-02)
there was PEP-0416[1] where a `frozendict` was rejected as hard to be
implemented.

Unlike other wrappers implementation here works similar to a `copy.deepcopy`
function which immediately copies mutable objects into immutable analogues
instead of wrapping them at access time. Therefore if a code passes already
immutable object, there is almost no overhead, but the code do not need to pay
attention whether to deepcopy of incoming (or outgoing) data or not.

[1] https://www.python.org/dev/peps/pep-0416/
