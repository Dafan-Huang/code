
.486
CODE SEGMENT  USE16
             ASSUME CS:CODE
    BEG:     JMP    START
    CCONPORT EQU    213H           ;���ƿڵ�ַ
    ;D7D6 ��ʾ������ѡ��
    ;D5D4 ��ʾ��д��ʽѡ��
    ;D3D2D1 ��ʾ������ʽѡ��
    ;D0 ��ʾ����ѡ��
    CCONBIT1 EQU    00110110B      ;������0������
    CCONBIT2 EQU    01110110B      ;������1������
    CCONBIT3 EQU    10110110B      ;������2������

    CDPORT1  EQU    210H           ;������0��ֵ�˿�
    CDPORT2  EQU    211H           ;������1��ֵ�˿�
    CDPORT3  EQU    212H           ;������2��ֵ�˿�

    ;N=fclk/fout
    CHDBIT1  EQU    400            ;������0��ֵ      100KHz/400=250Hz
    CHDBIT2  EQU    400            ;������1��ֵ      10KHz/400=25Hz
    CHDBIT3  EQU    400            ;������2��ֵ      1KHz/400=2.5Hz

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

; (1): �ر�ʵ�����Դ����������ԭ��ͼ���ߣ�
; (2): ��8254��A0,A1               ����   ��չ������A0��A1;
; (3): ��8254��/RD,/WR             ����   ��չ������/IOR,/IOW;
; (4): ��8254��/CS                 ����   I/O��ַ��/210H;
; (5): ��8254��OUT0,OUT1,OUT2      ����   LED��ʾ��L7��L6��L5;
; (6): ��8254��GATE0,GATE1,GATE2   ����   ��չʵ����+5V;
; (7): ��8254��CLK0,CLK1,CLK2      ����   ʱ��100K,10K,1K; 
