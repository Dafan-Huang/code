module COMP_RE
(
input clk,
output  pwm1,
output  pwm2,
input A1,
input A2,
output  O1,
output  O2
);


assign pwm1=~clk;
assign pwm2=~clk;
assign O1=~A1;
assign O2=~A2;

endmodule

