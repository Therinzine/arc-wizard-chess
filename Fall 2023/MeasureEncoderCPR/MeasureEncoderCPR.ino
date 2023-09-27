#include <pio_encoder.h>

const int MOTOR_PIN1 = 14;  // Control pin 1 for L293D
const int MOTOR_PIN2 = 15;  // Control pin 2 for L293D
const int MOTOR_ENABLE = 13;  // PWM Enable pin for L293D
const int ENCODER_A = 11;

const int POT_PIN = A2;  // Analog pin for the potentiometer

int startPotValue = 511;
int endPotValue = 767;

PioEncoder encoder0(ENCODER_A);

int encoderStartCount;
int encoderEndCount;

bool started = false;

void setup() {
  delay(10000);
  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(MOTOR_ENABLE, OUTPUT);
  encoder0.begin();
  encoder0.reset();
  Serial.begin(115200);

  // Start the motor rotation
  rotateMotor(true);
}

void loop() {
  int currentPotValue = analogRead(POT_PIN);
  if (currentPotValue == startPotValue) {
    encoderStartCount = encoder0.getCount();
    started = true;
  }

  if (currentPotValue == endPotValue && started) {
    encoderEndCount = encoder0.getCount();
    Serial.println("Rotated 1/2 turn");
    Serial.println("Encoder CPR: " + ((encoderEndCount - encoderStartCount) * 2));
  }

  delay(10); // Short delay to avoid reading noise

}

void rotateMotor(bool forward) {
  if (forward) {
    digitalWrite(MOTOR_PIN1, HIGH);
    digitalWrite(MOTOR_PIN2, LOW);
  } else {
    digitalWrite(MOTOR_PIN1, LOW);
    digitalWrite(MOTOR_PIN2, HIGH);
  }
  analogWrite(MOTOR_ENABLE, 255);  // Full speed, modify if needed
}

void stopMotor() {
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  analogWrite(MOTOR_ENABLE, 0); // Stop the motor
}
