class config:
	tab_space = 8
	comment = '//'
	functional_block = {
		'module'     :{'end':'endmodule',},
		'function'   :{'end':'endfunction',},
		'primitive'  :{'end':'endprimitive',},
		'task'       :{'end':'endtask',},
		'macromodule':{'end':'endmodule',},
		'table'      :{'end':'endtable', 'semicolon':False,},
		'case'       :{'end':'endcase', 'semicolon':False, 'putbrackets':True},
		'casex'      :{'end':'endcase', 'semicolon':False, 'putbrackets':True},
		'casez'      :{'end':'endcase', 'semicolon':False, 'putbrackets':True},
		'generate'   :{'end':'endgenerate', 'semicolon':False,},
	}
	statement_block = {
		'if'     :{'params':True, },
		'else'   :{'params':False,},
		'always' :{'params':False,'at_params':True,},
		'repeat' :{'params':True, },
		'while'  :{'params':True, },
		'elif'   :{'params':True, 'change_to':'else if',},
		'for'    :{'params':True, },
		'initial':{'params':False,},
		'forever':{'params':False,},
	}
