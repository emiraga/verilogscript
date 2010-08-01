import unittest
from scriptmain import parse_script, SyntaxError_, parse_line, SyntaxErrorGen
from StringIO import StringIO
import config

class TestParseScript(unittest.TestCase):
	def test_one(self):
		ae = self.assertEqual
		ar = self.assertRaises
		c = config.config
		ae(parse_script("file",StringIO(""), c),
			[])
		ae(parse_script("file",StringIO("lala\n\n\na"), c),
			["lala;","a;"])
		ae(parse_script("file",StringIO("lala\n\n//com\na"), c),
			["lala;",'//com',"a;"])
		ae(parse_script("file",StringIO("if 3:\n  if 4:\n    two\n  three"), c),
			["if(3)","begin","  if(4)","  begin",
			'    two;','  end','  three;','end'])
		ae(parse_script("file",StringIO("module hahaha:\n  pass"), c),
			["module hahaha;","endmodule"])
		ae(parse_script("file",StringIO("module hahaha(45):\n  a=3"), c),
			["module hahaha(45);","  a=3;","endmodule"])
		ae(parse_script("file",StringIO("module hahaha(45):\n  a=3\nb=1"), c),
			["module hahaha(45);","  a=3;","endmodule","b=1;"])
		ae(parse_script("file",StringIO("while 4:NAME\n  a=3\nb=1"), c),
			["while(4)","begin:NAME","  a=3;","end","b=1;"])
		ae(parse_script("file",StringIO("while(4):NAME\n  a=3\nb=1"), c),
			["while (4)","begin:NAME","  a=3;","end","b=1;"])
		ar(SyntaxError_,parse_script,"file",StringIO("while 4\n  a=3\nb=1"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("while 4:\n  a=3\n b=1"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("while 4:\n  a=3\n        b=1"), c)
		ae(parse_script("file",StringIO("if 4:\n  a=3\nelif 5:\n     b=1"), c),
			["if(4)","begin","  a=3;","end","else if(5)","begin","     b=1;","end"])
		ae(parse_script("file",StringIO("initial:\n  a=3\n  b=1"), c),
			["initial","begin","  a=3;","  b=1;","end"])
		ar(SyntaxError_,parse_script,"file",StringIO("initial 3:\n  a=3\n  b=1"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("function 3\n  a=3\n  b=1"), c)
		ae(parse_script("file",StringIO("34\\\n45"), c), ["3445;"])
		ae(parse_script("file",StringIO("(34\n45)"), c), ["(34 45);"])
		ar(SyntaxError_,parse_script,"file",StringIO("\\"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("("), c)
		ar(SyntaxError_,parse_script,"file",StringIO("if 3:\nif 4:"), c)
		ae(parse_script("file",StringIO("a:=b"), c),["assign a = b;"])
		ae(parse_script("file",StringIO("a  :=  b    "), c),["assign a = b;"])
		ae(parse_script("file",StringIO("a : = b"), c),["a : = b;"])
		ae(parse_script("file",StringIO("{a1,a2}:=b"), c),["assign {a1,a2} = b;"])
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

def main():
	unittest.main()

if __name__ == "__main__":
	main()
