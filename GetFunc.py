import os, glob, sys, pickle, struct, collections

Benchmarks = "benchmarks/"
Sources = "outs/" 

main_at = list()
dict_all_label = dict() # Record all functions from .nm file based on the start address
dict_all_function = dict()
dict_valid_function = dict() # Record valid functions based on the start address
list_valid_function = list()
dict_basicblock = dict() # Record basic blocks based on the start address


class Function:
	def __init__(self, name, start_addr = None, end_addr = None, num_bb = 0, num_inst = 0):
		self.name = name
		self.start_addr = start_addr
		self.end_addr = end_addr
		self.num_inst = num_inst

		self.list_inst = list()
		self.list_call = list() # One call, one callee.

	def add_inst(self,inst):
		if(len(self.list_inst)==0):
			self.start_addr = inst.address
			self.end_addr = inst.address
			assert self.num_inst == 0

			self.num_inst = 1
			self.list_inst.append(inst)
		else:
			#assert int(self.list_inst[-1].address,16) == int(inst.address,16) - 4 
			self.num_inst += 1
			self.end_addr = inst.address
			self.list_inst.append(inst)

	def update(self):
		assert self.num_inst != 0  
		assert len(self.list_inst) != 0
		assert len(self.list_call) == 0

		for inst in self.list_inst:
			if (inst.inst_type == 'Normal'):
				continue
			else:
				self.list_call.append(dict_all_label[inst.jump_to_addr])


class Instruction:
	def __init__ (self, address, exp_hexadecimal, exp_text, inst_type = None, jump_to_addr = None, jump_to_func = None):
		self.address = address
		self.exp_hexadecimal = exp_hexadecimal
		self.exp_text = exp_text
		self.jump_to_addr = jump_to_addr # If jump to function, this jump_to = <...>, otherwise hexadecimal
		self.jump_to_func = jump_to_func
		self.inst_type = inst_type #{Normal, FuncCall}
		#update()

	def update(self):
		temp = '00000000'
		fields = self.exp_text.split()
		if (self.exp_text[0:2] == 'bl' and dict_all_label.has_key(temp[:8-len(fields[1])]+fields[1])):
			self.inst_type = 'FuncCall'
			self.jump_to_addr = temp[:8-len(fields[1])]+fields[1]
			self.jump_to_func = fields[2][1:-1]
		else:
			self.inst_type = 'Normal'


# def GetFuncFrom(nm): #Generate dict_all_label
# 	for line in file(nm):
# 		fields = line.split()
# 		if (len(fields) < 3):
# 			continue
# 		if line.rstrip().endswith(" T main"):
# 			main_at.append(fields[0])

# 		if (fields[2] == 't' or fields[2] == 'T'):
# 			dict_all_label[fields[0]] = fields[3]
# 			print "here3"

# 		if (fields[0] == '00008114'):
# 			print fields

# 		if (fields[1] == 't' or fields[1] == 'T'):
# 			if not dict_all_label.has_key(fields[0]):
# 				dict_all_label[fields[0]] = fields[2]
# 				print fields[2]

def GetFuncFrom(nm): #Generate dict_all_label
	for line in file(nm):
		fields = line.split()
		if (len(fields) < 3):
			continue
		if line.rstrip().endswith(" T main"):
			main_at.append(fields[0])

		dict_all_label[fields[0]] = fields[-1]

#Generate dict_all_function
def GetAllFuncFrom(od): 
	enable = False
	#func = None
	for line in file(od):
		fields = line.split()
		if (len(fields) == 2 and len(fields[0])==8):
			enable = True
			assert dict_all_label.has_key(fields[0])
			func = Function(fields[1][1:-2])
			dict_all_function[fields[1][1:-2]] = func
			continue

		if enable and len(fields) >= 4:
			if (len(fields[0][:-1]) >= 4 and fields[2] != ".word"): # Instructions
				temp = "00000000"
				address = temp[:8-len(fields[0][:-1])]+fields[0][:-1]
				exp_hexadecimal = fields[1]
				exp_text = ' '.join(fields[2:])
				inst = Instruction(address, exp_hexadecimal, exp_text)
				inst.update()
				func.add_inst(inst)

def Search(func,f):
	for name in func.list_call:
		list_valid_function.append(name)
		f.write("	%s -> %s\n" % (func.name.replace(".","_"), name.replace(".","_")))
		Search(dict_all_function[name],f)



def GetValidFunc():
	for key in dict_all_function:
		dict_all_function[key].update()

	assert dict_all_function.has_key("main")
	assert len(dict_valid_function) == 0

	Search(dict_all_function["main"])

	print list_valid_function

def GenerateDOT():
    for key in dict_all_function:
    	dict_all_function[key].update()
	assert dict_all_function.has_key("main")
	assert len(dict_valid_function) == 0

	f = open("out.dot","w")
	f.writelines("digraph G {")
	Search(dict_all_function["main"],f) 
	f.writelines("}")
	f.close()

def output2():
	for key in dict_all_function:
		print "%s %s %s %s" % (key, dict_all_function[key].start_addr, dict_all_function[key].end_addr, dict_all_function[key].num_inst)
		print dict_all_function[key].list_call
		#print dict_all_function[key].list_inst


if __name__ == '__main__':
	assert len(sys.argv) == 3
	GetFuncFrom(sys.argv[1])
	 #assert len(main_at) == 1
	print main_at
	 #print dict_all_label

	GetAllFuncFrom(sys.argv[2])
	 #GetValidFunc()
	GenerateDOT()

	 #output2()
	 #print dict_all_function
	 #print dict_all_label