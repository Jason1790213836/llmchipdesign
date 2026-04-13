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

module CLA2 (
    input [1:0] a,
    input [1:0] b,
    input cin,
    output [1:0] sum,
    output cout
);
    wire [1:0] p, g;
    wire [2:0] c;

    assign p = a ^ b; // Propagate
    assign g = a & b; // Generate

    assign c[0] = cin;
    assign c[1] = g[0] | (p[0] & c[0]);
    assign c[2] = g[1] | (p[1] & c[1]);

    assign sum = p ^ c[1:0];
    assign cout = c[2];
endmodule

module RCA8 (
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    wire c2, c4, c6;

    CLA2 cla0 (
        .a(a[1:0]),
        .b(b[1:0]),
        .cin(1'b0),
        .sum(sum[1:0]),
        .cout(c2)
    );

    CLA2 cla1 (
        .a(a[3:2]),
        .b(b[3:2]),
        .cin(c2),
        .sum(sum[3:2]),
        .cout(c4)
    );

    CLA2 cla2 (
        .a(a[5:4]),
        .b(b[5:4]),
        .cin(c4),
        .sum(sum[5:4]),
        .cout(c6)
    );

    CLA2 cla3 (
        .a(a[7:6]),
        .b(b[7:6]),
        .cin(c6),
        .sum(sum[7:6]),
        .cout(cout)
    );
endmodule