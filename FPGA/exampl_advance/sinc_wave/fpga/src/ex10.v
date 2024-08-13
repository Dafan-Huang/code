module  ex10
(
input sys_clk_i,
input uart0_rxd_i,
output uart0_txd_o,
input reset_n_i

);


 wire [15:0] gpioin;
 wire [15:0] gpioout;
 wire [15:0] gpioouten;
	Gowin_EMPU_Top your_instance_name(
		.sys_clk(sys_clk_i), //input sys_clk
		.gpioin(gpioin_i), //input [15:0] gpioin
		.gpioout(gpioout_o), //output [15:0] gpioout
		.gpioouten(gpioouten_o), //output [15:0] gpioouten
		.uart0_rxd(uart0_rxd_i), //input uart0_rxd
		.uart0_txd(uart0_txd_o), //output uart0_txd
		.reset_n(reset_n_i) //input reset_n
	);
endmodule


 