# cinterp.py
'''
Tree-walking interpreter
'''
from collections import ChainMap
from cast    import *
from checker import Checker
from rich    import print
from funmath import *

import math

# Veracidad en MiniC
def _is_truthy(value):
	if isinstance(value, bool): #If the object is already a boolean
		return value
	elif value is None: # if the object is empty
		return False
	else:
		return True #if the object is not empty

		

class ReturnException(Exception):
	def __init__(self, value):
		self.value = value	#it sets the value for exception

class ContinueException(Exception):
	pass

class BreakException(Exception):
	pass
	

class MiniCExit(BaseException):
	pass

class CallError(Exception):
	pass

class AttributeError(Exception):
	pass

class Function:
	def __init__(self, node, env): #it receives the node and a context
		self.node = node
		self.env = env

	def __call__(self, interp, *args): #it receives de interpreter and a tuple
		if len(args) != len(self.node.parameters):
			raise CallError(f"Interp Error. Expected {len(self.node.params)} arguments")
		newenv = self.env.new_child() #we create a new environment
		for name, arg in zip(self.node.parameters, args):
			newenv[name] = arg

		oldenv = interp.env #we update the interpreter's environment
		interp.env = newenv
		try:
			interp.visit(self.node.stmts)
			result = None
		except ReturnException as e:
			result = e.value
		finally:
			interp.env = oldenv #we reset the last fully functional environment
		return result #returns Function exceptions

	def bind(self, instance): #I receive something called instance
		env = self.env.new_child() #I create a new environment
		env['this'] = instance #we add a new value for key 'this'
		return Function(self.node, env)


class Class:
	def __init__(self, name, sclass, methods): #this is a Class framework for any class
		self.name = name
		self.sclass = sclass
		self.methods = methods

	def __str__(self): #returns the string representation of the object
		return self.name

	def __call__(self, *args): #this class and can be called like a function.  Class()
		this = Instance(self)
		init = self.find_method('init')
		if init:
			init.bind(this)(*args) #I re-define the use for 'This'
		return this

	def find_method(self, name):
		meth = self.methods.get(name)
		if meth is None and self.sclass:
			return self.sclass.find_method(name)
		return meth

class Instance:
	def __init__(self, klass):
		self.klass = klass
		self.data = { }

	def __str__(self):
		return self.klass.name + " instance"

	def get(self, name):
		if name in self.data:
			return self.data[name]
		method = self.klass.find_method(name)
		if not method:
			raise AttributeError(f'interp Error, Not defined property {name}')
		return method.bind(self)

	def set(self, name, value):
		self.data[name] = value

class Excepcion:
	pass 

ThereIsBreak = False
ThereIsContinue = False


