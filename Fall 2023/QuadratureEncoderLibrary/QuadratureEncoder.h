//
// Created by Arnav Wadhwa on 9/27/23.
//

#ifndef QUADRATUREENCODER_H
#define QUADRATUREENCODER_H

#include <Arduino.h>
#include "quadrature_encoder.pio.h"

class QuadratureEncoder {
private:
    uint8_t pinA;
    uint8_t pinB;
    PIO pio;
    int encoderStateMachine;
    static bool firstInstance;
    static int encoderProgramOffset;
    int resetPosition;

public:
    int clockDivisor;
    QuadratureEncoder(uint8_t pinA, int clockDivisor = 10, PIO pio = pio0);
    void resetEncoderPosition();
    int readEncoderPosition();
};

#endif //QUADRATUREENCODER_H
