/*
 * Sketch to control the servo pins of Arduino via serial interface
 *
 */

char operation; // Holds operation (R, W, ...)
char mode; // Holds the mode (D, A)
int pin_number; // Holds the pin number
int digital_value; // Holds the digital value
int analog_value; // Holds the analog value
int value_to_write; // Holds the value that we want to write
int wait_for_transmission = 5; // Delay in ms in order to receive the serial data

int Motor_G = 6;
int Motor_D = 5;
int Buzzer = 9;


void setup() {
    Serial.begin(9600); // Serial Port at 9600 baud
    Serial.setTimeout(500); // Instead of the default 1000ms, in order
                            // to speed up the Serial.parseInt() 
    // Set output 
    pinMode(Motor_G, OUTPUT);
    pinMode(Motor_D, OUTPUT);
    pinMode(Buzzer, OUTPUT);
}

void loop() {
    // Check if characters available in the buffer
    if (Serial.available() > 0) 
    {
        // parse information
        // courtesy of lekum 
        operation = Serial.read();
        delay(wait_for_transmission); // If not delayed, second character is not correctly read
        mode = Serial.read();
        pin_number = Serial.parseInt(); // Waits for an int to be transmitted
        
        if (Serial.read()==':')
        {
            value_to_write = Serial.parseInt(); // Collects the value to be written
        }

        // if we recieve proper input write servo
        if (operation == 'W')
        {
            if (mode == 'F')
            {
                analogWrite(Motor_G, value_to_write);
                analogWrite(Motor_D, value_to_write);
                delay(200);
            }
            else if (mode == 'L')
            {
                analogWrite(Motor_D, value_to_write);
                analogWrite(Motor_G, 0);
                delay(200);
            }
            else if (mode == 'R')
            {
                analogWrite(Motor_G, value_to_write);
                analogWrite(Motor_D, 0);
                delay(200);
            }
            else if (mode == 'b')
            {
                // controle buzzer at 440hz              
                tone(Buzzer, 440);
                delay(500);
                noTone(Buzzer);
            }
        }
        
    }
}
