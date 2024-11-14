module disp(
    Clk,                // 时钟信号
    Reset_n,            // 复位信号
    Disp_Data,          // 显示数据
    SEL,                // 数码管选择信号
    SEG                 // 数码管段选信号
);
    input Clk;
    input Reset_n;
    input [7:0] Disp_Data; // 8 bits for 2 digits  
    output reg [1:0] SEL;   // Only 2 digits
    output reg [7:0] SEG;
    
    parameter MCNT_1MS = 6000000 /20 - 1;      // 1ms
    parameter MCNT_SEL = 2 - 1; // 2 digits
    reg [15:0] cnt_1ms;
    reg [1:0] cnt_sel; // Change to 2-bit counter for 2 digits
    reg [1:0] encode_sel;
    reg [7:0] LUT_seg;
    reg [3:0] data_temp;

    // 1ms Counter
    always @(posedge Clk or negedge Reset_n) begin
        if (!Reset_n)
            cnt_1ms <= 0;
        else if (cnt_1ms == MCNT_1MS)
            cnt_1ms <= 0;
        else 
            cnt_1ms <= cnt_1ms + 1'b1;
    end

    // Digit Selection Counter
    always @(posedge Clk or negedge Reset_n) begin
        if (!Reset_n)
            cnt_sel <= 0;
        else if (cnt_1ms == MCNT_1MS) begin
            if (cnt_sel == MCNT_SEL)
                cnt_sel <= 0;
            else
                cnt_sel <= cnt_sel + 1'b1;
        end
    end

    // 2-to-4 Decoder    //24线选通器
    always @(*) begin
        case (cnt_sel)
            2'b00: encode_sel = 2'b01; // Select first digit
            2'b01: encode_sel = 2'b10; // Select second digit
        endcase
    end

    always @(posedge Clk or negedge Reset_n) begin  
        if (!Reset_n)
            SEL <= 0;
        else
            SEL <= encode_sel;
    end

    // Segment Selection   //段选信号
    always @(*) begin
        case (cnt_sel)
            2'b00: data_temp = Disp_Data[3:0]; // First digit   //前四位
            2'b01: data_temp = Disp_Data[7:4]; // Second digit  //后四位
        endcase
    end

    // Segment Encoding   //段译码
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
            4'ha: LUT_seg = 8'h77; // A
            4'hb: LUT_seg = 8'h7c; // b
            4'hc: LUT_seg = 8'h39; // C
            4'hd: LUT_seg = 8'h5e; // d
            4'he: LUT_seg = 8'h79; // E
            4'hf: LUT_seg = 8'h71; // F
            default: LUT_seg = 8'hff; // Off
        endcase
    end

    always @(posedge Clk or negedge Reset_n) begin  
        if (!Reset_n)
            SEG <= 0;
        else
            SEG <= LUT_seg;  
    end

endmodule



// module tb_disp;
//     reg Clk;
//     reg Reset_n;
//     reg [7:0] Disp_Data;
//     wire [1:0] SEL;
//     wire [7:0] SEG;

//     // Instantiate the disp module
//     disp uut (
//         .Clk(Clk),
//         .Reset_n(Reset_n),
//         .Disp_Data(Disp_Data),
//         .SEL(SEL),
//         .SEG(SEG)
//     );

//     // Clock generation
//     initial begin
//         Clk = 0;
//         forever #5 Clk = ~Clk; // 10ns period
//     end

//     // Test sequence
//     initial begin
//         // Initialize inputs
//         Reset_n = 0;
//         Disp_Data = 8'h00;

//         // Apply reset
//         #20;
//         Reset_n = 1;

//         // Display 0 to F
//         Disp_Data = 8'h00; #20;
//         Disp_Data = 8'h11; #20;
//         Disp_Data = 8'h22; #20;
//         Disp_Data = 8'h33; #20;
//         Disp_Data = 8'h44; #20;
//         Disp_Data = 8'h55; #20;
//         Disp_Data = 8'h66; #20;
//         Disp_Data = 8'h77; #20;
//         Disp_Data = 8'h88; #20;
//         Disp_Data = 8'h99; #20;
//         Disp_Data = 8'haa; #20;
//         Disp_Data = 8'hbb; #20;
//         Disp_Data = 8'hcc; #20;
//         Disp_Data = 8'hdd; #20;
//         Disp_Data = 8'hee; #20;
//         Disp_Data = 8'hff; #20;

//         // Finish simulation
//         $stop;
//     end
// endmodule