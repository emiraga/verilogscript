from vsparser import parse_script, SyntaxError_
import config

class Converter(object):
	def __init__(self):
		self.maps = {}
	
	def convert_vs(self, file, target_file):
		out, map = parse_script(file, open(file), config.config)
		self.maps[target_file] = map
		with open(target_file,"w") as fout:
			fout.write("\n".join(out))
	def convert_error(self, file, line):
		if file not in self.maps or line not in self.maps[file]:
			return file, line
		return file+'s', self.maps[file][line]
