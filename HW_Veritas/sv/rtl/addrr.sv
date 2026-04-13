`include ”fsm˙pkg.svh”
import fsm10˙pkg::*;
module fsm(
input logic rst_n, // asynchronous active-low reset
input logic clk,
input logic jmp,
input logic go,
output logic y,
output state_e state
);
state_e next_state;

    always_ff @(posedge clk or negedge rst_n)begin
        if(!rst_n)begin
            state<=S0;

        end else begin
            state<=next_state;
        end
    end
    assign y=(state==S3);
    always_comb begin
        next_state=S0;
        case(state)
            S0: begin
                if(!go) next_state=S0;
                else if (go&&!jump)next_state=S1;
                else if (go&&jump)begin
                next_state=S3;
                y=1;
                end
            end
            S1: begin
            
                if (!jump)next_state=S2;
                else if (jump)begin
                next_state=S3;
                end
            end
            S2: begin
                next_state=S3;
            end
            S3: begin
                if (!jump)begin 
                    next_state=S4;
                end
            end
            S4: begin
                if (!jump)begin 
                    next_state=S5;
                end else if (jump)begin
                    next_state=S3;
                end
            end
            S5: begin
                if (!jump)begin 
                    next_state=S6;

                end else if (jump)begin
                next_state=S3;

                end
            end
            S6: begin
                if (!jump)begin 
                    next_state=S7;

                end else if (jump)begin
                next_state=S3;

                end
            end
            S7: begin
                if (!jump)begin 
                    next_state=S8;

                end else if (jump)begin
                next_state=S3;

                end
            end

            S8: begin
                if (!jump)begin 
                    next_state=S9;

                end else if (jump)begin
                next_state=S3;

                end
            end
            S9: begin
                if (!jump)begin 
                    next_state=S0;
 
                end else if (jump)begin
                next_state=S3;

                end
            end
            default:begin
                next_state=S0;

            end
        endcase
    end
// Implement the design
endmodule