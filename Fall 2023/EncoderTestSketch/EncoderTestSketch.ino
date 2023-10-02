//To program the Pico:
//    1) Press and hold the Pico's BOOTSEL button
//    2) Plug pico into USB port
//    3) Release the Pico's BOOTSEL button
//    4) Click on the Arduino IDE => button to program


// A Small example to run the pico motors with the serial monitor
#include <QuadratureEncoder.h>

const int motor1a = 14;
const int motor1b = 15;
const int l293Enable = 13;
const int encoderA = 11;

QuadratureEncoder motor0(encoderA, 100);
long encoderCounts = -999;
long newEncoderCounts;

int average;
int motorSpeed = 255;


void setup() {
    // put your setup code here, to run once:
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(motor1a, OUTPUT);
    pinMode(motor1b, OUTPUT);
    pinMode(l293Enable, OUTPUT);
    analogWrite(l293Enable, motorSpeed);
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.begin(115200);
    motor0.resetEncoderPosition();

    Serial.println("Enter a command: ");
    Serial.println("1: Forward");
    Serial.println("2: Backward");
    Serial.println("3: Stop");
    Serial.println("4: Reset Encoder");
    Serial.println("5: Read Encoder");
    Serial.println("6: Move for 1 second");
    Serial.println("7: Cut motor speed by 1/2");
    Serial.println("8: Set motor speed to max");
    Serial.println("Any Other number: Move motor for that many counts");
}

void loop() {

    // Read in from the serial monitor
    while (Serial.available() == 0) {
        // Do nothing, wait for serial input
    }
    int command = Serial.parseInt();

    // Execute the command
    switch (command) {
        case 0:
            break;
        case 1:
            Serial.println("Command 1: Forward");
            digitalWrite(motor1a, HIGH);
            digitalWrite(motor1b, LOW);
            break;
        case 2:
            Serial.println("Command 2: Backward");
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, HIGH);
            break;

        case 3:
            Serial.println("Command 3: Stop");
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
            break;

        case 4:
            Serial.println("Command 4: Reset Encoder");
            motor0.resetEncoderPosition();
            break;

        case 5:
            Serial.println("Command 5: Read Encoder");
            Serial.println(motor0.readEncoderPosition());
            break;

        case 6:
            Serial.println("Command 6: Move for 1 second");
            digitalWrite(motor1a, HIGH);
            digitalWrite(motor1b, LOW);
            delay(1000);
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
            break;

        case 7:
            Serial.println("Dividing motor speed by 2");
            motorSpeed /= 2;
            analogWrite(l293Enable, motorSpeed);
            break;

        case 8:
            Serial.println("Resetting Motor speed");
            motorSpeed = 255;
            analogWrite(l293Enable, motorSpeed);
            break;

        default:
            Serial.print("Moving motor for ");
            Serial.print(command);
            Serial.println(" counts.");
            encoderCounts = motor0.readEncoderPosition();
            newEncoderCounts = encoderCounts + command;
            while (encoderCounts < newEncoderCounts) {
                digitalWrite(motor1a, HIGH);
                digitalWrite(motor1b, LOW);
                encoderCounts = motor0.readEncoderPosition();
            }
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
            break;

    }
}