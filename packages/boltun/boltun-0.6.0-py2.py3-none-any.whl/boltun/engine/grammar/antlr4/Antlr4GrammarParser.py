# Generated from sources/boltun/engine/grammar/antlr4/Antlr4Grammar.g4 by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


import ast
import logging

from boltun.engine.grammar import RecognitionDisabledException
from boltun.util import Stack
from .Antlr4GrammarMode import Antlr4GrammarMode
from .node import NodeFilter
from .node.fork import ChoiceNode, ContentNode, RootNode
from .node.leaf import CallNode, CommentNode, DataNode

logger = logging.getLogger(__name__)

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3*")
        buf.write("\u00d0\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\3\2\3\2\7\2)\n\2\f\2\16\2,\13\2\3\2\5\2/\n\2\3\3\3\3")
        buf.write("\3\3\6\3\64\n\3\r\3\16\3\65\3\4\6\49\n\4\r\4\16\4:\3\4")
        buf.write("\3\4\3\5\3\5\3\6\3\6\3\6\5\6D\n\6\3\7\3\7\5\7H\n\7\3\7")
        buf.write("\3\7\5\7L\n\7\6\7N\n\7\r\7\16\7O\3\7\3\7\3\7\3\b\3\b\3")
        buf.write("\b\3\t\3\t\5\tZ\n\t\3\t\5\t]\n\t\3\t\3\t\5\ta\n\t\3\t")
        buf.write("\3\t\3\t\3\n\3\n\5\nh\n\n\3\n\3\n\3\n\3\n\5\nn\n\n\3\n")
        buf.write("\3\n\3\n\3\13\3\13\5\13u\n\13\3\13\5\13x\n\13\3\13\3\13")
        buf.write("\3\f\3\f\3\f\7\f\177\n\f\f\f\16\f\u0082\13\f\3\f\3\f\3")
        buf.write("\r\3\r\5\r\u0088\n\r\3\r\3\r\7\r\u008c\n\r\f\r\16\r\u008f")
        buf.write("\13\r\3\r\5\r\u0092\n\r\3\r\3\r\7\r\u0096\n\r\f\r\16\r")
        buf.write("\u0099\13\r\3\r\3\r\7\r\u009d\n\r\f\r\16\r\u00a0\13\r")
        buf.write("\5\r\u00a2\n\r\3\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3")
        buf.write("\17\3\17\3\17\3\20\3\20\5\20\u00b1\n\20\3\20\3\20\3\21")
        buf.write("\3\21\3\21\3\22\3\22\5\22\u00ba\n\22\3\22\3\22\7\22\u00be")
        buf.write("\n\22\f\22\16\22\u00c1\13\22\3\22\3\22\3\22\3\23\3\23")
        buf.write("\7\23\u00c8\n\23\f\23\16\23\u00cb\13\23\3\23\3\23\3\23")
        buf.write("\3\23\3\u00c9\2\24\2\4\6\b\n\f\16\20\22\24\26\30\32\34")
        buf.write("\36 \"$\2\3\4\2\21\22\25\25\2\u00db\2*\3\2\2\2\4\63\3")
        buf.write("\2\2\2\68\3\2\2\2\b>\3\2\2\2\nC\3\2\2\2\fE\3\2\2\2\16")
        buf.write("T\3\2\2\2\20W\3\2\2\2\22e\3\2\2\2\24r\3\2\2\2\26{\3\2")
        buf.write("\2\2\30\u0085\3\2\2\2\32\u00a6\3\2\2\2\34\u00a9\3\2\2")
        buf.write("\2\36\u00b0\3\2\2\2 \u00b4\3\2\2\2\"\u00b7\3\2\2\2$\u00c5")
        buf.write("\3\2\2\2&)\5\b\5\2\')\5\4\3\2(&\3\2\2\2(\'\3\2\2\2),\3")
        buf.write("\2\2\2*(\3\2\2\2*+\3\2\2\2+.\3\2\2\2,*\3\2\2\2-/\7\2\2")
        buf.write("\3.-\3\2\2\2./\3\2\2\2/\3\3\2\2\2\60\64\5\f\7\2\61\64")
        buf.write("\5\n\6\2\62\64\5\6\4\2\63\60\3\2\2\2\63\61\3\2\2\2\63")
        buf.write("\62\3\2\2\2\64\65\3\2\2\2\65\63\3\2\2\2\65\66\3\2\2\2")
        buf.write("\66\5\3\2\2\2\679\7\26\2\28\67\3\2\2\29:\3\2\2\2:8\3\2")
        buf.write("\2\2:;\3\2\2\2;<\3\2\2\2<=\b\4\1\2=\7\3\2\2\2>?\5\f\7")
        buf.write("\2?\t\3\2\2\2@D\5\20\t\2AD\5\22\n\2BD\5$\23\2C@\3\2\2")
        buf.write("\2CA\3\2\2\2CB\3\2\2\2D\13\3\2\2\2EG\7\3\2\2FH\5\16\b")
        buf.write("\2GF\3\2\2\2GH\3\2\2\2HM\3\2\2\2IK\7\31\2\2JL\5\16\b\2")
        buf.write("KJ\3\2\2\2KL\3\2\2\2LN\3\2\2\2MI\3\2\2\2NO\3\2\2\2OM\3")
        buf.write("\2\2\2OP\3\2\2\2PQ\3\2\2\2QR\7\4\2\2RS\b\7\1\2S\r\3\2")
        buf.write("\2\2TU\5\4\3\2UV\b\b\1\2V\17\3\2\2\2WY\7\5\2\2XZ\7\'\2")
        buf.write("\2YX\3\2\2\2YZ\3\2\2\2Z\\\3\2\2\2[]\7\25\2\2\\[\3\2\2")
        buf.write("\2\\]\3\2\2\2]`\3\2\2\2^_\7\32\2\2_a\5\26\f\2`^\3\2\2")
        buf.write("\2`a\3\2\2\2ab\3\2\2\2bc\7\6\2\2cd\b\t\1\2d\21\3\2\2\2")
        buf.write("eg\7\7\2\2fh\7\'\2\2gf\3\2\2\2gh\3\2\2\2hi\3\2\2\2ij\7")
        buf.write("\30\2\2jm\5\30\r\2kl\7\32\2\2ln\5\26\f\2mk\3\2\2\2mn\3")
        buf.write("\2\2\2no\3\2\2\2op\7\b\2\2pq\b\n\1\2q\23\3\2\2\2rt\7\30")
        buf.write("\2\2su\7\'\2\2ts\3\2\2\2tu\3\2\2\2uw\3\2\2\2vx\5\30\r")
        buf.write("\2wv\3\2\2\2wx\3\2\2\2xy\3\2\2\2yz\b\13\1\2z\25\3\2\2")
        buf.write("\2{\u0080\5\24\13\2|}\7\32\2\2}\177\5\24\13\2~|\3\2\2")
        buf.write("\2\177\u0082\3\2\2\2\u0080~\3\2\2\2\u0080\u0081\3\2\2")
        buf.write("\2\u0081\u0083\3\2\2\2\u0082\u0080\3\2\2\2\u0083\u0084")
        buf.write("\b\f\1\2\u0084\27\3\2\2\2\u0085\u00a1\7\13\2\2\u0086\u0088")
        buf.write("\5\34\17\2\u0087\u0086\3\2\2\2\u0087\u0088\3\2\2\2\u0088")
        buf.write("\u008d\3\2\2\2\u0089\u008a\7#\2\2\u008a\u008c\5\34\17")
        buf.write("\2\u008b\u0089\3\2\2\2\u008c\u008f\3\2\2\2\u008d\u008b")
        buf.write("\3\2\2\2\u008d\u008e\3\2\2\2\u008e\u00a2\3\2\2\2\u008f")
        buf.write("\u008d\3\2\2\2\u0090\u0092\5\32\16\2\u0091\u0090\3\2\2")
        buf.write("\2\u0091\u0092\3\2\2\2\u0092\u0097\3\2\2\2\u0093\u0094")
        buf.write("\7#\2\2\u0094\u0096\5\32\16\2\u0095\u0093\3\2\2\2\u0096")
        buf.write("\u0099\3\2\2\2\u0097\u0095\3\2\2\2\u0097\u0098\3\2\2\2")
        buf.write("\u0098\u009e\3\2\2\2\u0099\u0097\3\2\2\2\u009a\u009b\7")
        buf.write("#\2\2\u009b\u009d\5\34\17\2\u009c\u009a\3\2\2\2\u009d")
        buf.write("\u00a0\3\2\2\2\u009e\u009c\3\2\2\2\u009e\u009f\3\2\2\2")
        buf.write("\u009f\u00a2\3\2\2\2\u00a0\u009e\3\2\2\2\u00a1\u0087\3")
        buf.write("\2\2\2\u00a1\u0091\3\2\2\2\u00a2\u00a3\3\2\2\2\u00a3\u00a4")
        buf.write("\7\f\2\2\u00a4\u00a5\b\r\1\2\u00a5\31\3\2\2\2\u00a6\u00a7")
        buf.write("\5\36\20\2\u00a7\u00a8\b\16\1\2\u00a8\33\3\2\2\2\u00a9")
        buf.write("\u00aa\7\30\2\2\u00aa\u00ab\7 \2\2\u00ab\u00ac\5\36\20")
        buf.write("\2\u00ac\u00ad\b\17\1\2\u00ad\35\3\2\2\2\u00ae\u00b1\5")
        buf.write(" \21\2\u00af\u00b1\5\"\22\2\u00b0\u00ae\3\2\2\2\u00b0")
        buf.write("\u00af\3\2\2\2\u00b1\u00b2\3\2\2\2\u00b2\u00b3\b\20\1")
        buf.write("\2\u00b3\37\3\2\2\2\u00b4\u00b5\t\2\2\2\u00b5\u00b6\b")
        buf.write("\21\1\2\u00b6!\3\2\2\2\u00b7\u00b9\7\r\2\2\u00b8\u00ba")
        buf.write("\5\36\20\2\u00b9\u00b8\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba")
        buf.write("\u00bf\3\2\2\2\u00bb\u00bc\7#\2\2\u00bc\u00be\5\36\20")
        buf.write("\2\u00bd\u00bb\3\2\2\2\u00be\u00c1\3\2\2\2\u00bf\u00bd")
        buf.write("\3\2\2\2\u00bf\u00c0\3\2\2\2\u00c0\u00c2\3\2\2\2\u00c1")
        buf.write("\u00bf\3\2\2\2\u00c2\u00c3\7\16\2\2\u00c3\u00c4\b\22\1")
        buf.write("\2\u00c4#\3\2\2\2\u00c5\u00c9\7\t\2\2\u00c6\u00c8\7\27")
        buf.write("\2\2\u00c7\u00c6\3\2\2\2\u00c8\u00cb\3\2\2\2\u00c9\u00ca")
        buf.write("\3\2\2\2\u00c9\u00c7\3\2\2\2\u00ca\u00cc\3\2\2\2\u00cb")
        buf.write("\u00c9\3\2\2\2\u00cc\u00cd\7\n\2\2\u00cd\u00ce\b\23\1")
        buf.write("\2\u00ce%\3\2\2\2\36(*.\63\65:CGKOY\\`gmtw\u0080\u0087")
        buf.write("\u008d\u0091\u0097\u009e\u00a1\u00b0\u00b9\u00bf\u00c9")
        return buf.getvalue()


