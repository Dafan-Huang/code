;（2）用户登录验证程序的实现。
;程序执行后，给出提示操作，请用户键入用户名和密码；用户在键入密码时，程序不回显键入字符；
;只有当用户键入的用户名，密码字符串和程序内定的字符串相同时，
;显示欢迎界面并返回DOS；否则给出提示信息，用户名或密码错误，再次输入。界面颜色自定（彩色或黑白）

.586
DATA SEGMENT USE16
       PleaseU  DB 'Please enter your username:$'
       PleaseP  DB 'Please enter your password:$'

       BUF1     DB 30
                DB ?
                DB 30 DUP(?)
    
       BUF2     DB 30
                DB ?
                DB 30 DUP(?)

       ERROR_M  DB 'Wrong username or passsword!$'
       WELCOME  DB 'Welcome!$'
       Username DB 'admin'
       Password DB '123456'

DATA ENDS

CODE SEGMENT USE16
              ASSUME CS:CODE,DS:DATA,ES:DATA       ;?

       BEG:   
              MOV    AX,DATA
              MOV    DS,AX
              MOV    ES,AX                         ;?
           

       AGAIN1:
              MOV    AH,09H                        ;显示询问用户名字符串
              MOV    DX,OFFSET PleaseU
              INT    21H

              MOV    AH,0AH                        ;输入用户名
              MOV    DX,OFFSET BUF1                ;存储用户名
              INT    21H

              MOV    AH,02H                        ;显示换行
              MOV    DL,0AH
              INT    21H
       
       JUDGE1:
              MOV    SI,OFFSET BUF1+2              ;指向输入的用户名
              MOV    DI,OFFSET Username            ;指向系统设定的用户名
              MOV    CX,5                          ;用户名长度
       N1:    MOV    AL,[SI]
              MOV    BL,[DI]
              CMP    AL,BL
              JNE    ERROR                         ;如果不相等，重新输入用户名
              INC    SI
              INC    DI
              LOOP   N1
              JMP    AGAIN2                        ;如果相等，继续输入密码
       
       AGAIN2:
              MOV    AH,2
              MOV    DL,0AH
              INT    21H
              MOV    AH,09H                        ;显示询问密码字符串
              MOV    DX,OFFSET PleaseP
              INT    21H
              MOV    BX,OFFSET BUF2                ;把密码存储在BUF2中
              MOV    CX,6

       LAST:  
              MOV    AH,07H                        ;不回显字符
              INT    21H                           ;光标下移一行
              MOV    [BX+2],AL                     ;低位传给BX

       ;BUF+0是预置可容纳字符的个数
       ;BUF+1是实际输入的字符个数
       ;BUF+2是输入字符串的实际存储区域

              MOV    AH,02H                        ;显示字符
              MOV    DL,'*'
              INT    21H
              INC    BX                            ;BX后移一位,一共移6次
              LOOP   LAST
              JMP    JUDGE2
     
                 
       JUDGE2:
              MOV    SI,OFFSET BUF2+2              ;指向输入的密码
              MOV    DI,OFFSET Password            ;指向系统设定的密码
              MOV    CX,6                          ;密码长度
       N2:    MOV    AL,[SI]
              MOV    BL,[DI]
              CMP    AL,BL
              JNE    ERROR                         ;如果不相等，重新输入密码
              INC    SI
              INC    DI
              LOOP   N2
              JMP    RIGHT                         ;如果相等，显示欢迎信息

       ERROR: 
              MOV    AH,09H
              MOV    DX,OFFSET ERROR
              INT    21H

              MOV    AH,02H                        ;显示换行
              MOV    DL,0AH
              INT    21H
              JMP    AGAIN1

       RIGHT: 
              MOV    AH,02H
              MOV    DL,0AH
              INT    21H
              MOV    AH,09H
              MOV    DX,OFFSET WELCOME
              INT    21H
       ;JMP    EXIT

       EXIT:  
              MOV    AH,4CH                        ;返回DOS
              INT    21H
CODE ENDS
     END BEG

