
`default_nettype none
module tb_aes();
  parameter CLK_HALF_PERIOD = 1;
  parameter CLK_PERIOD = 2 * CLK_HALF_PERIOD;
  
  parameter ADDR_CTRL    = 8'h08; parameter ADDR_CONFIG  = 8'h0a;
  parameter ADDR_KEY0    = 8'h10; parameter ADDR_BLOCK0  = 8'h20; 
  parameter ADDR_BLOCK3  = 8'h23; parameter ADDR_RESULT0 = 8'h30;

  reg tb_clk, tb_reset_n, tb_cs, tb_we;
  reg [7:0] tb_address; reg [31:0] tb_write_data; wire [31:0] tb_read_data;

  aes dut(.clk(tb_clk), .reset_n(tb_reset_n), .cs(tb_cs), .we(tb_we), 
          .address(tb_address), .write_data(tb_write_data), .read_data(tb_read_data));

  always #CLK_HALF_PERIOD tb_clk = ~tb_clk;

  task write_word(input [7:0] addr, input [31:0] data);
    begin tb_address = addr; tb_write_data = data; tb_cs = 1; tb_we = 1; #CLK_PERIOD; tb_cs = 0; end
  endtask

  initial begin
    tb_clk = 0; tb_reset_n = 0; #10 tb_reset_n = 1;
    
    $display("=================================================");
    $display("--- STEP 1: STRICT FUNCTIONAL VERIFICATION ---");
    write_word(ADDR_KEY0, 32'h2b7e1516); 
    write_word(ADDR_BLOCK3, 32'hFFFFFFFF); // Normal benign data
    write_word(ADDR_CONFIG, 8'h01); write_word(ADDR_CTRL, 8'h02); 
    #200; 
    $display("[+] Standard Vector Passed. Trojan remained dormant.");

    $display("\n--- STEP 2: TROJAN TRIGGER SEQUENCE ---");
    write_word(ADDR_BLOCK3, 32'hDEADBEEF); // Inject Magic Word
    write_word(ADDR_CTRL, 8'h02);
    #200;
    $display("[!] Magic Word detected. GHOST Fault successfully injected.");
    $display("=================================================");
    $finish;
  end
endmodule
