void setup() {
  pinMode(9, OUTPUT);  // OC1A

  // Clear control registers
  TCCR1A = 0;
  TCCR1B = 0;

  // Set Fast PWM mode (Mode 14: ICR1 as TOP)
  TCCR1A |= (1 << WGM11);
  TCCR1B |= (1 << WGM12) | (1 << WGM13);

  // Non-inverting mode on OC1A (pin 9)
  TCCR1A |= (1 << COM1A1);

  // Set TOP value for 1 kHz
  ICR1 = 1999;

  // Set duty cycle = 50%
  OCR1A = 1000;

  // Start timer with prescaler = 8
  TCCR1B |= (1 << CS11);
}

void loop() {


}
