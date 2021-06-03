/*
 *  DHT22.h
 *
 *  Created on: May 3, 2021
 *  Author: Karolina Rapacz
 */

#ifndef INC_DHT22_H_
#define INC_DHT22_H_

#include "main.h"
#include "stm32f1xx_hal.h"

void Delay_Microseconds (uint16_t us);
void Set_Pin_Input_Mode (GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);
void Set_Pin_Output_Mode (GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

void DHT22_Start (void);
uint8_t DHT22_Check_Response (void);
uint8_t DHT22_Read (void);


#endif /* INC_DHT22_H_ */
