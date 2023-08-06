# Generated from sources/boltun/engine/grammar/antlr4/Antlr4Grammar.g4 by ANTLR 4.7.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



import logging

try:
    import queue as queue
except ImportError:
    import Queue as queue

from collections import defaultdict

logger = logging.getLogger(__name__)



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2*")
        buf.write("\u012e\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3")
        buf.write("\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3")
        buf.write("\13\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16")
        buf.write("\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\20\5\20\u00ac\n\20\3\21\3\21\3\21\5\21\u00b1")
        buf.write("\n\21\3\22\3\22\6\22\u00b5\n\22\r\22\16\22\u00b6\3\23")
        buf.write("\3\23\6\23\u00bb\n\23\r\23\16\23\u00bc\3\23\3\23\7\23")
        buf.write("\u00c1\n\23\f\23\16\23\u00c4\13\23\3\24\3\24\3\24\3\24")
        buf.write("\7\24\u00ca\n\24\f\24\16\24\u00cd\13\24\3\24\3\24\3\24")
        buf.write("\3\24\7\24\u00d3\n\24\f\24\16\24\u00d6\13\24\3\24\5\24")
        buf.write("\u00d9\n\24\3\25\3\25\3\25\3\26\3\26\3\26\3\27\3\27\3")
        buf.write("\27\3\30\3\30\6\30\u00e6\n\30\r\30\16\30\u00e7\3\30\3")
        buf.write("\30\7\30\u00ec\n\30\f\30\16\30\u00ef\13\30\3\31\3\31\3")
        buf.write("\32\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\37\3\37\3\37\3 \3 \3 \3!\3!\3!")
        buf.write("\3\"\3\"\3\"\3#\3#\3#\3$\3$\3$\3%\3%\3%\3&\3&\3&\3\'\3")
        buf.write("\'\3\'\3(\3(\3(\3)\3)\3)\3*\3*\6*\u0125\n*\r*\16*\u0126")
        buf.write("\3*\3*\3+\3+\3,\3,\2\2-\3\3\5\4\7\5\t\6\13\7\r\b\17\t")
        buf.write("\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23")
        buf.write("%\24\'\25)\2+\26-\27/\30\61\2\63\2\65\31\67\329\33;\34")
        buf.write("=\35?\36A\37C E!G\"I#K$M%O&Q\'S(U)W*\3\2\6\6\2\f\f\16")
        buf.write("\17))^^\6\2\f\f\16\17$$^^\6\2//C\\aac|\5\2\13\f\16\17")
        buf.write("\"\"\2\u0138\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3")
        buf.write("\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2")
        buf.write("\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2")
        buf.write("\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2")
        buf.write("#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2")
        buf.write("\2/\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3")
        buf.write("\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E")
        buf.write("\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2")
        buf.write("O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2")
        buf.write("\3Y\3\2\2\2\5_\3\2\2\2\7e\3\2\2\2\tk\3\2\2\2\13q\3\2\2")
        buf.write("\2\rw\3\2\2\2\17}\3\2\2\2\21\u0083\3\2\2\2\23\u0089\3")
        buf.write("\2\2\2\25\u008d\3\2\2\2\27\u0091\3\2\2\2\31\u0095\3\2")
        buf.write("\2\2\33\u0099\3\2\2\2\35\u009d\3\2\2\2\37\u00ab\3\2\2")
        buf.write("\2!\u00b0\3\2\2\2#\u00b2\3\2\2\2%\u00b8\3\2\2\2\'\u00c5")
        buf.write("\3\2\2\2)\u00da\3\2\2\2+\u00dd\3\2\2\2-\u00e0\3\2\2\2")
        buf.write("/\u00e3\3\2\2\2\61\u00f0\3\2\2\2\63\u00f2\3\2\2\2\65\u00f4")
        buf.write("\3\2\2\2\67\u00f8\3\2\2\29\u00fb\3\2\2\2;\u00fe\3\2\2")
        buf.write("\2=\u0101\3\2\2\2?\u0104\3\2\2\2A\u0107\3\2\2\2C\u010a")
        buf.write("\3\2\2\2E\u010d\3\2\2\2G\u0110\3\2\2\2I\u0113\3\2\2\2")
        buf.write("K\u0116\3\2\2\2M\u0119\3\2\2\2O\u011c\3\2\2\2Q\u011f\3")
        buf.write("\2\2\2S\u0122\3\2\2\2U\u012a\3\2\2\2W\u012c\3\2\2\2YZ")
        buf.write("\6\2\2\2Z[\7}\2\2[\\\7}\2\2\\]\3\2\2\2]^\b\2\2\2^\4\3")
        buf.write("\2\2\2_`\6\3\3\2`a\7\177\2\2ab\7\177\2\2bc\3\2\2\2cd\b")
        buf.write("\3\3\2d\6\3\2\2\2ef\6\4\4\2fg\7]\2\2gh\7]\2\2hi\3\2\2")
        buf.write("\2ij\b\4\4\2j\b\3\2\2\2kl\6\5\5\2lm\7_\2\2mn\7_\2\2no")
        buf.write("\3\2\2\2op\b\5\5\2p\n\3\2\2\2qr\6\6\6\2rs\7]\2\2st\7\'")
        buf.write("\2\2tu\3\2\2\2uv\b\6\6\2v\f\3\2\2\2wx\6\7\7\2xy\7\'\2")
        buf.write("\2yz\7_\2\2z{\3\2\2\2{|\b\7\7\2|\16\3\2\2\2}~\6\b\b\2")
        buf.write("~\177\7]\2\2\177\u0080\7%\2\2\u0080\u0081\3\2\2\2\u0081")
        buf.write("\u0082\b\b\b\2\u0082\20\3\2\2\2\u0083\u0084\6\t\t\2\u0084")
        buf.write("\u0085\7%\2\2\u0085\u0086\7_\2\2\u0086\u0087\3\2\2\2\u0087")
        buf.write("\u0088\b\t\t\2\u0088\22\3\2\2\2\u0089\u008a\6\n\n\2\u008a")
        buf.write("\u008b\7*\2\2\u008b\u008c\b\n\n\2\u008c\24\3\2\2\2\u008d")
        buf.write("\u008e\6\13\13\2\u008e\u008f\7+\2\2\u008f\u0090\b\13\13")
        buf.write("\2\u0090\26\3\2\2\2\u0091\u0092\6\f\f\2\u0092\u0093\7")
        buf.write("]\2\2\u0093\u0094\b\f\f\2\u0094\30\3\2\2\2\u0095\u0096")
        buf.write("\6\r\r\2\u0096\u0097\7_\2\2\u0097\u0098\b\r\r\2\u0098")
        buf.write("\32\3\2\2\2\u0099\u009a\6\16\16\2\u009a\u009b\7}\2\2\u009b")
        buf.write("\u009c\b\16\16\2\u009c\34\3\2\2\2\u009d\u009e\6\17\17")
        buf.write("\2\u009e\u009f\7\177\2\2\u009f\u00a0\b\17\17\2\u00a0\36")
        buf.write("\3\2\2\2\u00a1\u00a2\6\20\20\2\u00a2\u00a3\7V\2\2\u00a3")
        buf.write("\u00a4\7t\2\2\u00a4\u00a5\7w\2\2\u00a5\u00ac\7g\2\2\u00a6")
        buf.write("\u00a7\7H\2\2\u00a7\u00a8\7c\2\2\u00a8\u00a9\7n\2\2\u00a9")
        buf.write("\u00aa\7u\2\2\u00aa\u00ac\7g\2\2\u00ab\u00a1\3\2\2\2\u00ab")
        buf.write("\u00a6\3\2\2\2\u00ac \3\2\2\2\u00ad\u00ae\6\21\21\2\u00ae")
        buf.write("\u00b1\5#\22\2\u00af\u00b1\5%\23\2\u00b0\u00ad\3\2\2\2")
        buf.write("\u00b0\u00af\3\2\2\2\u00b1\"\3\2\2\2\u00b2\u00b4\6\22")
        buf.write("\22\2\u00b3\u00b5\4\62;\2\u00b4\u00b3\3\2\2\2\u00b5\u00b6")
        buf.write("\3\2\2\2\u00b6\u00b4\3\2\2\2\u00b6\u00b7\3\2\2\2\u00b7")
        buf.write("$\3\2\2\2\u00b8\u00ba\6\23\23\2\u00b9\u00bb\5#\22\2\u00ba")
        buf.write("\u00b9\3\2\2\2\u00bb\u00bc\3\2\2\2\u00bc\u00ba\3\2\2\2")
        buf.write("\u00bc\u00bd\3\2\2\2\u00bd\u00be\3\2\2\2\u00be\u00c2\5")
        buf.write("G$\2\u00bf\u00c1\5#\22\2\u00c0\u00bf\3\2\2\2\u00c1\u00c4")
        buf.write("\3\2\2\2\u00c2\u00c0\3\2\2\2\u00c2\u00c3\3\2\2\2\u00c3")
        buf.write("&\3\2\2\2\u00c4\u00c2\3\2\2\2\u00c5\u00d8\6\24\24\2\u00c6")
        buf.write("\u00cb\7)\2\2\u00c7\u00ca\5)\25\2\u00c8\u00ca\n\2\2\2")
        buf.write("\u00c9\u00c7\3\2\2\2\u00c9\u00c8\3\2\2\2\u00ca\u00cd\3")
        buf.write("\2\2\2\u00cb\u00c9\3\2\2\2\u00cb\u00cc\3\2\2\2\u00cc\u00ce")
        buf.write("\3\2\2\2\u00cd\u00cb\3\2\2\2\u00ce\u00d9\7)\2\2\u00cf")
        buf.write("\u00d4\7$\2\2\u00d0\u00d3\5)\25\2\u00d1\u00d3\n\3\2\2")
        buf.write("\u00d2\u00d0\3\2\2\2\u00d2\u00d1\3\2\2\2\u00d3\u00d6\3")
        buf.write("\2\2\2\u00d4\u00d2\3\2\2\2\u00d4\u00d5\3\2\2\2\u00d5\u00d7")
        buf.write("\3\2\2\2\u00d6\u00d4\3\2\2\2\u00d7\u00d9\7$\2\2\u00d8")
        buf.write("\u00c6\3\2\2\2\u00d8\u00cf\3\2\2\2\u00d9(\3\2\2\2\u00da")
        buf.write("\u00db\7^\2\2\u00db\u00dc\13\2\2\2\u00dc*\3\2\2\2\u00dd")
        buf.write("\u00de\6\26\25\2\u00de\u00df\13\2\2\2\u00df,\3\2\2\2\u00e0")
        buf.write("\u00e1\6\27\26\2\u00e1\u00e2\13\2\2\2\u00e2.\3\2\2\2\u00e3")
        buf.write("\u00e5\6\30\27\2\u00e4\u00e6\5\61\31\2\u00e5\u00e4\3\2")
        buf.write("\2\2\u00e6\u00e7\3\2\2\2\u00e7\u00e5\3\2\2\2\u00e7\u00e8")
        buf.write("\3\2\2\2\u00e8\u00ed\3\2\2\2\u00e9\u00ec\5\61\31\2\u00ea")
        buf.write("\u00ec\5\63\32\2\u00eb\u00e9\3\2\2\2\u00eb\u00ea\3\2\2")
        buf.write("\2\u00ec\u00ef\3\2\2\2\u00ed\u00eb\3\2\2\2\u00ed\u00ee")
        buf.write("\3\2\2\2\u00ee\60\3\2\2\2\u00ef\u00ed\3\2\2\2\u00f0\u00f1")
        buf.write("\t\4\2\2\u00f1\62\3\2\2\2\u00f2\u00f3\4\62;\2\u00f3\64")
        buf.write("\3\2\2\2\u00f4\u00f5\6\33\30\2\u00f5\u00f6\7~\2\2\u00f6")
        buf.write("\u00f7\7~\2\2\u00f7\66\3\2\2\2\u00f8\u00f9\6\34\31\2\u00f9")
        buf.write("\u00fa\7~\2\2\u00fa8\3\2\2\2\u00fb\u00fc\6\35\32\2\u00fc")
        buf.write("\u00fd\7\61\2\2\u00fd:\3\2\2\2\u00fe\u00ff\6\36\33\2\u00ff")
        buf.write("\u0100\7(\2\2\u0100<\3\2\2\2\u0101\u0102\6\37\34\2\u0102")
        buf.write("\u0103\7%\2\2\u0103>\3\2\2\2\u0104\u0105\6 \35\2\u0105")
        buf.write("\u0106\7@\2\2\u0106@\3\2\2\2\u0107\u0108\6!\36\2\u0108")
        buf.write("\u0109\7`\2\2\u0109B\3\2\2\2\u010a\u010b\6\"\37\2\u010b")
        buf.write("\u010c\7?\2\2\u010cD\3\2\2\2\u010d\u010e\6# \2\u010e\u010f")
        buf.write("\7#\2\2\u010fF\3\2\2\2\u0110\u0111\6$!\2\u0111\u0112\7")
        buf.write("\60\2\2\u0112H\3\2\2\2\u0113\u0114\6%\"\2\u0114\u0115")
        buf.write("\7.\2\2\u0115J\3\2\2\2\u0116\u0117\6&#\2\u0117\u0118\7")
        buf.write("\'\2\2\u0118L\3\2\2\2\u0119\u011a\6\'$\2\u011a\u011b\7")
        buf.write("\u0080\2\2\u011bN\3\2\2\2\u011c\u011d\6(%\2\u011d\u011e")
        buf.write("\7B\2\2\u011eP\3\2\2\2\u011f\u0120\6)&\2\u0120\u0121\7")
        buf.write("A\2\2\u0121R\3\2\2\2\u0122\u0124\6*\'\2\u0123\u0125\5")
        buf.write("U+\2\u0124\u0123\3\2\2\2\u0125\u0126\3\2\2\2\u0126\u0124")
        buf.write("\3\2\2\2\u0126\u0127\3\2\2\2\u0127\u0128\3\2\2\2\u0128")
        buf.write("\u0129\b*\20\2\u0129T\3\2\2\2\u012a\u012b\t\5\2\2\u012b")
        buf.write("V\3\2\2\2\u012c\u012d\13\2\2\2\u012dX\3\2\2\2\21\2\u00ab")
        buf.write("\u00b0\u00b6\u00bc\u00c2\u00c9\u00cb\u00d2\u00d4\u00d8")
        buf.write("\u00e7\u00eb\u00ed\u0126\21\3\2\2\3\3\3\3\4\4\3\5\5\3")
        buf.write("\6\6\3\7\7\3\b\b\3\t\t\3\n\n\3\13\13\3\f\f\3\r\r\3\16")
        buf.write("\16\3\17\17\2\3\2")
        return buf.getvalue()


