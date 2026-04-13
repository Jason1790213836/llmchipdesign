module HybridAdder8 (
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    wire [3:0] sum0, sum1;
    wire cout0, cout1, c4;

    // Lower 4 bits using CLA
    CLA4 cla0 (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),
        .sum(sum0),
        .cout(c4)
    );

    // Upper 4 bits using RCA
    RCA4 rca1 (
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c4),
        .sum(sum1),
        .cout(cout1)
    );

    assign sum = {sum1, sum0};
    assign cout = cout1;
endmodule

module CLA4 (
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire [3:0] p, g;
    wire [4:0] c;

    assign p = a ^ b; // Propagate
    assign g = a & b; // Generate

    assign c[0] = cin;
    assign c[1] = g[0] | (p[0] & c[0]);
    assign c[2] = g[1] | (p[1] & c[1]);
    assign c[3] = g[2] | (p[2] & c[2]);
    assign c[4] = g[3] | (p[3] & c[3]);

    assign sum = p ^ c[3:0];
    assign cout = c[4];
endmodule

module RCA4 (
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire [3:0] c;

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
    HybridAdder8 ha8 (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );
endmodule