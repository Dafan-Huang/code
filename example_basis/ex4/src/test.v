// 南京邮电大学-电子竞赛训练fpga部分
// PWM实验，滤波后产生锯齿波，比照例程，可以产生正弦波信号-by 郝学元

module test(clk,led1,led2,PWM0,key1, key2);
input clk, key1, key2;
output  PWM0;
output  led1,led2;
//定义变量
reg [7:0]cnt;//计数分频

//分频时钟分频
always @(posedge clk)//clk 
begin 
cnt = cnt + 1;
end
reg [7:0]cnt2;
always @(posedge cnt[7])//clk 2
begin 
cnt2 = cnt2 + 1;
end
reg [7:0]cnt3;
always @(posedge cnt2[2])//clk 3
begin 
cnt3 = cnt3 + 1;
end

//产生51hz锯齿波
assign PWM0=(cnt>cnt3)?1:0;

assign led1=~key2;
assign led2=~key1;


endmodule
