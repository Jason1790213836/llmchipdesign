
module full_addertb;
    reg a, b, cin;
    wire sum, cout;

    full_adder uut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    integer i;
    reg [1:0] exp;

    initial begin
        for (i = 0; i < 8; i = i + 1) begin
            {a,b,cin} = i[2:0]; #1;
            exp = a + b + cin;
            if (sum !== exp[0] || cout !== exp[1]) begin
                $display("FAIL full_adder: a=%b b=%b cin=%b got sum=%b cout=%b exp sum=%b cout=%b",
                         a,b,cin,sum,cout,exp[0],exp[1]);
                $finish;
            end
        end
        $display("passed!");
        $finish;
    end
endmodule
