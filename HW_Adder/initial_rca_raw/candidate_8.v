module RCA8 (
    input [7:0] a,  // First 8-bit input
    input [7:0] b,  // Second 8-bit input
    output [7:0] sum, // 8-bit sum output
    output cout      // 1-bit carry out
);
    wire [1:0] c;   // Internal carry signals for each 4-bit block

    // Instantiate the 1st 4-bit CLA
    CLA4 cla0 (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),     // Initial carry-in is 0
        .sum(sum[3:0]),
        .cout(c[0])     // Carry-out to the next block
    );

    // Instantiate the 2nd 4-bit RCA
    RCA4 rca1 (
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

module RCA4 (
    input [3:0] a,  // First 4-bit input
    input [3:0] b,  // Second 4-bit input
    input cin,      // Carry input
    output [3:0] sum, // 4-bit sum output
    output cout     // Carry output
);
    wire [3:0] c;   // Internal carry signals

    // Instantiate the 1st Full Adder
    FA fa0 (
        .a(a[0]),
        .b(b[0]),
        .cin(cin),     // Initial carry-in
        .sum(sum[0]),
        .cout(c[1])    // Carry-out to the next stage
    );

    // Instantiate the 2nd to 3rd Full Adders
    genvar i;
    generate
        for (i = 1; i < 3; i = i + 1) begin: full_adder_array
            FA faN (
                .a(a[i]),
                .b(b[i]),
                .cin(c[i]),    // Previous stage's carry-out
                .sum(sum[i]),
                .cout(c[i + 1]) // Carry-out to the next stage
            );
        end
    endgenerate

    // Instantiate the 4th Full Adder
    FA fa3 (
        .a(a[3]),
        .b(b[3]),
        .cin(c[3]),     // Carry from the 3rd stage
        .sum(sum[3]),
        .cout(cout)     // Final carry-out
    );
endmodule

module FA (
    input a,        // First input bit
    input b,        // Second input bit
    input cin,      // Carry input
    output sum,     // Sum output
    output cout     // Carry output
);
    // Sum output: sum = a XOR b XOR cin
    assign sum = a ^ b ^ cin;

    // Carry output: cout = (a AND b) OR (cin AND (a XOR b))
    assign cout = (a & b) | (cin & (a ^ b));
endmodule