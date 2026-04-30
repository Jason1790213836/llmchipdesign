module RCA8 (
    input [7:0] a,  // First 8-bit input
    input [7:0] b,  // Second 8-bit input
    output [7:0] sum, // 8-bit sum output
    output cout      // 1-bit carry out
);
    wire [1:0] c;   // Internal carry signals for each 4-bit block

    // Instantiate the 1st 4-bit Brent-Kung adder
    BK4 bk0 (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),     // Initial carry-in is 0
        .sum(sum[3:0]),
        .cout(c[0])     // Carry-out to the next block
    );

    // Instantiate the 2nd 4-bit Brent-Kung adder
    BK4 bk1 (
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c[0]),     // Carry from the previous block
        .sum(sum[7:4]),
        .cout(cout)     // Final carry-out
    );
endmodule

module BK4 (
    input [3:0] a,  // First 4-bit input
    input [3:0] b,  // Second 4-bit input
    input cin,      // Carry input
    output [3:0] sum, // 4-bit sum output
    output cout     // Carry output
);
    wire [3:0] p, g; // Propagate and generate signals
    wire [3:0] c;    // Internal carry signals

    // Generate and propagate signals
    assign p = a ^ b;
    assign g = a & b;

    // Brent-Kung prefix tree logic
    wire g0_p0 = g[0] | (p[0] & cin);
    wire g1_p1 = g[1] | (p[1] & g0_p0);
    wire g2_p2 = g[2] | (p[2] & g1_p1);
    assign cout = g[3] | (p[3] & g2_p2);

    // Carry signals
    assign c[0] = cin;
    assign c[1] = g0_p0;
    assign c[2] = g1_p1;
    assign c[3] = g2_p2;

    // Sum calculation
    assign sum = p ^ c;
endmodule