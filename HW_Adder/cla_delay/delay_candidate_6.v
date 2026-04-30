module PGGen(
    input a,
    input b,
    output g,
    output p
);
    and a1(g, a, b);
    xor x1(p, a, b);
endmodule

module CarrySelectAdder4(
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire [3:0] sum0, sum1;
    wire cout0, cout1;

    // Ripple carry adder for cin = 0
    assign {cout0, sum0} = a + b;

    // Ripple carry adder for cin = 1
    assign {cout1, sum1} = a + b + 4'b0001;

    // Select the appropriate sum and cout based on cin
    assign sum = cin ? sum1 : sum0;
    assign cout = cin ? cout1 : cout0;
endmodule

module CLA8(
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    wire c4;

    CarrySelectAdder4 csa_low(
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),
        .sum(sum[3:0]),
        .cout(c4)
    );

    CarrySelectAdder4 csa_high(
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c4),
        .sum(sum[7:4]),
        .cout(cout)
    );
endmodule