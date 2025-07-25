module top_cymometer#(
    //parameter define
    // parameter       DIV_N        = 26'd10_000_000   ,   // 分频系数

    parameter       CNT_GATE_MAX = 28'd75_000_000   ,   // 测频周期时间为1.5s  
    parameter       CNT_GATE_LOW = 28'd12_500_000   ,   // 闸门为低的时间0.25s
    parameter       CNT_TIME_MAX = 28'd80_000_000   ,   // 测频周期时间为1.6s
    parameter       CLK_FS_FREQ  = 28'd100_000_000  ,
    parameter       DATAWIDTH    = 8'd57
)(
    input              sys_clk    ,             // 时钟信号
    input              sys_rst_n  ,             // 复位信号
    input              clk_fx     ,             // 被测时钟

);
//wire define
wire    [29:0]       data_fx;        // 被测信号测量值       
wire                 clk_fs;

wire        en;             

wire [56:0] dividend;       
wire [56:0] divisor;        

wire        ready;          
wire [56:0] quotient;       
wire [56:0] remainder;     
wire        vld_out;        

//*****************************************************
//**                    main code
//*****************************************************

// 产生基准时钟100M
pll_100m u_pll_100m(
    .clk_out1       (clk_fs     ),      // 基准时钟，100M
    .clk_out2       (clk_out2  ),      // 50M以上被测信号
    .reset          (~sys_rst_n ),      // 复位信号
    .clk_in1        (sys_clk    )
);

//例化等精度频率计模块 
cymometer#(
    .CNT_GATE_MAX   (CNT_GATE_MAX),      // 测频周期时间为1.5s  
    .CNT_GATE_LOW   (CNT_GATE_LOW),      // 闸门为低的时间0.25s
    .CNT_TIME_MAX   (CNT_TIME_MAX),
    .CLK_FS_FREQ    (CLK_FS_FREQ )
)
u_cymometer(
    .sys_clk        (sys_clk    ),       // 系统时钟，50M
    .clk_fs         (clk_fs     ),       // 基准时钟，100M
    .sys_rst_n      (sys_rst_n  ),       // 系统复位，低电平有效
    .clk_fx         (clk_fx     ),       // 被测时钟信号
    .data_fx        (data_fx    ),       // 被测时钟频率值
    .dividend       (dividend   ),       
    .divisor        (divisor    ),       
    .en             (en         ),    
    .ready          (ready      ),       
    .quotient       (quotient   ),       
    .remainder      (remainder  ),       
    .vld_out        (vld_out    )        
    
);

//除法器模块
div_fsm
#(
    .DATAWIDTH      (DATAWIDTH  )
)
u_div_fsm(
    .clk            (sys_clk    ),      
    .rst_n          (sys_rst_n  ),      
    .en             (en         ),      

    .dividend       (dividend   ),      
    .divisor        (divisor    ),      

    .ready          (ready      ),      
    .quotient       (quotient   ),      
    .remainder      (remainder  ),      
    .vld_out        (vld_out    )       
);

//例化数码管显示模块


endmodule
