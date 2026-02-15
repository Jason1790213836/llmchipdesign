
module shift_register(
         input logic clk,
         input logic reset_n,
         input logic data_in,
         input logic shift_enable, 
         output logic [7:0] data_out

);


always_ff @(posedge clk)begin

if(!reset_n)begin
    data_out<=8'b0;
end else if (shift_enable)begin
    data_out<={data_out[6:0],data_in};
end

end
endmodule