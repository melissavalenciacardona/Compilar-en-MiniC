# mc.py
'''
usage: mc.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input
Compiler for MiniC programs
positional arguments:
  input              MiniC program file to compile
optional arguments:
  -h, --help         show this help message and exit
  -d, --debug        Generate assembly with extra information (for debugging
                     purposes)
  -o OUT, --out OUT  File name to store generated executable
  -l, --lex          Store output of lexer
  -D, --dot          Generate AST graph as DOT format
  -p, --png          Generate AST graph as png format
  -I, --ir           Dump the generated Intermediate representation
  --sym              Dump the symbol table
  -S, --asm          Store the generated assembly file
  -R, --exec         Execute the generated program
'''
#import docopt

#from argparse import ArgumentParser
from context import Context
from rich import print
from render import DotRender


def main(argv):
    if len(argv) > 2: # si el usuario ingresa más de 2 argumentos
        raise SystemExit(f'Usar: mc.py filename')

    ctxt = Context() # creamos un contexto
    if len(argv) == 2: 
        print(f'Compilador... {argv[0]}') # si el usuario ingresa como argumento el nombre del archivo
        print(f'Compilar... {argv[1]}') # si el usuario ingresa un archivo

        with open(argv[1]) as file: # abrimos el archivo
            source = file.read()

        

        print("\n ################################ MiniC Compiler ################################")
        ctxt.parse(source) # parseamos el archivo
        #imprimir tokens
        print("\t\t\t\n ################################### Tokens #####################################\n")
        lex = ctxt.lexer
        #print(i) error a nivel semantico i no definida 
        for tok in lex.tokenize(source): 
            print(tok)

        print("\n #################################### ARBOL #####################################\n")
        print(ctxt.ast) # imprimimos el AST
        print("\n ################################# DOT LANGUAGE #################################\n")
        dot = DotRender.render(ctxt.ast) # imprimimos el AST en DOT
        print(dot)

        print("\n ############################ CHECKER + INTERPRETER #############################")
        ctxt.run() # corremos el interprete

    else:
        try:
            while True:
                source = input("mc > ")
                ctxt.parse(source)
                if ctxt.have_errors: continue
                for stmt in ctxt.ast.stmts:
                    ctxt.ast = stmt
                    ctxt.run()

        except EOFError:
            pass

if __name__ == "__main__":
    from sys import argv # recibir argumentos

    main(argv) # ejecutar main