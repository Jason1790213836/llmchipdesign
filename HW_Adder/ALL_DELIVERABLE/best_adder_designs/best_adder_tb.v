`timescale 1ns/1ps

module best_adder_tb;

    reg  [7:0] a, b;
    wire [7:0] sum;
    wire cout;

    wire [8:0] expected;

    RCA8 dut (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );

    assign expected = a + b;

    integer i, j;
    integer errors;

    initial begin
        errors = 0;

        // Exhaustive test for all 8-bit input pairs
        for (i = 0; i < 256; i = i + 1) begin
            for (j = 0; j < 256; j = j + 1) begin
                a = i[7:0];
                b = j[7:0];
                #1;

                if ({cout, sum} !== expected) begin
                    $display("ERROR: a=%0d b=%0d -> got {%b,%h}, expected %h",
                             i, j, cout, sum, expected);
                    errors = errors + 1;
                end
            end
        end

        if (errors == 0)
            $display("@@@PASS");
        else
            $display("@@@FAIL: %0d mismatches", errors);

        $finish;
    end

endmodule