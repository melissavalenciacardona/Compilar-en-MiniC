'''
clex.py
El papel de este programa es convertir texto sin procesar en simbolos
conocidos como tokens. Un token consta de un tipo y un valor. Por
ejemplo, el texto '123' se representa como el token ('INTEGER', 123).
El siguiente conjunto de tokens son definidos.  El nombre sugerido del
token esta a la izquierda, un ejemplo del texto que coincida esta a la
derecha.
Palabras reservadas:
    VAR    : 'var'
    PRINT  : 'print'
    IF     : 'if'
    ELSE   : 'else'
    WHILE  : 'while'
    FUN    : 'fun'
    RETURN : 'return'
    TRUE   : 'true'
    FALSE  : 'false'
Identificadores/Nombres:
    IDENT  : Texto que inicia con una letra o '_', seguido por
             cualquier numero de letras, digitos o '_'.
             Ejemplo: 'abc', 'ABC', 'abc123', '_abc', 'a_b_c'
Literales (constantes):
    INTEGER : 123
    FLOAT   : 1.234
    STRING  : "esto es una cadena"
Operadores:
    PLUS    : '+'
    MINUS   : '-'
    TIMES   : '*'
    DIVIDE  : '/'
    LT      : '<'
    LE      : '<='
    GT      : '>'
    GE      : '>='
    EQ      : '=='
    NE      : '!='
    AND     : '&&'    (y logico, no a nivel de bits)
    OR      : '||'
    NOT     : '!'
    ASSIGN_ADD : '+='
    ASSIGN_SUB : '-='
Miselaneos:
    ASSIGN  : '='
    SEMI    : ';'
    LPAREN  : '('
    RPAREN  : ')'
    LBRACE  : '{'
    RBRACE  : '}'
    COMMA   : ','
Comentarios:
    //            Ignora el resto de la linea
    /* ... */     Ignora un bloque (no se permite anidamiento)
Errores: Su Analizador lexico opcionalmente puede reconocer y
reportar errores relacionados a caracteres ilegales, comentarios sin
terminar y otros problemas.
'''

