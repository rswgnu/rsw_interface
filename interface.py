# FILE:         interface.py
#
# SUMMARY:      Inheritable class interface/protocol support for Python; implements class `Interface' and conformance functions
# USAGE:        from interface import *; inherit from `Interface'; call one of the conformance functions described below
# KEYWORDS:     interface, utility
#
# AUTHOR:       Robert Weiner
# LICENSE:      Available under the terms of the MIT License
#
# DESCRIPTION:
"""
See the "Interface" class documentation string for details on what
interfaces are and how to use them.

The following are public functions defined in this module, not
methods.  (They are functions since many must work on objects of any
type; the ones that take operands of more specific types, such as
`extends' are functions so that they may be called similarly; type
checks ensure that they raise exceptions if called with an invalid
argument).

     assert_implements(aClass)
         call after a class definition to assert interface conformance

     extends(interface, *interfaces):
         boolean test of whether an interface extends one or more other interfaces (via inheritance);
         this is false if any arg is not an interface

     implements(obj, *interfaces)
         boolean test of whether a class or instance implements one or more interfaces;
         this is false if any of `*interfaces' is not an interface

     interface_names(obj)
         return a list of interface names which obj:
             implements, if `obj' is a class or instance;
             extends, if `obj' is an interface
         the list begins with `obj' itself if it is an interface

     interfaces(obj)
         return a list of interface objects which obj:
             implements, if `obj' is a class or instance;
             extends, if `obj' is an interface
         the list begins with `obj' itself if it is an interface

     is_interface(obj)
         boolean test of whether `obj' is an interface or class of interface

     -----

     ancestor_names(obj, exclude_interfaces=0)
         return a list of ancestor class or interface names of `obj' (class, interface or instance),
         including `obj' itself; ancestors are returned in depth-first order, left to right;
         with optional `exclude_interfaces', interface ancestors are removed

     ancestors(obj, exclude_interfaces=0)
         return a list of ancestor class or interface objects of `obj' (class, interface or instance),
         including `obj' itself; ancestors are returned in depth-first order, left to right;
         with optional `exclude_interfaces', interface ancestors are removed

     flatten (*objs)
         return a single-level list of all atomic objects in `*obj' (anything other than
         sequences, dictionaries and Indexable types) in original order

     unique(*sequences)
         return a flattened list with duplicates removed from any number of atomic or `sequence' args;
         does not sort the elements
"""
# DESCRIP-END.

## ------------------------------------------------------------------------
## Required modules and version levels
## ------------------------------------------------------------------------

import sys
from types import *
from inspect import isclass

def require_python_version(min_version):
    """
    Raises an error if Python version is less than `min_version'.
    Require: `min_version' is a float or string of only digits and periods
    Return:  python version number split into a tuple
    Raise:   SystemError if Python version is less than `min_version'.
    """
    assert type(min_version) in (float, str)

    if type(min_version) is float:
        # Don't use `min_version` here since has a buggy float conversion in V2.0.
        min_version = "%s" % min_version   
    # python_version_tuple would be (2, 0) for 2.0 final, for example
    python_version_tuple = tuple(map(int, sys.version.split()[0].split('.')))
    min_version_tuple = tuple(map(int, min_version.split('.')))
    if python_version_tuple >= min_version_tuple:
        return python_version_tuple

    raise SystemError("(%s): Requires Python %s or greater; running Python %s" % \
          (__name__, min_version, sys.version[0].split()))
                              
require_python_version('3.0.0')

## ------------------------------------------------------------------------
## Classes
## ------------------------------------------------------------------------

