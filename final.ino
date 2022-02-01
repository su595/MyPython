
// libraries
    // rtc
#include <Rtc_Pcf8563.h>

    // temperature sensor

#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

    // sd card
#include <SPI.h>
#include "SD.h"

    // sleep mode
#include <avr/sleep.h>
#include <avr/power.h>

    // others
#include <Wire.h>

// pin definitions

#define CRANK_HS_PIN 16 // A1
#define WHEEL_HS_PIN 15 // A2
#define MPU 0x68
#define SD_CS_PIN 10 // Chip Select can be anything, the others(Mosi, Miso, SCK) are defined by hardware
#define BUZZER_EN 6 // D6
#define BUZZER_BASE 7 // D7
#define LED_PIN 4 // D4
#define SWITCH_OUT 3 // D3 / Interrupt1
#define SWITCH_IN 2 // D2 / Interrupt0

// constants

#define WRITE_INTERVAL 10000 // [ms] how often a new data point is written (must be lower than ~32000 to prevent the sumOfDt variables from overflowing)

// this has a big impact on sampling rate of crank and wheel, because loops per second for 1 is 308, for 10 is 3169 and for 100 is 4169
#define MPU_UPDATE_FREQUENCY 10 // [ms] how often the MPU values are sampled (since this is quite computation intensive)

#define CRANK_SENSITIVITY 2 // the necessary deviation from idle state
#define CRANK_COOLDOWN 300 // [ms] any time delta lower than this will be invalid
#define CRANK_HIGH_CUTOFF 5000 // [ms] any time delta higher than this will be invalid
#define CRANK_FACTOR 60000.0 // makes the cadence be in rpm !SHOULD BE FLOAT!

#define WHEEL_SENSITIVITY 5 // the necessary deviation from idle state
#define WHEEL_COOLDOWN 96 // [ms] any time delta lower than this will be invalid (equvalent to a speed of 80km/h)
#define WHEEL_HIGH_CUTOFF 2000 // [ms] any time delta higher than this will be invalid
#define SPEED_FACTOR 7803.72 // 3'600'000 * wheel circumference in km (69cm)

#define ANTI_THEFT_ACC_SENSITIVITY 0.6
#define ANTI_THEFT_ALERT_TIME 10000 // [ms]

// global variables
    // crank hs
int idleCrankHS;
unsigned long crankLastTrigger;
float cadence;

    // wheel hs
int idleWheelHS;
unsigned long wheelLastTrigger;
float speed;

    // gyro
float AccX, AccY, AccZ;
float accAngleX, accAngleY;
float roll, pitch, yaw;
unsigned long lastMPU;

    // sd
unsigned long lastWriteToSD;
const char fileDirectory[] = "logs/";
const char fileExtension[] = ".txt";
const char comma[] = ", ";
char filepath[20];
File sdFile;

    // bme
float temperature; // in °C
float pressure; // in hPa
float humidity; // in %
Adafruit_BME280 bme;

    // rtc
Rtc_Pcf8563 rtc;

    // misc
unsigned long smartLedTimer;
volatile bool isSwitchTriggered;
uint8_t state;
unsigned long antiTheftLedTimer;
bool antiTheftLedOn;

void(* resetFunc) (void) = 0; // this locates the built-in reset function to memory adress 0, which is required for resetFunc() to work



