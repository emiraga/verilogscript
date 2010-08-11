Introduction
============

VerilogScript adds couple of things to regular Verilog:

 * Python-like block declarations, [Off-side rule](http://en.wikipedia.org/wiki/Off-side_rule).
 * New keywords and operators.
 * Automated pipeline generation *TODO*.

Motivation
----------

Being new to Verilog, I was working on some design, 
when I started to wonder that Verilog might be missing some advances (in terms of it's syntax) 
that modern languages such as python are offering. I decided to start the VerilogScript. 
It is not a real parser/programming language (at least not yet), instead it is set of rules 
for text transformation that are going to morph a certain VerilogScript syntax into a Verilog code.

    always @ posedge clock:
        if reset:
            q <= 0
        else:
            q <= d

New operators/keywords
======================

 * `elif` is an equivalent of `else if`. This term originates from [python](http://docs.python.org/tutorial/controlflow.html#if-statements).

 * `:=` is shortcut for `assign`. For example, statement `a := b` in VerilogScript is converted into `assign a = b;`.

 * `pass` is a statement that does nothing. Can be used as a place-holder for a function or conditional body that is not yet implemented. Name originates from [python](http://docs.python.org/tutorial/controlflow.html#pass-statements).

       while enable:
           pass

 * `pipeline` and `stage` *TODO*.

Example
=======

Copied and simplified from [here](http://www.asic-world.com/verilog/syntax2.html), a flip-flop:

    module dff (q, q_bar, clk, d, rst, pre);
        input clk, d, rst, pre;
        output q, q_bar;
        reg q;
        assign q_bar = ~q;
        always @ (posedge clk)
        if (rst) begin
            q <= 0;
        end else if (pre) begin
            q <= 1;
        end else begin
            q <= d;
        end
    endmodule

VerilogScript:

    module dff (input clk, input d, input rst, input pre, output reg q, output q_bar):
        q_bar := ~q
        always @ posedge clk:
            if rst:
                q <= 0
            elif pre:
                q <= 1
            else:
                q <= d

(Note: Ability to specify type/width of port inside a module declaration *is* available in newer Verilog.)

One more example
----------------

Copied from [here](http://www.asic-world.com/verilog/verilog_one_day2.html), strange counter: 

    module counter (clk,rst,enable,count);
    input clk, rst, enable;
    output [3:0] count;
    reg [3:0] count;
    always @ (posedge clk or posedge rst)
    if (rst) begin
      count <= 0;
    end else begin : COUNT
      while (enable) begin
        count <= count + 1;
        disable COUNT;
      end
    end
    endmodule

And VerilogScript:

    module counter (input clk, input rst, input enable, output reg [3:0] count):
        always @ posedge clk or posedge rst:
            if rst:
                count <= 0
            else: COUNT
                while enable:
                    count <= count + 1
                    disable COUNT

Preprocessor
============

Verilog inherits a preprocessor from C/C++, however Python specifically is against it.
And in fact, preprocessor is yet another language which has very little to do with Verilog itself.
For now, I recommend usage of Verilog preprocessor only for defining constants (any alternatives?),
and inclusing files.

    `define WIDTH_NUM [23:0]
	`include "defines.v"

If you make your script unrecognizable with (ab)use of preprocessor, VerilogScript will fail to 
parse your script correctly.

Compilation errors
==================

VerilogScript is not a compiler, instead it will only generate a Verilog code. 
That Verilog code would have to be further compiled. This presents a problem of error reporting. 
Verilog compiler/simulator will show error line in **generated** `.v` code and not the **original** `.vs` code.

To resolve this issue you should let VerilogScript.py perform the compilation step:

    VerilogScript.py examples/simple.vs -e "iverilog"

First parameter `examples/simple.vs` will tell VerilogScript to convert this `.vs` file into a `.v` file. 
Parameters `-e "iverilog"` will cause VerilogScript to execute a compiler after all conversions are done.

You can mix between `.vs` and `.v` files in parameters, you may also specify additional compiler options, for example:

    VerilogScript.py file1.v file2.vs file3.v -e "iverilog -o sim.out"

Language specification
======================

This is highly experimental language, and it is subject to incomplete specification and rapid change.

Statements
----------

Each line in VerilogScript code is interpreted in one of three ways.

1. Empty statement
2. Single-line statement
3. Part of multi-line statement

#### Empty statement

Empty statement does not translate into anything useful in terms for hardware desing. Blank lines, or lines
that contain only white space are empty statements. Lines with comment only are empty as well. For example:

    //This is a comment

Multi-line comments are not supported at the moment.

VerilogScript follows off-side rule from python, but these rules do not apply to empty and statements with comments.
Another way to express a empty statement is to use `pass` in one line. Contrary to previous empty statements,
off-side rules (indentation) applies to `pass` statement. It can be used as a place-holder for a function 
or conditional body that is not yet implemented. 

       while enable:
           pass

#### Single line statement

As name suggests entire line is just one Verilog statement. Semicolon is not required to be placed at the end
of such statement. For example:

    q <= 4'b0110

These statements must follow indentation blocks (off-side rule).

#### Multi-line statement

There are two ways to make single statement span multiple lines (a.k.a. multi-line statements). 
Firstly, ending a line with back-slash:

    This is \
	a statement

And second way is by opening brackets:

    This is (
      also {
      one single
       statement} )

In multi-line statements only first line must indentation blocks (off-side rule). It is recommended that
lines other than first are indented a bit. This is to avoid accidental creation of multiple statements
where original intention was a single statement.

Assignments
-----------

There are three types of assignments:

1. Blocking
       a = b
2. Non-blocking 
       a <= b
3. Continuous
       a := b
	   
Roadmap
=======

* Get feedback from community
* Add more features
* Move towards standardization by providing alternative implementation of language in some open-source verilog 
compiler/simulator, for example: `iverilog`

Contact
=======

Comments are welcome: [emiraga@gmail.com](mailto:emiraga@gmail.com)

TODO
====

* case? add begin end automatically for cases
