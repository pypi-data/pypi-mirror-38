from collections import namedtuple
from enum import Enum


class Variable(namedtuple("Variable", ["name", "dimensions"])):
    __slots__ = []

    def as_reference(self):
        return Reference(self, index_count=0)


Reference = namedtuple("Reference", ["variable", "index_count"])

ReferenceStatus = Enum("ReferenceStatus", names=["DECLARED", "RESOLVED"])
ReferenceDirection = Enum("ReferenceDirection", names=["DOWNWARD", "UPWARD"])
ReferenceAction = namedtuple("ReferenceAction", ["reference", "status"])

Allocation = namedtuple("Allocation", ["reference", "size"])