import sly
# Definición Analizador Léxico
class Lexer(sly.Lexer):
    def __init__(self, ctxt):
        self.ctxt=ctxt # contexto de ejecución del programa

    # Definición de Símbolos
    tokens = {
        # Palabras reservadas
        FUN, VAR, PRINT, IF, ELSE, WHILE, RETURN, TRUE, FALSE,
        CLASS, FOR, WHILE, TRUE, NIL, THIS, SUPER,

        # Operadores de Relacion (long-2)
        PLUS, MINUS, TIMES, DIVIDE, POINT, SEMI, COMMA, LPAREN,
        RPAREN, LBRACE, RBRACE, LT, LE, GT, GE,
        EQ, NE, AND, OR, NOT, ASSIGN, MODULE, END_IF,
        #LSQBRA, RSQBRA,

        # Otros tokens
        IDENT, NUM, REAL, STRING,
        ADDEQ, LESSEQ, TIMESEQ, DIVEQ, MODEQ,
        
        #operadores incremento y decremento
        DOUBLE_PLUS,
        DOUBLE_MINUS,

        #Operadores break y continue
        BREAK,
        CONTINUE,

        PRINTF,

        #punto 5
        
        MFUNC,
        CLOCK, 
        LEN, 
        INPUT, 
        ISINTEGER, 
        STR, 
        INTEGER, 
        ORD, 
        CHR,
        FORMAT,
        PI,
        EULER, 
        DEG, 
        GAMMA, 
        PHI
    }
    literals = '+-*/%=(){}[];,' # Caracteres especiales 

    # Ignoramos espacios en blanco (white-space)
    ignore = ' \t\r'

    # Ignoramos newline
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Ignorar Comentarios de varias líneas
    @_(r'/\*(.|\n)*\*/')
    def ignore_comments(self, t):
        self.lineno += t.value.count('\n')

    # Ignorar Comentarios de una sola línea
    @_(r'//.*\n')
    def ignore_cppcomments(self, t):
        self.lineno += 1

    # operadores asignacion 
    ADDEQ = r'\+=' 
    LESSEQ = r'-='
    TIMESEQ = r'\*='
    DIVEQ   = r'/='
    MODEQ   = r'%='
    DOUBLE_PLUS = r'\+\+'
    DOUBLE_MINUS = r'\-\-'

    # Definicion de Tokens a traves de regexp
    PLUS = r'\+' # \ se usa para escapar caracteres especiales
    MINUS =r'-'
    TIMES =r'\*'
    DIVIDE =r'/'
    POINT =r'\.'
    SEMI =r';'
    COMMA =r','
    LPAREN =r'\('
    RPAREN =r'\)'
    LBRACE =r'{'
    RBRACE =r'}'
    #LSQBRA =r'\['
    #RSQBRA =r'\]'
    LE  = r'<='
    LT  = r'<'
    GE  = r'>='
    GT  = r'>'
    EQ  = r'=='
    NE  = r'!='
    AND = r'&&'
    OR  = r'\|\|'
    NOT = r'!'
    ASSIGN=r'='
    MODULE=r'%'

    #operadores incremento y decremento

    #Operadores break y continue
    

    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #IDENT['format'] = FORMAT
    IDENT['fun']        = FUN
    IDENT['var']        = VAR
    IDENT['print']      = PRINT
    IDENT['if']         = IF
    IDENT['else']       = ELSE
    IDENT['while']      = WHILE
    IDENT['return']     = RETURN
    IDENT['true']       = TRUE
    IDENT['false']      = FALSE
    IDENT['class']      = CLASS
    IDENT['for']        = FOR
    IDENT['while']      = WHILE
    IDENT['true']       = TRUE
    IDENT['nil']        = NIL
    IDENT['this']       = THIS
    IDENT['super']      = SUPER
    IDENT['end_if']     = END_IF
    IDENT['printf']     = PRINTF
    IDENT['break']      = BREAK
    IDENT['continue']   = CONTINUE
    IDENT['clock']      = CLOCK
    IDENT['len']        = LEN
    IDENT['input']      = INPUT
    IDENT['isinteger']  = ISINTEGER
    IDENT['str']        = STR
    IDENT['sin']        = MFUNC
    IDENT['cos']        = MFUNC
    IDENT['tan']        = MFUNC
    IDENT['sqrt']       = MFUNC
    IDENT['floor']      = MFUNC
    IDENT['ceil']       = MFUNC
    IDENT['pi']         = PI
    IDENT['euler']      = EULER
    IDENT['int']        = INTEGER
    IDENT['ord']        = ORD
    IDENT['chr']        = CHR
    IDENT['format']     = FORMAT
    IDENT['deg']        = DEG
    IDENT['gamma']      = GAMMA
    IDENT['phi']        = PHI
    
    IDENT['atan']       = MFUNC
    IDENT['asin']       = MFUNC
    IDENT['acos']       = MFUNC
    IDENT['sinh']       = MFUNC
    IDENT['cosh']       = MFUNC
    IDENT['tanh']       = MFUNC
    IDENT['log']        = MFUNC
    IDENT['log10']      = MFUNC
    IDENT['exp']        = MFUNC
    IDENT['abs']        = MFUNC
    

    
    # Definición de Tokens a traves de funciones
    @_(r'".*"')
    def STRING(self, t):
        t.value = str(t.value)
        return t

    @_(r'(\d+\.\d*)|(\.\d+)')
    def REAL(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    @_(r"'\w'")
    def CHAR(self, t):
        t.value = str(t.value)
        return t

    # encontrar la columna de un token
    #     input is the input text string
    #     token is a token instance
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column
    
        
    # Error handling rule
    def error(self, t):
        self.ctxt.error(t, f"LEX ERROR. Illegal character {str(t.value[0])} + at line: {self.lineno}") #se lo mandamos al contexto de ejecución
        self.index += 1


if __name__ == '__main__':
    import sys 

    if len(sys.argv) != 2:
        print('Usage: python clex.py filename')
        exit(0)
    
    lex = Lexer() 
    txt = open(sys.argv[1]).read()
    
    for tok in lex.tokenize(txt):
        print(tok)