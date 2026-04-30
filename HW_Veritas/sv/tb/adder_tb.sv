`timescale 1ns/1ps

module tb;
       parameter N=4;
       logic clk;
       logic rst_n;
       logic si;
       logic [N-1:0]q;

       sipo dut(
        .clk(clk),
        .rst_n(rst_n),
        .si(si),
        .q(q)
       ); 
        
        initial clk=0;
        always #5 clk=~clk;
        task automatic apply_tb  (input logic si_i,input logic [N-1]expected) 
        begin
            @(negedge clk);
            si=si_i;
            @(posedge clk);
            #1;
            if({q!=expected)begin
                $display("@@@FAIL");
                $finish;
            end
        end 
        endtask

        initial begin
            rst_n=0;
            si=0;
            repeat (2) @(posedge clk);
            rst_n=1;
            apply_tb(1,4'b0001);
            $finish;
        end
       

endmodule