`timescale 1ns/1ps
`define OK 12
`define INCORRECT 13

// Golden reference model for shift_register
// Assumes DUT behavior: on posedge clk,
//   if (!reset_n) data_out <= 8'b0;
//   else if (shift_enable) data_out <= {data_out[6:0], data_in};
//   else hold state.
module reference_module (
    input  logic       clk,
    input  logic       reset_n,
    input  logic       data_in,
    input  logic       shift_enable,
    output logic [7:0] data_out
);
    always_ff @(posedge clk) begin
        if (!reset_n)
            data_out <= 8'b0;
        else if (shift_enable)
            data_out <= {data_out[6:0], data_in};
    end
endmodule


// Stimulus generator: drives inputs (same patterns as your original TB)
module stimulus_gen (
    input  logic clk,
    output logic reset_n,
    output logic data_in,
    output logic shift_enable
);
    logic [7:0]  test_case_reset_n      = 8'b0011_1111;
    logic [7:0]  test_case_data_in      = 8'b0101_0100;
    logic [7:0]  test_case_shift_enable = 8'b0011_1010;

    int i;

    initial begin
        reset_n      = 1'b1;
        data_in      = 1'b0;
        shift_enable = 1'b0;

        // Drive 7 cycles of stimulus, sampled by tb at posedge clk
        for (i = 0; i < 7; i++) begin
            reset_n      <= test_case_reset_n[i];
            data_in      <= test_case_data_in[i];
            shift_enable <= test_case_shift_enable[i];
            @(posedge clk);
        end

        #1 $finish;
    end
endmodule


module tb;

    typedef struct packed {
        int errors;
        int errortime;

        int errors_data_out;
        int errortime_data_out;

        int clocks;
    } stats_t;

    stats_t stats1;

    logic clk = 1'b0;
    always #5 clk = ~clk;

    // DUT + REF signals
    logic       reset_n;
    logic       data_in;
    logic       shift_enable;
    logic [7:0] data_out_ref;
    logic [7:0] data_out_dut;

    // Instantiate stimulus
    stimulus_gen stim1 (
        .clk(clk),
        .reset_n(reset_n),
        .data_in(data_in),
        .shift_enable(shift_enable)
    );

    // Golden reference
    reference_module good1 (
        .clk(clk),
        .reset_n(reset_n),
        .data_in(data_in),
        .shift_enable(shift_enable),
        .data_out(data_out_ref)
    );

    // DUT
    shift_register dut (
        .clk(clk),
        .reset_n(reset_n),
        .data_in(data_in),
        .shift_enable(shift_enable),
        .data_out(data_out_dut)
    );

    // Dump waves
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, tb);
    end

    // Verification: X-safe compare (X in REF treated as don't-care, X in DUT counts as mismatch)
    wire tb_match;
    wire tb_mismatch = ~tb_match;

    assign tb_match = ( {data_out_ref} === ( {data_out_ref} ^ {data_out_dut} ^ {data_out_ref} ) );

    // Sample/check each edge, like the AutoChip-style TB
    always @(posedge clk or negedge clk) begin
        stats1.clocks++;

        if (!tb_match) begin
            if (stats1.errors == 0) stats1.errortime = $time;
            stats1.errors++;
        end

        if (data_out_ref !== (data_out_ref ^ data_out_dut ^ data_out_ref)) begin
            if (stats1.errors_data_out == 0) stats1.errortime_data_out = $time;
            stats1.errors_data_out++;
        end
    end

    final begin
        if (stats1.errors_data_out)
            $display("Hint: Output '%s' has %0d mismatches. First mismatch occurred at time %0d.",
                     "data_out", stats1.errors_data_out, stats1.errortime_data_out);
        else
            $display("Hint: Output '%s' has no mismatches.", "data_out");

        $display("Hint: Total mismatched samples is %0d out of %0d samples\n", stats1.errors, stats1.clocks);
        $display("Simulation finished at %0d ns", $time);
        $display("Mismatches: %0d in %0d samples", stats1.errors, stats1.clocks);
    end

endmodule
