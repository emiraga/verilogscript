from __future__ import print_function
import sys
import re
import config
from vsparser import parse_script

def main():
	if len(sys.argv) < 2:
		print("Usage: %s: <input file>"%sys.argv[0]);
		sys.exit(-1)
	try:
		out = parse_script(sys.argv[1], open(sys.argv[1]), config.config)
		print("\n".join(out))
	except SyntaxError_, e:
		print("Syntax error: %s at line %d"%(e.msg, e.line))

if __name__ == "__main__":
	main()