void setup(){
    smartLed(3000);

        // setup Pins
    pinMode(BUZZER_EN, OUTPUT);
    pinMode(BUZZER_BASE, OUTPUT);
    digitalWrite(BUZZER_EN, LOW);
    digitalWrite(BUZZER_BASE, LOW);

    pinMode(LED_PIN, OUTPUT);
    pinMode(SWITCH_IN, INPUT_PULLUP); attachInterrupt(digitalPinToInterrupt(SWITCH_IN), switchISR, CHANGE);
    pinMode(SWITCH_OUT, INPUT_PULLUP); attachInterrupt(digitalPinToInterrupt(SWITCH_OUT), switchISR, CHANGE);
    isSwitchTriggered = true; // measure the switch states once at the beginning

        // setup MPU
    Wire.begin();                      // Initialize comunication 
    Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
    Wire.write(0x6B);                  // Talk to the register 6B
    Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
    Wire.endTransmission(true);        // end the transmission
    
        // setup BME
    if(!bme.begin(0x76)){
        Buzzer(1000, false);
    }
    // this sets the BME to forced mode, where it sleeps until I call bme.takeForcedMeasurement()
    bme.setSampling(Adafruit_BME280::MODE_FORCED,
                    Adafruit_BME280::SAMPLING_X1, // temperature
                    Adafruit_BME280::SAMPLING_X1, // pressure
                    Adafruit_BME280::SAMPLING_X1, // humidity
                    Adafruit_BME280::FILTER_OFF);

        // setup HSses (this will take 200ms)
    long sumOfHS = 0;
    // the magnet must be away from the HS during this "callibration"
    for(int i = 0; i < 100; i++){
        sumOfHS = sumOfHS + analogRead(WHEEL_HS_PIN);
        delay(1);
    }
    idleWheelHS = sumOfHS/100;

    sumOfHS = 0;
    for(int i = 0; i < 100; i++){
        sumOfHS = sumOfHS + analogRead(CRANK_HS_PIN);
        delay(1);
    }
    idleCrankHS = sumOfHS/100;

        // setup SD
    if (!SD.begin(SD_CS_PIN)) {
        Buzzer(1000, false);
    }
        // log the reset time
    memset(filepath, 0, sizeof(filepath)); // this completly clears the string for strcat
    strcat(filepath, fileDirectory);
    strcat(filepath, rtc.formatDate(0x3B));
    strcat(filepath, fileExtension);

    sdFile = SD.open(filepath, FILE_WRITE);
    if(sdFile){ // if file was opened incorrectly
        sdFile.print("*"); // this char marks a reset
        sdFile.println(rtc.formatTime());
    }
    else{
        Buzzer(500, false);
        Buzzer(500, false);
    }
    sdFile.close();
}

