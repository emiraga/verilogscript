Introduction
============

VerilogScript adds couple of things to regular Verilog:

 * Python-like block declarations, [Off-side rule](http://en.wikipedia.org/wiki/Off-side_rule).
 * New keywords and operators
 * Automated pipeline generation **TODO**

Motivation
----------

I am very new to Verilog as a programming language. I was working on some design, when I started to wonder that perhaps Verilog might be missing some advances in terms of it's syntax that modern languages such as python are offering. At some point I hit "the wall" and decided to start the VerilogScript. This is not a real parser/programming language (at least it is not yet), instead it is set of rules for text transformation, that are going to morph a certain VerilogScript syntax into a valid Verilog code. It's syntax, however, is mostly of Verilog with some elements of python.

New operators
=============

Most operators from verilog are supported here as well, some additional have been added.

 * `elif`

Transforms into `else if`. Term `elif` originates from Python.

 * operator `:=`

Statement `a := b` in VerilogScript is converted into `assign a = b;` in Verilog. I remember operator `:=` from Pascal.

 * `pipeline`

**TODO**

Coding standards
================

Verilog inherits a preprocessor from C/C++, however Python specifically speaks against it. So, now I am in dilema of whether preprocessor is needed. For now, I recommend usage of Verilog preprocessor only for defining constants (alternatives?). If you make your script unrecognizable with (ab)use of preprocessor, VerilogScript will fail to parse your script correctly.

