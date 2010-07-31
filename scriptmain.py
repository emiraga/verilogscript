from __future__ import print_function
import sys
import re
import config

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
			i += 2
			continue
		if open_str:
			if line[i] == '"':
				open_str = False
		else:
			if line[i] == '"':
				open_str = True
			elif line[i:i+len(comment)] == comment:
				return stack, line[0:i]
			elif line[i] == '(' or line[i] == '{' or line[i] == '[':
				stack.append(line[i])
			elif line[i] == ')':
				if stack[-1] != '(':
					raise on_error.syntax("Missmatched ')'");
				stack.pop()
			elif line[i] == ']':
				if stack[-1] != '[':
					raise on_error.syntax("Missmatched ']'");
				stack.pop()
			elif line[i] == '}':
				if stack[-1] != '{':
					raise on_error.syntax("Missmatched '}'");
				stack.pop()
		i += 1
	return stack, line

def parse_script(filename, file_open, config):
	reWhiteRest = re.compile("(\s*)(\S.*)")
	reNotSpace = re.compile("[^ ]")
	file_lines_num = enumerate(file_open, start = 1)
	on_error = SyntaxErrorGen(file = filename)
	out = []
	stack = [0]
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
			#out.append(" "*stack[-1]+"//"+rest[1:])
			continue
		#de-indentation
		while white < stack[-1]:
			out.append(" "*stack[-2]+"end")
			stack.pop()
		else:
			#add indentation
			if white > stack[-1]:
				out.append(" "*stack[-1]+"begin")
				stack.append(white)
		#check if indentation is valid
		if white != stack[-1]:
			raise on_error.syntax("White space missmatch")
		brackets, rest = parse_line([], rest, on_error, comment=config.comment)
		while True: #rest[-1] == '\\' or len(brackets) > 0:
			if len(rest) > 0 and rest[-1] == '\\':
				rest = rest[:-1]
			elif len(brackets) > 0:
				rest += " "
			else:
				break #end of multi-line statement
			try:
				on_error.line, new = file_lines_num.next()
			except StopIteration:
				if len(brackets):
					raise on_error.syntax("Unexpected EOF"
						", match missing for '%s'" % ''.join(brackets))
				raise on_error.syntax("Unexpected EOF")
			brackets, new = parse_line(brackets, new.rstrip(), on_error)
			rest += new
		out.append(" "*white+rest+';')
	while len(stack) > 1:
		out.append(stack[-2]*" "+"end")
		stack.pop()
	return out

from StringIO import StringIO
import unittest

class TestParseLine(unittest.TestCase):
	def setUp(self):
		self.error = SyntaxErrorGen('file')
	def test_one(self):
		ae = self.assertEqual
		ar = self.assertRaises
		ae(parse_line([],"str",None),([],"str"))
		ae(parse_line([],"str//add",None),([],"str"))
		ae(parse_line([],'st"r//"add',None),([],'st"r//"add'))
		ae(parse_line([],r'st"r\\"a//dd',None),([],r'st"r\\"a'))
		ae(parse_line([],r'st"r\"a//dd"',None),([],r'st"r\"a//dd"'))
		ae(parse_line([],r'st"[[}}r\"a//d"',None),([],r'st"[[}}r\"a//d"'))
		ae(parse_line([],r'st[[ra//d}}d"',None),(['[','['],r'st[[ra'))
		ae(parse_line([],r'st[[ra]//d}}d"',None),(['['],r'st[[ra]'))
		ae(parse_line([],r'st[[ra](//d}}d"',None),(['[','('],r'st[[ra]('))
		ae(parse_line([],r's[[ra](){//d}}d"',None),(['[','{'],r's[[ra](){'))
		ae(parse_line([],r'{}{',None),(['{'],r'{}{'))
		ae(parse_line([],'{}{\\//',None),(['{'],'{}{\\'))
		ar(SyntaxError_, parse_line, [], r'(]',self.error)
		ar(SyntaxError_, parse_line, [], r'[[[]]}',self.error)
		ar(SyntaxError_, parse_line, [], r'{[[}',self.error)
		ar(SyntaxError_, parse_line, [], r'[{{]',self.error)
		ar(SyntaxError_, parse_line, [], r'[)',self.error)

class TestParseScript(unittest.TestCase):
	def test_one(self):
		ae = self.assertEqual
		ar = self.assertRaises
		c = config.config
		ae(parse_script("file",StringIO(""),config=c),
				[])
		ae(parse_script("file",StringIO("lala\n\n\na"),config=c),
				["lala;","a;"])
		ae(parse_script("file",StringIO("lala\n\n//com\na"),config=c),
				["lala;","a;"])
		ae(parse_script("file",StringIO("lala\n  one\n    two\n  three"),config=c),
				["lala;","begin","  one;","  begin",'    two;','  end','  three;','end'])

def main():
	if len(sys.argv) < 2:
		print("Usage: %s: <input file>"%sys.argv[0]);
		sys.exit(-1)
	try:
		out = parse_script(sys.argv[1], open(sys.argv[1]))
	except SyntaxError_, e:
		print("Syntax error: %s at line %d"%(e.msg, e.line))
	print("\n".join(out))

if __name__ == "__main__":
		main()

