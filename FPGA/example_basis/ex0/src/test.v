// 南京邮电大学电子竞赛训练fpga部分
//按键控制LED实验-by 郝学元 598199570@qq.com
module test(led1,led2,key1, key2);

output  led1,led2;
input  key1, key2;

assign led1=~key2;
assign led2=~key1;


endmodule
