module CSLA4 (
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire [3:0] sum0, sum1;
    wire c0, c1;

    // Ripple Carry Adder for cin = 0
    RCA4 rca0 (
        .a(a),
        .b(b),
        .cin(1'b0),
        .sum(sum0),
        .cout(c0)
    );

    // Ripple Carry Adder for cin = 1
    RCA4 rca1 (
        .a(a),
        .b(b),
        .cin(1'b1),
        .sum(sum1),
        .cout(c1)
    );

    // Select the correct sum and carry based on cin
    assign sum = cin ? sum1 : sum0;
    assign cout = cin ? c1 : c0;
endmodule

module RCA4 (
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire [3:0] c;

    // Full Adders for each bit
    FA fa0 (.a(a[0]), .b(b[0]), .cin(cin), .sum(sum[0]), .cout(c[1]));
    FA fa1 (.a(a[1]), .b(b[1]), .cin(c[1]), .sum(sum[1]), .cout(c[2]));
    FA fa2 (.a(a[2]), .b(b[2]), .cin(c[2]), .sum(sum[2]), .cout(c[3]));
    FA fa3 (.a(a[3]), .b(b[3]), .cin(c[3]), .sum(sum[3]), .cout(cout));
endmodule

module FA (
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin) | (a & cin);
endmodule

module RCA8 (
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    wire c4;

    // Instantiate two 4-bit Carry Select Adders
    CSLA4 csla0 (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),
        .sum(sum[3:0]),
        .cout(c4)
    );

    CSLA4 csla1 (
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c4),
        .sum(sum[7:4]),
        .cout(cout)
    );
endmodule