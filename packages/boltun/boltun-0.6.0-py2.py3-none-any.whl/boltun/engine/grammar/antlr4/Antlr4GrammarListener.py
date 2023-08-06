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


# This class defines a complete listener for a parse tree produced by Antlr4GrammarParser.
class Antlr4GrammarListener(ParseTreeListener):

    # Enter a parse tree produced by Antlr4GrammarParser#document.
    def enterDocument(self, ctx:Antlr4GrammarParser.DocumentContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#document.
    def exitDocument(self, ctx:Antlr4GrammarParser.DocumentContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#content.
    def enterContent(self, ctx:Antlr4GrammarParser.ContentContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#content.
    def exitContent(self, ctx:Antlr4GrammarParser.ContentContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#data.
    def enterData(self, ctx:Antlr4GrammarParser.DataContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#data.
    def exitData(self, ctx:Antlr4GrammarParser.DataContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#polyadic_tag.
    def enterPolyadic_tag(self, ctx:Antlr4GrammarParser.Polyadic_tagContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#polyadic_tag.
    def exitPolyadic_tag(self, ctx:Antlr4GrammarParser.Polyadic_tagContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#unary_tag.
    def enterUnary_tag(self, ctx:Antlr4GrammarParser.Unary_tagContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#unary_tag.
    def exitUnary_tag(self, ctx:Antlr4GrammarParser.Unary_tagContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#choice_tag.
    def enterChoice_tag(self, ctx:Antlr4GrammarParser.Choice_tagContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#choice_tag.
    def exitChoice_tag(self, ctx:Antlr4GrammarParser.Choice_tagContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#choice_tag_content.
    def enterChoice_tag_content(self, ctx:Antlr4GrammarParser.Choice_tag_contentContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#choice_tag_content.
    def exitChoice_tag_content(self, ctx:Antlr4GrammarParser.Choice_tag_contentContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#data_filter_tag.
    def enterData_filter_tag(self, ctx:Antlr4GrammarParser.Data_filter_tagContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#data_filter_tag.
    def exitData_filter_tag(self, ctx:Antlr4GrammarParser.Data_filter_tagContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#call_tag.
    def enterCall_tag(self, ctx:Antlr4GrammarParser.Call_tagContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#call_tag.
    def exitCall_tag(self, ctx:Antlr4GrammarParser.Call_tagContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#fltr.
    def enterFltr(self, ctx:Antlr4GrammarParser.FltrContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#fltr.
    def exitFltr(self, ctx:Antlr4GrammarParser.FltrContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#fltr_chain.
    def enterFltr_chain(self, ctx:Antlr4GrammarParser.Fltr_chainContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#fltr_chain.
    def exitFltr_chain(self, ctx:Antlr4GrammarParser.Fltr_chainContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#attr.
    def enterAttr(self, ctx:Antlr4GrammarParser.AttrContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#attr.
    def exitAttr(self, ctx:Antlr4GrammarParser.AttrContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#attr_arg_def.
    def enterAttr_arg_def(self, ctx:Antlr4GrammarParser.Attr_arg_defContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#attr_arg_def.
    def exitAttr_arg_def(self, ctx:Antlr4GrammarParser.Attr_arg_defContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#attr_kw_arg_def.
    def enterAttr_kw_arg_def(self, ctx:Antlr4GrammarParser.Attr_kw_arg_defContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#attr_kw_arg_def.
    def exitAttr_kw_arg_def(self, ctx:Antlr4GrammarParser.Attr_kw_arg_defContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#attr_value.
    def enterAttr_value(self, ctx:Antlr4GrammarParser.Attr_valueContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#attr_value.
    def exitAttr_value(self, ctx:Antlr4GrammarParser.Attr_valueContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#attr_single_value.
    def enterAttr_single_value(self, ctx:Antlr4GrammarParser.Attr_single_valueContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#attr_single_value.
    def exitAttr_single_value(self, ctx:Antlr4GrammarParser.Attr_single_valueContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#attr_list_value.
    def enterAttr_list_value(self, ctx:Antlr4GrammarParser.Attr_list_valueContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#attr_list_value.
    def exitAttr_list_value(self, ctx:Antlr4GrammarParser.Attr_list_valueContext):
        pass


    # Enter a parse tree produced by Antlr4GrammarParser#comment_tag.
    def enterComment_tag(self, ctx:Antlr4GrammarParser.Comment_tagContext):
        pass

    # Exit a parse tree produced by Antlr4GrammarParser#comment_tag.
    def exitComment_tag(self, ctx:Antlr4GrammarParser.Comment_tagContext):
        pass


