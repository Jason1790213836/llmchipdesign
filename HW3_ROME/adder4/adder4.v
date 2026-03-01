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
module adder4(
    input wire [3:0] a,
    input wire [3:0] b,
    input wire cin,
    output wire [3:0] sum,
    output wire cout
);

wire c0, c1, c2, c3;

full_adder fa0(.a(a[0]), .b(b[0]), .cin(cin), .sum(sum[0]), .cout(c0));
full_adder fa1(.a(a[1]), .b(b[1]), .cin(c0), .sum(sum[0+1]), .cout(c1));
full_adder fa2(.a(a[2]), .b(b[2]), .cin(c1), .sum(sum[0+2]), .cout(c2));
full_adder fa3(.a(a[3]), .b(b[3]), .cin(c2), .sum(sum[0+3]), .cout(c3));

assign cout = c3;

endmodule