class Interface:
    """
    A protocol to which classes may conform by implementing its method signatures, pre- and post- conditions and attributes.
    This is the top-level class from which all interfaces inherit.

    An "interface" is a class which inherits from "Interface" and provides
    a series of "stub methods" (which may have doc strings as well as pre-
    and post-condition assertions).

    A stub method is distinguished from other methods by naming its first argument,
    `iself', short for "interface self".  Each stub method exists to provide a
    calling protocol to which any "implementor" must conform.

    The implementor may either overload the stub method, replacing it completely
    or more commonly may overload its "body method", keeping the stub method's
    signature, doc string and pre- and post-conditions.  Body method names are
    computed from the interface stub method name by adding a ``_body'' to the
    name:
          stub      =>     stub_body
        __stub      =>   __stub_body
        __stub__    =>   __stub_body__

    At the start of each interface definition, each stub body within the
    class should be equated to the "Interface.error" method so that if the 
    stub (or the stub body) is called, an exception will be signaled:

        stub_body1 = stub_body2 = Interface.error

    An interface i2 "extends" another interface i1 iff i2 inherits from i1.

    A class "implements" an interface (and thus conforms to it) iff:

       it inherits from the interface;

       it or its ancestors redefine/implement all of the stub or body methods
       declared by the interface, keeping the number of arguments per method the
       same and renaming the first arg of each stub method from `iself' to `self';
      
       and its definition is followed by a call to:
          assert_implements(aClass)
       this marks the class as a non-interface and confirms that it does in fact
       implement the interfaces from which it inherits.
    """

    ## Interface attributes

    # The next attribute is used to test whether or not a class is an interface.
    # Call "assert_implements(aClass)" after class definition to disable this
    # flag in classes which implement the interface.
    interface_flag = True

    # Interfaces set their method stub bodies to this method so that an error is 
    # triggered if an implementor fails to redefine the stub and mistakenly calls
    # the stub method.
    def error(self, *unused):
        raise InterfaceError("(%s): failed to implement the above interface stub method" % self.__name__)

    # Define this method in each interface to prevent instantiation of interfaces.
    def __init__(self, *args):
        """
        Initializes a newly created instance.
        The arguments passed are those from the class constructor expression.
        If a base class has an __init__() method, the derived class's
        __init__() method must explicitly call it to ensure proper
        initialization of the base class part of the instance.  For example,
        "BaseClass.__init__(self, [args ...])".
        """
        raise InterfaceError('(%s): an interface may not be instantiated; if an implementor, define "__init__" to eliminate this error' \
              % self.__class__)


class InterfaceError(Exception):
    "Class of Interface-related exceptions."

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)


## ------------------------------------------------------------------------
## Public functions
## ------------------------------------------------------------------------

def assert_implements(aClass):
    """
    If `aClass' fails to implement any of its interfaces, print all non-conformance issues.
    This should be called immediately after class definitions to validate proper interface conformance.
    Return: True if `aClass' implements all interfaces or if assertions are disabled (__debug__ is False)
    Raise: TypeError if `aClass' is not a class
           InterfaceError if __debug__ is enabled and `aClass' fails to conform to any of its interfaces
    """

    # Optimize away this entire function whenever assertions are ignored, i.e. when __debug__ is False
    # or "python -O" is used.
    if not __debug__:
        return True

    # Must allow for interfaces here because `aClass' is not declared
    # a non-interface until the end of this method.
    if not (isclass(aClass) or is_interface(aClass)):
        raise TypeError("(assert_implements): aClass arg `%s' is not a class" % aClass)

    # Add all ancestor interfaces to the implementation check
    interface_list = interfaces(aClass)
    errors = []
    for interface in interface_list:
        idict = interface.__dict__

        # Set istub_tuples to interface's stub methods given as (name, method) tuples.
        # Remove non-stub attributes and body methods.
        istub_tuples = [item for item in idict.items() \
                        if type(item[1]) is FunctionType and \
                        item[1].__code__.co_varnames[0] is 'iself']

        # Ensure all interface stub methods are redefined by the current class
        # and that the number of arguments to each remains the same.
        for stub_name, stub_method in istub_tuples:
            body_name = interface_body_name(stub_name)
            impl_method = getattr(aClass, stub_name)
            try:
                if hasattr(aClass, body_name):
                    body_method = getattr(aClass, body_name)
                    body_argcount = body_method.__code__.co_argcount
                else:
                    body_method = body_argcount = None

                body_method_unimplemented = body_method and body_method is Interface.error \
                                            or issubclass(interface, body_method.__class__)
                if impl_method is stub_method and not body_method or body_method_unimplemented:
                    # method is not implemented
                    errors.append("(%s): failed to define %s interface method %s or %s" % \
                                  (aClass.__name__, interface.__name__, body_name, stub_name))

                impl_method_argcount = impl_method.__code__.co_argcount
                stub_argcount = stub_method.__code__.co_argcount
                if impl_method != stub_method and impl_method_argcount != stub_argcount:
                    # impl_method has wrong number of args
                    errors.append("(%s.%s): takes %d args, instead of %d specified by %s.%s" % \
                                  (aClass.__name__, stub_name, impl_method_argcount, \
                                   stub_argcount, interface.__name__, stub_name))
                elif body_method and not body_method_unimplemented and body_argcount != stub_argcount:
                    # body_method has wrong number of args
                    errors.append("(%s.%s): takes %d args, instead of %d specified by %s.%s" % \
                                  (aClass.__name__, body_name, body_argcount,
                                   stub_argcount, interface.__name__, body_name))

            except AttributeError:
                if hasattr(aClass, stub_name) or hasattr(aClass, body_name):
                    pass
                else:
                    errors.append("(%s): failed to define %s interface method %s or %s" % \
                                  (aClass.__name__, interface.__name__, body_name, stub_name))

    if errors:
        print("assert_implements(%s) errors:" % aClass.__name__)
        for e in errors: print("  ", e)
        raise InterfaceError("(assert_implements): failed for %s" % aClass.__name__)
    elif interface_list:
        # Since interfaces don't implement other interfaces (they only extend them),
        # `aClass' must be a regular class, so disable the interface attribute.
        aClass.interface_flag = False
        return True
    else:
        return False


