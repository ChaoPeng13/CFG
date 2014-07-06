import os, glob, sys, pickle, struct, collections

dict_function = dict() # Record all functions from .nm file based on the start address
dict_valid_function = dict() # Record valid functions based on the start address
dict_basicblock = dict() # Record basic blocks based on the start address


class Function:
	def __init__(self, name, start_addr = None, end_addr = None, num_bb = 0, num_inst = 0):
		self.name = name
		self.start_addr = start_addr
		self.end_addr = end_addr
		self.num_bb = num_bb
		self.num_inst = num_inst

		self.list_bb = list()
		self.list_inst = list()
		self.list_bb_start = list()
		self.list_call = list()
		self.dict_call = dict() # Map basic block to function
		self.dict_return = dict() # Map function to basic block

	def isBelong(jump_address):
		if (int(jump_address,16) >= int(start_addr,16) && int(jump_address,16) <= int(end_addr,16)):
			return True
		return False

	def add_inst(inst):
		if(len(list_inst)==0):
			start_addr = inst.address
			end_addr = inst.address
			assert num_inst == 0

			num_inst = 1
			list_inst.append(inst)
		else:
			assert int(list_inst[-1].address,16) == int(inst.address,16) - 4 
			num_inst += 1
			end_addr = inst.address
			list_inst.append(inst)
    #In this function, the instructions of function are tarversed two times.
	def create_bb():
		assert len(list_bb) == 0
		assert len(list_bb_start) == 0
		assert len(list_inst) == 0
		assert (len(list_call)==0) && (len(dict_call)==0) && (len(dict_return)==0)
		assert num_bb == 0
		assert num_inst != 0

		cur_bb = None

		for inst in list_inst:
			if (cur_bb == None):
				cur_bb = BasicBlock(inst.address, start_addr)

			if (inst)

		





class Instruction:
	def __init__ (self, address, exp_hexadecimal, exp_text, inst_type = None, jump_to = None):
		self.address = address
		self.exp_hexadecimal = exp_hexadecimal
		self.exp_text = exp_text
		self.jump_to = jump_to # If jump to function, this jump_to = <...>, otherwise hexadecimal
		self.inst_type = inst_type #{NORMAL, BXLR}
		update()

	def update_type():

		exp_text[]


class BasicBlock:
	def __init__ (self, name, start_addr, end_addr = None, num_inst=0):
		self.name = name
		self.start_addr = start_addr
		self.end_addr = end_addr
		self.num_inst = num_inst
		sefl.list_inst = list()
		self.list_jump_to_func = list() # Call external functions
		self.list_jump_to_bb = list() # Jump to internal basic blocks

	def add_inst(inst):
		if(len(list_inst)==0):
			start_addr = inst.address
			end_addr = inst.address
			assert num_inst == 0

			num_inst = 1
			list_inst.append(inst)
		else:
			assert int(list_inst[-1].address,16) == int(inst.address,16) - 4 
			num_inst += 1
			end_addr = inst.address
			list_inst.append(inst)

