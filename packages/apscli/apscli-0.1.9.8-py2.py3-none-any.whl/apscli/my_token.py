#!/usr/bin/env python 
# encoding=utf-8
"""
   NAME
     my_token.py
 
   DESCRIPTION
     this file contains some functions to evaluate an expression, e.g. '1+a+b>=2 || (x+1)!=y'
 
   NOTES
     1. Console output for each workflow contains three parts:
       a. a list of JobNode each converted from a Python dict
       b. topo_sorted_result for a.
       c. executing_result for a.
 
   MODIFIED (MM/DD/YY)
   huayang   06/04/18 - initial version 
"""

# encoding=UTF-8

from __future__ import print_function
import string, re
class Token(object):
    def __init__(self, value=None):
        self.v = value
    def __str__(self):
        return self.__class__.__name__+'('+str(self.v)+')'
    def __repr__(self):
        return self.__str__()

class TokenError(Exception): pass

# Contains operators in groups of increasing precedence
_opGroups = [
    {"||"}, {"&&"}, {"==", "!="}, {"<", "<=", ">", ">="}, {"+"}
]
class Op(Token):
    # A mapping from operators to their precedence
    _precedence = dict(
        [
            (op,i) for i in range(len(_opGroups)) for op in _opGroups[i]
        ]
    )
    
    def __gt__(self, other):
        assert  other.__class__ is Op, 'illegal precedence comparison'
        return Op._precedence[self.v] > Op._precedence[other.v]
    def __ge__(self, other):
        assert  other.__class__ is Op, 'illegal precedence comparison'
        return Op._precedence[self.v] >= Op._precedence[other.v]
    def __lt__(self, other):
        assert  other.__class__ is Op, 'illegal precedence comparison'
        return Op._precedence[self.v] < Op._precedence[other.v]
    def __le__(self, other):
        assert  other.__class__ is Op, 'illegal precedence comparison'
        return Op._precedence[self.v] <= Op._precedence[other.v]
    def __eq__(self, other):
        assert  other.__class__ is Op, 'illegal precedence comparison'
        return Op._precedence[self.v] == Op._precedence[other.v]
    def __ne__(self, other):
        assert  other.__class__ is Op, 'illegal precedence comparison'
        return Op._precedence[self.v] != Op._precedence[other.v]
    
    # def __cmp__(self, other):
    #     assert  other.__class__ is Op, 'illegal Op_precedence comparison'
    #     return cmp(Op._precedence[self.v], Op._precedence[other.v])

def num_or_non_NA_ident(t):
    return t.__class__ is Num or t.__class__ is Ident and t.v != 'N/A'
    
class Ident(Token):
    def __gt__(self, other):
        assert self.v != 'N/A' and num_or_non_NA_ident(other), 'illegal: `Ident(%s) > %s(%s)' %(self.v, other.__class__.__name__, other.v)
        return self.v > other.v
    def __ge__(self, other):
        assert self.v != 'N/A' and num_or_non_NA_ident(other), 'illegal: `Ident(%s) >= %s(%s)' %(self.v, other.__class__.__name__, other.v)
        return self.v >= other.v
    def __lt__(self, other):
        assert self.v != 'N/A' and num_or_non_NA_ident(other), 'illegal: `Ident(%s) < %s(%s)' %(self.v, other.__class__.__name__, other.v)
        return self.v < other.v
    def __le__(self, other):
        assert self.v != 'N/A' and num_or_non_NA_ident(other), 'illegal: `Ident(%s) <= %s(%s)' %(self.v, other.__class__.__name__, other.v)
        return self.v <= other.v
    def __eq__(self, other):
        assert (self.v=='N/A' and other.__class__ is NA) or \
               (self.v!='N/A' and (other.__class__ in (Num, NA) or other.__class__ is Ident and other.v!='N/A')), \
               'illegal: `Ident(%s) == %s(%s)' % (self.v, other.__class__.__name__, other.v)
        return self.v == other.v
    def __ne__(self, other):
        assert (self.v=='N/A' and other.__class__ is NA) or \
               (self.v!='N/A' and (other.__class__ in (Num, NA) or other.__class__ is Ident and other.v!='N/A')), \
               'illegal: `Ident(%s) != %s(%s)' % (self.v, other.__class__.__name__, other.v)
        return self.v != other.v
    def __add__(self, other):
        assert self.v != 'N/A' and num_or_non_NA_ident(other), 'illegal: `Ident(%s) + %s(%s)' %(self.v, other.__class__.__name__, other.v)
        return Num(self.v + other.v)

            
