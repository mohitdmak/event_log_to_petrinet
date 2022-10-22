module mux2_1 (out, sel, in1, in2);
	input in1, in2, sel;
	output out;
	
	// creating wires
	wire not_sel, a1, a2;

	// gates
	not (not_sel, sel);
	and (a1, sel, in2);
	and (a2, not_sel, in1);
	or  (out, a1, a2);
endmodule
