module KoggeStone8 (
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    wire [7:0] p, g;
    wire [7:0] c;

    assign p = a ^ b; // Propagate
    assign g = a & b; // Generate

    wire [7:0] gp1, gp2, gp3;

    // Stage 1
    assign gp1[0] = g[0];
    assign gp1[1] = g[1] | (p[1] & g[0]);
    assign gp1[2] = g[2] | (p[2] & g[1]);
    assign gp1[3] = g[3] | (p[3] & g[2]);
    assign gp1[4] = g[4] | (p[4] & g[3]);
    assign gp1[5] = g[5] | (p[5] & g[4]);
    assign gp1[6] = g[6] | (p[6] & g[5]);
    assign gp1[7] = g[7] | (p[7] & g[6]);

    // Stage 2
    assign gp2[0] = gp1[0];
    assign gp2[1] = gp1[1];
    assign gp2[2] = gp1[2] | (p[2] & gp1[0]);
    assign gp2[3] = gp1[3] | (p[3] & gp1[1]);
    assign gp2[4] = gp1[4] | (p[4] & gp1[2]);
    assign gp2[5] = gp1[5] | (p[5] & gp1[3]);
    assign gp2[6] = gp1[6] | (p[6] & gp1[4]);
    assign gp2[7] = gp1[7] | (p[7] & gp1[5]);

    // Stage 3
    assign gp3[0] = gp2[0];
    assign gp3[1] = gp2[1];
    assign gp3[2] = gp2[2];
    assign gp3[3] = gp2[3];
    assign gp3[4] = gp2[4] | (p[4] & gp2[0]);
    assign gp3[5] = gp2[5] | (p[5] & gp2[1]);
    assign gp3[6] = gp2[6] | (p[6] & gp2[2]);
    assign gp3[7] = gp2[7] | (p[7] & gp2[3]);

    // Final carry
    assign c[0] = 1'b0;
    assign c[1] = gp3[0];
    assign c[2] = gp3[1];
    assign c[3] = gp3[2];
    assign c[4] = gp3[3];
    assign c[5] = gp3[4];
    assign c[6] = gp3[5];
    assign c[7] = gp3[6];
    assign cout = gp3[7];

    // Sum calculation
    assign sum = p ^ c;
endmodule

module RCA8 (
    input [7:0] a,
    input [7:0] b,
    output [7:0] sum,
    output cout
);
    KoggeStone8 ks8 (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );
endmodule