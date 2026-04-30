`timescale 1ns/1ps

module CLA8_tb;

    reg  [7:0] a;
    reg  [7:0] b;
    wire [7:0] sum;
    wire       cout;

    reg  [8:0] expected;
    integer i, j;
    integer errors;

    // DUT
    CLA8 dut (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );

    task run_test;
        input [7:0] ta;
        input [7:0] tb;
        begin
            a = ta;
            b = tb;
            #1;
            expected = ta + tb;

            if ({cout, sum} !== expected) begin
                $display("@@@FAIL a=%h b=%h | got cout,sum=%b_%h | expected=%h",
                         ta, tb, cout, sum, expected);
                errors = errors + 1;
            end
            else begin
                $display("@@@PASS a=%h b=%h | result=%h",
                         ta, tb, {cout, sum});
            end
        end
    endtask

    initial begin
        errors = 0;

        // Directed tests
        run_test(8'h00, 8'h00);
        run_test(8'h01, 8'h01);
        run_test(8'h0F, 8'h01);
        run_test(8'h0A, 8'h05);
        run_test(8'h0F, 8'h0F);
        run_test(8'h10, 8'h10);
        run_test(8'h55, 8'hAA);
        run_test(8'h7F, 8'h01);
        run_test(8'h80, 8'h80);
        run_test(8'hFF, 8'h00);
        run_test(8'hFF, 8'h01);
        run_test(8'hFF, 8'hFF);

        // Small sweep
        for (i = 0; i < 16; i = i + 1) begin
            for (j = 0; j < 16; j = j + 1) begin
                run_test(i[7:0], j[7:0]);
            end
        end

        // Random tests
        for (i = 0; i < 200; i = i + 1) begin
            run_test($random, $random);
        end

        if (errors == 0) begin
            $display("\n@@@PASS: ALL TESTS PASSED");
        end
        else begin
            $display("\n@@@FAIL: %0d TESTS FAILED", errors);
        end

        $finish;
    end

endmodule