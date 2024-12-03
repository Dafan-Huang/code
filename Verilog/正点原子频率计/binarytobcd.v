module binary2bcd(
    input   wire             sys_clk,       //时钟信号
    input   wire             sys_rst_n,     //复位信号
    input   wire    [7:0]   data,          //8位二进制数的值
    
    output  reg     [11:0]   bcd_data       //3位十进制数的BCD值
);
//parameter define
parameter   CNT_SHIFT_NUM = 7'd8;  //由data的位宽决定这里是8
//reg define
reg [6:0]       cnt_shift;         //移位判断计数器该值由data的位宽决定这里是6
reg [19:0]      data_shift;        //移位判断数据寄存器，由data和bcddata的位宽之和决定。
reg             shift_flag;        //移位判断标志信号


//cnt_shift计数
always@(posedge sys_clk or negedge sys_rst_n)begin
    if(!sys_rst_n)
        cnt_shift <= 7'd0;
    else if((cnt_shift == CNT_SHIFT_NUM + 1) && (shift_flag))
        cnt_shift <= 7'd0;
    else if(shift_flag)
        cnt_shift <= cnt_shift + 1'b1;
    else
        cnt_shift <= cnt_shift;
end

//data_shift 计数器为0时赋初值，计数器为1~CNT_SHIFT_NUM时进行移位操作
always@(posedge sys_clk or negedge sys_rst_n)begin
    if(!sys_rst_n)
        data_shift <= 20'd0;
    else if(cnt_shift == 7'd0)
        data_shift <= {12'b0,data};
    else if((cnt_shift <= CNT_SHIFT_NUM)&&(!shift_flag))begin
        // Calculate the BCD value, each line corresponds to a different segment, preparing the entire number for BCD conversion.
        data_shift[11: 8] <= (data_shift[11: 8] > 4) ? (data_shift[11: 8] + 2'd3):(data_shift[11: 8]);
        data_shift[15:12] <= (data_shift[15:12] > 4) ? (data_shift[15:12] + 2'd3):(data_shift[15:12]);
        data_shift[19:16] <= (data_shift[19:16] > 4) ? (data_shift[19:16] + 2'd3):(data_shift[19:16]);
        end  
        else if((cnt_shift <= CNT_SHIFT_NUM)&&(shift_flag))
        // Move the data to the left by one bit if the shift_flag is high and the counter is less than or equal to CNT_SHIFT_NUM
        data_shift <= data_shift << 1;
    else
        data_shift <= data_shift;
end

//shift_flag 移位判断标志信号，用于控制移位判断的先后顺序
always@(posedge sys_clk or negedge sys_rst_n)begin
    if(!sys_rst_n)
        shift_flag <= 1'b0;
    else
        shift_flag <= ~shift_flag;
end

//当计数器等于CNT_SHIFT_NUM时，移位判断操作完成，整体输出
always@(posedge sys_clk or negedge sys_rst_n)begin
    if(!sys_rst_n)
        bcd_data <= 12'd0;
    else if(cnt_shift == CNT_SHIFT_NUM + 1)
        bcd_data <= data_shift[19:8];
    else
        bcd_data <= bcd_data;
end

endmodule
