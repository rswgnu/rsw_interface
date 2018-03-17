# README.md:  RSW Interface - interface conformance for Python

## AUTHOR:       Robert Weiner

## VERSION:      1.0.0

## LICENSE:      Available under the terms of the MIT License

## DESCRIPTION:

This package helps Python scale to large multi-party implementations
where contractual enforcement of public interface specifications is
critical to both the development and quality assurance cycles.  It is
also an exercise in strong documentation and error reporting techniques.

The original package predates the addition of Abstract Base Classes
to Python and still contains features not provided therein.  The core
code is clean, well documented and fits in a single module.

An `interface` is a protocol to which classes may conform that
consists of a set of method signatures (calling conventions), pre- and
post- conditions and attributes.  An Interface typically represents
a common abstract pattern that is one aspect of a class, for example,
a Python List would conform to the Ordered and Indexable interfaces.

Interfaces are built using standard Python classes.  All
interfaces inherit from the top-level `Interface' class.

An interface `i2' ``extends'' another interface `i1' iff `i2' inherits
from `i1'.

A class ``implements'' an interface (and thus conforms to it) iff:

       it inherits from the interface;

       it or its ancestors redefine/implement all of the stub or body
       methods declared by the interface, keeping the number of
       arguments per method the same and renaming the first arg of
       each stub method from `iself' to `self';
      
       and its definition is followed by a call to:<br>
          assert_implements(aClass)<br>
       this marks the class as a non-interface and confirms that it
       does in fact implement the interfaces from which it inherits.

Interfaces are implemented using standard Python classes but have at
least one method that is not implemented (stub method); each interface
stub method may have a doc string as well as pre- and post-condition
assertions.  An attempt to instantiate an interface triggers an error.

A stub method is distinguished from other methods by naming its first
argument, `iself', short for "interface self".  Each stub method
exists to provide a calling protocol to which any implementor must
conform.  The implementor may either overload the stub method,
replacing it completely or more commonly may overload its "body
method", keeping the stub method's signature, doc string and pre- and
post-conditions.  Body method names are computed from the interface
stub method name by adding a ``_body'' to the name:

          stub      =>     stub_body<br>
        __stub      =>   __stub_body<br>
        __stub__    =>   __stub_body__

At the start of each interface definition, each stub body within the
class should be equated to the "Interface.error" method so that if the
stub (or the stub body) is called, an exception will be signaled:

        stub_body1 = stub_body2 = Interface.error

The "interface.py" module supplies the full mechanics for interfaces.
The following are public functions defined in this module, not
methods.  (They are functions since many must work on objects of any
type; the ones that take operands of more specific types, such as
`extends' are functions so that they may be called similarly; type
checks ensure that they raise exceptions if called with an invalid
argument).

     assert_implements(aClass)
         call after a class definition to assert interface conformance

     extends(interface, *interfaces):
         boolean test of whether an `interface' extends one or more
		 other `interfaces' (via inheritance); this is false if any arg
         is not an interface

     implements(obj, *interfaces)
         boolean test of whether a class or instance implements one or
		 more interfaces; this is false if any of `interfaces' is not
         an interface

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
         boolean test of whether `obj' is an interface

     -----

     ancestor_names(obj, exclude_interfaces=0)
         return a list of ancestor class or interface names of `obj'
         (class, interface or instance), including `obj' itself;
		 ancestors are returned in depth-first order, left to right;
         with optional `exclude_interfaces', interface ancestors are
         removed 

     ancestors(obj, exclude_interfaces=0)
         return a list of ancestor class or interface objects of `obj'
         (class, interface or instance), including `obj' itself;
		 ancestors are returned in depth-first order, left to right;
         with optional `exclude_interfaces', interface ancestors are
         removed 

     flatten (*objs)
         return a single-level list of all atomic objects in `*obj'
		 (anything other than sequences, dictionaries and Indexable
         types) in original order

     unique(*sequences)
         return a flattened list with duplicates removed from any
		 number of atomic or `sequence' args; does not sort the
		 elements


## SAMPLES

Four sample interfaces are provided:

    * GetSet - Interface for overloading get, set and del operations of attributes
    * Comparable - Interface for instances which are less-than, equal-to or greater-than each other
    * Hashable - Interface for instances which generate a hash code for use in dictionaries
    * Instantiable - Standard interface of overloadable instance methods to which most classes should conform


## TESTING

To test that Interface definition is working properly, use your
Python 3 executable like so:

	python getset.py

This will tell you if both the GetSet interface and the core interface
code are working properly.


## BENEFITS OF RSW INTERFACE OVER OTHER WORK

* RSW Interface has a simpler Interface inheritance structure
  and a simpler set of core interface handling functions.

* RSW Interface allows for implementation inheritance where
  appropriate.
  stubs (deferred methods).

* RSW Interface enforces the contractual responsibility of interfaces
  extended by other interfaces.  This minimizes the learning curve and
  maximizes the utility of interfaces.

* RSW Interface can embed pre- and post-conditions within
  Interface method stubs.

* RSW Interface provides a full set of functions which allow one to
  query both classes and interfaces uniformly for the interfaces which
  they support or to separately use the "extends" and "implements"
  functions to differentiate extension (interfaces extending other
  interfaces) from implementation (classes implementing interfaces).

* RSW Interface error messages are clear and explicit, pointing the
  developer to the precise source of any interface conformance problem.


## ATTRIBUTION

For completeness of attribution, please note that many of the
documentation strings within the included interfaces themselves are
derived from the standard Python library documentation.

All other work is original.


-- The End --