void loop(){

    if(isSwitchTriggered){
        updateState();
        isSwitchTriggered = false;
    }

    if(state == 2){ // out: unten, in: oben --> normal operation
        // after fifty days of continious looping, this number will overflow and might break the program
        unsigned long currentMillis = millis();

        if(currentMillis > smartLedTimer){
            digitalWrite(LED_PIN, LOW);
        }
        
        if(checkCrankHS()){
            int dt = currentMillis - crankLastTrigger; // with high cadence of 100 per minute, the average time delta will be 600ms
            
            if(dt > CRANK_COOLDOWN){
                crankLastTrigger = currentMillis;
                updateCadence(dt);
            }
        }

        if(checkWheelHS()){
            int dt = currentMillis - wheelLastTrigger; // with my current wheels, at a speed of 40km/h, the average time delta will be 180ms
            
            if(dt > WHEEL_COOLDOWN){
                wheelLastTrigger = currentMillis;
                updateSpeed(dt);
            }
        }

        if(currentMillis - lastMPU > MPU_UPDATE_FREQUENCY){
            int dt = currentMillis - lastMPU;
            lastMPU = currentMillis;
            getMotionWithoutLib(dt);
        }

        if(currentMillis - lastWriteToSD > WRITE_INTERVAL){
            lastWriteToSD = currentMillis;
            writeToSD();

        }
    } 
    
    else if(state == 3){ // out: unten, in: unten --> antiTheft
        // Anti-Theft works by detecting a change in acceleration, for example by falling over or someone taking the bike
        // if that is the case, it waits for an amount of time if the bike really is moving and not just laying on the ground
        // if two crank or wheel hs pulses within a reasonable amount of time occur, the bike is being taken away and an alarm is activated

        if(millis() > antiTheftLedTimer){
            if(antiTheftLedOn){ // if the led is on, turn it off for 4000 ms
                digitalWrite(LED_PIN, LOW);
                antiTheftLedOn = false;
                antiTheftLedTimer = millis() + 4000;
            }
            else{ // if led is off, turn on for 100 ms
                digitalWrite(LED_PIN, HIGH);
                antiTheftLedOn = true;
                antiTheftLedTimer = millis() + 100;
            }
        }

        float sumOfLastAcc = AccX + AccY + AccZ;
        getAcc();
        float deltaAcc = AccX + AccY + AccZ - sumOfLastAcc;

        // if the Acceleration has changed significantly
        if( ANTI_THEFT_ACC_SENSITIVITY < abs(deltaAcc) ){
            unsigned long startTime = millis();

            unsigned long wheelTriggerTime = 0;
            unsigned long crankTriggerTime = 0;
            while( millis() - startTime < ANTI_THEFT_ALERT_TIME ){
                
                
                if( checkCrankHS() ){
                    if( millis() - crankTriggerTime < CRANK_HIGH_CUTOFF && millis() - crankTriggerTime > CRANK_COOLDOWN ){
                        // ALARM
                        Alarm();

                        // After an alarm, force the arduino into sleep mode
                        state = 0;
                        break;
                    }
                    crankTriggerTime = millis();
                }
                if( checkWheelHS() ){
                    if( millis() - wheelTriggerTime < WHEEL_HIGH_CUTOFF && millis() - wheelTriggerTime > WHEEL_COOLDOWN ){
                        // ALARM
                        Alarm();

                        // After an alarm, force the arduino into sleep mode
                        state = 0;
                        break;
                    }
                    wheelTriggerTime = millis();
                }
            }
            delay(50); // wait for the bike to maybe accelerate
        }
    }
    
    else if(state == 0){ // out: oben, in: oben --> sleep mode
        // turn off the led
        digitalWrite(LED_PIN, LOW);

        // enter mpu into sleep mode
        Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
        Wire.write(0x6B);                  // Talk to the register 6B
        Wire.write(0x40);                  // set bit 6 of register 6B to 1 --> enable sleep mode
        Wire.endTransmission(true);        // end the transmission
        
        // put the arduino into sleep mode
        delay(200);
        set_sleep_mode(SLEEP_MODE_PWR_DOWN);
        sleep_enable();
        sleep_mode();
        
        // the program starts from here once any interrupt is triggered
        sleep_disable(); 

        // re-initialise everything to prevent errors if for example the SD card was taken out during sleep
        resetFunc();

        // this should never happen
        Buzzer(200, false);
    }
    
    else if(state == 1){ // out: oben, in: unten --> not used for now
        // just blink LED to indicate activity
        digitalWrite(LED_PIN, HIGH);
        delay(200);
        digitalWrite(LED_PIN, LOW);
        delay(200);
    }
    
    else isSwitchTriggered = true;

    // this DOES NOT WORK FOR CASE 3 for whatever reason!!! it just won't switch to case 3 when state == 3!!!! FUCK YOU
    /*
    switch(state){
        case 0: // out: oben, in: oben --> sleep mode

            // turn off the led
            digitalWrite(LED_PIN, LOW);

            // enter mpu into sleep mode
            Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
            Wire.write(0x6B);                  // Talk to the register 6B
            Wire.write(0x40);                  // set bit 6 of register 6B to 1 --> enable sleep mode
            Wire.endTransmission(true);        // end the transmission
            
            // put the arduino into sleep mode
            delay(200);
            set_sleep_mode(SLEEP_MODE_PWR_DOWN);
            sleep_enable();
            sleep_mode();
            
            // the program starts from here once any interrupt is triggered
            sleep_disable(); 

            // re-initialise everything to prevent errors if for example the SD card was taken out during sleep
            resetFunc();

            // this should never happen
            Buzzer(1, 200, false);

            break;
        case 1: // out: oben, in: unten --> not used for now
            break;
        case 2: // out: unten, in: oben --> normal operation
            
            // after fifty days of continious looping, this number will overflow and might break the program
            unsigned long currentMillis = millis();

            if(currentMillis > smartLedTimer){
                digitalWrite(LED_PIN, LOW);
            }
            
            if(checkCrankHS()){
                int dt = currentMillis - crankLastTrigger; // with high cadence of 100 per minute, the average time delta will be 600ms
                
                if(dt > CRANK_COOLDOWN){
                    crankLastTrigger = currentMillis;
                    updateCadence(dt);
                }
            }

            if(checkWheelHS()){
                int dt = currentMillis - wheelLastTrigger; // with my current wheels, at a speed of 40km/h, the average time delta will be 180ms
                
                if(dt > WHEEL_COOLDOWN){
                    wheelLastTrigger = currentMillis;
                    updateSpeed(dt);
                }
            }

            if(currentMillis - lastWriteToSD > WRITE_INTERVAL){
                int dt = currentMillis - lastWriteToSD;
                lastWriteToSD = currentMillis;
                writeToSD(dt);

                // speed test
                loopsPerSec = loopsPerSec * 1000 / WRITE_INTERVAL; // write interval is in ms, thus *1000
                Serial.print("Loops per second: ");
                Serial.println(loopsPerSec);
                loopsPerSec = 0;

            }

            break;
        case 3: // out: unten, in: unten --> antiTheft
            // Anti-Theft works by detecting a change in acceleration, for example by falling over or someone taking the bike
            // if that is the case, it waits for an amount of time if the bike really is moving and not just laying on the ground
            // if two crank or wheel hs pulses within a reasonable amount of time occur, the bike is being taken away and an alarm is activated
            Serial.println("hello?");
            float sumOfLastAcc = AccX + AccY + AccZ;
            getAcc();
            float deltaAcc = AccX + AccY + AccZ - sumOfLastAcc;

            Serial.println(abs(deltaAcc));

            // if the Acceleration has changed significantly
            if( ANTI_THEFT_ACC_SENSITIVITY < abs(deltaAcc) ){
                Serial.println("sensitivity ");
                unsigned long startTime = millis();

                unsigned long wheelTriggerTime = 0;
                unsigned long crankTriggerTime = 0;
                while( millis() - startTime < ANTI_THEFT_ALERT_TIME ){
                    
                    
                    if( checkCrankHS() ){
                        if( millis() - crankTriggerTime < CRANK_HIGH_CUTOFF && millis() - crankTriggerTime > CRANK_COOLDOWN ){
                            // ALARM
                            //Alarm();
                            Serial.println("Crank Alarm");
                        }
                        crankTriggerTime = millis();
                    }
                    if( checkWheelHS() ){
                        if( millis() - wheelTriggerTime < WHEEL_HIGH_CUTOFF && millis() - wheelTriggerTime > WHEEL_COOLDOWN ){
                            // ALARM
                            //Alarm();
                            Serial.println("Wheel alarm");
                        }
                        wheelTriggerTime = millis();
                    }
                }
                delay(50); // wait for the bike to maybe accelerate
            }

            break;
        default: // default shouldn't happen, so update the state
            isSwitchTriggered = true;
            
    }
    */
}

