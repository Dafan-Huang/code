
.486
CODE SEGMENT  USE16
             ASSUME CS:CODE
    BEG:     JMP    START
    CCONPORT EQU    213H           ;���ƿڵ�ַ

    CCONBIT1 EQU    00110110B      ;������0������
    CCONBIT2 EQU    01110110B      ;������1������
    CCONBIT3 EQU    10110110B      ;������2������

    CDPORT1  EQU    210H           ;������0��ֵ�˿�
    CDPORT2  EQU    211H           ;������1��ֵ�˿�
    CDPORT3  EQU    212H           ;������2��ֵ�˿�

    CHDBIT1  EQU    10000          ;������0��ֵ
    CHDBIT2  EQU    2000           ;������1��ֵ
    CHDBIT3  EQU    1000           ;������2��ֵ

    START:   NOP                   ;������ʱ
             MOV    DX,CCONPORT    ;д�������(������0)
             MOV    AL,CCONBIT1
             OUT    DX,AL
             MOV    DX,CDPORT1     ;д���ֵ��������0��
             MOV    AX,CHDBIT1
             OUT    DX,AL          ;д���8λ
             MOV    AL,AH
             OUT    DX,AL          ;д���8λ
             MOV    DX,CCONPORT    ;д������֣�������1��
             MOV    AL,CCONBIT2
             OUT    DX,AL
             MOV    DX,CDPORT2     ;д���ֵ��������1��
             MOV    AX,CHDBIT2
             OUT    DX,AL
             MOV    AL,AH
             OUT    DX,AL
             MOV    DX,CCONPORT    ;д������֣�������2��
             MOV    AL,CCONBIT3
             OUT    DX,AL
             MOV    DX,CDPORT3     ;д���ֵ��������2��
             MOV    AX,CHDBIT3
             OUT    DX,AL
             MOV    AL,AH
             OUT    DX,AL
    WT:      NOP
             JMP    WT
CODE ENDS
          END    BEG
