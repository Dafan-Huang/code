module div_fsm#(
    parameter   DATAWIDTH = 10'd8                   // 数据宽度
)
(
    input                         clk,              // 时钟信号
    input                         rst_n,            // 复位信号
    input                         en,               // 使能信号
    input     [DATAWIDTH-1:0]     dividend,         // 被除数
    input     [DATAWIDTH-1:0]     divisor,          // 除数
    
    output                        ready,            // 准备信号
    output    [DATAWIDTH-1:0]     quotient,         // 商
    output    [DATAWIDTH-1:0]     remainder,        // 余数
    output                        vld_out           // 有效信号
);
//localparam define             // 状态坤定义
localparam IDLE  = 2'b00;       // 空闲状态
localparam SUB   = 2'b01;       // 减法
localparam SHIFT = 2'b10;       // 移位
localparam DONE  = 2'b11;       // 完成
//reg define
reg [DATAWIDTH * 2'd2 - 1'b1:0] dividend_e;         // 被除数
reg [DATAWIDTH * 2'd2 - 1'b1:0] divisor_e;          // 除数
reg [DATAWIDTH - 1'b1:0]        quotient_e;         // 商
reg [DATAWIDTH - 1'b1:0]        remainder_e;        // 余数
reg [1:0]                       current_state;      // 当前状态
reg [1:0]                       next_state;         // 下一个状态
reg [DATAWIDTH-1'b1:0]          count;              // 计数器

//*****************************************************
//**                    main code
//*****************************************************

// 赋值 
assign quotient  = quotient_e;                      //商
assign remainder = remainder_e;                     //余数

// 产生使能信号
assign ready = (current_state == IDLE) ? 1'b1 : 1'b0;
assign vld_out = (current_state == DONE) ? 1'b1 : 1'b0;

// 状态跳转
always@(posedge clk or negedge rst_n)begin
    if(!rst_n)
        current_state <= IDLE;
    else 
        current_state <= next_state;
end

always@(*)begin
    next_state <= 2'bx;
    case(current_state)
        IDLE: begin
            if(en)
                next_state <=  SUB;
            else
                next_state <=  IDLE;
        end
        SUB: next_state <= SHIFT;
        SHIFT: begin
            if(count<DATAWIDTH) 
                next_state <= SUB;
            else 
                next_state <= DONE;
        end
        DONE: next_state <= IDLE;
        default: next_state <= IDLE;
    endcase
end

always@(posedge clk or negedge rst_n) begin
    if(!rst_n) begin
        dividend_e  <= 1'b0;
        divisor_e   <= 1'b0;
        quotient_e  <= 1'b0;
        remainder_e <= 1'b0;
        count       <= 1'b0;
    end else begin
        case(current_state)
            IDLE:begin
                // Zero padding for dividend and divisor       // 为被除数和除数补零
                dividend_e <= {{DATAWIDTH{1'b0}}, dividend};
                divisor_e  <= {divisor, {DATAWIDTH{1'b0}}};
            end
            SUB:begin
                // Subtract divisor from dividend                              // 从被除数中减去除数         
                if(dividend_e >= divisor_e) begin
                    // Quotient bit is 1, then subtract divisor from dividend  // 商位为1，从被除数中减去除数
                    quotient_e <= {quotient_e[DATAWIDTH-2'd2:0], 1'b1};        // 商 
                    dividend_e <= dividend_e - divisor_e;                      // 被除数
                end else begin
                    // Quotient bit is 0, then shift quotient to left by 1     // 商位为0，将商左移1位
                    quotient_e <= {quotient_e[DATAWIDTH-2'd2:0], 1'b0};        // 商 
                    dividend_e <= dividend_e;                                  // 被除数
                end
            end
            SHIFT:begin                                                        // 移位 
                // Shift dividend to left by 1                                 // 将被除数左移1位
                if(count < DATAWIDTH) begin                                    // 计数器小于数据宽度         
                    // Shift dividend to left by 1                             
                    dividend_e <= (dividend_e << 1'b1);                        // 被除数左移1位
                    count      <= count + 1'b1;                                // 计数器加1
                end else begin
                    // Shift dividend to left by 1
                    remainder_e <= dividend_e[DATAWIDTH*2-1:DATAWIDTH];        // 余数
                end
            end
            DONE:begin
                count <= 1'b0; // 计数器清零                                   
            end    
        endcase
    end
end

endmodule