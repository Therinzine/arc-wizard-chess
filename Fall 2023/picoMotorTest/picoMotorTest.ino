// A Small example to run the pico motors with the serial monitor
#include <pio_encoder.h>

const int motor1a = 16;
const int motor1b = 17;
const int l293Enable = 15;
const int encoderA = 2;

PioEncoder motor0(encoderA);
long encoderCounts = -999;
long newEncoderCounts;


void setup() {
    // put your setup code here, to run once:
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(motor1a, OUTPUT);
    pinMode(motor1b, OUTPUT);
    pinMode(l293Enable, OUTPUT);
    digitalWrite(l293Enable, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.begin(115200);
    motor0.begin();
    motor0.reset();


}

void loop() {
    Serial.println("Enter a command: ");
    Serial.println("1: Forward");
    Serial.println("2: Backward");
    Serial.println("3: Stop");
    Serial.println("4: Reset Encoder");
    Serial.println("5: Read Encoder");
    Serial.println("6: Move for 1 second");
    Serial.println("7: Move for 1000 counts");
    // Read in from the serial monitor
    while(Serial.available() == 0) {
        // Do nothing, wait for serial input
    }
    int command = Serial.parseInt();

    // Execute the command
    switch (command) {
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
            motor0.reset();
            break;

        case 5:
            Serial.println("Command 5: Read Encoder");
            Serial.println(motor0.getCounts());
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
            Serial.println("Command 7: Move for 1000 counts");
            encoderCounts = motor0.getCounts();
            newEncoderCounts = encoderCounts + 1000;
            while (encoderCounts < newEncoderCounts) {
                digitalWrite(motor1a, HIGH);
                digitalWrite(motor1b, LOW);
                encoderCounts = motor0.getCounts();
            }
            digitalWrite(motor1a, LOW);
            digitalWrite(motor1b, LOW);
            break;

        default:
            Serial.println("Command not recognized");
            break;
    }
}