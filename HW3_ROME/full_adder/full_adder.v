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
module full_adder(
    input wire a,
    input wire b,
    input wire cin,
    output wire sum,
    output wire cout
);

wire w1, w2, w3, w4, w5;

half_adder ha1(.a(a), .b(b), .sum(w1), .carry(w2));
half_adder ha2(.a(w1), .b(cin), .sum(w3), .carry(w4));

xor_gate xor2(.a(w2), .b(w4), .out(w5));
assign sum = w3;
assign cout = w5;

endmodule
