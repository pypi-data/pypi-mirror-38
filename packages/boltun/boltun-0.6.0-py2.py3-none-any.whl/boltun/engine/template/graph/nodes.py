from __future__ import absolute_import, division, print_function

from abc import ABCMeta

import attr
from six import with_metaclass


@attr.s
class Node(with_metaclass(ABCMeta, object)):
    pass


@attr.s
class Optional(Node):
    value = attr.ib()
    alternative = attr.ib(default=None)

    def __call__(self, *args, **kwargs):
        return [self.value, self.alternative]


@attr.s
class Any(Node):
    values = attr.ib(type=list, factory=list)

    def __call__(self, *args, **kwargs):
        return self.values


@attr.s
class Const(Node):
    value = attr.ib()

    def __call__(self, *args, **kwargs):
        return self.value


@attr.s
class Call(Node):
    callable = attr.ib(type=callable)

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)
