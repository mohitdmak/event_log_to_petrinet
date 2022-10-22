module non_parallel(t,a,b,c,d);
	input t;
	output reg a, b, c, d;
	initial
	begin
		#t;
		fork
			a = 2'b01;
			#5 b = 2'b00;
			//b = 1'b0;
			#10 c = 2'b01;
		join
		#6 d = 2'b01;
	end
endmodule

module test_non_parallel;
	//reg t;
	//t = 2;
	wire a,b,c,d;
	non_parallel np(2'b10, a, b, c, d);
	initial
	begin
		$monitor(, $time, " A=%b, B=%b, C=%b, D=%b", a, b, c, d);
	end
endmodule

