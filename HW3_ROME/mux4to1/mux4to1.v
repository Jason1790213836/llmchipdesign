module mux2to1(input wire in1, input wire in2, input wire select, output wire out);
    wire w_and1, w_and2, w_not;

    assign w_and1 = in1 & ~select;
    assign w_and2 = in2 & select;
    assign w_not = w_and1 | w_and2;

    assign out = w_not;
endmodule
module mux4to1(input [1:0] sel, input [3:0] in, output wire out);
    wire w_mux1_out, w_mux2_out, w_mux3_out;
    wire w_sel1, w_sel2, w_sel3;
    
    mux2to1 mux1(in[0], in[1], sel[0], w_mux1_out);
    mux2to1 mux2(in[2], in[3], sel[0], w_mux2_out);
    mux2to1 mux3(w_mux1_out, w_mux2_out, sel[1], w_mux3_out);
    
    assign out = w_mux3_out;
endmodule
