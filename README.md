Introduction
============

VerilogScript adds couple of things to regular Verilog:

 * Python-like block declarations, [Off-side rule](http://en.wikipedia.org/wiki/Off-side_rule).
 * New keywords and operators.
 * Automated pipeline generation *TODO*.

Motivation
----------

I am very new to Verilog as a programming language. I was working on some design, when I started to wonder that perhaps Verilog is missing some advances (in terms of it's syntax) that modern languages such as python are offering. At some point of using Verilog I hit "the wall", and decided to start the VerilogScript. This is not a real parser/programming language (at least not yet), instead it is set of rules for text transformation that are going to morph a certain VerilogScript syntax into a valid Verilog code.

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

 * `pipeline` *TODO*.

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

(Note: Ability to specify type/width of port inside a module declaration is available in Verilog 2005.)

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

Coding standards
================

Verilog inherits a preprocessor from C/C++, however Python specifically speaks against it. So, now I am in dilemma of whether preprocessor is needed. For now, I recommend usage of Verilog preprocessor only for defining constants (alternatives?). If you make your script unrecognizable with (ab)use of preprocessor, VerilogScript will fail to parse your script correctly.

Compilation errors
==================

VerilogScript is not a compiler, instead it will only generate a Verilog code. That Verilog code would have to be further compiled. This presents a problem of error reporting. Verilog compiler/simulator will show error line in **generated** `.v` code and not the **original** `.vs` code.

To resolve this issue you should let VerilogScript.py perform the compilation step:

    VerilogScript.py examples/simple.vs -e "iverilog"

With first parameter `examples/simple.vs` will tell VerilogScript to convert this `.vs` file into a `.v` file. Parameters `-e "iverilog"` will cause VerilogScript to execute a compiler after all conversions are done.

You can mix between `.vs` and `.v` files in parameters, you may also specify additional compiler options, for example:

    VerilogScript.py file1.v file2.vs file3.v -e "iverilog -o sim.out"

Contact
=======

Comments are welcome: [emiraga@gmail.com](mailto:emiraga@gmail.com)
