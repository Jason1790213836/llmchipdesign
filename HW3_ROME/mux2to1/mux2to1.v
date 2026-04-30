module mux2to1(input wire in1, input wire in2, input wire select, output wire out);
    wire w_and1, w_and2, w_not;
    
    assign w_and1 = in1 & ~select;
    assign w_and2 = in2 & select;
    assign w_not = w_and1 | w_and2;
    
    assign out = w_not;
endmodule