bool checkCrankHS(){ // make as one func
    // if the value is different from the value without a magnet, return true
    int HSdelta = analogRead(CRANK_HS_PIN) - idleCrankHS;
    if( -CRANK_SENSITIVITY > HSdelta || HSdelta > CRANK_SENSITIVITY ){
        return true;
    }
    return false;
}

bool checkWheelHS(){
    // if the value is different from the value without a magnet, return true
    int HSdelta = analogRead(WHEEL_HS_PIN) - idleWheelHS;
    if( -WHEEL_SENSITIVITY > HSdelta || HSdelta > WHEEL_SENSITIVITY ){
        return true;
    }
    return false;
}

void updateCadence(int dt){
    if(dt < CRANK_HIGH_CUTOFF){
        float fdt = float(dt);

        float cadenceNow = CRANK_FACTOR / fdt;

        // in one write cycle (10s long), the sum of dt will equal 10s, thus cadence = 0 + 1 * result (over time)
        cadence = cadence + fdt/float(WRITE_INTERVAL) * cadenceNow;
    }
}

void updateSpeed(int dt){
    if(dt < WHEEL_HIGH_CUTOFF){
        float fdt = float(dt);

        float speedNow = SPEED_FACTOR / fdt;
        speed = speed + fdt/float(WRITE_INTERVAL) * speedNow;
    }
}