def extends(interface, *interfaces):
    """
    Return: True if `interface' inherits from all interfaces in `interfaces', else False.
    Raise: TypeError, if any argument is not an interface.
    """
    if not is_interface(interface):
        raise TypeError('(extends): first arg %s must be an interface; try using "implements" instead' % interface)
    if False in map(is_interface, interfaces):
        raise TypeError('(extends): some arg from interfaces is not an interface: %s' % interfaces)
    return all([issubclass(interface, anc_interface) for anc_interface in interfaces])


def implements(obj, *interfaces):
    "Return: True if obj (a class or instance) implements all interfaces in `interfaces', else False."
    if isclass(obj):
        return __class_implements(obj, interfaces)
    elif isinstance(obj, object):
        return __instance_implements(obj, interfaces)
    elif is_interface(obj):
        return False
    else:
        # !!! Later will have to add support for Python builtin types.
        # For now, just signal an error for any other input.
        raise TypeError("(implements): obj arg `%s' must be a class or instance" % obj)


def interface_body_name(imethod_name):
    "Return: the name of the body method for interface method `imethod_name'."
    if type(imethod_name) != str:
        raise TypeError("(%s.body_name): `imethod_name' must be a string: %s" % \
              (self.__name__, imethod_name))
    if len(imethod_name) < 3 or imethod_name[-2:] != "__":
        return imethod_name + "_body"
    else:
        return imethod_name[:-2] + "_body" + imethod_name[-2:]


def interface_names(obj):
    """
    Return: a list of interface names to which `obj' is conformant.
    The list begins with `obj' itself if it is an interface.
    Names are returned in depth-first order, left to right.
    """
    return [o.__name__ for o in interfaces(obj)]


def interfaces(obj):
    """
    Return: a list of interface objects to which `obj' conforms.
    The list begins with `obj' itself if it is an interface.
    Interfaces are returned in depth-first order, left to right.
    """
    if not isclass(obj) and isinstance(obj, object):
        obj = obj.__class__
    if isclass(obj) or is_interface(obj):
        return [i for i in ancestors(obj) if is_interface(i)]
    else:
        # !!! Later will have to add support for Python builtin types.
        # For now, just return None
        return None


def is_interface(obj):
    """
    Return: True if `obj' is an interface or class of interface (inherits from Interface and contains stub methods), else False.
    """
    return issubclass(obj, Interface) if isclass(obj) else getattr(obj, 'interface_flag', False)

## -----


def ancestor_names(obj, exclude_interfaces=0):
    """
    Return: a list of ancestor class or interface names of `obj', starting with `obj' itself.
    Ancestors are returned in depth-first order, left to right.
    With optional `exclude_interfaces', interface ancestors are removed.
    """
    return [a.__name__ for a in ancestors(obj, exclude_interfaces)]


def ancestors(obj, exclude_interfaces=0):
    """
    Return: a list of ancestor class and interface objects of `obj', starting with `obj' itself.
    Ancestors are returned in depth-first order, left to right.
    With optional `exclude_interfaces', interface ancestors are removed.
    """
    assert isclass(obj) or is_interface(obj) or isinstance(obj, object), \
           "(ancestors): obj arg `%s' must be a class, interface or instance" % obj

    if not isclass(obj) and isinstance(obj, object):
        obj = obj.__class__

    if exclude_interfaces:
        repeated_ancestors = __get_ancestors_no_interfaces(obj)
    else:
        repeated_ancestors = __get_ancestors(obj)

    return list(set(repeated_ancestors))