class Interpreter(Visitor): #This is a visitor
	def __init__(self, ctxt):
		self.ctxt = ctxt 				#receives a Context (the project's manager)
		self.env  = ChainMap()			#generates ChainMap
		self.check_env = ChainMap()
		self.localmap = {}
		self.loop_iterator = None
		#self.env['print'] = print		#adds print to the environment
		#self.env['input'] = input		#adds input to the environment

	def new_label(self):
		'''Generates a new jump label and returns it'''
		label = ".L%d" % self.__label
		self.__label += 1
		return label

	def _check_numeric_operands(self, node, left, right):
		if isinstance(left, (int, float)) and isinstance(right, (int, float)):
			return True
		else:
			self.error(node, f"Interp Error. In '{node.op}' the operands must be numerical type")

	def _check_numeric_operand(self, node, value):
		if isinstance(value, (int, float)):
			return True
		else:
			self.error(node, f"Interp Error. In '{node.op}' the operand must be numerical type")

	def error(self, position, message):
		self.ctxt.error(position, message)
		raise MiniCExit()



	# Punto de entrada alto-nivel
	def interpret(self, node):
		try:
			Checker.check(node, self.ctxt) #primero se checa el programa
			if not self.ctxt.have_errors:
				print("\n ############################ EMPEZAR A INTERPRETAR #############################")
				self.visit(node)
				print("\n ########################## INTERPRETACIÓN TERMINADA #############################")
				print("\n ############################## GRACIAS PROFE UWU ################################")
			else:
				print("\n\t\t\t El programa no se puede interpretar porque cheker tiene errores")
		except MiniCExit as e:
			pass

	def visit(self, node: Block):
		#self.env = self.env.new_child() #think about it as a typewriter, it advances one row
										#and then you have to reset the pointer
		for stmt in node.stmts:
			self.visit(stmt)
			if ThereIsBreak:
				return 0
			if ThereIsContinue:
				return 1
			
		#self.env = self.env.parents		#you "reset" the pointer

	def visit(self, node: Program):
		#self.env = self.env.new_child()
		#================================================================================================
		for k, v in LibFuncs.items():
			self.env[k] = v
		#================================================================================================
		for d in node.decl:
			self.visit(d)
		#self.env = self.env.parents

	def visit(self, node: ClassDeclaration):
		if node.sclass:
			sclass = self.visit(node.sclass)
			env = self.env.new_child()
			env['super'] = sclass			#we accommodate this framework for any User-made class
		else:
			sclass = None
			env = self.env
		methods = { }
		for meth in node.methods:
			methods[meth.name] = Function(meth, env)
		cls = Class(node.name, sclass, methods)
		self.env[node.name] = cls

	def visit(self, node: FuncDeclaration):

		func = Function(node, self.env)
		self.env[node.name] = func

	def visit(self, node: VarDeclaration):
		if node.expr:
			expr = self.visit(node.expr)
		else:
			expr = None
		self.env[node.name] = expr

	def visit(self, node: Print):
		print(self.visit(node.expr))

	def visit(self, node: WhileStmt):
		global ThereIsContinue
		global ThereIsBreak

		while _is_truthy(self.visit(node.cond)):
			ThereIsContinue = False
			ThereIsBreak = False
			#somethin will return from block 
			flowControl = self.visit(node.body)
			if flowControl == 0:
				break
			elif flowControl == 1:
				continue
			else:
				pass
			
			#self.visit(node.body)
		

	def visit(self, node: ContinueStmt):
		global ThereIsContinue
		ThereIsContinue = True
		#num_itecion = list(self.env.maps[0])
		#self.env[num_itecion[0]] += 1
		#return ContinueException()
		

	def visit(self, node: BreakStmt):
		global ThereIsBreak
		ThereIsBreak = True


	def visit(self, node: ForStmt):
		global ThereIsContinue
		global ThereIsBreak
	
		while _is_truthy(self.visit(node.for_cond)):
			ThereIsContinue = False
			ThereIsBreak = False

			flowControl = self.visit(node.for_body)
			if flowControl == 0:
				break
			elif flowControl == 1:
				self.visit(node.for_increment) #POFIN!!!! ESTO INCREMENTA EN la iteracion
				continue
			else:
				pass
			#self.visit(node.for_body)
			self.visit(node.for_increment)

	def visit(self, node: IfStmt):
		test = self.visit(node.cond)
		if _is_truthy(test):
			self.visit(node.cons)
		elif node.altr:
			self.visit(node.altr)

	def visit(self, node: Return):
		raise ReturnException(self.visit(node.expr))

	def visit(self, node: ExprStmt):
		self.visit(node.expr)

	def visit(self, node: Literal):
		return node.value
	#Esto es lo que hace la suma 
	def visit(self, node: Binary):
		left  = self.visit(node.left)
		right = self.visit(node.right)
		if node.op == '+':
			(isinstance(left, str) and isinstance(right, str)) or self._check_numeric_operands(node, left, right)
			return left + right
		elif node.op == '-':
			self._check_numeric_operands(node, left, right)
			return left - right
		elif node.op == '*':
			self._check_numeric_operands(node, left, right)
			return left * right
		elif node.op == '/':
			self._check_numeric_operands(node, left, right)
			return left / right
		elif node.op == '%':
			self._check_numeric_operands(node, left, right)
			return left % right
		elif node.op == '==':
			return left == right
		elif node.op == '!=':
			return left != right
		elif node.op == '<':
			self._check_numeric_operands(node, left, right)
			return left < right
		elif node.op == '>':
			self._check_numeric_operands(node, left, right)
			return left > right
		elif node.op == '<=':
			self._check_numeric_operands(node, left, right)
			return left <= right
		elif node.op == '>=':
			self._check_numeric_operands(node, left, right)
			return left >= right
		else:
			raise NotImplementedError(f"Interp Error. Wrong Operator {node.op}")
	#para los operadores logicos and y or
	def visit(self, node: Logical):
		left = self.visit(node.left)
		if node.op == '||':
			return left if _is_truthy(left) else self.visit(node.right)
		if node.op == '&&':
			return self.visit(node.right) if _is_truthy(left) else left
		raise NotImplementedError(f"Interp Error. Wrong Operator {node.op}")

	def visit(self, node: Unary): #unary operators are only for numbers
		expr = self.visit(node.expr)
		if node.op == "-":
			self._check_numeric_operand(node, expr)
			return - expr
		elif node.op == "!":
			return not _is_truthy(expr)
		else:
			raise NotImplementedError(f"Interp Error. Wrong Operator {node.op}")

	def visit(self, node: Grouping):
		return self.visit(node.expr)

	def visit(self, node: Assign): 	
		var_name = node.op #variable con el nombre del operador de asignacion
		expr = self.visit(node.expr) 
		if var_name == '+=':
			self.env[node.name] += expr
		elif var_name == '-=':
			self.env[node.name] -= expr
		elif var_name == '*=':
			self.env[node.name] *= expr
		elif var_name == '/=':
			self.env[node.name] /= expr
		elif var_name == '%=':
			self.env[node.name] %= expr
		else:
			self.env[node.name] = expr


	def visit(self, node: PreExp):
		exp = self.visit(node.expr)
		if node.op == '++':
			exp = exp + 1
			self.env[node.name] = exp
		elif node.op == '--':
			exp = exp - 1
			self.env[node.name] = exp
		return exp #IMPORTANTE PARA LA ASIGNACION

	#definitivo para los operadores de incremento y decremento
	def visit(self, node: PostExp):
		exp = self.visit(node.expr)
		exp2 = exp
		if node.op == '++':
			exp = exp + 1
			self.env[node.name] = exp 
		elif node.op == '--':
			exp = exp - 1
			self.env[node.name] = exp
		return exp2 #IMPORTANTE PARA LA ASIGNACION



	def visit(self, node: MFUNC):
		value = self.visit(node.value)
		fun = node.name
		if fun == 'sin':
			self.env[node.name] = math.sin(value)
		elif fun == 'cos':
			self.env[node.name] = math.cos(value)
		elif fun == 'tan':
			self.env[node.name] = math.tan(value)
		elif fun == 'sqrt':
			self.env[node.name] = math.sqrt(value)
		elif fun == 'floor':
			self.env[node.name] = math.floor(value)
		elif fun == 'ceil':
			self.env[node.name] = math.ceil(value)
		elif fun == 'atan':
			self.env[node.name] = math.atan(value)
		elif fun == 'asin':
			self.env[node.name] = math.asin(value)
		elif fun == 'acos':
			self.env[node.name] = math.acos(value)
		elif fun == 'sinh':
			self.env[node.name] = math.sinh(value)
		elif fun == 'cosh':
			self.env[node.name] = math.cosh(value)
		elif fun == 'tanh':
			self.env[node.name] = math.tanh(value)
		elif fun == 'log':
			self.env[node.name] = math.log(value)
		elif fun == 'log10':
			self.env[node.name] = math.log10(value)
		elif fun == 'exp':
			self.env[node.name] = math.exp(value)
		elif fun == 'abs':
			self.env[node.name] = abs(value)

	def visit(self, node: Call):
		callee = self.visit(node.func)
		if not callable(callee):
			self.error(node.func, f'Interp Error {self.ctxt.find_source(node.func)!r} is not callable')

		args = [ self.visit(arg) for arg in node.args ]
		try:
			return callee(self, *args)
		except CallError as err:
			self.error(node.func, str(err))

	def visit(self, node: Variable):
		#self.error(node, f'Interp Error{self.ctxt.find_source(node)!r} ')
		#return self.env.maps[self.localmap[id(node)]][node.name] #maps reads ChainMap as a list
		return self.env[node.name]

	def visit(self, node: Set):
		obj = self.visit(node.object)
		val = self.visit(node.value)
		if isinstance(obj, Instance):
			obj.set(node.name, val)
			return val
		else:
			self.error(node.object, f'Interp Error{self.ctxt.find_source(node.object)!r} is not an instance')

	def visit(self, node: Get):
		obj = self.visit(node.object)
		if isinstance(obj, Instance):
			try:
				return obj.get(node.name)
			except AttributeError as err:
				self.error(node.object, str(err))
		else:
			self.error(node.object, f'Interp Error{self.ctxt.find_source(node.object)!r}  is not an instance')

	def visit(self, node: This):
		return self.env['this']

	def visit(self, node: Super):
		distance = self.localmap[id(node)]
		sclass = self.env.maps[distance]['super']  #????
		this = self.env.maps[distance-1]['this']
		method = sclass.find_method(node.name)
		if not method:
			self.error(node.object, f'Interp Error. Not defined property {node.name!r}')
		return method.bind(this)

	# def visit(self, node: Input):
	# 	if node.prompt:
	# 		input(node.prompt)
	# 	else:
	# 		return input()

	def visit(self, node: Format):
		return 0