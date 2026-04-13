`timescale 1ns/1ps

module RCA8_tb;

    reg  [7:0] a;
    reg  [7:0] b;
    wire [7:0] sum;
    wire       cout;

    integer total_tests;
    integer passed_tests;

    reg  [8:0] expected_fullsum;
    reg  [7:0] expected_sum;
    reg        expected_cout;
    reg  [7:1] expected_c;

    // DUT instantiation
    RCA8 dut (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );

    // Task to compute expected internal carries for RCA
    task compute_expected_carries;
        input  [7:0] ta;
        input  [7:0] tb;
        output [7:1] tc;
        reg carry;
        integer i;
        begin
            carry = 1'b0;
            for (i = 0; i < 7; i = i + 1) begin
                carry = (ta[i] & tb[i]) | (carry & (ta[i] ^ tb[i]));
                tc[i+1] = carry;
            end
        end
    endtask

    // Task to run one test case
    task run_test;
        input [7:0] ta;
        input [7:0] tb;
        begin
            a = ta;
            b = tb;
            #1;

            total_tests = total_tests + 1;

            expected_fullsum = ta + tb;
            expected_sum     = expected_fullsum[7:0];
            expected_cout    = expected_fullsum[8];
            compute_expected_carries(ta, tb, expected_c);

            $display("--------------------------------------------------");
            $display("TEST %0d", total_tests);
            $display("a = 0x%0h (%08b), b = 0x%0h (%08b)", ta, ta, tb, tb);
            $display("Expected: sum = %08b, cout = %b, c = %b",
                     expected_sum, expected_cout, expected_c);
            $display("Actual  : sum = %08b, cout = %b, c = %b",
                     sum, cout, dut.c[7:1]);

            if ((sum === expected_sum) &&
                (cout === expected_cout) &&
                (dut.c[7:1] === expected_c)) begin
                passed_tests = passed_tests + 1;
                $display("Result  : PASS");
            end else begin
                $display("Result  : FAIL");
                if (sum !== expected_sum)
                    $display("  Mismatch in sum");
                if (cout !== expected_cout)
                    $display("  Mismatch in cout");
                if (dut.c[7:1] !== expected_c)
                    $display("  Mismatch in internal carries");
            end
        end
    endtask

    initial begin
        $dumpfile("RCA8_tb.vcd");
        $dumpvars(0, RCA8_tb);

        total_tests  = 0;
        passed_tests = 0;

        // Representative directed tests
        run_test(8'h00, 8'h00);
        run_test(8'h01, 8'h01);
        run_test(8'h0F, 8'h01);
        run_test(8'hFF, 8'h01);
        run_test(8'hAA, 8'h55);
        run_test(8'h7F, 8'h01);
        run_test(8'h80, 8'h80);
        run_test(8'hF0, 8'h0F);
        run_test(8'h3C, 8'h42);
        run_test(8'h99, 8'h66);

        // A few random tests
        run_test(8'h12, 8'h34);
        run_test(8'h5A, 8'hA5);
        run_test(8'hC3, 8'h3C);
        run_test(8'hFE, 8'h02);
        run_test(8'h81, 8'h7F);

        $display("==================================================");
        $display("SUMMARY: %0d / %0d tests passed", passed_tests, total_tests);

        if (passed_tests == total_tests)
            $display("@@@PASS");
        else
            $display("@@@FAIL");

        $finish;
    end

endmodule