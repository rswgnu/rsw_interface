#
# SUMMARY:      Interface for overloading get, set and del operations of attributes
# USAGE:        inherit from GetSet; test with: python getset.py
# KEYWORDS:     attribute, interface, overload
#
# AUTHOR:       Robert Weiner
# LICENSE:      Available under the terms of the MIT License
#
# DESCRIPTION:  
"""
Interface for overloading get, set and del operations of attributes.
Use this interface to customize the meaning of attribute access (use
of, assignment to, or deletion of x.name) for class instances.

For performance reasons, these methods are cached in the class object at
class definition time; therefore, they cannot be changed after the
class definition is loaded.
"""
# DESCRIP-END.

## ------------------------------------------------------------------------
## Required modules
## ------------------------------------------------------------------------

from interface import *


## ------------------------------------------------------------------------
## Interfaces
## ------------------------------------------------------------------------

class GetSet(Interface):
    """
    Interface for deletion, get and set of object attributes.
    Specifies methods which implement:
         del iself.attrname          or   delattr(iself, attrname)
         iself.attrname              or   getattr(iself, attrname)
         iself.attrname = attrvalue  or   setattr(iself, attrname, attrvalue)
    """
    # Raise a clear exception if these methods are called before an implementor
    # redefines them.
    __delattr_body__ = __getattr_body__ = __setattr_body__ = Interface.error

    def __delattr__(iself, name):
        "Implement: attribute deletion, del iself.name."
        __delattr_body__(iself, name)

    def __getattr__(iself, name):
        """
        Implement: attribute retrieval, iself.name.
        Return:    the value of attribute `name'.
        Raise:     AttributeError when `name' is not found.
        Called only when an instance attribute or class attribute lookup fails.
        """
        return __getattr_body__(iself, name)

    def __setattr__(iself, name, value):
        """
        Implement: attribute storage, iself[name] = value.
        Called whenever an attribute assignment is attempted.
        To assign to an instance attribute within this method,
        use: self.__dict__[name] = value.
        """
        __setattr_body__(iself, name, value)


## ------------------------------------------------------------------------
## Private functions
## ------------------------------------------------------------------------

def __test():
    "Test GetSet interface and print results."
    class G(GetSet):
        def __init__(self): pass
        def __delattr_body__(self, name): return 0
        def __getattr_body__(self, name): return 0
        def __setattr_body__(self, name, value): return 0
    assert_implements(G)

    class NoG(GetSet):
        def __init__(self): pass

    if implements(G, GetSet):
        print("Success - class G implements GetSet")
    else:
        print("  FAILURE - class G fails to implement GetSet")

    if implements(NoG, GetSet):
        print("  FAILURE - class NoG implements GetSet")
    else:
        print("Success - class NoG fails to implement GetSet")

    g = G(); noG = NoG()
    if implements(g, GetSet):
        print("Success - instance g implements GetSet")
    else:
        print("  FAILURE - instance g fails to implement GetSet")

    if implements(noG, GetSet):
        print("  FAILURE - instance noG implements GetSet")
    else:
        print("Success - instance noG fails to implement GetSet")

    if assert_implements(G):
        print("Success - assert_implements(G)")

    try:
        assert_implements(NoG)
        print("  FAILURE - assert_implements(noG) did not trigger an InterfaceError")
    except InterfaceError:
        print("Success - assert_implements(noG) triggered an InterfaceError")


## ------------------------------------------------------------------------
## Program execution
## ------------------------------------------------------------------------

if __name__ == '__main__':
    __test()
