module xor_gate(
    input wire a,
    input wire b,
    output wire out
);

assign out = a ^ b;

endmodule
module and_gate(
    input wire a,
    input wire b,
    output wire out
);

assign out = a & b;

endmodule
module half_adder(
    input wire a, 
    input wire b, 
    output wire sum, 
    output wire carry
);

wire w1, w2;

xor_gate xor1(.a(a), .b(b), .out(w1));
and_gate and1(.a(a), .b(b), .out(w2));
assign sum = w1;
assign carry = w2;

endmodule
