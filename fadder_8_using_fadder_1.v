// creating 3:8 decoder
module decoder (d0, d1, d2, d3, d4, d5, d6, d7, x, y, z);
	
	// set inputs, wires and outputs
	input x, y, z;
	output d0, d1, d2, d3, d4, d5, d6, d7;
	wire not_x, not_y, not_z;

	// set not gates
	not n1 (not_x, x);
	not n2 (not_y, y);
	not n3 (not_z, z);

	// set outputs for d0-d7
	and and0 (d0, not_z, not_y, not_x);
	and and1 (d1, z    , not_y, not_x);
	and and2 (d2, not_z, y    , not_x);
	and and3 (d3, z    , y    , not_x);
	and and4 (d4, not_z, not_y, x    );
	and and5 (d5, z    , not_y, x    );
	and and6 (d6, not_z, y    , x    );
	and and7 (d7, z    , y    , x    );

endmodule

// creating fadder using 3:8 decoder
module fadder(sum, carry, x, y, z);

	// set input, wires and outputs
	input x, y, z;
	wire d0, d1, d2, d3, d4, d5, d6, d7;
	output sum, carry;

	// get decoder outputs to wires
	decoder decoder_3_8(d0, d1, d2, d3, d4, d5, d6, d7, x, y, z);
	
	// get sum and carry outputs via or gates (GATE OPS)
	// or orsum (sum, d1, d2, d4, d7);
	// or orcarry (carry, d3, d5, d6, d7);
	// SAME THING IN ARITHMETIC OPS
	assign sum = d1 | d2 | d4 | d7;
	assign carry = d3 | d5 | d6 | d7;

endmodule

// create testbench
module testbench;
	reg x,y,z;
	wire sum, carry;
	fadder fl(sum, carry, x, y, z);
 	initial
 		$monitor(,$time,"x=%b,y=%b,z=%b,s=%b,c=%b",x,y,z,sum,carry);
 	initial
 	begin
 		#0 x=1'b0;y=1'b0;z=1'b0;
 		#4 x=1'b1;y=1'b0;z=1'b0;
 		#4 x=1'b0;y=1'b1;z=1'b0;
 		#4 x=1'b1;y=1'b1;z=1'b0;
		#4 x=1'b0;y=1'b0;z=1'b1;
		#4 x=1'b1;y=1'b0;z=1'b1;
 		#4 x=1'b0;y=1'b1;z=1'b1;
		#4 x=1'b1;y=1'b1;z=1'b1;
 	end
endmodule
