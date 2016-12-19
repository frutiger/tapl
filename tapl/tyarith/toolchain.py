# tapl.tyarith.toolchain

import tapl.arith.toolchain

from .typing import typeof

class Toolchain(tapl.arith.toolchain.Toolchain):
    @staticmethod
    def typeof(node):
        return typeof(node)

