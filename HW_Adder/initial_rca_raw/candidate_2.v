module RCA8 (
    input [7:0] a,  // First 8-bit input
    input [7:0] b,  // Second 8-bit input
    output [7:0] sum, // 8-bit sum output
    output cout      // 1-bit carry out
);
    wire [3:0] c;   // Internal carry signals for each 4-bit block

    // Instantiate the 1st 4-bit CLA
    CLA4 cla0 (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),     // Initial carry-in is 0
        .sum(sum[3:0]),
        .cout(c[0])     // Carry-out to the next block
    );

    // Instantiate the 2nd 4-bit CLA
    CLA4 cla1 (
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c[0]),     // Carry from the previous block
        .sum(sum[7:4]),
        .cout(cout)     // Final carry-out
    );
endmodule

module CLA4 (
    input [3:0] a,  // First 4-bit input
    input [3:0] b,  // Second 4-bit input
    input cin,      // Carry input
    output [3:0] sum, // 4-bit sum output
    output cout     // Carry output
);
    wire [3:0] p, g; // Propagate and generate signals
    wire [3:1] c;    // Internal carry signals

    // Generate and propagate signals
    assign p = a ^ b;
    assign g = a & b;

    // Carry look-ahead logic
    assign c[1] = g[0] | (p[0] & cin);
    assign c[2] = g[1] | (p[1] & c[1]);
    assign c[3] = g[2] | (p[2] & c[2]);
    assign cout = g[3] | (p[3] & c[3]);

    // Sum calculation
    assign sum = p ^ {c[3:1], cin};
endmodule