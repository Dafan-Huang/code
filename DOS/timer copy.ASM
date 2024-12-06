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
    HOUR     DB 23                       ; 时
    MINUTE   DB 59                       ; 分
    SECOND   DB 55                       ; 秒
    TIME_STR DB 'HH:MM:SS', 0DH , '$'    ; 时间字符串
    ;01:34:67
    COUNT    DB 18                       ; 计数器
    OLD1C    DD ?                        ; 存放原1C中断向量
    TEN      DB 10
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
    CHECK_KEY:     
    ; 检查键盘输入
                   MOV    AH, 1                   ; DOS功能号01H，检查键盘
                   INT    16H                     ; 调用DOS功能
                   JZ     CHECK_KEY               ; 没有按键则继续等待,否则退出
                   CLI
                   CALL   RESET                   ; 恢复1C中断向量
                   STI
    ; 退出程序
                   MOV    AH, 4CH
                   INT    21H

TIMER_ISR PROC FAR
                   PUSHA
    ; 更新时间
                   DEC    COUNT                   ; 计数器减1
                   JNZ    END_UPDATE              ; 如果计数器不为0，跳转到END_UPDATE
                   MOV    COUNT, 18               ; 否则，重置计数器为18（大约1秒）

                   INC    SECOND                  ; 秒自增
                   CMP    SECOND, 60              ; 检查是否达到60秒
                   JNE    UPDATE_MINUTE           ; 如果不到60秒，跳转到UPDATE_MINUTE
                   MOV    SECOND, 0               ; 否则，秒归零
                   INC    MINUTE                  ; 分钟自增
                   
    UPDATE_MINUTE: 
                   CMP    MINUTE, 60              ; 检查是否达到60分钟
                   JNE    UPDATE_HOUR             ; 如果不到60分钟，跳转到UPDATE_HOUR
                   MOV    MINUTE, 0               ; 否则，分钟归零
                   INC    HOUR                    ; 小时自增
                   
    UPDATE_HOUR:   
                   CMP    HOUR, 24                ; 检查是否达到24小时
                   JNE    END_UPDATE              ; 如果不到24小时，跳转到END_UPDATE
                   MOV    HOUR, 0                 ; 否则，小时归零
                   
    END_UPDATE:    
    ; 显示时间
                   CALL   DISPLAY_TIME            ; 显示时间

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



CONVERT_TO_DEC PROC
    ; 将二进制转换为十进制
                   MOV    AH, 0
                   DIV    TEN                     ; AH 是余数 AL 是商,从而可以分离10进制数的十位和个位
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
                   PUSH   DS
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
