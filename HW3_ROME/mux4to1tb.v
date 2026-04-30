
module mux4to1tb;
    reg [1:0] sel;
    reg [3:0] in;
    wire out;
    mux4to1 uut (.sel(sel), .in(in), .out(out));
    initial begin
        in = 4'b1010;
        sel = 2'b00; #10; if (out !== 0) $finish;
        sel = 2'b01; #10; if (out !== 1) $finish;
        sel = 2'b10; #10; if (out !== 0) $finish;
        sel = 2'b11; #10; if (out !== 1) $finish;
        $display("passed!");
        $finish;
    end
endmodule
