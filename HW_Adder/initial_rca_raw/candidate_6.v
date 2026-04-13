module RCA8 (
    input [7:0] a,  // First 8-bit input
    input [7:0] b,  // Second 8-bit input
    output [7:0] sum, // 8-bit sum output
    output cout      // 1-bit carry out
);
    wire [1:0] c;   // Internal carry signals for each 4-bit block

    // Instantiate the 1st 4-bit Carry Select Adder
    CSA4 csa0 (
        .a(a[3:0]),
        .b(b[3:0]),
        .cin(1'b0),     // Initial carry-in is 0
        .sum(sum[3:0]),
        .cout(c[0])     // Carry-out to the next block
    );

    // Instantiate the 2nd 4-bit Carry Select Adder
    CSA4 csa1 (
        .a(a[7:4]),
        .b(b[7:4]),
        .cin(c[0]),     // Carry from the previous block
        .sum(sum[7:4]),
        .cout(cout)     // Final carry-out
    );
endmodule

module CSA4 (
    input [3:0] a,  // First 4-bit input
    input [3:0] b,  // Second 4-bit input
    input cin,      // Carry input
    output [3:0] sum, // 4-bit sum output
    output cout     // Carry output
);
    wire [3:0] sum0, sum1;
    wire cout0, cout1;

    // 4-bit Ripple Carry Adder with carry-in 0
    RCA4 rca0 (
        .a(a),
        .b(b),
        .cin(1'b0),
        .sum(sum0),
        .cout(cout0)
    );

    // 4-bit Ripple Carry Adder with carry-in 1
    RCA4 rca1 (
        .a(a),
        .b(b),
        .cin(1'b1),
        .sum(sum1),
        .cout(cout1)
    );

    // Select the correct sum and carry-out based on the input carry
    assign sum = cin ? sum1 : sum0;
    assign cout = cin ? cout1 : cout0;
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