/*
float correctHSVal(float value, unsigned int sumOfDt){
    // sum of dt is not reset each write_interval, thus the missing dt automatically averages out over multiple write_intervals, making this unneccessary
    // correct speed for the missing time since sumOfDtWheel should equal WRITE_INTERVAL, but it can be off by as much as one dt
    return value + (float(WRITE_INTERVAL - sumOfDt) / float(WRITE_INTERVAL)) * value; 
}*/

void getAcc(){
    Wire.beginTransmission(MPU);
    Wire.write(0x3B); // Start with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
    //For a range of +-2g, we need to divide the raw values by 16384, according to the datasheet
    AccX = (Wire.read() << 8 | Wire.read()) / 16384.0; // X-axis value
    AccY = (Wire.read() << 8 | Wire.read()) / 16384.0; // Y-axis value
    AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0; // Z-axis value
}

void getMotionWithoutLib(int dt) {
    // === Read acceleromter data === //

    Wire.beginTransmission(MPU);
    Wire.write(0x3B); // Start with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
    //For a range of +-2g, we need to divide the raw values by 16384, according to the datasheet
    AccX = (Wire.read() << 8 | Wire.read()) / 16384.0; // X-axis value
    AccY = (Wire.read() << 8 | Wire.read()) / 16384.0; // Y-axis value
    AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0; // Z-axis value
    // Calculating Roll and Pitch from the accelerometer data
    accAngleX = (atan(AccY / sqrt(pow(AccX, 2) + pow(AccZ, 2))) * 180 / PI); // AccErrorX See the calculate_IMU_error()custom function for more details
    accAngleY = (atan(-1 * AccX / sqrt(pow(AccY, 2) + pow(AccZ, 2))) * 180 / PI); // AccErrorY 
    
    // === Read gyroscope data === //

    float elapsedTime = float(dt) / 1000.0; // Divide by 1000 to get seconds
    Wire.beginTransmission(MPU);
    Wire.write(0x43); // Gyro data first register address 0x43
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
    float GyroX = (Wire.read() << 8 | Wire.read()) / 131.0; // For a 250deg/s range we have to divide first the raw value by 131.0, according to the datasheet
    float GyroY = (Wire.read() << 8 | Wire.read()) / 131.0;
    float GyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;
        
        // i can do all these corrections better in post
    // Correct the outputs with the calculated error values
    //GyroX = GyroX - GyroErrorX; // GyroErrorX
    //GyroY = GyroY - GyroErrorY; // GyroErrorY
    //GyroZ = GyroZ - GyroErrorZ; // GyroErrorZ
    // Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
    /*gyroAngleX = gyroAngleX + GyroX * elapsedTime; // deg/s * s = deg
    gyroAngleY = gyroAngleY + GyroY * elapsedTime;
    yaw =  yaw + GyroZ * elapsedTime;
    // Complementary filter - combine acceleromter and gyro angle values
    roll = 0.96 * gyroAngleX + 0.04 * accAngleX;
    pitch = 0.96 * gyroAngleY + 0.04 * accAngleY;*/

    roll = roll + GyroX * elapsedTime; // deg/s * s = deg
    pitch = pitch + GyroY * elapsedTime;
    yaw =  yaw + GyroZ * elapsedTime;
    // Complementary filter - combine acceleromter and gyro angle values
    roll = 0.92 * roll + 0.08 * accAngleX;
    pitch = 0.92 * pitch + 0.08 * accAngleY;
}

void getTemperature(){
    // this is needed in forced mode
    bme.takeForcedMeasurement();
    delay(2);

    temperature = bme.readTemperature();
    pressure = bme.readPressure() / 100.0F;
    humidity = bme.readHumidity();
}

