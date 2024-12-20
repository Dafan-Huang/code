
.486
CODE SEGMENT  USE16
             ASSUME CS:CODE
    BEG:     JMP    START
    CCONPORT EQU    213H           ;控制口地址

    CCONBIT1 EQU    00110110B      ;计数器0控制字
    CCONBIT2 EQU    01110110B      ;计数器1控制字
    CCONBIT3 EQU    10110110B      ;计数器2控制字

    CDPORT1  EQU    210H           ;计数器0初值端口
    CDPORT2  EQU    211H           ;计数器1初值端口
    CDPORT3  EQU    212H           ;计数器2初值端口

    CHDBIT1  EQU    10000          ;计数器0初值
    CHDBIT2  EQU    2000           ;计数器1初值
    CHDBIT3  EQU    1000           ;计数器2初值

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
