#!/usr/bin/python3

import ltr_properties
from PyQt5.QtWidgets import QApplication
import json
import sys

from typing import List, Dict, Optional
from enum import Enum, auto

filename = "data/mainOutput.json"

def printLoadedClass(obj):
    classDesc = type(obj).__name__ + ":"
    for slot in obj.__slots__:
        if hasattr(obj, slot):
            classDesc += " " + slot + "=" + str(getattr(obj, slot))
    print("Loaded " + classDesc)

class Color():
    __slots__ = "r", "g", "b"
    def __init__(self, r=0, g=0, b=0):
        self.setRgb(r, g, b)

    def postLoad(self):
        printLoadedClass(self)
    
    def getRgb(self):
        return self.r, self.g, self.b

    def setRgb(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Vector():
    __slots__ = "x", "y", "z"
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def postLoad(self):
        printLoadedClass(self)

class Baz():
    __slots__ = "x"
    def __init__(self):
        self.x = 10000

    def postLoad(self):
        printLoadedClass(self)

class FancyBaz(Baz):
    __slots__ = "fanciness"
    fanciness: ltr_properties.Link[Color]

class Bar(object):
    __slots__ = "a", "b", "c", "d", "e", "f", "_hidden"

    # Type hints are optional, but are checked when deserializing. For lists and
    # dicts, they allow empty lists/dicts to be filled with new elements, rather
    # than requiring an existing element to duplicate.
    a: Dict[str, str]
    b: str
    c: List[Color]
    d: List[Vector]
    e: Baz
    f: Optional[Vector]
    def __init__(self):
        self.a = {"one": "a", "two": "b"}
        self.b = "two"
        self.c = [Color(0, 150, 255), Color(), Color(255, 255, 255)]
        self.d = [Vector(), Vector(1, 4, 9), Vector(255, 0, -255)]
        self.e = Baz()
        self._hidden = "Shouldn't show up"

    def postLoad(self):
        printLoadedClass(self)

class EnumVal(Enum):
    Val1 = auto()
    Val2 = auto()
    Val3 = auto()

class Foo(object):
    __slots__ = "x", "y", "z", "w", "s", "b", "v", "ev"
    ev: EnumVal
    def __init__(self):
        self.x = 0
        self.y = -25.1
        self.z = [-100, 20, 3]
        self.w = True
        self.s = "test"
        self.b = Bar()
        self.v = Vector(1, 4, 9)
        self.ev = EnumVal.Val1

    def postLoad(self):
        printLoadedClass(self)

class OptionalTest(object):
    __slots__ = "f", "of"
    f: float
    of: Optional[float]

    def postLoad(self):
        printLoadedClass(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    currentModule = sys.modules[__name__]

    ltrEditor = ltr_properties.LtrEditor("data", currentModule, serializerIndent=4)
    ltrEditor.addCustomEditorMapping(Color, ltr_properties.EditorColor)
    ltrEditor.addCustomEditorMapping(Vector, ltr_properties.EditorSlottedClassHorizontal)

    ltrEditor.setGeometry(300, 200, 900, 900)
    ltrEditor.setWindowTitle('LtRandolph Property Editor')
    ltrEditor.show()
    app.exec_()