def flatten (*objs):
    """
    Return: a single-level list of all atoms in `*objs' in original order.
    Any object type other than a sequence, dictionary or Indexable type is considered atomic
    by this function.

    SeeAlso: `sys.setrecursionlimit' to increase recursion limit if need be.
    """
    ## Test case:   flatten(('a', 'b', ('c', 'd')), 'e', ('f', ('g', ['h', ('i', 'j'), ['k', 'l', 'm']], ('n'))))
    ## Should produce: => (a b c d e f g h i j k l m n)
    if len(objs) == 1: objs = objs[0]
    if objs in (None, (), [], {}, set()):
        return []
    elif type(objs) in (tuple, list, set, slice):
# !!!     Add next line after Indexable interface is defined and loaded:
#         or implements(objs, Indexable):
        if objs in (None, (), [], set()):
            return []
        else:
            return flatten(objs[0]) + flatten(objs[1:])
    elif type(objs) is dict:
        return flatten(objs.values())
    else:
        return [objs]


def unique(*sequences):
    """
    Return: a flattened list with duplicates removed from any number of atomic or `sequence' args.
    Do not sort the elements.
    """
    return list(set(flatten(*sequences)))

## ------------------------------------------------------------------------
## Private functions
## ------------------------------------------------------------------------

def __class_implements(aClass, interface_seq):
    "Return: True if `aClass' implements all interfaces in `interface_seq', else False."
    # Add all ancestor interfaces to the implementation check
    if interface_seq:
        interface_seq = unique(interfaces(*interface_seq))
    for interface in interface_seq:
        if not is_interface(interface):
            raise TypeError( \
                  "(__class_implements): aClass arg = `%s', interface arg `%s' must be an Interface" % \
                  (aClass.__name__, interface))
        if not (issubclass(aClass, interface) and __implements(aClass, interface)):
            return False

    return True


def __get_ancestors(aClass):
    if aClass in (None, (), [], {}, set()):
        return []
    else:
        return [aClass] + flatten([__get_ancestors(c) for c in aClass.__bases__])


def __get_ancestors_no_interfaces(aClass):
    if aClass in (None, (), [], {}, set()) or is_interface(aClass):
        return []
    else:
        return [aClass] + flatten([__get_ancestors_no_interfaces(c) for c in aClass.__bases__])


def __implements(obj, interface):
    idict = interface.__dict__

    # To be an interface implementor, either the interface has no methods
    # to implement (e.g. Interface) or a class must implement at least one
    # of the interface's methods.  This flag tracks whether `obj' has done so.
    implemented_a_method = False

    # Set istub_tuples to interface's stub methods given as (name, method) tuples.
    # Remove non-stub attributes
    istub_tuples = [item for item in idict.items() \
                    if type(item[1]) is FunctionType and \
                    item[1].__code__.co_varnames[0] is 'iself']

    # Ensure all interface stub methods are redefined by the current class
    # and that the number of arguments to each remains the same.
    try:
        for stub_name, stub_method in istub_tuples:
            impl_method = getattr(obj, stub_name)
            body_name = interface_body_name(stub_name)
            if hasattr(obj, body_name):
                body_method = getattr(obj, body_name)
                body_argcount = body_method.__code__.co_argcount
            else:
                body_method = body_argcount = None

            body_method_unimplemented = body_method and body_method is Interface.error \
                                        or issubclass(interface, body_method.__class__)
            if impl_method == stub_method and not body_method or body_method_unimplemented:
                # method is not implemented
                return False
            else:
                implemented_a_method = True
            
            impl_method_argcount = impl_method.__code__.co_argcount
            stub_argcount = stub_method.__code__.co_argcount
            if impl_method != stub_method and \
               impl_method_argcount != stub_argcount or \
               body_method and not body_method_unimplemented and \
               body_argcount != stub_argcount:
                # method has wrong number of args
                return False
    except AttributeError:
        return False

    return not istub_tuples or implemented_a_method


def __instance_implements(instance, interface_seq):
    "Return: True if `instance' implements `interface_seq', else False."
    # Add all ancestor interfaces to the implementation check
    if interface_seq:
        interface_seq = unique(interfaces(*interface_seq))
    for interface in interface_seq:
        if not is_interface(interface):
            raise TypeError( \
                  "(__instance_implements): instance arg = `%s', interface arg `%s' must be an Interface" % \
                  (instance, interface))
        if not (isinstance(instance, interface) and __implements(instance, interface)):
            return False

    return True
