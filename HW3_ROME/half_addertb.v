
module half_addertb;
    reg a, b;
    wire sum, carry;

    half_adder uut (.a(a), .b(b), .sum(sum), .carry(carry));

    integer i;
    reg exp_sum, exp_carry;

    initial begin
        for (i = 0; i < 4; i = i + 1) begin
            {a,b} = i[1:0]; #1;
            exp_sum = a ^ b;
            exp_carry = a & b;
            if (sum !== exp_sum || carry !== exp_carry) begin
                $display("FAIL half_adder: a=%b b=%b got sum=%b carry=%b exp sum=%b carry=%b",
                         a,b,sum,carry,exp_sum,exp_carry);
                $finish;
            end
        end
        $display("passed!");
        $finish;
    end
endmodule
