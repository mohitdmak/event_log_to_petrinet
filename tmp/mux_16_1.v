// creating mux 4:1
module mux_4_1_gate(out, inp, select);
	// setting inputs and outputs by 'input'/'output' keywords
	input [0:3] inp;
	input [0:1] select;
	output out;

	// setting required wires
	wire not_select0, not_select1, a1, a2, a3, a4;

	// getting not of selects
	not n0 (not_select0, select[0]);
	not n1 (not_select1, select[1]);

	// geting and of 3-tuple -> input, 2 selects
	and and1 (a1, inp[0], not_select1, not_select0  );
	and and2 (a2, inp[1], not_select0, select[1]    );
	and and3 (a3, inp[2], select[0]  , not_select1  );
	and and4 (a4, inp[3], select[0]  , select[1]    );

	// final or to output
	or final_or (out, a1, a2, a3, a4);
	
endmodule


// creating 16:1 mux using 4:1 mux module
module mux_16_1(out, inp, select);
	// setting inputs and outputs
	input [0:15] inp;
	input [0:3] select;
	output out;

	// setting wires
	wire [0:3] mux_4_1_op;

	// getting outputs from 4:1 mux gate (inner 4 gates)
	mux_4_1_gate mux1 (mux_4_1_op[0], inp[0:3]  , select[2:3]);
	mux_4_1_gate mux2 (mux_4_1_op[1], inp[4:7]  , select[2:3]);
	mux_4_1_gate mux3 (mux_4_1_op[2], inp[8:11] , select[2:3]);
	mux_4_1_gate mux4 (mux_4_1_op[3], inp[12:15], select[2:3]);

	// getting output for outer 4:1 mux gate
	mux_4_1_gate mux5 (out, mux_4_1_op, select[0:1]);
	
endmodule
	
	
// creating testbench
module test_mux_16_1;
	reg [0:15] inp;
	reg [0:3] select;
	wire out;
 
 	mux_16_1 mux(out, inp, select);
	initial
	begin
		// creating dumpfile for graphical output
		$dumpfile("mux_16_1.vcd");
		$dumpvars;

		$monitor("inp=%b | select=%b | out=%b", inp, select, out);
	end

	initial 
	begin
		inp=16'b1000000000000000;    select=4'b0000;
 		#3 inp=16'b0100000000000000; select=4'b0001; 
		#3 inp=16'b0010000000000000; select=4'b0010;
		#3 inp=16'b0001000000000000; select=4'b0011;
		#3 inp=16'b0000100000000000; select=4'b0100;
		#3 inp=16'b0000010000000000; select=4'b0101; 
		#3 inp=16'b0000001000000000; select=4'b0110;
		#3 inp=16'b0000000100000000; select=4'b0111; 
		#3 inp=16'b0000000010000000; select=4'b1000;
		#3 inp=16'b0000000001000000; select=4'b1001; 
		#3 inp=16'b0000000000100000; select=4'b1010;
		#3 inp=16'b0000000000010000; select=4'b1011;
		#3 inp=16'b0000000000001000; select=4'b1100;
		#3 inp=16'b0000000000000100; select=4'b1101; 
		#3 inp=16'b0000000000000010; select=4'b1110;
		#3 inp=16'b0000000000000001; select=4'b1111;
	end
endmodule