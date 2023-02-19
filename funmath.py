import math

class Format:
    def __call__(self, interp, *args):
        
        return args[0]

    def __str__(self):
        return '<Contruyendo Format>'

class ArcTan:
    def __call__(self, interp, *args):
        if len(args) != 1:
            raise Exception("ArcTan: Invalid number of arguments") #CallError
        if not isinstance(args[0], (int, float)):
            raise Exception("ArcTan: Invalid argument type") #CallError
        return math.atan(args[0])

    def __str__(self):
        return '<building ArcTan>'

class Logarithm:
    def __call__(self, interp, *args):
        if len(args) != 1:
            raise Exception("Logarithm: Invalid number of arguments") #CallError
        if not isinstance(args[0], (int, float)):
            raise Exception("Logarithm: Invalid argument type") #CallError
        return math.log(args[0])

    def __str__(self):
        return '<building Logarithm>'

LibFuncs = {

    'format': Format(),
    'atan': ArcTan(),
    'log': Logarithm(),
}