class Antlr4GrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    LL_BRACE = 1
    RR_BRACE = 2
    LL_TEXT_BRACK = 3
    RR_TEXT_BRACK = 4
    LL_CALL_BRACK = 5
    RR_CALL_BRACK = 6
    LL_COMMENT_BRACK = 7
    RR_COMMENT_BRACK = 8
    L_PAREN = 9
    R_PAREN = 10
    L_BRACK = 11
    R_BRACK = 12
    L_BRACE = 13
    R_BRACE = 14
    BOOL = 15
    NUMBER = 16
    INT_NUMBER = 17
    FLOAT_NUMBER = 18
    STRING = 19
    DATA = 20
    COMMENT_DATA = 21
    NAME = 22
    DOUBLE_PIPE = 23
    PIPE = 24
    SLASH = 25
    AMP = 26
    HASH = 27
    GREATER = 28
    HAT = 29
    EQUAL = 30
    BANG = 31
    DOT = 32
    COMMA = 33
    PERCENT = 34
    TILDA = 35
    COMMAT = 36
    QUESTION = 37
    WS_SKIP = 38
    WS = 39
    UNKNOWN = 40

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "LL_BRACE", "RR_BRACE", "LL_TEXT_BRACK", "RR_TEXT_BRACK", "LL_CALL_BRACK", 
            "RR_CALL_BRACK", "LL_COMMENT_BRACK", "RR_COMMENT_BRACK", "L_PAREN", 
            "R_PAREN", "L_BRACK", "R_BRACK", "L_BRACE", "R_BRACE", "BOOL", 
            "NUMBER", "INT_NUMBER", "FLOAT_NUMBER", "STRING", "DATA", "COMMENT_DATA", 
            "NAME", "DOUBLE_PIPE", "PIPE", "SLASH", "AMP", "HASH", "GREATER", 
            "HAT", "EQUAL", "BANG", "DOT", "COMMA", "PERCENT", "TILDA", 
            "COMMAT", "QUESTION", "WS_SKIP", "WS", "UNKNOWN" ]

    ruleNames = [ "LL_BRACE", "RR_BRACE", "LL_TEXT_BRACK", "RR_TEXT_BRACK", 
                  "LL_CALL_BRACK", "RR_CALL_BRACK", "LL_COMMENT_BRACK", 
                  "RR_COMMENT_BRACK", "L_PAREN", "R_PAREN", "L_BRACK", "R_BRACK", 
                  "L_BRACE", "R_BRACE", "BOOL", "NUMBER", "INT_NUMBER", 
                  "FLOAT_NUMBER", "STRING", "STRING_ESC_SEQ", "DATA", "COMMENT_DATA", 
                  "NAME", "NAME_LETTERS", "NAME_NUMBERS", "DOUBLE_PIPE", 
                  "PIPE", "SLASH", "AMP", "HASH", "GREATER", "HAT", "EQUAL", 
                  "BANG", "DOT", "COMMA", "PERCENT", "TILDA", "COMMAT", 
                  "QUESTION", "WS_SKIP", "WS", "UNKNOWN" ]

    grammarFileName = "Antlr4Grammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None



    @property
    def _state(self):
        try:
            return self.__state
        except AttributeError:
            self.__state = defaultdict(bool)
            return self.__state

    def _in(self, state):
        self._state[state] += 1

    def _out(self, state):
        self._state[state] -= 1

    def _is(self, state):
        return self._state[state] > 0

    def _not(self, state):
        return self._state[state] == 0

    def _reset_all_states(self):
        del self.__state

    @property
    def _bracket_queue(self):
        try:
            return self.__bracket_queue
        except AttributeError:
            self.__bracket_queue = queue.LifoQueue()
            return self.__bracket_queue

    def _open_bracket(self, current):
        self._bracket_queue.put(current)

    def _close_bracket(self, expected):
        if self._bracket_queue.get() == expected:
            return True
        return None

    def reset(self):
        super(Antlr4GrammarLexer, self).reset()

        self._reset_all_states()
        while not self._bracket_queue.empty():
            try:
                self._bracket_queue.get(False)
            except queue.Empty:
                continue

        self._bracket_queue.task_done()



    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[0] = self.LL_BRACE_action 
            actions[1] = self.RR_BRACE_action 
            actions[2] = self.LL_TEXT_BRACK_action 
            actions[3] = self.RR_TEXT_BRACK_action 
            actions[4] = self.LL_CALL_BRACK_action 
            actions[5] = self.RR_CALL_BRACK_action 
            actions[6] = self.LL_COMMENT_BRACK_action 
            actions[7] = self.RR_COMMENT_BRACK_action 
            actions[8] = self.L_PAREN_action 
            actions[9] = self.R_PAREN_action 
            actions[10] = self.L_BRACK_action 
            actions[11] = self.R_BRACK_action 
            actions[12] = self.L_BRACE_action 
            actions[13] = self.R_BRACE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))

    def LL_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            self._open_bracket(current='{{')
            self._in(state='choice')

     

    def RR_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:

            self._close_bracket(expected='{{')
            self._out(state='choice')

     

    def LL_TEXT_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:

            self._open_bracket(current='[[')
            self._in(state='tag')

     

    def RR_TEXT_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:

            self._close_bracket(expected='[[')
            self._out(state='tag')

     

    def LL_CALL_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:

            self._open_bracket(current='[[')
            self._in(state='tag')

     

    def RR_CALL_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:

            self._close_bracket(expected='[[')
            self._out(state='tag')

     

    def LL_COMMENT_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:

            self._open_bracket(current='[[')
            self._in(state='tag')
            self._in(state='comment')

     

    def RR_COMMENT_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 7:

            self._close_bracket(expected='[[')
            self._out(state='tag')
            self._out(state='comment')

     

    def L_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 8:

            self._open_bracket(current='(')
            self._in(state='attr')

     

    def R_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 9:

            self._close_bracket(expected='(')
            self._out(state='attr')

     

    def L_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 10:

            self._open_bracket(current='[')
            self._in(state='list')

     

    def R_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 11:

            self._close_bracket(expected='[')
            self._out(state='list')

     

    def L_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 12:

            self._open_bracket(current='{')
            self._in(state='choice_keep_ws')

     

    def R_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 13:

            self._close_bracket(expected='{')
            self._out(state='choice_keep_ws')

     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[0] = self.LL_BRACE_sempred
            preds[1] = self.RR_BRACE_sempred
            preds[2] = self.LL_TEXT_BRACK_sempred
            preds[3] = self.RR_TEXT_BRACK_sempred
            preds[4] = self.LL_CALL_BRACK_sempred
            preds[5] = self.RR_CALL_BRACK_sempred
            preds[6] = self.LL_COMMENT_BRACK_sempred
            preds[7] = self.RR_COMMENT_BRACK_sempred
            preds[8] = self.L_PAREN_sempred
            preds[9] = self.R_PAREN_sempred
            preds[10] = self.L_BRACK_sempred
            preds[11] = self.R_BRACK_sempred
            preds[12] = self.L_BRACE_sempred
            preds[13] = self.R_BRACE_sempred
            preds[14] = self.BOOL_sempred
            preds[15] = self.NUMBER_sempred
            preds[16] = self.INT_NUMBER_sempred
            preds[17] = self.FLOAT_NUMBER_sempred
            preds[18] = self.STRING_sempred
            preds[20] = self.DATA_sempred
            preds[21] = self.COMMENT_DATA_sempred
            preds[22] = self.NAME_sempred
            preds[25] = self.DOUBLE_PIPE_sempred
            preds[26] = self.PIPE_sempred
            preds[27] = self.SLASH_sempred
            preds[28] = self.AMP_sempred
            preds[29] = self.HASH_sempred
            preds[30] = self.GREATER_sempred
            preds[31] = self.HAT_sempred
            preds[32] = self.EQUAL_sempred
            preds[33] = self.BANG_sempred
            preds[34] = self.DOT_sempred
            preds[35] = self.COMMA_sempred
            preds[36] = self.PERCENT_sempred
            preds[37] = self.TILDA_sempred
            preds[38] = self.COMMAT_sempred
            preds[39] = self.QUESTION_sempred
            preds[40] = self.WS_SKIP_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def LL_BRACE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return  self._not(state='choice_keep_ws') \
                        and self._not(state='tag') 
         

    def RR_BRACE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 1:
                return  self._not(state='choice_keep_ws') \
                        and self._not(state='tag') 
         

    def LL_TEXT_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 2:
                return  self._not(state='tag') \
                            and self._not(state='attr') \
                            and self._not(state='list') \
                            and self._not(state='comment') 
         

    def RR_TEXT_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 3:
                return  self._is(state='tag') \
                            and self._not(state='comment') \
                            and self._not(state='attr') \
                            and self._not(state='list') 
         

    def LL_CALL_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 4:
                return  self._not(state='tag') \
                            and self._not(state='comment') 
         

    def RR_CALL_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 5:
                return  self._is(state='tag') \
                            and self._not(state='comment') 
         

    def LL_COMMENT_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 6:
                return  self._not(state='tag') \
                                and self._not(state='comment') 
         

    def RR_COMMENT_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 7:
                return  self._is(state='tag') \
                                and self._is(state='comment') 
         

    def L_PAREN_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 8:
                return  self._not(state='comment') 
         

    def R_PAREN_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 9:
                return  self._not(state='comment') 
         

    def L_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 10:
                return  self._is(state='attr') \
                        and self._not(state='comment') 
         

    def R_BRACK_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 11:
                return  self._is(state='attr') \
                        and self._not(state='comment') 
         

    def L_BRACE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 12:
                return  self._is(state='choice') \
                        and self._not(state='choice_keep_ws') \
                        and self._not(state='tag') 
         

    def R_BRACE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 13:
                return  self._is(state='choice') \
                        and self._is(state='choice_keep_ws') \
                        and self._not(state='tag') 
         

    def BOOL_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 14:
                return  self._is(state='tag') and self._not(state='comment') 
         

    def NUMBER_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 15:
                return  self._is(state='tag') and self._not(state='comment') 
         

    def INT_NUMBER_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 16:
                return  self._is(state='tag') and self._not(state='comment') 
         

    def FLOAT_NUMBER_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 17:
                return self._is(state='tag') and self._not(state='comment') 
         

    def STRING_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 18:
                return  self._is(state='choice') \
                         or self._is(state='tag') and self._not(state='comment') 
         

    def DATA_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 19:
                return self._not(state='tag')
         

    def COMMENT_DATA_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 20:
                return self._is(state='tag') and self._is(state='comment')
         

    def NAME_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 21:
                return self._is(state='tag') and self._not(state='comment')
         

    def DOUBLE_PIPE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 22:
                return self._is(state='choice') and self._not(state='tag')
         

    def PIPE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 23:
                return self._is(state='tag')
         

    def SLASH_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 24:
                return self._is(state='tag')
         

    def AMP_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 25:
                return self._is(state='tag')
         

    def HASH_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 26:
                return self._is(state='tag')
         

    def GREATER_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 27:
                return self._is(state='tag')
         

    def HAT_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 28:
                return self._is(state='tag')
         

    def EQUAL_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 29:
                return self._is(state='tag')
         

    def BANG_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 30:
                return self._is(state='tag')
         

    def DOT_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 31:
                return self._is(state='tag')
         

    def COMMA_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 32:
                return self._is(state='tag')
         

    def PERCENT_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 33:
                return self._is(state='tag')
         

    def TILDA_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 34:
                return self._is(state='tag')
         

    def COMMAT_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 35:
                return self._is(state='tag')
         

    def QUESTION_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 36:
                return self._is(state='tag')
         

    def WS_SKIP_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 37:
                return  self._is(state='tag') and self._not(state='comment') 
         


