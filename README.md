Introduction
============

This project add two things to Verilog:

 * Python-like block declarations i.e. [Off-side rule](http://en.wikipedia.org/wiki/Off-side_rule)
 * Automated pipeline generator

Motivation
----------

I am very new to Verilog as a programming language. I was working on some design, when I started to wonder that perhaps Verilog might be missing some simplicities in terms of syntax that modern languages such as python are offering. At some point I hit "the wall" and decided to start a VerilogScript. That is not a real parser/programming language (at least not yet it's not), instead it is set of rules for text transformation, that are going to morph a certain VerilogScript syntax into a valid Verilog code. It's syntax is mostly of Verilog with some elements of python.

I expect is that Verilog veterans are going to declare this project as "bad" and it's syntax as "ugly". If you feel like puking, stop reading right now.