class Num(Token):
    def __gt__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) > %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return self.v > other.v
    def __ge__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) >= %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return self.v >= other.v
    def __lt__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) < %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return self.v < other.v
    def __le__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) <= %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return self.v <= other.v
    def __eq__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) == %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return self.v == other.v
    def __ne__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) != %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return self.v != other.v
    def __add__(self, other):
        assert num_or_non_NA_ident(other), 'illegal: `Num(%s) + %s(%s)' % (self.v, other.__class__.__name__, getattr(other,'v',other))
        return Num(self.v + other.v)

            
class NA(Token):
    pass

class LBracket(Token):
    pass

class RBracket(Token):
    pass


def _token(source):
    tokens = []
    pattern_NA_ident = re.compile(r"('N/A')( )*(=|!)=( )*([^\d\W]\w*)", re.UNICODE)
    pattern_ident_NA = re.compile(r"([^\d\W]\w*)( )*(=|!)=( )*('N/A')", re.UNICODE)

    i = 0
    while i < len(source):
        ch = source[i]
        if ch == "+":   # "+"
            i += 1
            tokens.append( Op(ch) )
        elif ch == "(":   # "(" 
            i += 1
            tokens.append( LBracket(ch) )
        elif ch == ")":   # ")"
            i += 1
            tokens.append( RBracket(ch) )
        elif ch == "=":     # "=="
            i += 1
            if i < len(source) and source[i] == "=":
                i += 1
                tokens.append( Op("==") )
            else:
                raise TokenError('illegal character at %d-%s' % (i+1,ch,))
        elif ch == "!":     # "!="
            i += 1
            if i < len(source) and source[i] == "=":
                i += 1
                tokens.append( Op("!=") )
            else:
                raise TokenError('illegal character at %d-%s' % (i+1,ch,))
        elif ch == "<":     # "<", "<="
            i += 1
            if i < len(source) and source[i] == "=":
                i += 1
                tokens.append( Op("<=") )
            else:
                tokens.append( Op("<") )
        elif ch == ">":     # ">", ">="
            i += 1
            if i < len(source) and source[i] == "=":
                i += 1
                tokens.append( Op(">=") )
            else:
                tokens.append( Op(">") )
        elif ch == "|":     #  "||"
            i += 1
            if i < len(source) and source[i] == "|":
                i += 1
                tokens.append( Op("||") )
            else:
                raise TokenError('illegal character at %d-%s' % (i+1,ch,))
        elif ch == "&":     #  "&&"
            i += 1
            if i < len(source) and source[i] == "&":
                i += 1
                tokens.append( Op("&&") )
            else:
                raise TokenError('illegal character at %d-%s' % (i+1,ch,))
        elif (ch.isalpha() or ch == "_") and re.match(pattern_ident_NA, source[i:]):
            result = re.match(pattern_ident_NA, source[i:])
            ident, _, op, _, na = result.groups()
            tokens.extend([Ident(ident), NA('N/A'), Op(op+'='), ])
            i += result.end()
        elif ch.isalpha() or ch == "_":
            identifier = ch
            i += 1
            while i < len(source):
                t = source[i]
                if t.isalpha() or t.isdigit() or t == '_':
                    identifier += t
                    i += 1
                else:
                    break
            tokens.append( Ident(identifier) )
        elif ch.isdigit():
            n = ch
            i += 1
            while i < len(source):
                t = source[i]
                if t.isdigit():
                    i += 1
                    n += t
                else:
                    break
            tokens.append( Num(int(n)) )
        elif ch == "'" and re.match(pattern_NA_ident, source[i:]):
            result = re.match(pattern_NA_ident, source[i:])
            na, _, op, _, ident = result.groups()
            tokens.extend([NA('N/A'), Op(op+'='), Ident(ident)])
            i += result.end()
        elif ch == " ":
            i += 1
            continue
        else:
            raise TokenError('illegal character at %d-%s' % (i,ch,))
    
    if tokens[0].__class__ not in (Ident, Num, NA, LBracket):
        raise TokenError('illegal character at 0')
    if tokens[-1].__class__ not in (Ident, Num, NA, RBracket):
        raise TokenError('illegal character at 0')
    # print('token: %s' % tokens)
    return tokens


