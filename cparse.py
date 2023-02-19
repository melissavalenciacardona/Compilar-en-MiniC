from clex import Lexer
import sly
from cast import *
#en el archivo cast.py se encuentra la definición de la clase Visitor
#que usaremos para imprimir el AST de forma bonita

#ANALIZADOR SINTACTICO: 

class Parser(sly.Parser):
    debugfile="minic.txt" #imprime la gramatica 
    # La lista de tokens se copia desde Lexer
    tokens = Lexer.tokens 

    def __init__(self, ctxt):
        self.ctxt=ctxt # recibe el contetxto y el token y quien es su creador 

    # preceencia de operadores
    precedence = (
        ('right', ADDEQ, LESSEQ, TIMESEQ, DIVEQ, MODEQ, ASSIGN),     # menor precedencia
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE),
        ('left', LT, LE, GT, GE),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MODULE),
        ('right', UNARY), # se lee de izquierda a derecha
        ('left', DOUBLE_PLUS, DOUBLE_MINUS),
        ('nonassoc', 'ELSE')
    )

    # Definimos las reglas en BNF (o en EBNF)
    @_("{ declaration }")
    def program(self, p):
        return Program(p.declaration)

    @_("class_declaration",
       "func_declaration",
       "var_declaration",
       "statement")
    def declaration(self, p):
        return p[0]

    @_("CLASS IDENT [ LPAREN LT IDENT RPAREN ] LBRACE { function } RBRACE ")
    def class_declaration(self, p):
        return ClassDeclaration(p.IDENT0, p.IDENT1, p.function)

    @_("FUN function")
    def func_declaration(self, p):
        return p[1]

    @_("VAR IDENT [ ASSIGN expression ] SEMI")
    def var_declaration(self, p):
        return VarDeclaration(p.IDENT, p.expression)

    @_("expr_stmt",
       "for_stmt",
       "if_stmt",
       "print_stmt",
       "return_stmt",
       "while_stmt",
       "block",
       "format_stmt")
    def statement(self, p):
        return p[0]

    @_("expression SEMI")
    def expr_stmt(self, p):
        return ExprStmt(p.expression)
        #pass

    @_("FOR LPAREN for_initialize [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        body = p.statement
        if p.expression1:
            if not isinstance(body, Block):
                body = Block([ body ])

        #              init, cond, inc, body
        body = ForStmt(p.for_initialize,p.expression0,p.expression1,body)#
        #body = WhileStmt(p.expression0 or Literal(True), body)
        body = Block([p.for_initialize, body])
        return body

    @_("FOR LPAREN SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        body = p.statement 
        if p.expression1:
            if not isinstance(body, Block):
                body = Block([ body ])

            body.stmts.append(ExprStmt(p.expression1))
        body = WhileStmt(p.expression0 or Literal(True), body)
        return body

    @_("var_declaration",
        "expr_stmt")
    def for_initialize(self, p):
        return p[0]
#########################################
    @_("IF LPAREN [ expression ] RPAREN statement [ ELSE statement ] END_IF")
    def if_stmt(self, p):
        return IfStmt(p.expression, p.statement0, p.statement1)

#########################################
    @_("PRINT LPAREN expression RPAREN SEMI")
    def print_stmt(self, p):
        return Print(p.expression)

    @_("RETURN [ expression ] SEMI")
    def return_stmt (self, p):
        return Return(p.expression) 

    #agregando sentencias de continue y break a la gramatica
    @_("BREAK SEMI")
    def statement(self, p):
        return BreakStmt()

    @_("CONTINUE SEMI")
    def statement(self, p):
        return ContinueStmt()

    @_("WHILE LPAREN expression RPAREN statement")
    def while_stmt(self, p):
        return WhileStmt(p.expression, p.statement)

    @_("LBRACE { declaration } RBRACE")
    def block(self, p):
        return Block(p.declaration)
    #agregando reglas para la gramatica



    @_("expression ADDEQ expression",
       "expression LESSEQ expression",
       "expression TIMESEQ expression",
       "expression DIVEQ expression",
       "expression MODEQ expression",
       "expression ASSIGN expression")
    def expression(self, p):
        if isinstance(p.expression0, Variable):
            return Assign(p[1],p.expression0.name, p.expression1) # p[1] es el operador de asignacion que sale de cast 
        elif isinstance(p.expression0, Get):
            return Set(p[1],p.expression0.obj, p.expression0.name, p.expression1) # p[1] es el operador de asignacion que sale de cast
        else:
            raise SyntaxError(f"{p.lineno}: PARSER ERROR, it was impossible to assign {p.expression0}")

    

    @_("expression OR  expression",
       "expression AND expression")
    def expression(self, p):
        return Logical(p[1], p.expression0, p.expression1)

    @_("expression PLUS expression",
       "expression MINUS expression",
       "expression TIMES expression" ,
       "expression DIVIDE expression" ,
       "expression MODULE expression" ,
       "expression LT  expression" ,
       "expression LE  expression" ,
       "expression GT  expression" ,
       "expression GE  expression" ,
       "expression EQ  expression" ,
       "expression NE  expression")
    def expression(self, p):
        return Binary(p[1], p.expression0, p.expression1)

    @_("factor")
    def expression(self, p):
        return p.factor

    @_("REAL", "NUM", "STRING") #estos son los terminales
    def factor(self, p):
        return Literal(p[0])

    @_("TRUE", "FALSE")
    def factor(self, p):
        return Literal(p[0] == 'true')

    @_("NIL")
    def factor(self, p):
        return Literal(None)

    @_("THIS")
    def factor(self, p):
        return This()

    @_("IDENT")
    def factor(self, p):
        return Variable(p.IDENT)

    @_("SUPER POINT IDENT")
    def factor(self, p):
        return Super(p.IDENT)

    @_("factor POINT IDENT")
    def factor(self, p):
        return Get(p.factor, p.IDENT)

    @_("factor LPAREN [ arguments ] RPAREN ")
    def factor(self, p):
        return Call(p.factor, p.arguments)

    @_(" LPAREN expression RPAREN ")
    def factor(self, p):
        return Grouping(p.expression)

    @_("MINUS factor %prec UNARY",
       "NOT factor %prec UNARY")
    def factor(self, p):
        return Unary(p[0], p.factor)

    @_("MFUNC LPAREN expression RPAREN SEMI")
    def factor(self, p):
        print("FUNCION MATEMATICA")
        return MFUNC(p.name, p.expression)

    @_("FORMAT LPAREN expression RPAREN SEMI")
    def format_stmt(self, p):
        print("entrooo...  FORMATO :D")
        return Format(p.expression)

    @_("DOUBLE_PLUS expression",
       "DOUBLE_MINUS expression")
    def expression(self, p):
 
        if isinstance(p.expression, Variable):
            return PreExp(p[0], p.expression.name, p.expression)

    @_("expression DOUBLE_PLUS",
       "expression DOUBLE_MINUS")
    def expression(self, p):
        
        if isinstance(p.expression, Variable):
            return PostExp(p[1], p.expression.name, p.expression)
        
    # @_("INPUT '(' [ STRING ] ')' ';'")
    # def input(self, p):
    #     return Input(p.STRING)

    @_("IDENT LPAREN [ parameters ] RPAREN block")
    def function(self, p):
        return FuncDeclaration(p.IDENT, p.parameters, p.block)

    @_("IDENT { COMMA IDENT }")
    def parameters(self, p):
        return [ p.IDENT0 ] + p.IDENT1

    @_("expression { COMMA expression }")
    def arguments(self, p):
        return [ p. expression0 ] + p.expression1
    #p es una lista de objetos que se generan en el analisis sintactico
    #p.value es el valor del token
    #p.type es el tipo del token
    def error(self, p):  # la responsabilidad de marcar un error es de su creador ctxt
        if p:
            self.ctxt.error(p, f"PARSER ERROR, error de sintaxis en el Token {p.type} debido a: {p}") 
            # Just discard the token and tell the parser it's okay.
        else:
            self.ctxt.error(p, f"PARSER ERROR, Syntax Error in EOF")