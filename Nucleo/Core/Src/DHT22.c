/*
 * 		DHT22.c
 *
 *  	Created on: May 3, 2021
 *      Author: Karolina Rapacz
 */
#include "DHT22.h"

extern TIM_HandleTypeDef htim1;

void Delay_Microseconds (uint16_t us)
{
	__HAL_TIM_SET_COUNTER(&htim1,0);  			 // set the counter value a 0
	while (__HAL_TIM_GET_COUNTER(&htim1) < us);  // wait for the counter to reach the us input in the parameter
}

void Set_Pin_Input_Mode (GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	GPIO_InitStruct.Pin = GPIO_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);
}

void Set_Pin_Output_Mode (GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	GPIO_InitStruct.Pin = GPIO_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);
}

void DHT22_Start (void)
{
	Set_Pin_Output_Mode(DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin); 	 // set the pin as output
	HAL_GPIO_WritePin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin, 0);   // pull the pin low
	Delay_Microseconds(1200);   									 // wait for > 1ms

	HAL_GPIO_WritePin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin, 1);   // pull the pin high
	Delay_Microseconds(20);   										 // wait for 30us

	Set_Pin_Input_Mode(DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin);   	 // set as input
}

uint8_t DHT22_Check_Response (void)
{
	uint8_t Response = 0;

	Set_Pin_Input_Mode(DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin);   							// set as input
	Delay_Microseconds(40);

	// wait for 40us
	if (!(HAL_GPIO_ReadPin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin))) 					// if the pin is low
	{
		Delay_Microseconds(80);   														// wait for 80us

		if ((HAL_GPIO_ReadPin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin))) Response = 1;  // if the pin is high, response is ok
		else Response = -1;
	}

	while ((HAL_GPIO_ReadPin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin)));   				// wait for the pin to go low
	return Response;
}

uint8_t DHT22_Read (void)
{
	uint8_t i, j;

	for (j=0; j<8; j++)
	{
		while (!(HAL_GPIO_ReadPin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin)));   // wait for the pin to go high
		Delay_Microseconds(40);   												// wait for 40 us

		if (!(HAL_GPIO_ReadPin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin)))   	// if the pin is low
		{
			i &= ~(1<<(7-j));   								   				// write 0
		}
		else i |= (1<<(7-j));  								   					// if the pin is high, write 1
		while ((HAL_GPIO_ReadPin (DHT22_1Wire_GPIO_Port, DHT22_1Wire_Pin)));    // wait for the pin to go low
	}

	return i;
}
