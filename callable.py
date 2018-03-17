#
# SUMMARY:      Interface to make instances callable as functions
# USAGE:        inherit from Callable
# KEYWORDS:     function, instance, interface
#
# AUTHOR:       Robert Weiner
# LICENSE:      Available under the terms of the MIT License
#
# DESCRIPTION:  
"""
Callable is an interface which governs the behavior of instances
called as functions with an arbitrary number of arguments.
"""
# DESCRIP-END.

## ------------------------------------------------------------------------
## Required modules
## ------------------------------------------------------------------------

from interface import *


## ------------------------------------------------------------------------
## Interfaces
## ------------------------------------------------------------------------

class Callable(Interface):

    def __call__(iself, *args):
        """
        Invoked when the instance is ``called'' as a function.
        If this method is defined, x(arg1, arg2, ...) is a shorthand
        for x.__call__(arg1, arg2, ...).
        """
        return apply(iself.__call_body__, args)
