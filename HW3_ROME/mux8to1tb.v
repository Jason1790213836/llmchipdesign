
module mux8to1tb;
    reg [2:0] sel;
    reg [7:0] in;
    wire out;
    mux8to1 uut (.sel(sel), .in(in), .out(out));
    initial begin
        in = 8'b10110010;
        sel = 3'b000; #10; if (out !== 0) $finish;
        sel = 3'b001; #10; if (out !== 1) $finish;
        sel = 3'b100; #10; if (out !== 1) $finish;
        sel = 3'b111; #10; if (out !== 1) $finish;
        $display("passed!");
        $finish;
    end
endmodule
