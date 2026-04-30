
module mux2to1tb;
    reg in1, in2, select;
    wire out;
    mux2to1 uut (.in1(in1), .in2(in2), .select(select), .out(out));
    initial begin
        in1 = 0; in2 = 1; select = 0; #10;
        if (out !== 0) $finish;
        in1 = 0; in2 = 1; select = 1; #10;
        if (out !== 1) $finish;
        $display("passed!");
        $finish;
    end
endmodule
