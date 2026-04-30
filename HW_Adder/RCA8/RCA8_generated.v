
module FA (
    input a,        // First input bit
    input b,        // Second input bit
    input cin,      // Carry input
    output sum,     // Sum output
    output cout     // Carry output
);
    wire w0;        // Intermediate wire for sum calculation

    // Sum output: sum = a XOR b XOR cin
    assign w0 = a ^ b;
    assign sum = w0 ^ cin;

    // Carry output: cout = (a AND b) OR (cin AND (a XOR b))
    assign cout = (a & b) | (cin & w0);
endmodule

// 8-bit Ripple Carry Adder Module
module RCA8 (
    input [7:0] a,  // First 8-bit input
    input [7:0] b,  // Second 8-bit input
    output [7:0] sum, // 8-bit sum output
    output cout      // 1-bit carry out
);
    wire [7:0] c;   // Internal carry signals

    // Instantiate the 1st Full Adder
    FA fa0 (
        .a(a[0]),
        .b(b[0]),
        .cin(1'b0),     // Initial carry-in is 0
        .sum(sum[0]),
        .cout(c[1])     // Carry-out to the next stage
    );

    // Instantiate the 2nd to 7th Full Adders using a generate loop
    genvar i;
    generate
        for (i = 1; i < 7; i = i + 1) begin: full_adder_array
            FA faN (
                .a(a[i]),
                .b(b[i]),
                .cin(c[i]),    // Previous stage's carry-out
                .sum(sum[i]),
                .cout(c[i + 1]) // Carry-out to the next stage
            );
        end
    endgenerate

    // Instantiate the 8th Full Adder
    FA fa7 (
        .a(a[7]),
        .b(b[7]),
        .cin(c[7]),     // Carry from the 7th stage
        .sum(sum[7]),
        .cout(cout)     // Final carry-out
    );
endmodule
