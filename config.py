class config:
	tab_space = 4
	comment = '//'
	def_block = {
		'module':{'end':'endmodule',},
		'function':{'end':'endfunction',},
		'primitive':{'end':'endprimitive',},
		'task':{'end':'endtask',},
		'macromodule':{'end':'endmodule',},
	}
	statement_block = {
		'if':{'params':True,},
		'else':{'params':False,},
		'always@':{'params':True,},
		'always':{'params':False,},
		'repeat':{'params':True,},
		'while':{'params':True,},
		'elif':{'params':True, 'change_to':'else if' },
		'for':{'params':True,},
		'initial':{'params':False,},
	}
