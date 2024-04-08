
/*
 * *****************************************************************************************
 *
 * 		Copyright (C) 2014-2019 Gowin Semiconductor Technology Co.,Ltd.
 * 		
 * @file			main.c
 * @author		Embedded Development Team
 * @version		V1.0.0
 * @date			2019-10-1 09:00:00
 * @brief			Main program body.
 ******************************************************************************************
 */

/* Includes ------------------------------------------------------------------*/
#include "gw1ns4c.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "string.h"	 
#include "math.h"


//串口0初始化
void Uart0Init(void)
{
  UART_InitTypeDef UART_InitStruct;
	
  UART_InitStruct.UART_Mode.UARTMode_Tx = ENABLE;
  UART_InitStruct.UART_Mode.UARTMode_Rx = ENABLE;
  UART_InitStruct.UART_Int.UARTInt_Tx = DISABLE;
  UART_InitStruct.UART_Int.UARTInt_Rx = ENABLE;
  UART_InitStruct.UART_Ovr.UARTOvr_Tx = DISABLE;
  UART_InitStruct.UART_Ovr.UARTOvr_Rx = DISABLE;
  UART_InitStruct.UART_Hstm = DISABLE;
  UART_InitStruct.UART_BaudRate = 9600;//Baud Rate

	
  UART_Init(UART0,&UART_InitStruct);
}
//串口0中断

void UART0_Handler(void)                
	{
	uint8_t Res;     


		if(UART_GetRxIRQStatus(UART0) == SET)
		{
		Res =UART_ReceiveChar(UART0);	
		UART_ClearRxIRQ(UART0);
		UART_SendChar( UART0, (Res));					 
				
     } 

} 


void delay_ms(__IO uint32_t delay_ms)
{
	for(delay_ms=(SystemCoreClock>>15)*delay_ms*1.63; delay_ms != 0; delay_ms--);
}

unsigned int *pp;

int main()
{   

	NVIC_InitTypeDef InitTypeDef_NVIC;	
	//Init System
	SystemInit();

	//delay_ms(10);//Wait SPI_Nor_Flash initialization
		
	//Init Uart
	Uart0Init();

	
	//UART0/1 Interrupt

	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);

	InitTypeDef_NVIC.NVIC_IRQChannel = UART0_IRQn;
	InitTypeDef_NVIC.NVIC_IRQChannelPreemptionPriority = 0;
	InitTypeDef_NVIC.NVIC_IRQChannelSubPriority = 1;
	InitTypeDef_NVIC.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&InitTypeDef_NVIC);



#define pi 3.14
double t,s;
int i; 
unsigned char data;
 
 
	while(1)
	{		
	    for (int i=0; i<8000; i++)
        {
				  	delay_ms(100);
           
            s=127+127*sin(2*pi*10*i/2000);
				 
						data=s;
				
					
					UART_SendChar( UART0, (data));			
					
        }
	}

}






