;（1）数据段从BUF单元开始存有一字符串（长度<255），
;编程实现统计该字符串中的ASCII在42H～45H之间的字符个数，      ; （B、C、D、E）
;并将统计结果以二进制形式显示在屏幕上。

.586
DATA SEGMENT USE16
     BUF   DB 'ABCDEFG',0     ; 待统计的字符串
     COUNT DB 0               ; 统计结果
DATA ENDS

CODE SEGMENT USE16
          ASSUME CS:CODE, DS:DATA          ; 段寄存器赋值
     BEG: 
          MOV    AX, DATA                  ; 数据段地址赋值
          MOV    DS, AX                    ; 数据段寄存器赋值
          MOV    BX, OFFSET BUF            ; BX指向BUF

          MOV    CX, 8                     ; 字符串长度
          MOV    DL, 0                     ; 初始化计数器
     LAST:                                 ; 循环判断是否为42H~45H
          CMP    BYTE PTR DS:[BX], 42H
          JC     NEXT
          CMP    BYTE PTR DS:[BX], 45H
          JA     NEXT
          INC    COUNT                     ; 统计结果加1
         
     NEXT:
          INC    BX                        ; 指向下一个字符
          LOOP   LAST                      ; 循环判断
     
          ADD    COUNT, 30H                ; 转换为ASCII码
          MOV    DL, COUNT                 ; 显示结果
          MOV    AH, 02H                   ; 显示字符
          INT    21H
          MOV    AH, 4CH                   ;退出DOS系统
          INT    21H
CODE ENDS
     END    BEG