def calc(expr, context):
    ops, opnd = [], []

    for t in _token(expr):
        if t.__class__ in (Num, NA, Ident):
            opnd.append(t)
        elif t.__class__ is LBracket:
            ops.append(t)
        elif t.__class__ is RBracket:
           while len(ops)>0 and ops[-1].__class__ is not LBracket:
                rhs = opnd.pop()
                lhs = opnd.pop()
                opnd.append( _op(lhs, rhs, ops.pop(), context) )
           if ops[-1].__class__ is LBracket:
               ops.pop()
        else:   # token is Op
            if len(ops)>0 and ops[-1].__class__ is not LBracket:
                while len(ops)>0 and ops[-1].__class__ is not LBracket and t<=ops[-1]:
                    rhs = opnd.pop()
                    lhs = opnd.pop()
                    opnd.append( _op(lhs, rhs, ops.pop(), context) )
            ops.append(t)

    while len(ops)>0:
        rhs = opnd.pop()
        lhs = opnd.pop()
        opnd.append( _op(lhs, rhs, ops.pop(), context) )

    last_opnd = opnd.pop()
    if last_opnd.__class__ is not bool:
        raise ValueError('illegal expr_calc_result:%s' % last_opnd)
    return last_opnd


def _op(lhs, rhs, operator, context):
    """
    function to calc logical and comparison operation and plus operation.
    Args:
        source  (str): an expression
    Returns:
        set<str>, all legal format var_definition
    Raises:
        Exception: N/A
    """
    
    if type(lhs) is Ident:
        lhs.v = context[lhs.v]
    if type(rhs) is Ident:
        rhs.v = context[rhs.v]
    operator = operator.v
    # print('lhs:%s %s rhs:%s' % (lhs, operator, rhs))

    if operator in ('+', '==', '!=', '<', '<=', '>','>=') and \
        (lhs.__class__ is bool or rhs.__class__ is bool):
            raise ValueError('illegal: `%s(%s) + %s(%s)' % (lhs.__class__.__name__, getattr(lhs,'v',lhs), rhs.__class__.__name__, getattr(rhs,'v',rhs)))
    if operator in ('||', '&&') and \
        (type(lhs) is not bool or type(rhs) is not bool):
            raise ValueError('illegal: `%s(%s) || %s(%s)' % (lhs.__class__.__name__, getattr(lhs,'v',lhs), rhs.__class__.__name__, getattr(rhs,'v',rhs)))

    if operator == '+':
        return lhs + rhs
    elif operator == '||':
        # return bool(lhs_v or rhs_v)  
        return lhs or rhs
    elif operator == '&&':
        # return bool(lhs_v and rhs_v)
        return lhs and rhs
    elif operator == '==':
        return lhs == rhs
    elif operator == '!=':
        return lhs != rhs
    elif operator == '<':
        return lhs < rhs
    elif operator == '<=':
        return lhs <= rhs
    elif operator == '>':
        return lhs > rhs
    elif operator == '>=':
        return lhs >= rhs


