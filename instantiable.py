#
# SUMMARY:      Basic interfaces for most class instances
# USAGE:        inherit from Comparable, Hashable, or Instantiable
# KEYWORDS:     class, dictionary, instance, interface, overload
#
# AUTHOR:       Robert Weiner
# LICENSE:      Available under the terms of the MIT License
#
# DESCRIPTION:  
"""
Basic interfaces implemented by most classes:
     Comparable   - for instances which are less-than, equal-to or greater-than each other
     Hashable     - for instances which generate a hash code for use in dictionaries
     Instantiable - for basic instance methods overloaded by most classes
"""
# DESCRIP-END.

## ------------------------------------------------------------------------
## Required modules
## ------------------------------------------------------------------------

from interface import *


## ------------------------------------------------------------------------
## Interfaces
## ------------------------------------------------------------------------

class Comparable(Interface):
    """
    Interface for instances which are less-than, equal-to or greater-than each other.
    Specifies the following methods:
         iself.__cmp__(other)        - return whether `iself' is <, ==, or > `other'
         iself.__rcmp__(other)       - return whether `other' is <, ==, or > `iself'
    """
    # Raise a clear exception if these methods are called before an implementor
    # redefines them.
    __cmp_body__ = __rcmp_body__ = Interface.error

    def __cmp__(iself, other):
        """
        Return: a negative, zero or positive number based on whether `iself' is <, ==, or > `other'.

        Called by all comparison operations.  If no __cmp__() operation
        is defined, class instances are compared by object identity (address).
        """
        __cmp_body__(iself, other)

    def __rcmp__(iself, other):
        "Return: a negative, zero or positive number based on whether `other' is <, ==, or > `iself'."
        __rcmp_body__(iself, other)


class Hashable(Comparable):
    """
    Interface for instances which generate a hash code for use in dictionaries.

    Specifies the following methods:
         iself.__hash__()            - return a hash code for `iself'

    If a class does not conform to Comparable, it should not conform to
    Hashable.  If it conforms to Comparable but not to Hashable, its
    instances will not be usable as dictionary keys.

    If a class defines mutable objects and conforms to Comparable, it
    should not conform to Hashable, since the dictionary implementation
    requires that a key's hash value be immutable (if the object's hash
    value changes, it will be in the wrong hash bucket).
    """
    # Raise a clear exception if this method is called before an implementor
    # redefines it.
    __hash_body__ = Interface.error

    def __hash__(iself):
        """
        Return: a hash code for `iself' typically for use in dictionary lookups.
        Require: Objects which compare equal and return the same hash values.

        Called to produce the lookup key for a dictionary item, and by
        the built-in function "hash".  A good hashing technique involves
        mixing together (e.g. using bitwise xor) the hash values for the
        components of the object which play a part in equality
        comparisons.
        """
        __hash_body__(iself)


class Instantiable(Interface):
    """
    Standard interface of overloadable instance methods to which most classes should conform.
    Specifies the following methods:
         iself.__init__([, args...]) - initialize `iself' upon creation (inherited from "Interface")
         iself.__del__()             - delete `iself'
         iself.__nonzero__()         - return 0 to treat an instance as logically false, else true
         iself.__repr__()            - return string representation useful in reconstruction of `iself'
         iself.__str__()             - return a printable string representation of `iself'
    """
    # Raise a clear exception if these methods are called before an implementor
    # redefines them.
    __del_body__ = __nonzero_body__ = __repr_body__ = __str_body__ = Interface.error

    def __del__(iself):
        """
        Implement: instance deletion, del iself.

        Destructor called when an instance is about to be destroyed. If
        a base class has a __del__() method, the derived class's
        __del__() method must explicitly call it to ensure proper
        deletion of the base class part of the instance.  It is not
        guaranteed that __del__() methods will be called for objects
        which exist when the Python interpreter exits.

        Warning: due to the precarious circumstances under which
        __del__() methods are invoked, exceptions that occur during
        their execution are ignored, and a warning is printed to
        sys.stderr instead. Also, when __del__() is invoked in response
        to a module being deleted (e.g., when execution of the program
        is done), other globals referenced by the __del__() method may
        already have been deleted. For this reason, __del__() methods
        should do the absolute minimum needed to maintain external
        invariants.  Python guarantees that globals whose name begin
        with a single underscore are deleted from their module before
        other globals are deleted; if no other references to such
        globals exist, this may help in assuring that imported modules
        are still available at the time the __del__() method is called.
        """
        __del_body__(iself)

    def __nonzero__(iself):
        """
        Return: 0 to treat an instance as logically false, else return 1 for true.
        Implement: object truth-value testing, e.g. if `iself' ...

        When this method is not defined, __len__() is called instead, if it is
        defined. If a class defines neither __len__() nor __nonzero__(),
        all its instances are considered true.
        """
        __nonzero_body__(iself)

    def __repr__(iself):
        """
        Return: string representation useful in reconstruction of `iself'.


        Called by the repr() built-in function and by reverse quotes
        string conversions to compute the official string
        representation of an object.  This should normally be a valid
        Python expression which can be used to recreate an object with
        the same value.  By convention, objects which cannot be
        trivially converted to strings which can be used to create a
        similar object instead produce a string of the form "<...some
        useful description...>".
        """
        __repr_body__(iself)

    def __str__(self):
        """
        Return: a printable string representation of `iself'.

        Called by the str() built-in function and by the print statement
        to compute the informal string representation of an
        object.  This differs from __repr__ in that it does not have
        to be a valid Python expression: a more convenient or concise
        representation may be used instead.
        """
        __str_body__(iself)
