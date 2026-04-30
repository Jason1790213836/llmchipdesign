module PGGen(
    input a,
    input b,
    output g,
    output p
);
    and a1(g, a, b);
    xor x1(p, a, b);
endmodule

module BrentKung4(
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire [3:0] g, p;
    wire [3:0] c;

    PGGen pg0(a[0], b[0], g[0], p[0]);
    PGGen pg1(a[1], b[1], g[1], p[1]);
    PGGen pg2(a[2], b[2], g[2], p[2]);
    PGGen pg3(a[3], b[3], g[3], p[3]);

    wire g01, p01, g23, p23;
    wire g012, p012, g123, p123;

    assign g01 = g[1] | (p[1] & g[0]);
    assign p01 = p[1] & p[0];
    assign g23 = g[3] | (p[3] & g[2]);
    assign p23 = p[3] & p[2];

    assign g012 = g[2] | (p[2] & g01);
    assign p012 = p[2] & p01;
    assign g123 = g23 | (p23 & g01);

    assign c[0] = cin;
    assign c[1] = g[0] | (p[0] & cin);
    assign c[2] = g01 | (p01 & cin);
    assign c[3] = g012 | (p012 & cin);
    assign cout = g123 | (p23 & p01 & cin);

    xor x0(sum[0], p[0], c[0]);
    xor x1(sum[1], p[1], c[1]);
    xor x2(sum[2], p[2], c[2]);
    xor x3(sum[3], p[3], c[3]);
endmodule

module CLA8(
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    wire c4;

    BrentKung4 bk_low(
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),
        .sum(sum[3:0]),
        .cout(c4)
    );

    BrentKung4 bk_high(
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c4),
        .sum(sum[7:4]),
        .cout(cout)
    );
endmodule