void writeToSD(){
    smartLed(500);

    getTemperature();

    // this makes a new txt file for each day
    memset(filepath, 0, sizeof(filepath)); // this completly clears the string for strcat
    strcat(filepath, fileDirectory);
    strcat(filepath, rtc.formatDate(0x3B));
    strcat(filepath, fileExtension);

    sdFile = SD.open(filepath, FILE_WRITE);

    if(sdFile){
        // structure of the CSV (comma seperated values) text file is:
        // hh:mm:ss, cadence, speed, temperature, pressure, humidity, AccX, AccY, AccZ, Roll, Pitch, Yaw 
        
        sdFile.print(rtc.formatTime());     sdFile.print(comma);
        sdFile.print(cadence);              sdFile.print(comma);
        sdFile.print(speed);                sdFile.print(comma);
        sdFile.print(temperature);          sdFile.print(comma);
        sdFile.print(pressure);             sdFile.print(comma);
        sdFile.print(humidity);             sdFile.print(comma);
        sdFile.print(AccX);                 sdFile.print(comma);
        sdFile.print(AccY);                 sdFile.print(comma);
        sdFile.print(AccZ);                 sdFile.print(comma);
        sdFile.print(roll);                 sdFile.print(comma);
        sdFile.print(pitch);                sdFile.print(comma);
        sdFile.print(yaw); 
        sdFile.println();
    }
    else{
        Buzzer(200, false);
        Buzzer(200, false);
    }
    sdFile.close();

    /*
    Serial.print(rtc.formatTime());     Serial.print(comma);
    Serial.print(cadence);              Serial.print(comma);
    Serial.print(speed);                Serial.print(comma);
    Serial.print(temperature);          Serial.print(comma);
    Serial.print(pressure);             Serial.print(comma);
    Serial.print(humidity);             Serial.print(comma);
    Serial.print(AccX);                 Serial.print(comma);
    Serial.print(AccY);                 Serial.print(comma);
    Serial.print(AccZ);                 Serial.print(comma);
    Serial.print(roll);                 Serial.print(comma); 
    Serial.print(pitch);                Serial.print(comma);
    Serial.print(yaw); 
    Serial.println(); */

    // after these global values have been printed, they need to be reset to 0 for the next cycle
    cadence = 0;

    speed = 0;
}

void switchISR(){
    isSwitchTriggered = true;
}

void updateState(){
    // format the two switches as a number from 0 to 3
    state = (digitalRead(SWITCH_OUT) << 1) + digitalRead(SWITCH_IN);
}

// instead of using delay(), this sets an end time that gets checked in loop
void smartLed(unsigned int time){
    digitalWrite(LED_PIN, HIGH);
    smartLedTimer = millis() + time;
}

void Buzzer(unsigned int duration, bool loud){

    // this uses delay and will mess with the rest of the program, but since an error already occured, it doesn't really matter
    digitalWrite(BUZZER_BASE, HIGH);
    if(loud) digitalWrite(BUZZER_EN, HIGH);
    digitalWrite(LED_PIN, HIGH);

    delay(duration);

    digitalWrite(BUZZER_BASE, LOW);
    digitalWrite(BUZZER_EN, LOW);
    digitalWrite(LED_PIN, LOW);
    delay(duration);
    
}

void Alarm(){
    
    sdFile = SD.open("README.txt", FILE_WRITE);

    if(sdFile){
        sdFile.print(rtc.formatTime());
        sdFile.print(F(", "));
        sdFile.println(rtc.formatDate());
        sdFile.println(F("An alarm has been triggered. If you are not a thief, please contact the owner of this bike at yannick.he595@gmail.com"));
        sdFile.println(F("Ein Alarm wurde ausgelöst. Wenn Sie kein Dieb sind, wenden Sie sich bitte an den Besitzer dieses Fahrrads unter yannick.he595@gmail.com "));
        sdFile.println(F("Został uruchomiony alarm. Jeśli nie jesteś złodziejem, skontaktuj się z właścicielem tego roweru pod adresem yannick.he595@gmail.com"));
        sdFile.println(F("Aktiviran je alarm. Ako niste lopov, kontaktirajte vlasnika ovog bicikla na yannick.he595@gmail.com"));
        sdFile.println(F("Sprožen je bil alarm. Če niste tat, se obrnite na lastnika tega kolesa na yannick.he595@gmail.com"));
        sdFile.println();
    }
    sdFile.close();

    Buzzer(1000, true); // change this to true for production code
    Buzzer(1000, true);
    Buzzer(1000, true);
    Buzzer(1000, true);
    Buzzer(1000, true);
    Buzzer(1000, true);
}
