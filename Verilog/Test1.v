`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    13:40:21 11/04/2024 
// Design Name: 
// Module Name:    zhizhang 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module zhizhang(
    input           clk_6M,          // 6MHz系统时钟
    input           square,          // 待测方波信号
    input           reset_n,          // 复位信号   //加个按键消抖
	 
    output reg [1:0] SEL,            // 数码管选择器
    output reg [7:0] SEG             // 数码管段选信号
);

// 频率计模块定义
parameter GATE_TIME = 28'd6_000_000 - 1; // 闸门时间为1s

reg square_r0 = 1'b0;      // 方波信号的寄存器
reg square_r1 = 1'b0;
reg square_r2 = 1'b0;
reg square_r3 = 1'b0;

reg [27:0] cnt1 = 28'd0;   // 产生 1s 的闸门信号的计数器
reg gate = 1'b0;           // 闸门信号
reg gatebuf = 1'b0;        // 与方波同步之后的闸门信号
reg gatebuf1 = 1'b0;       // 同步闸门信号延时一拍

reg [27:0] cnt2 = 28'd0;    // 计数系统时钟周期
reg [27:0] cnt2_r = 28'd0;
reg [27:0] cnt3 = 28'd0;
reg [27:0] cnt3_r = 28'd0;

wire square_pose, square_nege;
wire gate_start, gate_end;
wire [27:0] CNTCLK;        // 闸门内系统时钟周期计数
wire [27:0] CNTSQU;        // 闸门内待测方波时钟周期计数

wire [27:0] freq_x;        // 频率计数结果
reg [27:0] number;         // 纸张数目

// 二进制转BCD码模块定义
reg [7:0] data;           // 8位二进制数的值
reg [11:0] bcd_data;      // 3位十进制数的8421BCD值

parameter CNT_SHIFT_NUM = 7'd8;  // 由data的位宽决定这里是8
reg [6:0] cnt_shift;             // 移位判断计数器该值由data的位宽决定这里是6
reg [19:0] data_shift;           // 移位判断数据寄存器，由data和bcddata的位宽之和决定。
reg shift_flag;                  // 移位判断标志信号

// 数码管显示模块定义
parameter MCNT_1MS = 28'd6_000_000 / 10 - 1; // 1ms
parameter MCNT_SEL = 2 - 1;                  // 位选信号计数器

wire [7:0] Disp_Data;        // 显示数据
reg [27:0] cnt_1ms;          // 1ms计数器
reg [1:0] cnt_sel;           // 位选信号计数器
reg [1:0] encode_sel;        // 2-to-4编码器输出
reg [7:0] LUT_seg;           // 数码管段选信号
reg [3:0] data_temp;         // 临时存储数据   

//// 频率计模块 ////

// 使方波和6MHz时钟同步并捕捉待测方波的边沿
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n) begin
        square_r0 <= 1'b0;
        square_r1 <= 1'b0;
        square_r2 <= 1'b0;
        square_r3 <= 1'b0;
    end else begin
        square_r0 <= square;
        square_r1 <= square_r0;
        square_r2 <= square_r1;
        square_r3 <= square_r2;
    end
end

assign square_pose = square_r2 & ~square_r3;  // 捕捉方波的上升沿
assign square_nege = ~square_r2 & square_r3;  // 捕捉方波的下降沿

always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n) begin
        cnt1 <= 28'd0;
        gate <= 1'b0;
    end else if (cnt1 == GATE_TIME) begin
        cnt1 <= 28'd0;
        gate <= ~gate; // 产生 1s 的闸门信号
    end else begin
        cnt1 <= cnt1 + 1'b1;
    end
end

always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n) begin
        gatebuf <= 1'b0;
        gatebuf1 <= 1'b0;
    end else begin
        if (square_pose == 1'b1) begin // 上升沿时，开始同步
            gatebuf <= gate; // 使闸门信号与待测方波同步，保证一个闸门包含整数个方波周期
        end else begin
            gatebuf <= gatebuf;
        end
        gatebuf1 <= gatebuf; // 将同步之后的闸门信号打一拍，用于捕捉闸门信号的边沿
    end
end

assign gate_start = gatebuf & ~gatebuf1; // 表示闸门开始时刻
assign gate_end = ~gatebuf & gatebuf1;   // 闸门结束时刻

// 计数系统时钟周期
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n) begin
        cnt2 <= 28'd0;
        cnt2_r <= 28'd0;
        gatebuf1 <= 1'b0;
    end else begin
        if (gate_start == 1'b1) begin
            cnt2 <= 28'd1;
        end else if (gate_end == 1'b1) begin
            cnt2_r <= cnt2; // 将所得结果保存在cnt2_r中，并将计数器清零
            cnt2 <= 28'd0;
        end else if (gatebuf1 == 1'b1) begin // 在闸门内计数系统时钟周期
            cnt2 <= cnt2 + 1'b1;
        end
        gatebuf1 <= gatebuf; //同步更新gatebuf1
    end
end

// 计数待测方波周期数
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n) begin
        cnt3 <= 28'd0;
        cnt3_r <= 28'd0;
    end else begin
        if (gate_start == 1'b1) begin
            cnt3 <= 28'd0;
        end else if (gate_end == 1'b1) begin
            cnt3_r <= cnt3; // 将所得结果保存在cnt3_r中，并将计数器清零
            cnt3 <= 28'd0;
        end else if (gatebuf1 == 1'b1 && square_nege == 1'b1) begin // 在闸门内计数待测方波周期数(数闸门内方波的下降沿）
            cnt3 <= cnt3 + 1'b1;
        end
    end
end

assign CNTCLK = cnt2_r; // 将计数结果输出
assign CNTSQU = cnt3_r; // 将计数结果输出

assign freq_x = CNTSQU; 

//// 纸张数目判断模块 ////
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        number <= 8'd0;
    else
        if(freq_x < 50_000)
            number <= 8'd0;
        else if(freq_x >= 68_000 && freq_x < 98_000)
            number <= 8'd1;
        else if(freq_x >= 97_000 && freq_x < 170_000)
            number <= 8'd2;
        else if(freq_x >= 121_000 && freq_x < 131_000)
            number <= 8'd3;
        else if(freq_x >= 145_000 && freq_x < 155_000)
            number <= 8'd4;
        else if(freq_x >= 173_000 && freq_x < 183_000)
            number <= 8'd5;
        else if(freq_x >= 192_000 && freq_x < 202_000)
            number <= 8'd6;
        else if(freq_x >= 207_000 && freq_x < 216_000)
            number <= 8'd7;
        else if(freq_x >= 216_000 && freq_x < 226_000)
            number <= 8'd8;
        else if(freq_x >= 231_000 && freq_x < 241_000)
            number <= 8'd9;
        else if(freq_x >= 246_000 && freq_x < 256_000)
            number <= 8'd10;
        else if(freq_x >= 260_000 && freq_x < 270_000)
            number <= 8'd11;
        else if(freq_x >= 274_000 && freq_x < 284_000)
            number <= 8'd12;
        else if(freq_x >= 289_000 && freq_x < 299_000)
            number <= 8'd13;
        else if(freq_x >= 302_000 && freq_x < 312_000)
            number <= 8'd14;
        else if(freq_x >= 313_000 && freq_x < 323_000)
            number <= 8'd15;
        else if(freq_x >= 324_000 && freq_x < 334_000)
            number <= 8'd16;
        else if(freq_x >= 336_500 && freq_x < 341_500)
            number <= 8'd17;
        else if(freq_x >= 346_500 && freq_x < 351_500)
            number <= 8'd18;
        else if(freq_x >= 355_500 && freq_x < 360_500)
            number <= 8'd19;
        else if(freq_x >= 363_500 && freq_x < 368_500)
            number <= 8'd20;
        else if(freq_x >= 370_500 && freq_x < 375_500)
            number <= 8'd21;
        else if(freq_x >= 377_500 && freq_x < 382_500)
            number <= 8'd22;
        else if(freq_x >= 384_500 && freq_x < 389_500)
            number <= 8'd23;
        else if(freq_x >= 390_500 && freq_x < 395_500)
            number <= 8'd24;
        else if(freq_x >= 396_500 && freq_x < 401_500)
            number <= 8'd25;
        else if(freq_x >= 401_500 && freq_x < 406_500)
            number <= 8'd26;
        else if(freq_x >= 407_500 && freq_x < 412_500)
            number <= 8'd27;
        else if(freq_x >= 414_500 && freq_x < 419_500)
            number <= 8'd28;
        else if(freq_x >= 419_500 && freq_x < 424_500)
            number <= 8'd29;
        else if(freq_x >= 424_500 && freq_x < 440_000)
            number <= 8'd30;
        else 
            number <= 8'd0;
end

//// 二进制转BCD码模块 ////

// cnt_shift计数
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        cnt_shift <= 7'd0;
    else if ((cnt_shift == CNT_SHIFT_NUM + 1) && (shift_flag))
        cnt_shift <= 7'd0;
    else if (shift_flag)
        cnt_shift <= cnt_shift + 1'b1;
    else
        cnt_shift <= cnt_shift;
end

// 给data赋值
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        data <= 8'd0;
    else
        data <= number;
end

// data_shift 计数器为0时赋初值，计数器为1~CNT_SHIFT_NUM时进行移位操作
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        data_shift <= 20'd0;
    else if (cnt_shift == 7'd0)
        data_shift <= {14'b0, data};
    else if ((cnt_shift <= CNT_SHIFT_NUM) && (!shift_flag)) begin
        // Calculate the BCD value, each line corresponds to a different segment, preparing the entire number for BCD conversion.
        data_shift[11: 8] <= (data_shift[11: 8] > 4) ? (data_shift[11: 8] + 2'd3) : (data_shift[11: 8]);
        data_shift[15:12] <= (data_shift[15:12] > 4) ? (data_shift[15:12] + 2'd3) : (data_shift[15:12]);
        data_shift[19:16] <= (data_shift[19:16] > 4) ? (data_shift[19:16] + 2'd3) : (data_shift[19:16]);
    end else if ((cnt_shift <= CNT_SHIFT_NUM) && (shift_flag))
        // Move the data to the left by one bit if the shift_flag is high and the counter is less than or equal to CNT_SHIFT_NUM
        data_shift <= data_shift << 1;
    else
        data_shift <= data_shift;
end

// shift_flag 移位判断标志信号，用于控制移位判断的先后顺序
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        shift_flag <= 1'b0;
    else
        shift_flag <= ~shift_flag;
end

// 当计数器等于CNT_SHIFT_NUM时，移位判断操作完成，整体输出
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        bcd_data <= 12'd0;
    else if (cnt_shift == CNT_SHIFT_NUM + 1)
        bcd_data <= data_shift[19:8];
    else
        bcd_data <= bcd_data;
end

assign Disp_Data = bcd_data[7:0];

//// 显示模块 ////

// 1ms Counter
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        cnt_1ms <= 0;
    else if (cnt_1ms == MCNT_1MS)
        cnt_1ms <= 0;
    else
        cnt_1ms <= cnt_1ms + 1'b1;
end

// Digit Selection Counter
always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        cnt_sel <= 0;
    else if (cnt_1ms == MCNT_1MS) begin
        if (cnt_sel == MCNT_SEL)
            cnt_sel <= 0;
        else
            cnt_sel <= cnt_sel + 1'b1;
    end
end

// 2-to-4 Decoder
always @(*) begin
    case (cnt_sel)
        2'b00: encode_sel = 2'b01; // Select first digit
        2'b01: encode_sel = 2'b10; // Select second digit
    endcase
end

always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        SEL <= 0;
    else
        SEL <= encode_sel;
end

// Segment Selection
always @(*) begin
    case (cnt_sel)
        2'b00: data_temp = Disp_Data[3:0]; //个位
        2'b01: data_temp = Disp_Data[7:4]; //十位
    endcase
end

// Segment Encoding
always @(*) begin
    case (data_temp)
        0  : LUT_seg = 8'h3f; // 0
        1  : LUT_seg = 8'h06; // 1
        2  : LUT_seg = 8'h5b; // 2
        3  : LUT_seg = 8'h4f; // 3
        4  : LUT_seg = 8'h66; // 4
        5  : LUT_seg = 8'h6d; // 5
        6  : LUT_seg = 8'h7d; // 6
        7  : LUT_seg = 8'h07; // 7
        8  : LUT_seg = 8'h7f; // 8
        9  : LUT_seg = 8'h6f; // 9
        default: LUT_seg = 8'hff; // Off
    endcase
end

always @(posedge clk_6M or negedge reset_n) begin
    if (!reset_n)
        SEG <= 0;
    else
        SEG <= LUT_seg;
end

endmodule


// Testbench
// `timescale 1ns / 1ps

// module zhizhang_tb;

//     // Inputs
//     reg clk_6M;
//     reg square;
//     reg reset_n;

//     // Outputs
//     wire [1:0] SEL;
//     wire [7:0] SEG;

//     // Instantiate the Unit Under Test (UUT)
//     zhizhang uut (
//         .clk_6M(clk_6M), 
//         .square(square), 
//         .reset_n(reset_n), 
//         .SEL(SEL), 
//         .SEG(SEG)
//     );

//     initial begin
//         // Initialize Inputs
//         clk_6M = 0;
//         square = 0;
//         reset_n = 0;

//         // Wait 100 ns for global reset to finish
//         #100;
//         reset_n = 1;

//         // Add stimulus here
//         #200 square = 1;
//         #200 square = 0;
//         #200 square = 1;
//         #200 square = 0;
//         #200 square = 1;
//         #200 square = 0;
//     end

//     // Clock generation
//     always #83.333 clk_6M = ~clk_6M; // 6MHz clock
    
//     //square wave generation
//     always #2320 square = ~square;
// endmodule