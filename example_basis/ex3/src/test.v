// 南京邮电大学-电子竞赛训练fpga部分
// PWM实验，滤波后产生可调的直流信号-by 郝学元

module test(clk,led1,led2,PWM0,PWM1,key1, key2);
input clk, key1, key2;
output reg PWM0;
output PWM1;
output  led1,led2;

//定义变量
reg [7:0]cnt;//计数分频

//分频时钟分频
always @(posedge clk)//clk 2
begin 
cnt = cnt + 1;
end
//通过key1和key2，改变PWM的占空比
wire [1:0]sel={key2,key1};

always @(*) 
begin 
case(sel)
2'b00:begin
PWM0=(cnt<10)?1:0;
end
2'b01:begin
PWM0=(cnt<50)?1:0;
end
2'b10:begin
PWM0=(cnt<100)?1:0;
end
2'b11:begin
PWM0=(cnt<200)?1:0;
end
default:begin
PWM0=(cnt<128)?1:0;
end
endcase

end

assign PWM1=~PWM0;
assign led1=~key2;
assign led2=~key1;


endmodule
