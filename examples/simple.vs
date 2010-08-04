
module counter (input clk, input rst, input enable, output reg [3:0] count):
	always @ posedge clk or posedge rst:
		if rst:
			count <= 0
		else: COUNT
			while enable:
				count <= count + 1
				disable COUNT

module dff (input clk, input d, input rst, input pre, output reg q, output q_bar):
	q_bar := ~q
	always @ posedge clk:
		if rst:
			q <= 0
		elif pre:
			q <= 1
		else:
			q <= d
