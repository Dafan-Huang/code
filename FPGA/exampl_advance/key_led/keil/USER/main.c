
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

 
 
 	

	
void Clear_led()
{
		GPIO_SetBit(GPIO0,GPIO_Pin_0);//led
		GPIO_SetBit(GPIO0,GPIO_Pin_1);//led
		GPIO_SetBit(GPIO0,GPIO_Pin_2);//led}
}

	
void Set_led()
{
		GPIO_ResetBit(GPIO0,GPIO_Pin_0);//led
		GPIO_ResetBit(GPIO0,GPIO_Pin_1);//led
		GPIO_ResetBit(GPIO0,GPIO_Pin_2);//led}
}



void delay_ms(__IO uint32_t delay_ms)
{
	for(delay_ms=(SystemCoreClock>>15)*delay_ms; delay_ms != 0; delay_ms--);
}


void GPIOInit(void)
{
 	//MISO端口设为输入
	GPIO0->OUTENSET = 0xffffffef;	
	GPIO_SetBit(GPIO0,GPIO_Pin_0);//led
	GPIO_ResetBit(GPIO0,GPIO_Pin_1); //led
}

int main()
{   
  uint32_t GPIO_my;
	NVIC_InitTypeDef InitTypeDef_NVIC;	
	//Init System
	SystemInit();
	GPIOInit();
	
	while(1)
	{	

 GPIO_my= GPIO_ReadBits(GPIO0);
		if  ((GPIO_my&0x10)==0x10) 
		{ 		
		Clear_led();
		GPIO_ResetBit(GPIO0,GPIO_Pin_0); //led 
    delay_ms(1000); 			
 	/////////////////////////////////		
		Clear_led();
		GPIO_ResetBit(GPIO0,GPIO_Pin_1); //led 
    delay_ms(1000); 			
 	/////////////////////////////////		
			Clear_led();
		GPIO_ResetBit(GPIO0,GPIO_Pin_2); //led 
    delay_ms(1000); 			
 	/////////////////////////////////
		}
		else		
		{		
		Clear_led();		
    delay_ms(1000); 
		Set_led();
		delay_ms(1000); 				
		}
	
		       
	}
	
	
	
	
	
	
	
	

}






