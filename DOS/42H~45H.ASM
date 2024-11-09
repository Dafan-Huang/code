;（1）数据段从BUF单元开始存有一字符串（长度<255），
;编程实现统计该字符串中的ASCII在42H～45H之间的字符个数，      ; （B、C、D、E）
;并将统计结果以二进制形式显示在屏幕上。

.586
DATA SEGMENT USE16
    BUF   DB 'ABCDEFG',0    ; The string to be analyzed with null terminator
    COUNT DB 0              ; Variable to store the count
DATA ENDS

CODE SEGMENT USE16
         ASSUME CS:CODE, DS:DATA
    BEG: 
         MOV    AX, DATA
         MOV    DS, AX
         MOV    BX, OFFSET BUF

         MOV    CX, 8
         MOV    DL, 0
    LAST:
         CMP    BYTE PTR DS:[BX], 42H
         JC     NEXT
         CMP    BYTE PTR DS:[BX], 45H
         JA     NEXT
         INC    COUNT 
         
    NEXT:
         INC    BX
         LOOP   LAST
    
         ADD    COUNT, 30H
         MOV    DL, COUNT
         MOV    AH, 02H
         INT    21H
         MOV    AH, 4CH
         INT    21H
CODE ENDS
     END    BEG