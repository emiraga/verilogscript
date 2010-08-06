import unittest
from vsparser import parse_script, SyntaxError_, parse_line, SyntaxErrorGen
from StringIO import StringIO
import config

class TestParseScript(unittest.TestCase):
	def test_one(self):
		#testing without line mapping
		ae = self.assertEqual
		ar = self.assertRaises
		c = config.config
		ae(parse_script("file",StringIO(""), c)[0],
			[])
		ae(parse_script("file",StringIO("lala\n\n\na"), c)[0],
			["lala;","a;"])
		ae(parse_script("file",StringIO("lala\n\n//com\na"), c)[0],
			["lala;",'//com',"a;"])
		ae(parse_script("file",StringIO("if 3:\n  if 4:\n    two\n  three"), c)[0],
			["if(3)","begin","  if(4)","  begin",
			'    two;','  end','  three;','end'])
		ae(parse_script("file",StringIO("module hahaha:\n  pass"), c)[0],
			["module hahaha;","endmodule"])
		ae(parse_script("file",StringIO("module hahaha(45):\n  a=3"), c)[0],
			["module hahaha(45);","  a=3;","endmodule"])
		ae(parse_script("file",StringIO("module hahaha(45):\n  a=3\nb=1"), c)[0],
			["module hahaha(45);","  a=3;","endmodule","b=1;"])
		ae(parse_script("file",StringIO("while 4:NAME\n  a=3\nb=1"), c)[0],
			["while(4)","begin:NAME","  a=3;","end","b=1;"])
		ae(parse_script("file",StringIO("while(4):NAME\n  a=3\nb=1"), c)[0],
			["while (4)","begin:NAME","  a=3;","end","b=1;"])
		ar(SyntaxError_,parse_script,"file",StringIO("while 4\n  a=3\nb=1"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("while 4:\n  a=3\n b=1"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("while 4:\n  a=3\n        b=1"), c)
		ae(parse_script("file",StringIO("if 4:\n  a=3\nelif 5:\n     b=1"), c)[0],
			["if(4)","begin","  a=3;","end","else if(5)","begin","     b=1;","end"])
		ae(parse_script("file",StringIO("initial:\n  a=3\n  b=1"), c)[0],
			["initial","begin","  a=3;","  b=1;","end"])
		ar(SyntaxError_,parse_script,"file",StringIO("initial 3:\n  a=3\n  b=1"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("function 3\n  a=3\n  b=1"), c)
		ae(parse_script("file",StringIO("34\\\n45"), c)[0], ["3445;"])
		ae(parse_script("file",StringIO("(34\n45)"), c)[0], ["(34 45);"])
		ae(parse_script("file",StringIO("(34\n    \t45)"), c)[0], ["(34 45);"])
		ar(SyntaxError_,parse_script,"file",StringIO("\\"), c)
		ar(SyntaxError_,parse_script,"file",StringIO("("), c)
		ar(SyntaxError_,parse_script,"file",StringIO("if 3:\nif 4:"), c)
		ae(parse_script("file",StringIO("a:=b"), c)[0],["assign a = b;"])
		ae(parse_script("file",StringIO("a  :=  b    "), c)[0],["assign a = b;"])
		ae(parse_script("file",StringIO("a : = b"), c)[0],["a : = b;"])
		ae(parse_script("file",StringIO("{a1,a2}:=b"), c)[0],["assign {a1,a2} = b;"])
		ae(parse_script("file",StringIO("always:\n  a"), c)[0],["always","begin","  a;","end"])
		ae(parse_script("file",StringIO("always  @  4  :\n  a"), c)[0],["always @ (4)","begin","  a;","end"])
		ar(SyntaxError_, parse_script, "file", StringIO("always  4  :\n  a"), c)
		ae(parse_script("file",StringIO("`define SOME\n`include ELSE"), c)[0],
			["`define SOME","`include ELSE"])
		ae(parse_script("file",StringIO("case var:\n  0: a=2\n  1: a=3\n"), c)[0],
			["case (var)","  0: a=2;","  1: a=3;","endcase"])
		ae(parse_script("file",StringIO("table:\n  0 2\n  1 3\n"), c)[0],
			["table","  0 2;","  1 3;","endtable"])
		
		#testing of line mapping
		ae(parse_script("file",StringIO("1\n\n\n2\n"), c), (["1;","2;"],{1:1, 2:4}))
		ae(parse_script("file",StringIO("module a(\ninput A,\ninput B\n):\n  q=3\n  g=1"), c),
			(["module a( input A, input B );","  q=3;","  g=1;", "endmodule"],
			{1:4, 2:5, 3:6, 4:6}))
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
