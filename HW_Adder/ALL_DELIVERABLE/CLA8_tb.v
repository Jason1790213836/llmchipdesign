`timescale 1ns/1ps

module CLA8_tb;

    reg  [7:0] a;
    reg  [7:0] b;
    wire [7:0] sum;
    wire       cout;

    integer total_tests;
    integer passed_tests;

    reg  [7:0] expected_g;
    reg  [7:0] expected_p;
    reg  [7:0] expected_c;
    reg  [7:0] expected_sum;
    reg        expected_cout;
    reg        cin;

    CLA8 dut (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );

    task compute_expected;
        input  [7:0] ta;
        input  [7:0] tb;
        output [7:0] tg;
        output [7:0] tp;
        output [7:0] tc;
        output [7:0] tsum;
        output       tcout;
        reg          tcin;
        begin
            tcin = 1'b0;

            tg = ta & tb;
            tp = ta ^ tb;

            tc[0] = tg[0] | (tp[0] & tcin);

            tc[1] = tg[1]
                  | (tp[1] & tg[0])
                  | (tp[1] & tp[0] & tcin);

            tc[2] = tg[2]
                  | (tp[2] & tg[1])
                  | (tp[2] & tp[1] & tg[0])
                  | (tp[2] & tp[1] & tp[0] & tcin);

            tc[3] = tg[3]
                  | (tp[3] & tg[2])
                  | (tp[3] & tp[2] & tg[1])
                  | (tp[3] & tp[2] & tp[1] & tg[0])
                  | (tp[3] & tp[2] & tp[1] & tp[0] & tcin);

            tc[4] = tg[4]
                  | (tp[4] & tg[3])
                  | (tp[4] & tp[3] & tg[2])
                  | (tp[4] & tp[3] & tp[2] & tg[1])
                  | (tp[4] & tp[3] & tp[2] & tp[1] & tg[0])
                  | (tp[4] & tp[3] & tp[2] & tp[1] & tp[0] & tcin);

            tc[5] = tg[5]
                  | (tp[5] & tg[4])
                  | (tp[5] & tp[4] & tg[3])
                  | (tp[5] & tp[4] & tp[3] & tg[2])
                  | (tp[5] & tp[4] & tp[3] & tp[2] & tg[1])
                  | (tp[5] & tp[4] & tp[3] & tp[2] & tp[1] & tg[0])
                  | (tp[5] & tp[4] & tp[3] & tp[2] & tp[1] & tp[0] & tcin);

            tc[6] = tg[6]
                  | (tp[6] & tg[5])
                  | (tp[6] & tp[5] & tg[4])
                  | (tp[6] & tp[5] & tp[4] & tg[3])
                  | (tp[6] & tp[5] & tp[4] & tp[3] & tg[2])
                  | (tp[6] & tp[5] & tp[4] & tp[3] & tp[2] & tg[1])
                  | (tp[6] & tp[5] & tp[4] & tp[3] & tp[2] & tp[1] & tg[0])
                  | (tp[6] & tp[5] & tp[4] & tp[3] & tp[2] & tp[1] & tp[0] & tcin);

            tc[7] = tg[7]
                  | (tp[7] & tg[6])
                  | (tp[7] & tp[6] & tg[5])
                  | (tp[7] & tp[6] & tp[5] & tg[4])
                  | (tp[7] & tp[6] & tp[5] & tp[4] & tg[3])
                  | (tp[7] & tp[6] & tp[5] & tp[4] & tp[3] & tg[2])
                  | (tp[7] & tp[6] & tp[5] & tp[4] & tp[3] & tp[2] & tg[1])
                  | (tp[7] & tp[6] & tp[5] & tp[4] & tp[3] & tp[2] & tp[1] & tg[0])
                  | (tp[7] & tp[6] & tp[5] & tp[4] & tp[3] & tp[2] & tp[1] & tp[0] & tcin);

            tsum[0] = tp[0] ^ tcin;
            tsum[1] = tp[1] ^ tc[0];
            tsum[2] = tp[2] ^ tc[1];
            tsum[3] = tp[3] ^ tc[2];
            tsum[4] = tp[4] ^ tc[3];
            tsum[5] = tp[5] ^ tc[4];
            tsum[6] = tp[6] ^ tc[5];
            tsum[7] = tp[7] ^ tc[6];

            tcout = tc[7];
        end
    endtask

    task run_test;
        input [7:0] ta;
        input [7:0] tb;
        begin
            a = ta;
            b = tb;
            #1;

            total_tests = total_tests + 1;

            compute_expected(ta, tb, expected_g, expected_p, expected_c, expected_sum, expected_cout);

            $display("--------------------------------------------------");
            $display("TEST %0d", total_tests);
            $display("a = 0x%0h (%08b), b = 0x%0h (%08b)", ta, ta, tb, tb);
            $display("Expected: sum=%08b cout=%b g=%08b p=%08b c=%08b",
                     expected_sum, expected_cout, expected_g, expected_p, expected_c);
            $display("Actual  : sum=%08b cout=%b g=%08b p=%08b c=%08b",
                     sum, cout, dut.g, dut.p, dut.c);

            if ((sum   === expected_sum)  &&
                (cout  === expected_cout) &&
                (dut.g === expected_g)    &&
                (dut.p === expected_p)    &&
                (dut.c === expected_c)) begin
                passed_tests = passed_tests + 1;
                $display("Result  : PASS");
            end else begin
                $display("Result  : FAIL");
                if (sum !== expected_sum)   $display("  Mismatch in sum");
                if (cout !== expected_cout) $display("  Mismatch in cout");
                if (dut.g !== expected_g)   $display("  Mismatch in g");
                if (dut.p !== expected_p)   $display("  Mismatch in p");
                if (dut.c !== expected_c)   $display("  Mismatch in c");
            end
        end
    endtask

    initial begin
        $dumpfile("CLA8_tb.vcd");
        $dumpvars(0, CLA8_tb);

        total_tests  = 0;
        passed_tests = 0;

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