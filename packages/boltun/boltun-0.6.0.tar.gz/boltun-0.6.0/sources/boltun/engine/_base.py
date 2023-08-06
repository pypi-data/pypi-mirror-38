from __future__ import absolute_import, division, print_function

import attr

from boltun.engine.environment import Environment
from boltun.engine.environment.extension.core import CoreExtension
from boltun.engine.grammar import Grammar
from boltun.engine.grammar.antlr4 import Antlr4Grammar
from boltun.engine.template import Compiler
from boltun.engine.template.graph import ObjectGraphCompiler


@attr.s
class Engine(object):
    grammar = attr.ib(type=Grammar, default=attr.Factory(Antlr4Grammar))
    compiler = attr.ib(type=Compiler,
                       default=attr.Factory(ObjectGraphCompiler))

    environment = attr.ib(type=Environment,
                          default=attr.Factory(
                              Environment, takes_self=True),
                          init=False)

    def __attrs_post_init__(self):
        self.environment.add_extension(CoreExtension())

    def create_template(self, input_str):
        grammar_parse_result = self.grammar.parse(input_str)

        node_tree = grammar_parse_result.node_tree

        template = \
            self.compiler.__template__(grammar_node_tree=node_tree,
                                       environment=self.environment)
        return template

    def render(self, input_str):
        template = self.create_template(input_str)
        return template.render()
