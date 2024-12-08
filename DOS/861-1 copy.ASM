; 利用1CH中断，每隔一定时间间隔，
; 在屏幕上打印一行自定义的字符串（例如自己的学号），
; 按下键盘任意键后程序自动退出。
.486

DATA SEGMENT USE16
    MESG   DB 'B22110530', 0DH, 0AH, '$'    ; 定义要打印的字符串
    OLD1C  DD ?                             ; 存放原1C中断向量
    ICOUNT DB 18                            ; 计数器 18*55ms = 990ms 约等于1s
DATA ENDS

CODE SEGMENT USE16
              ASSUME CS:CODE, DS:DATA

    BEG:      
              MOV    AX, DATA                ; 初始化数据段
              MOV    DS, AX
              CLI                            ; 关中断
              CALL   READ1C                  ; 读取1C中断向量
              CALL   WRITE1C                 ; 设置1C中断向量
              STI                            ; 开中断

    CHECK_KEY:
              MOV    AH, 01H                 ; DOS功能号01H，检查键盘
              INT    16H                     ; 调用DOS功能
              JZ     CHECK_KEY               ; 没有键盘输入，退出
           
              CLI                            ; 关中断
              CALL   RESET                   ; 复位1C中断向量
              STI                            ; 开中断

              MOV    AH, 4CH                 ; DOS功能号4CH，退出程序
              INT    21H                     ; 调用DOS功能

SERVICE PROC                                 ; 1C中断服务程序
              PUSHA                          ; 保护现场  将所有寄存器压栈
              PUSH   DS                      ; 保护现场  将DS压栈
              MOV    AX, DATA                ; 初始化数据段
              MOV    DS, AX                  ; 初始化数据段
              DEC    ICOUNT                  ; 计数器减1
              JNZ    EXIT                    ; 计数器不为0，退出
              MOV    ICOUNT, 18              ; 计数器复位
              MOV    AH, 9                   ; DOS功能号09H，打印字符串
              LEA    DX, MESG                ; 要打印的字符串
              INT    21H                     ; 调用DOS功能

    EXIT:                                    ; 退出
              POP    DS                      ; 恢复现场
              POPA                           ; 恢复现场
              IRET                           ; 中断返回
SERVICE ENDP                                 ; 中断服务程序结束


READ1C PROC                                  ; 读取1C中断向量
              MOV    AX, 351CH               ; DOS功能号35H，读取中断向量
              INT    21H                     ; 调用DOS功能
              MOV    WORD PTR OLD1C, BX      ; 保存1C中断向量
              MOV    WORD PTR OLD1C+2, ES    ; 保存1C中断向量
              RET                            ; 返回
READ1C ENDP                                  ; 读取1C中断向量结束

WRITE1C PROC                                 ; 设置1C中断向量
              PUSH   DS                      ; 保护现场
              MOV    AX, SEG SERVICE         ; 初始化代码段
              MOV    DS, AX                  ; 初始化代码段
              MOV    DX, OFFSET SERVICE      ; 设置1C中断服务程序
              MOV    AX, 251CH               ; DOS功能号25H，设置中断向量
              INT    21H                     ; 调用DOS功能
              POP    DS                      ; 恢复现场
              RET                            ; 返回
WRITE1C ENDP                                 ; 设置1C中断向量结束

RESET PROC                                   ; 复位1C中断向量
              MOV    DX, WORD PTR OLD1C      ; 恢复1C中断向量
              MOV    DS, WORD PTR OLD1C+2    ; 恢复1C中断向量
              MOV    AX, 251CH               ; DOS功能号25H，设置中断向量
              INT    21H                     ; 调用DOS功能
              RET                            ; 返回
RESET ENDP                                   ; 复位1C中断向量结束
        
CODE ENDS
END BEG
