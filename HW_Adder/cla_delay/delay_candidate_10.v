module PGGen(
    input a,
    input b,
    output g,
    output p
);
    and a1(g, a, b);
    xor x1(p, a, b);
endmodule

module CarrySelectAdder2(
    input [1:0] a,
    input [1:0] b,
    input cin,
    output [1:0] sum,
    output cout
);
    wire [1:0] sum0, sum1;
    wire cout0, cout1;

    // Ripple carry adder for cin = 0
    assign {cout0, sum0} = a + b;

    // Ripple carry adder for cin = 1
    assign {cout1, sum1} = a + b + 2'b01;

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
    wire c2, c4, c6;

    CarrySelectAdder2 csa0(
        .a(a[1:0]),
        .b(b[1:0]),
        .cin(1'b0),
        .sum(sum[1:0]),
        .cout(c2)
    );

    CarrySelectAdder2 csa1(
        .a(a[3:2]),
        .b(b[3:2]),
        .cin(c2),
        .sum(sum[3:2]),
        .cout(c4)
    );

    CarrySelectAdder2 csa2(
        .a(a[5:4]),
        .b(b[5:4]),
        .cin(c4),
        .sum(sum[5:4]),
        .cout(c6)
    );

    CarrySelectAdder2 csa3(
        .a(a[7:6]),
        .b(b[7:6]),
        .cin(c6),
        .sum(sum[7:6]),
        .cout(cout)
    );
endmodule