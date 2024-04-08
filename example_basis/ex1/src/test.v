// 南京邮电大学-电子竞赛训练fpga部分
// 蜂鸣器实验-by 郝学元
//按键控制蜂鸣器，实现特定音调
module test(clk,led1,led2,buzz,key1, key2);
input clk, key1, key2;
output reg buzz;
output  led1,led2;

//定义变量
reg [15:0]cnt;//计数分频

//分频时钟分频
always @(posedge clk) 
begin 
cnt = cnt + 1;
end


//通过key1和key2，改变蜂鸣器的频率值，蜂鸣器的音调会改变

always @(key1,key2,cnt) 
begin 

buzz=cnt[11];

//if ((key1==0)&& (key2==0))
//buzz=cnt[11];
//else if ((key1==1)&& (key2==0))
//buzz=cnt[12];
//else if ((key1==0)&& (key2==1))
//buzz=cnt[13];
//else if ((key1==1)&& (key2==1))
//buzz=cnt[14];


end





assign led1=~key2;
assign led2=~key1;


endmodule
