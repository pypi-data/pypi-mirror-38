# Generated from sources/boltun/engine/grammar/antlr4/Antlr4Grammar.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Antlr4GrammarParser import Antlr4GrammarParser
else:
    from Antlr4GrammarParser import Antlr4GrammarParser

import ast
import logging

from boltun.engine.grammar import RecognitionDisabledException
from boltun.util import Stack
from .Antlr4GrammarMode import Antlr4GrammarMode
from .node import NodeFilter
from .node.fork import ChoiceNode, ContentNode, RootNode
from .node.leaf import CallNode, CommentNode, DataNode

logger = logging.getLogger(__name__)


# This class defines a complete generic visitor for a parse tree produced by Antlr4GrammarParser.

class Antlr4GrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by Antlr4GrammarParser#document.
    def visitDocument(self, ctx:Antlr4GrammarParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#content.
    def visitContent(self, ctx:Antlr4GrammarParser.ContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#data.
    def visitData(self, ctx:Antlr4GrammarParser.DataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#polyadic_tag.
    def visitPolyadic_tag(self, ctx:Antlr4GrammarParser.Polyadic_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#unary_tag.
    def visitUnary_tag(self, ctx:Antlr4GrammarParser.Unary_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#choice_tag.
    def visitChoice_tag(self, ctx:Antlr4GrammarParser.Choice_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#choice_tag_content.
    def visitChoice_tag_content(self, ctx:Antlr4GrammarParser.Choice_tag_contentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#data_filter_tag.
    def visitData_filter_tag(self, ctx:Antlr4GrammarParser.Data_filter_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#call_tag.
    def visitCall_tag(self, ctx:Antlr4GrammarParser.Call_tagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#fltr.
    def visitFltr(self, ctx:Antlr4GrammarParser.FltrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#fltr_chain.
    def visitFltr_chain(self, ctx:Antlr4GrammarParser.Fltr_chainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#attr.
    def visitAttr(self, ctx:Antlr4GrammarParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#attr_arg_def.
    def visitAttr_arg_def(self, ctx:Antlr4GrammarParser.Attr_arg_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#attr_kw_arg_def.
    def visitAttr_kw_arg_def(self, ctx:Antlr4GrammarParser.Attr_kw_arg_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#attr_value.
    def visitAttr_value(self, ctx:Antlr4GrammarParser.Attr_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#attr_single_value.
    def visitAttr_single_value(self, ctx:Antlr4GrammarParser.Attr_single_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#attr_list_value.
    def visitAttr_list_value(self, ctx:Antlr4GrammarParser.Attr_list_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by Antlr4GrammarParser#comment_tag.
    def visitComment_tag(self, ctx:Antlr4GrammarParser.Comment_tagContext):
        return self.visitChildren(ctx)



del Antlr4GrammarParser