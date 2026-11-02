#include "pico/stdlib.h"
#include "hardware/pwm.h"

int main() {
    //outputs pins
    const uint Serwo_PIN_1 = 15;
    const uint Serwo_PIN_2 = 16;
    const uint Serwo_PIN_3 = 18;
    const uint Serwo_PIN_4 = 20;


    //TODO change to better range adjusted to servo's
    //duty (0-100%)
    uint16_t PIN_1_Duty_Percent = 1;
    uint16_t PIN_2_Duty_Percent = 25;
    uint16_t PIN_3_Duty_Percent = 50;
    uint16_t PIN_4_Duty_Percent = 75;

    //frequency (hz)
    uint16_t frequency = 60;

    //configuration
    gpio_set_function(Serwo_PIN_1, GPIO_FUNC_PWM);
    gpio_set_function(Serwo_PIN_2, GPIO_FUNC_PWM);
    gpio_set_function(Serwo_PIN_3, GPIO_FUNC_PWM);
    gpio_set_function(Serwo_PIN_4, GPIO_FUNC_PWM);


    uint slice1 = pwm_gpio_to_slice_num(Serwo_PIN_1);
    uint slice2 = pwm_gpio_to_slice_num(Serwo_PIN_2);
    uint slice3 = pwm_gpio_to_slice_num(Serwo_PIN_3);
    uint slice4 = pwm_gpio_to_slice_num(Serwo_PIN_4);


    uint32_t ClockFreq = 125000000;
    uint16_t divider = 64;
    uint32_t counterMax = ClockFreq/(divider*frequency) - 1;


    pwm_set_clkdiv(slice1, divider);
    pwm_set_wrap(slice1, counterMax);

    pwm_set_clkdiv(slice2, divider);
    pwm_set_wrap(slice2, counterMax);

    pwm_set_clkdiv(slice3, divider);
    pwm_set_wrap(slice3, counterMax);

    pwm_set_clkdiv(slice4, divider);
    pwm_set_wrap(slice4, counterMax);



    //start generating pwm
    pwm_set_enabled(slice1, true);
    pwm_set_enabled(slice2, true);
    pwm_set_enabled(slice3, true);
    pwm_set_enabled(slice4, true);




  

    while (true) {
    //TODO change PIN_x_Duty_Percent from usb reveived commands


    uint16_t PIN_1_Duty_Value = counterMax * PIN_1_Duty_Percent/100;
    uint16_t PIN_2_Duty_Value = counterMax * PIN_2_Duty_Percent/100;
    uint16_t PIN_3_Duty_Value = counterMax * PIN_3_Duty_Percent/100;
    uint16_t PIN_4_Duty_Value = counterMax * PIN_4_Duty_Percent/100;


    pwm_set_gpio_level(Serwo_PIN_1, PIN_1_Duty_Value);
    pwm_set_gpio_level(Serwo_PIN_2, PIN_2_Duty_Value);
    pwm_set_gpio_level(Serwo_PIN_3, PIN_3_Duty_Value);
    pwm_set_gpio_level(Serwo_PIN_4, PIN_4_Duty_Value);


    sleep_ms(10);

    }
}