def _legal_var_name(s):
    """
    function to judge if a str is legal format var_definition
    Args:
        s  (str)
    Returns:
        bool
    Raises:
        Exception: N/A
    """
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if len(s.strip()) == 0:
        return False
    elif s[0] == '_' or s[0] in letters: # whether startsWith alpha or '_'
        for i in s:
            if i == '_' or i in letters or i in string.digits: # whether composed of alpha, num, or '_'
                pass
            else:
                return False
        return True
    else:
        return False


def find_var(source):
    """
    function to find all legal format var_definition in the token_list
    Args:
        source  (str): an expression
    Returns:
        set<str>, all legal format var_definition
    Raises:
        Exception: N/A
    """
    token_list = _token(source)
    return {
        token.v for token in token_list if _legal_var_name(str(token.v))
    }


if __name__ == "__main__":
    expr_list = ["3=='N/A'"
       ,"'N/A'!=3"
       ,"'N/A'!='N/A'"
       ,"1!= (0)"
       ,"x != 'N/A'"
       ,"y != 'N/A'"
       ,"x == 'N/A'"
       ,"y == 'N/A'"
       ,"x == 3"
       ,"y == 3"
       ,"x != 3"
       ,"y != 3"
       ,"x == x"
       ,"y == y"
       ,"x == y"
       ,"x != y"
       ,"'N/A' > 1"
       ,"x <= 1"
       ,"x > 1"
       ,"x + 1"
       ,"x > y"
       ,"x <= 'N/A'"
       ,"x != x"
       ,"'N/A' + 3"
       ,"3 + 'N/A'"
       ,"1 && x"
       ,"1  && (x )"
       ,"x=='N/A' || 1  && (x==y ) "
       ,"x=='N/A' || 1"
       ,"x=='N/A' || 1  && (x!=y ) "
       ,"'N/A'+x || 1  && (y+3) "
       ," || 1  && (y+3) 'N/A'==x"
       ,"3+('N/A') || 1  && (y+3) "
       ,"'N/A'>=2 || 1  && (y+3) "
       ,"(x!='N/A' || y!='N/A') && (x==3 || y==3)"
       ,"x!='N/A' || x==3"
       ,"x+3"
       ,"y+1"
       ,"x"
       ,"x>y+1"
       ,"(x!='N/A')+1"
       ,"x + x"
       ,"y+y"
       ,"True"
       ,"false"
       ,"z+1"
       ,"1==y"
       ,"(y>1)>10"
       ,"(y>1)+10"
       ,"(y>1)==10"
       ,"'N/A'==10"
       ,"x>(y>1)"
    ]
    # expr_list = [expr]
    context = {'a':100, '_1a':10, 'x': 'N/A', 'y':3}
    # for expr in expr_list:
    #     print('expr: %s' % expr)
    #     try:
    #         print(calc(expr, context))
    #     except:
    #         from traceback import print_exc
    #         print_exc()
    #     print('-')*80
    print('\n'.join(dir(Num)))
    # print(find_var('a && b && c && d'))
    # expr = '1  + y && 3 '
    # expr = '( 1  + a) && 3 == _1a + (2 || x >= 7) != y'
    # expr = '( 1  + ((0||a)&&7) && 3 == _1a + ((2 || x) >= 7) != y)'
    # tokens = list(_token(expr))
    # print(tokens)
    #ops = [t for t in tokens if t.__class__ is Op]
    #print(ops)
    #print(tokens[1]<=tokens[2])

    # context = {'a':100, '_1a':10, 'x': 1, 'y':5}
    
    #print(calc('( 1  + a) && 3 == _1a + (2 || x >= 7) != y'))
    


    # == 
    # 1. (a.变量是否是N/A(启动)  b.变量是否等于值)  
    # 2.变量是否等于变量  
    # 3.值是否等于值(a.3=='N/A' <- 通过语法报错检测 b.'N/A'=='N/A' <- 通过语法报错检测 c.0==1 正常进行计算)