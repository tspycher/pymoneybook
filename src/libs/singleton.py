"""
.. module:: incamail
   :synopsis: singleton decorator
.. moduleauthor:: Thomas Spycher <thomas.spyche@tech.swisssign.com>
"""

class Singleton(object):
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    The decorated class cannot be inherited from.
    """

    def __init__(self, decorated):
        """
        Stores the decorated method in an attribute
        """
        self._decorated = decorated

    def instance(self, *args, **kwargs):
        """
        This method is the ONLY way of getting an instance of the Decorated Class.
        
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated(*args, **kwargs)
            return self._instance

    def __call__(self, *args, **kwargs):
        """
        Call method that raises an exception in order to prevent creation
        of multiple instances of the singleton. The `Instance` method should
        be used instead.
        """
        raise TypeError(
            'Singletons must be accessed through the `Instance` method.')