
module adder8tb;
    reg  [7:0] a, b;
    reg        cin;
    wire [7:0] sum;
    wire       cout;

    adder8 uut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    integer i;
    reg [8:0] exp;

    task check;
        input [7:0] ta, tb;
        input       tcin;
        begin
            a = ta; b = tb; cin = tcin;
            #1;
            exp = a + b + cin;
            if (sum !== exp[7:0] || cout !== exp[8]) begin
                $display("FAIL adder8: a=%h b=%h cin=%b got sum=%h cout=%b exp sum=%h cout=%b",
                         a,b,cin,sum,cout,exp[7:0],exp[8]);
                $finish;
            end
        end
    endtask

    initial begin
        // Edge cases
        check(8'h00, 8'h00, 1'b0);
        check(8'h00, 8'h00, 1'b1);
        check(8'hFF, 8'h00, 1'b0);
        check(8'hFF, 8'h00, 1'b1);
        check(8'hFF, 8'hFF, 1'b0);
        check(8'hFF, 8'hFF, 1'b1);
        check(8'h80, 8'h80, 1'b0);
        check(8'h7F, 8'h01, 1'b0);

        // Deterministic sweep
        for (i = 0; i < 1000; i = i + 1) begin
            check((i*37) & 8'hFF, (i*91) & 8'hFF, i[0]);
        end

        $display("passed!");
        $finish;
    end
endmodule
