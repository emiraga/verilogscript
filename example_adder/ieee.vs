
`define TOTALBITS 32 //number of bits in representation of a number
`define SIGN_LEN 1 //sign of a number needs 1 bit
`define EXPO_LEN 8 //length of exponent part
`define SIGNIFICAND_LEN `TOTALBITS - `SIGN_LEN - `EXPO_LEN // mantissa or significand of a number
`define GUARDBITS 3 //additional bits added to make addition/subtraction more precise

`define LASTBIT `TOTALBITS - 1
`define FIRSTBIT 0
`define EXPO_LASTBIT `LASTBIT - `SIGN_LEN
`define EXPO_FIRSTBIT `EXPO_LASTBIT - `EXPO_LEN + 1
`define SIGNIFICAND_LASTBIT `SIGNIFICAND_LEN - 1
`define SIGNIFICAND_FIRSTBIT 0

`define TYPE_NUMBER [`LASTBIT:`FIRSTBIT]
`define TYPE_SIGNIF [`SIGNIFICAND_LEN:-`GUARDBITS]
`define TYPE_EXPO   [`EXPO_LEN-1:0]

module ieee_adder_prepare_input(
		input add_sub_bit,
		input `TYPE_NUMBER number,
		output sign,
		output `TYPE_EXPO exponent,
		output `TYPE_SIGNIF significand):
	//Take input and convert it to suitable format.
	sign := number[`LASTBIT] ^ add_sub_bit
	exponent := number[`EXPO_LASTBIT:`EXPO_FIRSTBIT]
	//Added bit 1 in front, in case that exponent is zero, we add 0 in front instead.
	significand := {| exponent, number[`SIGNIFICAND_LASTBIT:`SIGNIFICAND_FIRSTBIT], `GUARDBITS'b0}

module ieee_adder_compare(
		input `TYPE_EXPO exponentA,
		input `TYPE_EXPO exponentB,
		input `TYPE_SIGNIF significandA,
		input `TYPE_SIGNIF significandB,
		output expA_bigger_expB,
		output inputA_bigger_inputB,
		output `TYPE_EXPO shift_amount):
	// Compare exponents and significands between inputs
	wire sub_borrow
	{sub_borrow, shift_amount} := exponentA - exponentB
	expA_bigger_expB := !sub_borrow
	inputA_bigger_inputB := {exponentA,significandA} > {exponentB,significandB}

module ieee_adder_stage3(
	input `TYPE_SIGNIF significandA,
	input `TYPE_SIGNIF significandB,
	input `TYPE_EXPO shift_amount,
	input expA_bigger_expB,
	output `TYPE_NUMBER outputC):
	//Store shifted significands, significand with smaller exponent will be shifted to the right
	wire `TYPE_SIGNIF significandA2
	significandA2 := expA_bigger_expB ? significandA : significandA >> -shift_amount
	wire `TYPE_SIGNIF significandB2
	significandB2 := expA_bigger_expB ? significandB >> shift_amount : significandB
	//Add two significands and store the carry of addition
	wire `TYPE_SIGNIF out_significand1
	wire carry_significand
	{carry_significand, out_significand1} := significandA2 + significandB2
	//Store output exponent, this is simply the biggest out of two exponents
	wire `TYPE_EXPO out_exponent1
	out_exponent1 := expA_bigger_expB ? exponentA : exponentB
	//In case that there was a significand overflow, exponent1 will be incremented by one,
	wire `TYPE_EXPO out_exponent2
	wire exponent_overflow
	{exponent_overflow, out_exponent2} := carry_significand ? 1 + out_exponent1 : {1'b0, out_exponent1}
	//Construct output, in case there was significand overflow implies bit '1' in front.
	outputC := {
		carry_significand ? 
		  {signA, out_exponent2, out_significand1[`SIGNIFICAND_LEN  :1]}
		: {signA, out_exponent2, out_significand1[`SIGNIFICAND_LEN-1:0]}
	}
