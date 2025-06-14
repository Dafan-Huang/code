// 南京邮电大学-电子竞赛训练fpga部分
// 蜂鸣器实验-by 郝学元
//按键控制蜂鸣器，实现特定音调
module test(clk,led1,led2,buzz,key1, key2);
input clk, key1, key2;
output reg buzz;
output  led1,led2;

//定义音符时序周期数
localparam			M0 	= 98800,
M1	= 95600,
M2	= 85150,
M3	= 75850,
M4	= 71600,
M5  = 63750,
M6	= 56800,
M7	= 50600;
//信号定义
reg		[16:0]		cnt0		;	//计数每个音符对应的时序周期
reg		[10:0]		cnt1		;	//计数每个音符重复次数
reg		[5 :0]		cnt2		;	//计数曲谱中音符个数
reg		[16:0]		pre_set		;	//预装载值
wire	[16:0]		pre_div		;	//占空比
reg		[10:0]		cishu		;	//定义不同音符重复不同次数
wire	[10:0]		cishu_div	;	//音符重复次数占空比
reg 				flag		;	//歌曲种类标志：0小星星，1两只老虎
reg		[5 :0]		YINFU		;	//定义曲谱中音符个数
//歌曲种类标志位
always @(posedge clk or negedge rst_n) begin
if(!rst_n) begin
flag <= 1'b0;
end
else if(press) begin
flag <= ~flag;
end
end
//重设音符的个数
always @(posedge clk or negedge rst_n) begin
if(!rst_n)
YINFU <= 48;
else if(flag == 1'b1)
YINFU <= 36;
else
YINFU <= 48;
end
//计数每个音符的周期，也就是表示音符的一个周期
always @(posedge clk or negedge rst_n) begin
if(!rst_n) begin
cnt0 <= 0;
end
else if(press)
cnt0 <= 0;
else begin
if(cnt0 == pre_set - 1)
cnt0 <= 0;
else
cnt0 <= cnt0 + 1;
end
end
//计数每个音符重复次数，也就是表示一个音符的响鸣持续时长
always @(posedge clk or negedge rst_n) begin
if(!rst_n) begin
cnt1 <= 0;
end
else if(press)
cnt1 <= 0;
else begin
if(cnt0 == pre_set - 1)begin
if(cnt1 == cishu)
cnt1 <= 0;
else
cnt1 <= cnt1 + 1;
end
end
end
//计数有多少个音符，也就是曲谱中有共多少个音符
always @(posedge clk or negedge rst_n) begin
if(!rst_n) begin
cnt2 <= 0;
end
else if(press)
cnt2 <= 0;
else begin
if(cnt1 == cishu && cnt0 == pre_set - 1) begin
if(cnt2 == YINFU - 1) begin
cnt2 <= 0;
end
else
cnt2 <= cnt2 + 1;
end
end
end
//定义音符重复次数
always @(*) begin
case(pre_set)
M0:cishu = 242;
M1:cishu = 250;
M2:cishu = 281;
M3:cishu = 315;
M4:cishu = 334;
M5:cishu = 375;
M6:cishu = 421;
M7:cishu = 472;
endcase
end

//曲谱定义
always @(*) begin
begin
case(cnt2)	//小星星歌谱
0 : pre_set = M1;
1 : pre_set = M1;
2 : pre_set = M5;
3 : pre_set = M5;
4 : pre_set = M6;
5 : pre_set = M6;
6 : pre_set = M5;
7 : pre_set = M0;
8 : pre_set = M4;
9 : pre_set = M4;
10: pre_set = M3;
11: pre_set = M3;
12: pre_set = M2;
13: pre_set = M2;
14: pre_set = M1;
15: pre_set = M0;
16: pre_set = M5;
17: pre_set = M5;
18: pre_set = M4;
19: pre_set = M4;
20: pre_set = M3;
21: pre_set = M3;
22: pre_set = M2;
23: pre_set = M0;
24: pre_set = M5;
25: pre_set = M5;
26: pre_set = M4;
27: pre_set = M4;
28: pre_set = M3;
29: pre_set = M3;
30: pre_set = M2;
31: pre_set = M0;
32: pre_set = M1;
33: pre_set = M1;
34: pre_set = M5;
35: pre_set = M5;
36: pre_set = M6;
37: pre_set = M6;
38: pre_set = M5;
39: pre_set = M0;
40: pre_set = M4;
41: pre_set = M4;
42: pre_set = M3;
43: pre_set = M3;
44: pre_set = M2;
45: pre_set = M2;
46: pre_set = M1;
47: pre_set = M0;
endcase
end

end





assign led1=~key2;
assign led2=~key1;


endmodule
