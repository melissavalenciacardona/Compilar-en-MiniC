'''
cast.py

Estructura del árbol de síntaxis abstracto
'''
from dataclasses import *
from typing import Any, List
from multimethod import multimeta

#----------------------------------------------------------------------
#clases abstractas
#----------------------------------------------------------------------

@dataclass
class Visitor(metaclass=multimeta):
    '''
    Implementa el Patron Visitor
    '''
    pass

@dataclass
class Node():
    def accept(self, vis: Visitor):
        return vis.visit(self)

@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    pass

@dataclass
class Declaration(Statement):
    pass

# ---------------------------------------------------------------------
#  Declaration son Statement especiales que declara la existencia de algo
# ---------------------------------------------------------------------
@dataclass
class ClassDeclaration(Declaration):
    name   : str
    sclass : str
    methods: List[Statement] = field(default_factory=list)


@dataclass
class FuncDeclaration(Declaration):
    name   : str
    parameters: List[Expression] = field(default_factory=list)
    stmts  : List[Statement] = field(default_factory=list)

@dataclass
class VarDeclaration(Declaration):
    name   : str
    expr   : Expression


#---------------------------------------------------------------
# Statement representan acciones sin valores asociados
#---------------------------------------------------------------

@dataclass
class Program(Statement):
    decl   : List[Statement] = field(default_factory=list)

#@dataclass
#class Print(Statement):
#    expr   : Expression

@dataclass
class Print(Statement):
    expr: list[Expression] = field(default_factory=list)

@dataclass
class MFUNC(Expression):
    name   : str
    value  : Expression

@dataclass
class IfStmt(Statement):
    cond   : Expression
    cons   : List [Statement]=field(default_factory=list) #el consecuente
    altr   : List [Statement]=field(default_factory=list)

@dataclass
class WhileStmt(Statement): #clase que representa un while
    
    cond  : Expression
    body  : List[Statement]=field(default_factory=list)
    in_loop: bool = True

@dataclass
class ForStmt(Statement): #clase que representa un for
    for_init : Expression # inicializacion
    for_cond : Expression # condicion
    for_increment : Expression # incremento
    for_body : List[Statement]=field(default_factory=list)


@dataclass
class Return(Statement):
    expr  : Expression

@dataclass
class ExprStmt(Statement):
    expr  : Expression

@dataclass
class Block(Statement):
    stmts :  List[Statement] = field(default_factory=list)

@dataclass
class ContinueStmt(Statement):
    "una sentencia continue para el for"
    pass

@dataclass
class BreakStmt(Statement):
    "una sentencia break para el for"
    pass
    
# @dataclass
# class Input(Statement):
#     prompt: str 
#---------------------------------------------------------------
# Expression representan valores
#---------------------------------------------------------------

@dataclass
class Literal(Expression):
    #todo lo de primary
    value  : Any

@dataclass
class Binary(Expression): #tiene un hijo izquierdo y un hijo derecho, o sea, suma, resta, multiplicación y división
    op     : str
    left   : Expression
    right  : Expression


@dataclass
class Logical(Expression):
    op     : str            # <, <=, >, >=, ==, !=, && , ||
    left   : Expression
    right  : Expression


@dataclass
class Unary(Expression):
    op     : str           # -, !
    expr   : Expression

@dataclass
class Grouping(Expression):
    expr  : Expression


@dataclass
class Variable(Expression):
    name   : str

@dataclass
class Assign(Expression):
    op     : str            # =, +=, -=, *=, /=, %=
    name   : str
    expr   : Expression

@dataclass
class Call(Expression):
    func  : Expression
    args  : List[Expression]=field(default_factory=list)


@dataclass
class Set(Expression):
    obj   : str
    name  : str
    expr  : Expression


@dataclass
class Get(Expression):
    obj   : str
    name  : str


@dataclass
class Super(Expression):
    name   : str

@dataclass
class List(Expression):
    name   : str

@dataclass
class This(Expression):
    pass

@dataclass
class PostExp(Expression):
    op     : str            
    name   : str
    expr   : Expression

@dataclass
class PreExp(Expression):
    op     : str            
    name   : str
    expr   : Expression
    
@dataclass
class Format(Expression):
    format : Expression

# @dataclass
# class Input(Statement):
#     prompt: str = None
