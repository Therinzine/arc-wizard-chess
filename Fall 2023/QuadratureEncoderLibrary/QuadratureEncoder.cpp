//
// Created by Arnav Wadhwa on 9/27/23.
//

#include "QuadratureEncoder.h"
#include <hardware/pio.h>

bool QuadratureEncoder::firstInstance = true;
int QuadratureEncoder::encoderProgramOffset = -1;

QuadratureEncoder::QuadratureEncoder(uint8_t pinA, int clockDivisor, PIO pio)
        : pinA(pinA), pinB(pinA + 1), clockDivisor(clockDivisor), pio(pio) {
    // Set the pins to input and pull up (using RP2040 SDK functions)
    gpio_init(pinA);
    gpio_init(pinB);
    gpio_set_dir(pinA, GPIO_IN);
    gpio_set_dir(pinB, GPIO_IN);
    gpio_pull_up(pinA);
    gpio_pull_up(pinB);

    if (firstInstance) {
        encoderProgramOffset = pio_add_program(this->pio, &quadrature_encoder_program);
        firstInstance = false;
    }
    encoderStateMachine = pio_claim_unused_sm(this->pio, false);
    quadrature_encoder_program_init(this->pio, encoderStateMachine, encoderProgramOffset, this->pinA, this->clockDivisor);
    this->resetPosition = quadrature_encoder_get_count(this->pio, encoderStateMachine);
}

void QuadratureEncoder::resetEncoderPosition() {
    this->resetPosition = quadrature_encoder_get_count(pio, encoderStateMachine);
}

int QuadratureEncoder::readEncoderPosition() {
    return quadrature_encoder_get_count(pio, encoderStateMachine) - resetPosition;
}