class Antlr4GrammarParser ( Parser ):

    grammarFileName = "Antlr4Grammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "LL_BRACE", "RR_BRACE", "LL_TEXT_BRACK", 
                      "RR_TEXT_BRACK", "LL_CALL_BRACK", "RR_CALL_BRACK", 
                      "LL_COMMENT_BRACK", "RR_COMMENT_BRACK", "L_PAREN", 
                      "R_PAREN", "L_BRACK", "R_BRACK", "L_BRACE", "R_BRACE", 
                      "BOOL", "NUMBER", "INT_NUMBER", "FLOAT_NUMBER", "STRING", 
                      "DATA", "COMMENT_DATA", "NAME", "DOUBLE_PIPE", "PIPE", 
                      "SLASH", "AMP", "HASH", "GREATER", "HAT", "EQUAL", 
                      "BANG", "DOT", "COMMA", "PERCENT", "TILDA", "COMMAT", 
                      "QUESTION", "WS_SKIP", "WS", "UNKNOWN" ]

    RULE_document = 0
    RULE_content = 1
    RULE_data = 2
    RULE_polyadic_tag = 3
    RULE_unary_tag = 4
    RULE_choice_tag = 5
    RULE_choice_tag_content = 6
    RULE_data_filter_tag = 7
    RULE_call_tag = 8
    RULE_fltr = 9
    RULE_fltr_chain = 10
    RULE_attr = 11
    RULE_attr_arg_def = 12
    RULE_attr_kw_arg_def = 13
    RULE_attr_value = 14
    RULE_attr_single_value = 15
    RULE_attr_list_value = 16
    RULE_comment_tag = 17

    ruleNames =  [ "document", "content", "data", "polyadic_tag", "unary_tag", 
                   "choice_tag", "choice_tag_content", "data_filter_tag", 
                   "call_tag", "fltr", "fltr_chain", "attr", "attr_arg_def", 
                   "attr_kw_arg_def", "attr_value", "attr_single_value", 
                   "attr_list_value", "comment_tag" ]

    EOF = Token.EOF
    LL_BRACE=1
    RR_BRACE=2
    LL_TEXT_BRACK=3
    RR_TEXT_BRACK=4
    LL_CALL_BRACK=5
    RR_CALL_BRACK=6
    LL_COMMENT_BRACK=7
    RR_COMMENT_BRACK=8
    L_PAREN=9
    R_PAREN=10
    L_BRACK=11
    R_BRACK=12
    L_BRACE=13
    R_BRACE=14
    BOOL=15
    NUMBER=16
    INT_NUMBER=17
    FLOAT_NUMBER=18
    STRING=19
    DATA=20
    COMMENT_DATA=21
    NAME=22
    DOUBLE_PIPE=23
    PIPE=24
    SLASH=25
    AMP=26
    HASH=27
    GREATER=28
    HAT=29
    EQUAL=30
    BANG=31
    DOT=32
    COMMA=33
    PERCENT=34
    TILDA=35
    COMMAT=36
    QUESTION=37
    WS_SKIP=38
    WS=39
    UNKNOWN=40

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    @property
    def recognition_mode(self):
        try:
            return self.__recognition_mode
        except AttributeError:
            self.__recognition_mode = Antlr4GrammarMode.CALL
            return self.__recognition_mode

    @recognition_mode.setter
    def recognition_mode(self, value):
        self.__recognition_mode = value

    @property
    def error_strategy(self):
        return self._errHandler

    @error_strategy.setter
    def error_strategy(self, value):
        self._errHandler = value

    def _validate_recognition_mode(self, mode):
        if self.recognition_mode >= mode:
            return
        raise RecognitionDisabledException(mode=mode, recognizer=self)

    @property
    def node_stack(self):
        try:
            return self._node_stack
        except AttributeError:
            self._node_stack = Stack()
            return self._node_stack

    def _get_start_pos(self, ctx):
        if not ctx:
            return None
        return ctx.start.start if ctx.start else None

    def _get_stop_pos(self, ctx):
        if not ctx:
            return None
        return ctx.stop.stop if ctx.stop else None



    class DocumentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def polyadic_tag(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Polyadic_tagContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Polyadic_tagContext,i)


        def content(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.ContentContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.ContentContext,i)


        def EOF(self):
            return self.getToken(Antlr4GrammarParser.EOF, 0)

        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_document

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocument" ):
                listener.enterDocument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocument" ):
                listener.exitDocument(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDocument" ):
                return visitor.visitDocument(self)
            else:
                return visitor.visitChildren(self)




    def document(self):

        localctx = Antlr4GrammarParser.DocumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_document)


        root_node = RootNode()
        self.node_stack.push(root_node)


        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Antlr4GrammarParser.LL_BRACE) | (1 << Antlr4GrammarParser.LL_TEXT_BRACK) | (1 << Antlr4GrammarParser.LL_CALL_BRACK) | (1 << Antlr4GrammarParser.LL_COMMENT_BRACK) | (1 << Antlr4GrammarParser.DATA))) != 0):
                self.state = 38
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 36
                    self.polyadic_tag()
                    pass

                elif la_ == 2:
                    self.state = 37
                    self.content()
                    pass


                self.state = 42
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 44
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 43
                self.match(Antlr4GrammarParser.EOF)


            self._ctx.stop = self._input.LT(-1)


            root_node = self.node_stack.peek()
            root_node.start = self._get_start_pos(localctx)
            root_node.stop = self._get_stop_pos(localctx)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ContentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def choice_tag(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Choice_tagContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Choice_tagContext,i)


        def unary_tag(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Unary_tagContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Unary_tagContext,i)


        def data(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.DataContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.DataContext,i)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_content

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContent" ):
                listener.enterContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContent" ):
                listener.exitContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContent" ):
                return visitor.visitContent(self)
            else:
                return visitor.visitChildren(self)




    def content(self):

        localctx = Antlr4GrammarParser.ContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_content)


        content_node = ContentNode()
        self.node_stack.push(content_node)


        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 49
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [Antlr4GrammarParser.LL_BRACE]:
                        self.state = 46
                        self.choice_tag()
                        pass
                    elif token in [Antlr4GrammarParser.LL_TEXT_BRACK, Antlr4GrammarParser.LL_CALL_BRACK, Antlr4GrammarParser.LL_COMMENT_BRACK]:
                        self.state = 47
                        self.unary_tag()
                        pass
                    elif token in [Antlr4GrammarParser.DATA]:
                        self.state = 48
                        self.data()
                        pass
                    else:
                        raise NoViableAltException(self)


                else:
                    raise NoViableAltException(self)
                self.state = 51 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

            self._ctx.stop = self._input.LT(-1)


            content_node = self.node_stack.pop()

            content_node.start = self._get_start_pos(localctx)
            content_node.stop = self._get_stop_pos(localctx)

            self.node_stack.peek().add_child(content_node)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DataContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._DATA = None # Token
            self.var_chars = list() # of Tokens

        def DATA(self, i:int=None):
            if i is None:
                return self.getTokens(Antlr4GrammarParser.DATA)
            else:
                return self.getToken(Antlr4GrammarParser.DATA, i)

        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_data

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterData" ):
                listener.enterData(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitData" ):
                listener.exitData(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitData" ):
                return visitor.visitData(self)
            else:
                return visitor.visitChildren(self)




    def data(self):

        localctx = Antlr4GrammarParser.DataContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_data)


        self._validate_recognition_mode(Antlr4GrammarMode.DATA)


        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 53
                    localctx._DATA = self.match(Antlr4GrammarParser.DATA)
                    localctx.var_chars.append(localctx._DATA)

                else:
                    raise NoViableAltException(self)
                self.state = 56 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)



            data_str = ''.join([c.text for c in localctx.var_chars])

            node = DataNode(data_str)


            self._ctx.stop = self._input.LT(-1)


            node.start = self._get_start_pos(localctx)
            node.stop = self._get_stop_pos(localctx)
            self.node_stack.peek().add_child(node)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Polyadic_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def choice_tag(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Choice_tagContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_polyadic_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPolyadic_tag" ):
                listener.enterPolyadic_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPolyadic_tag" ):
                listener.exitPolyadic_tag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPolyadic_tag" ):
                return visitor.visitPolyadic_tag(self)
            else:
                return visitor.visitChildren(self)




    def polyadic_tag(self):

        localctx = Antlr4GrammarParser.Polyadic_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_polyadic_tag)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.choice_tag()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Unary_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def data_filter_tag(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Data_filter_tagContext,0)


        def call_tag(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Call_tagContext,0)


        def comment_tag(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Comment_tagContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_unary_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnary_tag" ):
                listener.enterUnary_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnary_tag" ):
                listener.exitUnary_tag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary_tag" ):
                return visitor.visitUnary_tag(self)
            else:
                return visitor.visitChildren(self)




    def unary_tag(self):

        localctx = Antlr4GrammarParser.Unary_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_unary_tag)
        try:
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Antlr4GrammarParser.LL_TEXT_BRACK]:
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                self.data_filter_tag()
                pass
            elif token in [Antlr4GrammarParser.LL_CALL_BRACK]:
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.call_tag()
                pass
            elif token in [Antlr4GrammarParser.LL_COMMENT_BRACK]:
                self.enterOuterAlt(localctx, 3)
                self.state = 64
                self.comment_tag()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Choice_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._choice_tag_content = None # Choice_tag_contentContext
            self.var_content_choises = list() # of Choice_tag_contentContexts

        def LL_BRACE(self):
            return self.getToken(Antlr4GrammarParser.LL_BRACE, 0)

        def RR_BRACE(self):
            return self.getToken(Antlr4GrammarParser.RR_BRACE, 0)

        def DOUBLE_PIPE(self, i:int=None):
            if i is None:
                return self.getTokens(Antlr4GrammarParser.DOUBLE_PIPE)
            else:
                return self.getToken(Antlr4GrammarParser.DOUBLE_PIPE, i)

        def choice_tag_content(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Choice_tag_contentContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Choice_tag_contentContext,i)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_choice_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChoice_tag" ):
                listener.enterChoice_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChoice_tag" ):
                listener.exitChoice_tag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChoice_tag" ):
                return visitor.visitChoice_tag(self)
            else:
                return visitor.visitChildren(self)




    def choice_tag(self):

        localctx = Antlr4GrammarParser.Choice_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_choice_tag)


        self._validate_recognition_mode(Antlr4GrammarMode.CALL)

        choice_node = ChoiceNode()
        self.node_stack.push(choice_node)


        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.match(Antlr4GrammarParser.LL_BRACE)
            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Antlr4GrammarParser.LL_BRACE) | (1 << Antlr4GrammarParser.LL_TEXT_BRACK) | (1 << Antlr4GrammarParser.LL_CALL_BRACK) | (1 << Antlr4GrammarParser.LL_COMMENT_BRACK) | (1 << Antlr4GrammarParser.DATA))) != 0):
                self.state = 68
                localctx._choice_tag_content = self.choice_tag_content()
                localctx.var_content_choises.append(localctx._choice_tag_content)


            self.state = 75 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 71
                self.match(Antlr4GrammarParser.DOUBLE_PIPE)
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Antlr4GrammarParser.LL_BRACE) | (1 << Antlr4GrammarParser.LL_TEXT_BRACK) | (1 << Antlr4GrammarParser.LL_CALL_BRACK) | (1 << Antlr4GrammarParser.LL_COMMENT_BRACK) | (1 << Antlr4GrammarParser.DATA))) != 0):
                    self.state = 72
                    localctx._choice_tag_content = self.choice_tag_content()
                    localctx.var_content_choises.append(localctx._choice_tag_content)


                self.state = 77 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==Antlr4GrammarParser.DOUBLE_PIPE):
                    break

            self.state = 79
            self.match(Antlr4GrammarParser.RR_BRACE)



            self._ctx.stop = self._input.LT(-1)


            choice_node = self.node_stack.pop()
            choice_node.start = self._get_start_pos(localctx)
            choice_node.stop = self._get_stop_pos(localctx)

            self.node_stack.peek().add_child(choice_node)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Choice_tag_contentContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def content(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.ContentContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_choice_tag_content

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChoice_tag_content" ):
                listener.enterChoice_tag_content(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChoice_tag_content" ):
                listener.exitChoice_tag_content(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChoice_tag_content" ):
                return visitor.visitChoice_tag_content(self)
            else:
                return visitor.visitChildren(self)




    def choice_tag_content(self):

        localctx = Antlr4GrammarParser.Choice_tag_contentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_choice_tag_content)


        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.content()



            self._ctx.stop = self._input.LT(-1)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Data_filter_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.var_optional = None # Token
            self.var_data = None # Token
            self.var_fltr_chain = None # Fltr_chainContext

        def LL_TEXT_BRACK(self):
            return self.getToken(Antlr4GrammarParser.LL_TEXT_BRACK, 0)

        def RR_TEXT_BRACK(self):
            return self.getToken(Antlr4GrammarParser.RR_TEXT_BRACK, 0)

        def PIPE(self):
            return self.getToken(Antlr4GrammarParser.PIPE, 0)

        def QUESTION(self):
            return self.getToken(Antlr4GrammarParser.QUESTION, 0)

        def STRING(self):
            return self.getToken(Antlr4GrammarParser.STRING, 0)

        def fltr_chain(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Fltr_chainContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_data_filter_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterData_filter_tag" ):
                listener.enterData_filter_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitData_filter_tag" ):
                listener.exitData_filter_tag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitData_filter_tag" ):
                return visitor.visitData_filter_tag(self)
            else:
                return visitor.visitChildren(self)




    def data_filter_tag(self):

        localctx = Antlr4GrammarParser.Data_filter_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_data_filter_tag)


        self._validate_recognition_mode(Antlr4GrammarMode.CALL)


        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(Antlr4GrammarParser.LL_TEXT_BRACK)
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.QUESTION:
                self.state = 86
                localctx.var_optional = self.match(Antlr4GrammarParser.QUESTION)


            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.STRING:
                self.state = 89
                localctx.var_data = self.match(Antlr4GrammarParser.STRING)


            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.PIPE:
                self.state = 92
                self.match(Antlr4GrammarParser.PIPE)
                self.state = 93
                localctx.var_fltr_chain = self.fltr_chain()


            self.state = 96
            self.match(Antlr4GrammarParser.RR_TEXT_BRACK)


            data=ast.literal_eval((None if localctx.var_data is None else localctx.var_data.text)) if localctx.var_data else None
            optional=localctx.var_optional is not None

            node = DataNode(content=data, optional=optional)

            if localctx.var_fltr_chain:
                filters = localctx.var_fltr_chain.__data__.get('filters', None)
                node.add_filters(filters)


            self._ctx.stop = self._input.LT(-1)


            node.start = self._get_start_pos(localctx)
            node.stop = self._get_stop_pos(localctx)
            self.node_stack.peek().add_child(node)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Call_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.var_optional = None # Token
            self.var_name = None # Token
            self.var_attr = None # AttrContext
            self.var_fltr_chain = None # Fltr_chainContext

        def LL_CALL_BRACK(self):
            return self.getToken(Antlr4GrammarParser.LL_CALL_BRACK, 0)

        def RR_CALL_BRACK(self):
            return self.getToken(Antlr4GrammarParser.RR_CALL_BRACK, 0)

        def NAME(self):
            return self.getToken(Antlr4GrammarParser.NAME, 0)

        def attr(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.AttrContext,0)


        def PIPE(self):
            return self.getToken(Antlr4GrammarParser.PIPE, 0)

        def QUESTION(self):
            return self.getToken(Antlr4GrammarParser.QUESTION, 0)

        def fltr_chain(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Fltr_chainContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_call_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCall_tag" ):
                listener.enterCall_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCall_tag" ):
                listener.exitCall_tag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall_tag" ):
                return visitor.visitCall_tag(self)
            else:
                return visitor.visitChildren(self)




    def call_tag(self):

        localctx = Antlr4GrammarParser.Call_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_call_tag)


        self._validate_recognition_mode(Antlr4GrammarMode.CALL)


        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(Antlr4GrammarParser.LL_CALL_BRACK)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.QUESTION:
                self.state = 100
                localctx.var_optional = self.match(Antlr4GrammarParser.QUESTION)


            self.state = 103
            localctx.var_name = self.match(Antlr4GrammarParser.NAME)
            self.state = 104
            localctx.var_attr = self.attr()
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.PIPE:
                self.state = 105
                self.match(Antlr4GrammarParser.PIPE)
                self.state = 106
                localctx.var_fltr_chain = self.fltr_chain()


            self.state = 109
            self.match(Antlr4GrammarParser.RR_CALL_BRACK)


            name=(None if localctx.var_name is None else localctx.var_name.text)
            optional=localctx.var_optional is not None
            arg_params = localctx.var_attr.__data__.get('arg_params', None)
            kwarg_params = localctx.var_attr.__data__.get('kwarg_params', None)

            node = CallNode(name=name, optional=optional,
                            arg_params=arg_params, kwarg_params=kwarg_params)

            if localctx.var_fltr_chain:
                filters = localctx.var_fltr_chain.__data__.get('filters', None)
                node.add_filters(filters)


            self._ctx.stop = self._input.LT(-1)


            node.start = self._get_start_pos(localctx)
            node.stop = self._get_stop_pos(localctx)
            self.node_stack.peek().add_child(node)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FltrContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self.var_name = None # Token
            self.var_optional = None # Token
            self.var_attr = None # AttrContext

        def NAME(self):
            return self.getToken(Antlr4GrammarParser.NAME, 0)

        def QUESTION(self):
            return self.getToken(Antlr4GrammarParser.QUESTION, 0)

        def attr(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.AttrContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_fltr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFltr" ):
                listener.enterFltr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFltr" ):
                listener.exitFltr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFltr" ):
                return visitor.visitFltr(self)
            else:
                return visitor.visitChildren(self)




    def fltr(self):

        localctx = Antlr4GrammarParser.FltrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_fltr)



        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            localctx.var_name = self.match(Antlr4GrammarParser.NAME)
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.QUESTION:
                self.state = 113
                localctx.var_optional = self.match(Antlr4GrammarParser.QUESTION)


            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==Antlr4GrammarParser.L_PAREN:
                self.state = 116
                localctx.var_attr = self.attr()




            localctx.__data__ = {
                'name' : (None if localctx.var_name is None else localctx.var_name.text),
                'optional': localctx.var_optional is not None,

                'arg_params' : localctx.var_attr.__data__.get('arg_params') \
                               if localctx.var_attr else [],

                'kwarg_params' : localctx.var_attr.__data__.get('kwarg_params') \
                                 if localctx.var_attr else {}
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Fltr_chainContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self._fltr = None # FltrContext
            self.var_fltrs = list() # of FltrContexts

        def fltr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.FltrContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.FltrContext,i)


        def PIPE(self, i:int=None):
            if i is None:
                return self.getTokens(Antlr4GrammarParser.PIPE)
            else:
                return self.getToken(Antlr4GrammarParser.PIPE, i)

        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_fltr_chain

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFltr_chain" ):
                listener.enterFltr_chain(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFltr_chain" ):
                listener.exitFltr_chain(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFltr_chain" ):
                return visitor.visitFltr_chain(self)
            else:
                return visitor.visitChildren(self)




    def fltr_chain(self):

        localctx = Antlr4GrammarParser.Fltr_chainContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_fltr_chain)



        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 121
            localctx._fltr = self.fltr()
            localctx.var_fltrs.append(localctx._fltr)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==Antlr4GrammarParser.PIPE:
                self.state = 122
                self.match(Antlr4GrammarParser.PIPE)
                self.state = 123
                localctx._fltr = self.fltr()
                localctx.var_fltrs.append(localctx._fltr)
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)



            filters = []

            for fltr_def in localctx.var_fltrs:
                name = fltr_def.__data__.get('name')
                optional = fltr_def.__data__.get('optional')
                arg_params = fltr_def.__data__.get('arg_params')
                kwarg_params = fltr_def.__data__.get('kwarg_params')

                filter_ = NodeFilter(name=name, optional=optional,
                                     arg_params=arg_params, kwarg_params=kwarg_params)
                filters.append(filter_)

            localctx.__data__ = {
                'filters' : filters,
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AttrContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self._attr_kw_arg_def = None # Attr_kw_arg_defContext
            self.var_attr_kw_arg_defs = list() # of Attr_kw_arg_defContexts
            self._attr_arg_def = None # Attr_arg_defContext
            self.var_attr_arg_defs = list() # of Attr_arg_defContexts

        def L_PAREN(self):
            return self.getToken(Antlr4GrammarParser.L_PAREN, 0)

        def R_PAREN(self):
            return self.getToken(Antlr4GrammarParser.R_PAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(Antlr4GrammarParser.COMMA)
            else:
                return self.getToken(Antlr4GrammarParser.COMMA, i)

        def attr_kw_arg_def(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Attr_kw_arg_defContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Attr_kw_arg_defContext,i)


        def attr_arg_def(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Attr_arg_defContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Attr_arg_defContext,i)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_attr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr" ):
                listener.enterAttr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr" ):
                listener.exitAttr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)




    def attr(self):

        localctx = Antlr4GrammarParser.AttrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_attr)



        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(Antlr4GrammarParser.L_PAREN)
            self.state = 159
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 133
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==Antlr4GrammarParser.NAME:
                    self.state = 132
                    localctx._attr_kw_arg_def = self.attr_kw_arg_def()
                    localctx.var_attr_kw_arg_defs.append(localctx._attr_kw_arg_def)


                self.state = 139
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==Antlr4GrammarParser.COMMA:
                    self.state = 135
                    self.match(Antlr4GrammarParser.COMMA)
                    self.state = 136
                    localctx._attr_kw_arg_def = self.attr_kw_arg_def()
                    localctx.var_attr_kw_arg_defs.append(localctx._attr_kw_arg_def)
                    self.state = 141
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass

            elif la_ == 2:
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Antlr4GrammarParser.L_BRACK) | (1 << Antlr4GrammarParser.BOOL) | (1 << Antlr4GrammarParser.NUMBER) | (1 << Antlr4GrammarParser.STRING))) != 0):
                    self.state = 142
                    localctx._attr_arg_def = self.attr_arg_def()
                    localctx.var_attr_arg_defs.append(localctx._attr_arg_def)


                self.state = 149
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,21,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 145
                        self.match(Antlr4GrammarParser.COMMA)
                        self.state = 146
                        localctx._attr_arg_def = self.attr_arg_def()
                        localctx.var_attr_arg_defs.append(localctx._attr_arg_def) 
                    self.state = 151
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

                self.state = 156
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==Antlr4GrammarParser.COMMA:
                    self.state = 152
                    self.match(Antlr4GrammarParser.COMMA)
                    self.state = 153
                    localctx._attr_kw_arg_def = self.attr_kw_arg_def()
                    localctx.var_attr_kw_arg_defs.append(localctx._attr_kw_arg_def)
                    self.state = 158
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass


            self.state = 161
            self.match(Antlr4GrammarParser.R_PAREN)


            localctx.__data__ = {
                'arg_params' : [
                    v.__data__.get('value') for v in localctx.var_attr_arg_defs
                ],
                'kwarg_params' : {
                    v.__data__.get('name'): v.__data__.get('value')
                    for v in localctx.var_attr_kw_arg_defs
                }
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attr_arg_defContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self.var_value = None # Attr_valueContext

        def attr_value(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Attr_valueContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_attr_arg_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_arg_def" ):
                listener.enterAttr_arg_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_arg_def" ):
                listener.exitAttr_arg_def(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_arg_def" ):
                return visitor.visitAttr_arg_def(self)
            else:
                return visitor.visitChildren(self)




    def attr_arg_def(self):

        localctx = Antlr4GrammarParser.Attr_arg_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_attr_arg_def)



        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            localctx.var_value = self.attr_value()


            localctx.__data__ = {
                'value': localctx.var_value.__data__.get('value')
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attr_kw_arg_defContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self.var_name = None # Token
            self.var_value = None # Attr_valueContext

        def EQUAL(self):
            return self.getToken(Antlr4GrammarParser.EQUAL, 0)

        def NAME(self):
            return self.getToken(Antlr4GrammarParser.NAME, 0)

        def attr_value(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Attr_valueContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_attr_kw_arg_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_kw_arg_def" ):
                listener.enterAttr_kw_arg_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_kw_arg_def" ):
                listener.exitAttr_kw_arg_def(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_kw_arg_def" ):
                return visitor.visitAttr_kw_arg_def(self)
            else:
                return visitor.visitChildren(self)




    def attr_kw_arg_def(self):

        localctx = Antlr4GrammarParser.Attr_kw_arg_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_attr_kw_arg_def)



        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            localctx.var_name = self.match(Antlr4GrammarParser.NAME)
            self.state = 168
            self.match(Antlr4GrammarParser.EQUAL)
            self.state = 169
            localctx.var_value = self.attr_value()


            localctx.__data__ = {
                'name': localctx.var_name.text,
                'value': localctx.var_value.__data__.get('value')
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attr_valueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self.var_single_content = None # Attr_single_valueContext
            self.var_list_content = None # Attr_list_valueContext

        def attr_single_value(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Attr_single_valueContext,0)


        def attr_list_value(self):
            return self.getTypedRuleContext(Antlr4GrammarParser.Attr_list_valueContext,0)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_attr_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_value" ):
                listener.enterAttr_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_value" ):
                listener.exitAttr_value(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_value" ):
                return visitor.visitAttr_value(self)
            else:
                return visitor.visitChildren(self)




    def attr_value(self):

        localctx = Antlr4GrammarParser.Attr_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_attr_value)



        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [Antlr4GrammarParser.BOOL, Antlr4GrammarParser.NUMBER, Antlr4GrammarParser.STRING]:
                self.state = 172
                localctx.var_single_content = self.attr_single_value()
                pass
            elif token in [Antlr4GrammarParser.L_BRACK]:
                self.state = 173
                localctx.var_list_content = self.attr_list_value()
                pass
            else:
                raise NoViableAltException(self)



            content = None
            if localctx.var_single_content:
                content = localctx.var_single_content.__data__.get('value')
            elif localctx.var_list_content:
                content = localctx.var_list_content.__data__.get('values')

            localctx.__data__ = {
                'value': content
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attr_single_valueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self.var_value = None # Token

        def BOOL(self):
            return self.getToken(Antlr4GrammarParser.BOOL, 0)

        def NUMBER(self):
            return self.getToken(Antlr4GrammarParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(Antlr4GrammarParser.STRING, 0)

        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_attr_single_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_single_value" ):
                listener.enterAttr_single_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_single_value" ):
                listener.exitAttr_single_value(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_single_value" ):
                return visitor.visitAttr_single_value(self)
            else:
                return visitor.visitChildren(self)




    def attr_single_value(self):

        localctx = Antlr4GrammarParser.Attr_single_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_attr_single_value)



        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            localctx.var_value = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Antlr4GrammarParser.BOOL) | (1 << Antlr4GrammarParser.NUMBER) | (1 << Antlr4GrammarParser.STRING))) != 0)):
                localctx.var_value = self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()


            localctx.__data__ = {
                'value': ast.literal_eval((None if localctx.var_value is None else localctx.var_value.text))
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Attr_list_valueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self._attr_value = None # Attr_valueContext
            self.var_values = list() # of Attr_valueContexts

        def L_BRACK(self):
            return self.getToken(Antlr4GrammarParser.L_BRACK, 0)

        def R_BRACK(self):
            return self.getToken(Antlr4GrammarParser.R_BRACK, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(Antlr4GrammarParser.COMMA)
            else:
                return self.getToken(Antlr4GrammarParser.COMMA, i)

        def attr_value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(Antlr4GrammarParser.Attr_valueContext)
            else:
                return self.getTypedRuleContext(Antlr4GrammarParser.Attr_valueContext,i)


        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_attr_list_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_list_value" ):
                listener.enterAttr_list_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_list_value" ):
                listener.exitAttr_list_value(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_list_value" ):
                return visitor.visitAttr_list_value(self)
            else:
                return visitor.visitChildren(self)




    def attr_list_value(self):

        localctx = Antlr4GrammarParser.Attr_list_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_attr_list_value)



        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
            self.match(Antlr4GrammarParser.L_BRACK)
            self.state = 183
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << Antlr4GrammarParser.L_BRACK) | (1 << Antlr4GrammarParser.BOOL) | (1 << Antlr4GrammarParser.NUMBER) | (1 << Antlr4GrammarParser.STRING))) != 0):
                self.state = 182
                localctx._attr_value = self.attr_value()
                localctx.var_values.append(localctx._attr_value)


            self.state = 189
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==Antlr4GrammarParser.COMMA:
                self.state = 185
                self.match(Antlr4GrammarParser.COMMA)
                self.state = 186
                localctx._attr_value = self.attr_value()
                localctx.var_values.append(localctx._attr_value)
                self.state = 191
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 192
            self.match(Antlr4GrammarParser.R_BRACK)


            localctx.__data__ = {
                'values': [v.__data__.get('value') for v in localctx.var_values]
            }


            self._ctx.stop = self._input.LT(-1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Comment_tagContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.__data__ = dict()
            self._COMMENT_DATA = None # Token
            self.var_chars = list() # of Tokens

        def LL_COMMENT_BRACK(self):
            return self.getToken(Antlr4GrammarParser.LL_COMMENT_BRACK, 0)

        def RR_COMMENT_BRACK(self):
            return self.getToken(Antlr4GrammarParser.RR_COMMENT_BRACK, 0)

        def COMMENT_DATA(self, i:int=None):
            if i is None:
                return self.getTokens(Antlr4GrammarParser.COMMENT_DATA)
            else:
                return self.getToken(Antlr4GrammarParser.COMMENT_DATA, i)

        def getRuleIndex(self):
            return Antlr4GrammarParser.RULE_comment_tag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment_tag" ):
                listener.enterComment_tag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment_tag" ):
                listener.exitComment_tag(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComment_tag" ):
                return visitor.visitComment_tag(self)
            else:
                return visitor.visitChildren(self)




    def comment_tag(self):

        localctx = Antlr4GrammarParser.Comment_tagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_comment_tag)


        self._validate_recognition_mode(Antlr4GrammarMode.DATA)


        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 195
            self.match(Antlr4GrammarParser.LL_COMMENT_BRACK)
            self.state = 199
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,27,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 196
                    localctx._COMMENT_DATA = self.match(Antlr4GrammarParser.COMMENT_DATA)
                    localctx.var_chars.append(localctx._COMMENT_DATA) 
                self.state = 201
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,27,self._ctx)

            self.state = 202
            self.match(Antlr4GrammarParser.RR_COMMENT_BRACK)


            content = ''.join([c.text for c in localctx.var_chars]) if localctx.var_chars else None

            localctx.__data__ = {
                'content' : content
            }

            node = CommentNode(content=content)
            node.start = self._get_start_pos(localctx)
            node.stop = self._get_stop_pos(localctx)


            self._ctx.stop = self._input.LT(-1)


            node.start = self._get_start_pos(localctx)
            node.stop = self._get_stop_pos(localctx)
            self.node_stack.peek().add_child(node)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





