""" LocalEffects computes read/write effect on variables, per statement. """

from pythran.analyses.aliases import Aliases
from pythran.analyses.ancestors import Ancestors
from pythran.analyses.argument_effects import ArgumentEffects
from pythran.passmanager import FunctionAnalysis
from pythran.tables import MODULES
import pythran.intrinsic as intrinsic

import gast as ast

from collections import defaultdict
from functools import reduce

class ReadWrite(object):

    def __init__(self):
        self.reads = set()
        self.writes = set()



class LocalEffects(FunctionAnalysis):

    def __init__(self):
        # maps each statement to its read and written variables
        self.result = defaultdict(ReadWrite)
        super(LocalEffects, self).__init__(ArgumentEffects, Ancestors, Aliases)

    def parent_statement(self, node):
        for n in reversed(self.ancestors[node]):
            if isinstance(n, ast.stmt):
                return n
        raise ValueError("unexpected node without parent statement")

    def update(self, parent, ctx, alias):
        if isinstance(ctx, (ast.Load, ast.Param)):
            self.result[parent].reads.add(alias)
        elif isinstance(ctx, ast.Store):
            self.result[parent].writes.add(alias)
        else:
            raise ValueError("unexpected ctx" + str(ctx))

    def visit_Name(self, node):
        parent = self.parent_statement(node)
        self.update(parent, node.ctx, node.id)

    def visit_Subscript(self, node):
        self.generic_visit(node)
        parent = self.parent_statement(node)
        aliases = self.aliases(node.value)
        for alias in aliases:
            self.update(parent, ctx, alias)

    def visit_Call(self, node):
        self.generic_visit(node)
        func_aliases = self.aliases[node.func]
        for fa in func_aliases:
            ae = self.argument_effects[fa]
            for arg, arg_eff in zip(node.args, ae):
                if arg_eff:
                    Ctx = ast.Store
                else:
                    Ctx = ast.Load
                if isinstance(arg, ast.Name):
                    fake = ast.Name(arg.id, Ctx(), None)
                elif isinstance(arg, ast.Subscript):
                    fake = ast.Subscript(arg.value, arg.slice, Ctx())
                else:
                    continue
                self.ancestors[fake] = self.ancestors[node]
                self.visit(fake)
                del self.ancestors[fake]
