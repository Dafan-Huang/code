// 南京邮电大学电子竞赛训练fpga部分
// 数码管动态扫描实验-by 郝学元 598199570@qq.com
//按键响应实验
module test(clk,Wx,display, led1,led2,key1, key2);
output reg [3:0] Wx;
output reg [6:0] display;
output  led1,led2;
input clk, key1, key2;
//定义常量
parameter zero =7'b1000000; //'0'
parameter one =7'b1111001; //'1'
parameter two =7'b0100100; //'2'
parameter three =7'b0110000; //'3'
parameter four =7'b0011001; //'4'
parameter five =7'b0010010; //'5'
parameter six =7'b0000010; //'6'
parameter seven =7'b1111000; //'7'
parameter eight =7'b0000000; //'8'
parameter nine =7'b0010000; //'9'

wire clk_1hz;//分频以后的时钟信号
reg [31:0]cnt;//计数分频
reg [1:0]cnt1;//计数
wire [1:0]sel;//数码管位数选择


//分频时钟分频
always @(posedge clk) 
begin 
cnt = cnt + 1;
end

assign clk_1hz=cnt[23];//27M/2^24=clk_1hz is 1.6hz
//计数
always @(posedge clk_1hz) 
begin 
cnt1 = cnt1 + 1;
end

assign sel=cnt1;
 
always @(posedge clk_1hz) 
begin 
            if (sel==0)
            begin
            Wx[0]=0;
            Wx[1]=1;
            Wx[2]=1;
            Wx[3]=1;
            display=eight;
           // display=zero;
            end
            else if (sel==1)
            begin
            Wx[0]=1;
            Wx[1]=0;
            Wx[2]=1;
            Wx[3]=1;
            display=eight;
            //display=one;
            end

            else if (sel==2)
            begin
            Wx[0]=1;
            Wx[1]=1;
            Wx[2]=0;
            Wx[3]=1;
            display=eight;
           // display=two;
            end

            else if (sel==3)
            begin
            Wx[0]=1;
            Wx[1]=1;
            Wx[2]=1;
            Wx[3]=0;
            display=eight;
           // display=three;

            end

end

assign led1=~key2;
assign led2=~key1;


endmodule
