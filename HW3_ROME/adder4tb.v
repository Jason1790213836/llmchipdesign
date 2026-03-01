
module adder4tb;
    reg  [3:0] a, b;
    reg        cin;
    wire [3:0] sum;
    wire       cout;

    adder4 uut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    integer ia, ib, ic;
    reg [4:0] exp;

    initial begin
        for (ia = 0; ia < 16; ia = ia + 1) begin
            for (ib = 0; ib < 16; ib = ib + 1) begin
                for (ic = 0; ic < 2; ic = ic + 1) begin
                    a = ia[3:0];
                    b = ib[3:0];
                    cin = ic[0];
                    #1;
                    exp = a + b + cin;
                    if (sum !== exp[3:0] || cout !== exp[4]) begin
                        $display("FAIL adder4: a=%h b=%h cin=%b got sum=%h cout=%b exp sum=%h cout=%b",
                                 a,b,cin,sum,cout,exp[3:0],exp[4]);
                        $finish;
                    end
                end
            end
        end
        $display("passed!");
        $finish;
    end
endmodule
