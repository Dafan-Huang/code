; 利用系统定时源设计计时器，
; 具体内容：利用日时钟1CH中断设计定时中断程序，
; 每隔一秒刷新屏幕上显示的时、分、秒，按下键盘任意键后程序自动退出。
; （提示：最终屏幕中的打印形式为24小时制形式：HH:MM:SS，
; 每秒钟进行刷新一次，可采用INT 21H打印字符串的子功能，
; 每秒进行重新打印即可实现覆盖刷新。
; 同时要注意时间显示格式要采用24小时制的时、分、秒的更新，24进制的时分秒都是2位数，
; 所以可以使用字节除法指令，除以10之后，商在AL中，余数在AH中，
; 从而可以分离10进制数的十位和个位，在屏幕输出时，只打印0DH字符，就可以实现每次打印的覆盖。）

.586
DATA SEGMENT USE16                       ; 数据段
    HOUR     DB 0                        ; 时
    MINUTE   DB 0                        ; 分
    SECOND   DB 0                        ; 秒
    TIME_STR DB 'HH:MM:SS', 0DH , '$'    ; 时间字符串
    ;01:34:67
    ;time_str
    OLD1C    DD ?                        ; 存放原1C中断向量
DATA ENDS

CODE SEGMENT USE16
                   ASSUME CS:CODE, DS:DATA        ; 设置段寄存器
    BEG:           
                   MOV    AX, DATA                ; 设置数据段地址
                   MOV    DS, AX                  ; 设置数据段地址
                   CLI                            ; 关中断
                   CALL   READ1C                  ; 读取1C中断向量
                   CALL   WRITE1C                 ; 写入1C中断向量
                   STI                            ; 开中断
    SCAN:          
                   CALL   WAIT_KEY                ; 等待键盘输入
                   JMP    SCAN                    ; 循环
    
    WAIT_KEY:      
    ; 检查键盘输入
                   MOV    AH, 1
                   INT    16H
                   JZ     WAIT_KEY                ; 没有按键则继续等待,否则退出
                   MOV    AH, 0
                   INT    16H
                   CLI
                   CALL   RESET                   ; 恢复1C中断向量
                   STI
    ; 退出程序
                   MOV    AH, 4CH
                   INT    21H

TIMER_ISR PROC FAR
                   PUSHA
                   PUSHF
    ; 更新时间
                   MOV    AH, 2CH                 ;  读取时间
                   INT    21H                     ;  AL=时，CH=分，DH=秒
                   MOV    HOUR, CH                ; 保存时间
                   MOV    MINUTE, CL              ; 保存时间
                   MOV    SECOND, DH              ; 保存时间
        
    ; 显示时间
                   CALL   DISPLAY_TIME            ; 显示时间
        
    ; 发送EOI信号
                   MOV    AL, 20H                 ; 发送EOI信号
                   OUT    20H, AL                 ; 发送EOI信号
        
                   POPF
                   POPA
                   IRET
TIMER_ISR ENDP

DISPLAY_TIME PROC
    ; 将时间转换为字符串
                   MOV    AL, HOUR                ; 将时转换为字符串
                   CALL   CONVERT_TO_DEC          ; 转换为十进制
                   MOV    TIME_STR, AL            ; 保存十位
                   MOV    TIME_STR+1, AH          ; 保存个位
        
                   MOV    AL, MINUTE              ; 将分转换为字符串
                   CALL   CONVERT_TO_DEC          ; 转换为十进制
                   MOV    TIME_STR+3, AL          ; 保存十位
                   MOV    TIME_STR+4, AH          ; 保存个位
        
                   MOV    AL, SECOND              ; 将秒转换为字符串
                   CALL   CONVERT_TO_DEC          ; 转换为十进制
                   MOV    TIME_STR+6, AL          ; 保存十位
                   MOV    TIME_STR+7, AH          ; 保存个位
        
    ; 显示字符串
                   MOV    DX, OFFSET TIME_STR     ; 设置字符串地址
                   MOV    AH, 09H                 ; 显示字符串
                   INT    21H
                   RET
DISPLAY_TIME ENDP

    TEN            DB     10

CONVERT_TO_DEC PROC
    ; 将二进制转换为十进制
                   MOV    AH, 0
                   DIV    TEN                     ;AH 是余数 AL 是商,从而可以分离10进制数的十位和个位
                   ADD    AL, '0'                 ; 转换为ASCII码
                   ADD    AH, '0'                 ; 转换为ASCII码
                   RET

CONVERT_TO_DEC ENDP

READ1C PROC                                       ; 读取1C中断向量
                   MOV    AX, 351CH
                   INT    21H
                   MOV    WORD PTR OLD1C, BX
                   MOV    WORD PTR OLD1C+2, ES
                   RET
READ1C ENDP

WRITE1C PROC                                      ; 写入1C中断向量
                   push   DS
                   MOV    AX, CODE
                   MOV    DS, AX
                   MOV    DX, OFFSET TIMER_ISR    ; 设置中断处理程序
                   MOV    AX, 251CH
                   INT    21H
                   POP    DS
                   RET
WRITE1C ENDP

RESET PROC                                        ; 恢复1C中断向量
                   MOV    DX, WORD PTR OLD1C
                   MOV    DS, WORD PTR OLD1C+2
                   MOV    AX, 251CH
                   INT    21H
                   RET
RESET ENDP

CODE ENDS
END BEG