from __future__ import print_function

from twisted.internet.defer import Deferred, gatherResults
from twisted.internet import reactor

from types import ClassType


class BoundHook(object):

    def __init__(self, hooked, original, instance):
        self.hooked = hooked
        self.original = original
        self.instance = instance

    def __call__(self, *args, **kw):
        result = self.original(self.instance, *args, **kw)
        self.hooked.called.callback(self.instance)
        self.hooked.called = Deferred()
        return result


class HookedCall(object):

    def __init__(self, class_, hook):
        self.called = Deferred()
        self.original = getattr(class_, hook)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return BoundHook(self.called, self.original, instance)


def hook(class_, *hooks):
    methods = {}
    for hook in hooks:
        d = Deferred()
        methods[hook] = HookedCall(class_, hook)

    if issubclass(class_, object):
        type_ = type
    else:  # pragma: no cover
        # some protocols don't have object has a base class!
        type_ = ClassType

    return type_('Hooked'+class_.__name__, (class_,), methods)


def waitUntilAll(**deferreds):
    for name, d in deferreds.items():
        # This short timeout is important so that if something goes wrong, we find
        # out about it soon, rather than blocking forever on something that can
        # can no longer happen.
        d.addTimeout(0.2, reactor)
    return gatherResults(deferreds.values())
