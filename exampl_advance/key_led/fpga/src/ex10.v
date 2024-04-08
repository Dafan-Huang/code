module  ex10
(

input clk, key1,
output  led1,led2,led3,
output  led_en,
input sys_clk_i,
input uart0_rxd_i,
output uart0_txd_o,
input reset_n_i

);


 wire [15:0]gpioin_i;
 wire [15:0]gpioout_o;
 wire [15:0]gpioouten_o;
	Gowin_EMPU_Top your_instance_name(
		.sys_clk(sys_clk_i), //input sys_clk
		.gpioin({gpioin_i[15:4],key1,gpioin_i[3:0]}), //input [15:0] gpioin
		.gpioout(gpioout_o), //output [15:0] gpioout
		.gpioouten(gpioouten_o), //output [15:0] gpioouten
		.uart0_rxd(uart0_rxd_i), //input uart0_rxd
		.uart0_txd(uart0_txd_o), //output uart0_txd
		.reset_n(reset_n_i) //input reset_n
	);

assign  led1=gpioout_o[0];
assign  led2=gpioout_o[1];
assign  led3=gpioout_o[2];
assign  led_en=0;


endmodule


 