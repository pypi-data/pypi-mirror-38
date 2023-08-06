# lextab.py. This file automatically created by PLY (version 3.9). Don't edit!
_tabversion   = '3.8'
_lextokens    = set(('SUBSET', 'NUMBER', 'SQ_LPAREN', 'SEPARATOR', 'TRUE', 'MINUS', 'DIVIDE', 'LE', 'RPAREN', 'NE', 'LT', 'COMMA', 'PLUS', 'AND', 'GT', 'STRING', 'EQUALS', 'TIMES', 'GE', 'LPAREN', 'IN', 'VAR', 'EQ', 'SQ_RPAREN', 'FALSE', 'NOT', 'OR'))
_lexreflags   = 0
_lexliterals  = '!'
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_STRING>"[^\\"]*")|(?P<t_NUMBER>(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?(kb|gb|mb|tb|pb|Kb|Gb|Mb|Tb|Pb)?)|(?P<t_VAR>[a-zA-Z_][a-zA-Z0-9_]*)|(?P<t_AND>\\&\\&)|(?P<t_OR>\\|\\|)|(?P<t_LE>\\<\\=)|(?P<t_NE>\\!\\=)|(?P<t_GE>\\>\\=)|(?P<t_EQ>\\=\\=)|(?P<t_LPAREN>\\()|(?P<t_PLUS>\\+)|(?P<t_SEPARATOR>\\;)|(?P<t_COMMA>\\,)|(?P<t_SQ_LPAREN>\\[)|(?P<t_SQ_RPAREN>\\])|(?P<t_LT>\\<)|(?P<t_TIMES>\\*)|(?P<t_RPAREN>\\))|(?P<t_GT>\\>)|(?P<t_DIVIDE>/)|(?P<t_MINUS>-)|(?P<t_EQUALS>=)', [None, ('t_STRING', 'STRING'), ('t_NUMBER', 'NUMBER'), None, None, None, None, ('t_VAR', 'VAR'), (None, 'AND'), (None, 'OR'), (None, 'LE'), (None, 'NE'), (None, 'GE'), (None, 'EQ'), (None, 'LPAREN'), (None, 'PLUS'), (None, 'SEPARATOR'), (None, 'COMMA'), (None, 'SQ_LPAREN'), (None, 'SQ_RPAREN'), (None, 'LT'), (None, 'TIMES'), (None, 'RPAREN'), (None, 'GT'), (None, 'DIVIDE'), (None, 'MINUS'), (None, 'EQUALS')])]}
_lexstateignore = {'INITIAL': ' \t\n'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
