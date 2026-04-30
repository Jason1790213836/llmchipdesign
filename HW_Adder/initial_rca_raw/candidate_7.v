module RCA8 (
    input [7:0] a,  // First 8-bit input
    input [7:0] b,  // Second 8-bit input
    output [7:0] sum, // 8-bit sum output
    output cout      // 1-bit carry out
);
    wire [2:0] c;   // Internal carry signals for each 2-bit block

    // Instantiate the 1st 2-bit CLA
    CLA2 cla0 (
        .a(a[1:0]),
        .b(b[1:0]),
        .cin(1'b0),     // Initial carry-in is 0
        .sum(sum[1:0]),
        .cout(c[0])     // Carry-out to the next block
    );

    // Instantiate the 2nd 2-bit CLA
    CLA2 cla1 (
        .a(a[3:2]),
        .b(b[3:2]),
        .cin(c[0]),     // Carry from the previous block
        .sum(sum[3:2]),
        .cout(c[1])     // Carry-out to the next block
    );

    // Instantiate the 3rd 2-bit CLA
    CLA2 cla2 (
        .a(a[5:4]),
        .b(b[5:4]),
        .cin(c[1]),     // Carry from the previous block
        .sum(sum[5:4]),
        .cout(c[2])     // Carry-out to the next block
    );

    // Instantiate the 4th 2-bit CLA
    CLA2 cla3 (
        .a(a[7:6]),
        .b(b[7:6]),
        .cin(c[2]),     // Carry from the previous block
        .sum(sum[7:6]),
        .cout(cout)     // Final carry-out
    );
endmodule

module CLA2 (
    input [1:0] a,  // First 2-bit input
    input [1:0] b,  // Second 2-bit input
    input cin,      // Carry input
    output [1:0] sum, // 2-bit sum output
    output cout     // Carry output
);
    wire [1:0] p, g; // Propagate and generate signals
    wire c1;         // Internal carry signal

    // Generate and propagate signals
    assign p = a ^ b;
    assign g = a & b;

    // Carry look-ahead logic
    assign c1 = g[0] | (p[0] & cin);
    assign cout = g[1] | (p[1] & c1);

    // Sum calculation
    assign sum = p ^ {c1, cin};
endmodule