`include "src/defines.v"
///////////////////////////////////////////////
// MODULE: ieee_adder_prepare_input
///////////////////////////////////////////////
//
// Take input and convert it to suitable format.
//
////////////////////////////////////////////////

module ieee_adder_prepare_input(
	add_sub_bit,
	number,
	sign,
	exponent,
	significand,
);
	//Two inputs and control bit
	// add_sub_bit=0 -> addition
	// add_sub_bit=1 -> subtraction
	input add_sub_bit;
	input `TYPE_NUMBER number;
	
	//Sign of numbers
	output sign;
	
	assign sign = number[`LASTBIT] ^ add_sub_bit;
	
	//Exponents
	output `TYPE_EXPO exponent;
	
	assign exponent = number[`EXPO_LASTBIT:`EXPO_FIRSTBIT];
	
	//Nonzero exponent
	wire nonzero_exp;
	
	assign nonzero_exp = | exponent;
	
	//Significands with added bit 1 in front, and three guard bits,
	//in case that exponent is zero, we add 0 in front instead.
	output `TYPE_SIGNIF significand;
	
	assign significand = {nonzero_exp, number[`SIGNIFICAND_LASTBIT:`SIGNIFICAND_FIRSTBIT], `GUARDBITS'b0};
	
endmodule

////////////////////////////////////////////////////
// MODULE: ieee_adder_compare
////////////////////////////////////////////////////
//
// Compare exponents and significands between inputs
//
////////////////////////////////////////////////////

module ieee_adder_compare(
	exponentA,
	exponentB,
	significandA,
	significandB,
	expA_bigger_expB,
	inputA_bigger_inputB,
	shift_amount
);

	input `TYPE_EXPO exponentA;
	input `TYPE_EXPO exponentB;
	input `TYPE_SIGNIF significandA;
	input `TYPE_SIGNIF significandB;
	
	//How much to shift?
	output `TYPE_EXPO shift_amount;
	//Borrow from subtraction.
	wire sub_borrow;
	
	assign {sub_borrow, shift_amount} = exponentA - exponentB;
	
	//Which exponent is bigger?
	output expA_bigger_expB;
	
	assign expA_bigger_expB = !sub_borrow;
	
	//Are exponents equal?
	//wire expA_equal_expB;
	
	//assign expA_equal_expB = ~& shift_amount;
	
	//Which input number is bigger?
	output inputA_bigger_inputB;
	
	//assign inputA_bigger_inputB = expA_equal_expB ? significandA > significandB :  expA_bigger_expB;
	
	//alternative option:
	assign inputA_bigger_inputB = {exponentA,significandA} > {exponentB,significandB};
endmodule

//////////////////////////////
// Module: ieee_adder_stage3
//////////////////////////////
//
//
//////////////////////////////

module ieee_adder_stage3(
	significandA,
	significandB,
	shift_amount,
	expA_bigger_expB,
	outputC
);
	input `TYPE_SIGNIF significandA;
	input `TYPE_SIGNIF significandB;
	input `TYPE_EXPO shift_amount;
	input expA_bigger_expB;
	output `TYPE_NUMBER outputC;
	
	//Store shifted significands, significand with smaller exponent will be shifted to the right
	wire `TYPE_SIGNIF significandA2;
	wire `TYPE_SIGNIF significandB2;
	
	assign significandA2 = expA_bigger_expB ? significandA : significandA >> -shift_amount;
	assign significandB2 = expA_bigger_expB ? significandB >> shift_amount : significandB;
	
	//Add two significands and store the carry of addition
	wire `TYPE_SIGNIF out_significand1;
	wire carry_significand;
	
	assign {carry_significand, out_significand1} = significandA2 + significandB2;
	
	//Store output exponent, this is simply the biggest out of two exponents
	wire `TYPE_EXPO out_exponent1;
	
	assign out_exponent1 = expA_bigger_expB ? exponentA : exponentB;
	
	//In case that there was a significand overflow, exponent1 will be incremented by one,
	wire `TYPE_EXPO out_exponent2;
	wire exponent_overflow;
	
	assign {exponent_overflow, out_exponent2} = 
		carry_significand ? 1 + out_exponent1
		: {1'b0, out_exponent1};
	
	/* 
	 * FUNCTION: normalize significand
	 * 
	 * Given the significand, we try to normalize it.
	 * It will not be needed if we need only addition.
	 * In case of subtraction it would be needed to normalize this thing!
	 */
	/*function [24:-3] normalize_significand;
		input [24:-3] significand;
		begin
			casex(significand)
				27'b1xxxxxxxxxxxxxxxxxxxxxxxxxx : normalize_significand = significand;
				//this is already normalized
				default: normalize_significand = {28{1'b0}};
			endcase
		end
	endfunction
	
	wire [24:-3] signf_normal;
	
	assign signf_normal = normalize_significand(out_significand1);*/
	
	//Construct output
	// in case there was significand overflow implies bit '1' in front.
	assign outputC = carry_significand ? 
		  {signA, out_exponent2, out_significand1[`SIGNIFICAND_LEN  :1]}
		: {signA, out_exponent2, out_significand1[`SIGNIFICAND_LEN-1:0]};

endmodule

