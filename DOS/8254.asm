
.486
CODE SEGMENT  USE16
             ASSUME CS:CODE
    BEG:     JMP    START
    CCONPORT EQU    213H           ;控制口地址
    ;D7D6 表示计数器选择
    ;D5D4 表示读写方式选择
    ;D3D2D1 表示工作方式选择
    ;D0 表示数制选择
    CCONBIT1 EQU    00110110B      ;计数器0控制字
    CCONBIT2 EQU    01110110B      ;计数器1控制字
    CCONBIT3 EQU    10110110B      ;计数器2控制字

    CDPORT1  EQU    210H           ;计数器0初值端口
    CDPORT2  EQU    211H           ;计数器1初值端口
    CDPORT3  EQU    212H           ;计数器2初值端口

    ;N=fclk/fout
    CHDBIT1  EQU    400            ;计数器0初值      100KHz/400=250Hz
    CHDBIT2  EQU    400            ;计数器1初值      10KHz/400=25Hz
    CHDBIT3  EQU    400            ;计数器2初值      1KHz/400=2.5Hz

    START:   NOP                   ;启动延时
             MOV    DX,CCONPORT    ;写入控制字(计数器0)
             MOV    AL,CCONBIT1
             OUT    DX,AL
             MOV    DX,CDPORT1     ;写入初值（计数器0）
             MOV    AX,CHDBIT1
             OUT    DX,AL          ;写入低8位
             MOV    AL,AH
             OUT    DX,AL          ;写入高8位
             MOV    DX,CCONPORT    ;写入控制字（计数器1）
             MOV    AL,CCONBIT2
             OUT    DX,AL
             MOV    DX,CDPORT2     ;写入初值（计数器1）
             MOV    AX,CHDBIT2
             OUT    DX,AL
             MOV    AL,AH
             OUT    DX,AL
             MOV    DX,CCONPORT    ;写入控制字（计数器2）
             MOV    AL,CCONBIT3
             OUT    DX,AL
             MOV    DX,CDPORT3     ;写入初值（计数器2）
             MOV    AX,CHDBIT3
             OUT    DX,AL
             MOV    AL,AH
             OUT    DX,AL
    WT:      NOP
             JMP    WT
CODE ENDS
          END    BEG

; (1): 关闭实验箱电源，按照下面原理图连线；
; (2): 将8254的A0,A1               接至   扩展总线区A0，A1;
; (3): 将8254的/RD,/WR             接至   扩展总线区/IOR,/IOW;
; (4): 将8254的/CS                 接至   I/O地址区/210H;
; (5): 将8254的OUT0,OUT1,OUT2      接至   LED显示区L7，L6，L5;
; (6): 将8254的GATE0,GATE1,GATE2   接至   扩展实验区+5V;
; (7): 将8254的CLK0,CLK1,CLK2      接至   时钟100K,10K,1K; 
