import re

class SyntaxError_(Exception):
	def __init__(self, msg, line, file):
		self.msg = msg
		self.line = line
		self.file = file

class SyntaxErrorGen(object):
	def __init__(self, file):
		self.file = file
		self.line = 1
	def syntax(self, msg):
		return SyntaxError_(msg, self.line, self.file)

def parse_line(stack, line, on_error, comment = '//'):
	i = 0
	open_str = False
	while i < len(line):
		if open_str and line[i] == '\\':
			i += 2 #skip back-slash and character after it
			continue
		if open_str:
			if line[i] == '"':
				open_str = False
		else:
			if line[i] == '"':
				open_str = True
			elif line[i:i+len(comment)] == comment:
				line = line[0:i]
				break
			elif line[i] == '(' or line[i] == '{' or line[i] == '[':
				stack.append(line[i])
			elif line[i] == ')':
				if stack[-1] != '(':
					raise on_error.syntax("Missmatched ')'")
				stack.pop()
			elif line[i] == ']':
				if stack[-1] != '[':
					raise on_error.syntax("Missmatched ']'")
				stack.pop()
			elif line[i] == '}':
				if stack[-1] != '{':
					raise on_error.syntax("Missmatched '}'")
				stack.pop()
		i += 1
	return stack, line

def parse_script(filename, file_open, config):
	reWhiteRest = re.compile("(\s*)(\S.*)")
	reNotSpace = re.compile("[^ ]")
	reBeginText = re.compile("^[a-z]*")
	reEndWord = re.compile("\w*$")
	reAssignOp = re.compile("^(.+?)\s*:=\s*")
	file_lines_num = enumerate(file_open, start = 1)
	on_error = SyntaxErrorGen(file = filename)
	out = []
	stack = [(0,'','')]
	prev_special = None
	
	def de_indent():
		if stack[-1][1] == 'funcblock':
			end = config.functional_block[stack[-1][2]]['end']
		else:
			end = "end"
		out.append(" " * stack[-2][0] + end)
		line_map[len(out)] = on_error.line
		#print('removing',stack[-1])
		stack.pop()
		prev_special = None
	line_map = {}
	for on_error.line, line in file_lines_num:
		line = line.rstrip()
		#skip empty lines
		if len(line) == 0:
			continue
		#cut in two parts white and after white
		white,rest = re.match(reWhiteRest, line).groups()
		#convert tabs into TAB_SPACE spaces
		white = len(re.sub(reNotSpace, " " * config.tab_space, white))
		#skip comments
		if rest.startswith(config.comment):
			#should comments fall through?
			out.append(" " * white+"//"+rest[len(config.comment):])
			line_map[len(out)] = on_error.line
			continue
		if white == stack[-1][0]:
			if prev_special is not None:
				raise on_error.syntax("Missing indented block")
		else:
			#remove indentation
			while white < stack[-1][0]:
				de_indent()
			#add indentation
			if white > stack[-1][0]:
				if prev_special is None:
					raise on_error.syntax("Indentation error")
				if prev_special[0] == 'statblock':
					begin = "begin"
					if len(prev_special[2]) > 0:
						begin += ":" + prev_special[2]
					out.append(" " * stack[-1][0] + begin)
					line_map[len(out)] = on_error.line
				stack.append((white, prev_special[0], prev_special[1]))
				#print('adding',stack[-1])
		#start parsing for a potential multi-line statement
		statement_start = on_error.line
		brackets, rest = parse_line([], rest, on_error, config.comment)
		while True: #rest[-1] == '\\' or len(brackets) > 0:
			if len(rest) > 0 and rest[-1] == '\\':
				rest = rest[:-1]
			elif len(brackets) > 0:
				rest += " "
			else:
				break #end of multi-line statement
			try:
				#take a next line
				on_error.line, new = file_lines_num.next()
			except StopIteration:
				if len(brackets):
					raise on_error.syntax("Unexpected EOF, match missing for '%s', "
						"multi-line statement started in line %d." % (''.join(brackets), statement_start))
				raise on_error.syntax("Unexpected EOF")
			brackets, new = parse_line(
					brackets, new.rstrip(), on_error, config.comment)
			rest += new.strip()
		
		start_bl = re.search(reBeginText,rest).group(0)
		#Is this beginning of block statement?
		if start_bl in config.statement_block or start_bl in config.functional_block:
			rest = rest[len(start_bl):].lstrip()
			if start_bl in config.statement_block:
				#Start of a statement block (while, if, for, etc.)
				block_type = 'statblock'
				#block name comes at the end of line, (while enable: BLOCKNAME)
				block_name = re.search(reEndWord,rest).group(0)
				if len(block_name):
					rest = rest[:-len(block_name)].rstrip()
				#colon is requirement from python
				if len(rest) == 0 or rest[-1] != ':':
					raise on_error.syntax("Expected ':'")
				rest = rest[:-1].rstrip()
				#Should we change the name of output statement?
				if 'change_to' in config.statement_block[start_bl]:
					output_name = config.statement_block[start_bl]['change_to']
				else:
					output_name = start_bl
				#Does this statement accept more parameters?
				more_params = config.statement_block[start_bl]['params']
				if 'at_params' in config.statement_block[start_bl] and len(rest) > 0:
					if rest[0] != '@':
						raise on_error.syntax("Expected '@'")
					more_params = True
					rest = rest[1:].lstrip()
					output_name += ' @ '
				if more_params:
					if rest[0] != '(' or rest[-1] != ')':
						out.append(" " * white + output_name + "(" + rest + ")")
					else:
						out.append(" " * white + output_name + " " + rest)
				else:
					#No more parameters are needed
					if len(rest) > 0:
						raise on_error.syntax("Extra text after '%s' keyword" % start_bl)
					out.append(" " * white + output_name)
			else:
				#Start of functional block (module, function, etc.)
				block_type = 'funcblock'
				block_name = ''
				if len(rest) == 0 or rest[-1] != ':':
					raise on_error.syntax("Expected ':'")
				rest = rest[:-1]
				#add brackets if needed, default=False
				if 'putbrackets' in config.functional_block[start_bl] and \
						config.functional_block[start_bl]['putbrackets']:
					rest = '('+rest+')'
				#add semicolon if needed, default=True
				if 'semicolon' not in config.functional_block[start_bl] or \
						 config.functional_block[start_bl]['semicolon']:
					rest += ";"
				if len(rest) > 0:
					rest = " " + rest
				#write beginning of functional block
				out.append(" " * white + start_bl + rest)
			#mark that this statement is of block start
			prev_special = (block_type, start_bl, block_name)
		else:
			#Regular statement
			if rest != 'pass':
				rest = re.sub(reAssignOp, "assign \\1 = ", rest)
				if rest.startswith('`define') or \
						rest.startswith('`include') or rest.endswith(';'):
					out.append(" " * white + rest)
				else:
					out.append(" " * white + rest + ';')
			prev_special = None
		line_map[len(out)] = on_error.line
	#remove indentation at the end
	while len(stack) > 1:
		de_indent()
	return out, line_map
