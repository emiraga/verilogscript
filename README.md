Introduction
============

VerilogScript adds couple of things to regular Verilog:

 * Python-like block declarations, [Off-side rule](http://en.wikipedia.org/wiki/Off-side_rule).
 * New keywords and operators.
 * Automated pipeline generation *TODO*.

Motivation
----------

I am very new to Verilog as a programming language. I was working on some design, when I started to wonder that perhaps Verilog might be missing some advances in terms of it's syntax that modern languages such as python are offering. At some point I hit "the wall" and decided to start the VerilogScript. This is not a real parser/programming language (at least it is not yet), instead it is set of rules for text transformation, that are going to morph a certain VerilogScript syntax into a valid Verilog code. It's syntax, however, is mostly of Verilog with some elements of python.

New operators
=============

Most operators from verilog are supported here as well, some additional have been added.

 * `elif`

   Transforms into `else if`. Term `elif` originates from Python.

 * `:=`

   Statement `a := b` in VerilogScript is converted into `assign a = b;` in Verilog.

 * `pipeline`

   *TODO*.

Example
=======
Copied from [here](http://www.asic-world.com/verilog/syntax2.html)

     module dff (q, q_bar, clk, d, rst, pre);
     input clk, d, rst, pre;
     output q, q_bar;
     reg q;
     assign q_bar = ~q;
     always @ (posedge clk)
     if (rst == 1'b1) begin
       q <= 0;
     end else if (pre == 1'b1) begin
       q <= 1;
     end else begin
       q <= d;
     end
     endmodule

That was Verilog, now in VerilogScript:

     module dff (input clk, input d, input rst, input pre, output q, output q_bar):
         reg q
         q_bar := ~q
         always@ posedge clk:
            if rst == 1'b1:
               q <= 0
            elif pre == 1'b1:
               q <= 1
            else:
               q <= d

Coding standards
================

Verilog inherits a preprocessor from C/C++, however Python specifically speaks against it. So, now I am in dilemma of whether preprocessor is needed. For now, I recommend usage of Verilog preprocessor only for defining constants (alternatives?). If you make your script unrecognizable with (ab)use of preprocessor, VerilogScript will fail to parse your script correctly.

