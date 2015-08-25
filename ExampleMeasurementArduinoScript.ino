// A script to measure time between to events

//Initialize global variables
int ledRed = 8;                //Red LED pin
int ledGreen = 9;              //Green LED pin
int sensorCurrent = 10;        //Sensor pin
int sensorRed = 0;             //Red laser light sensor
int sensorGreen = 0;           //Green laser light sensor
int measurements = 0;          //Number of measurements done
int numberOfMeasurements = 1;  //Measurements to be done (must be the same as nSamples in the Python script)
float t1;                      //Initial time (time at the start of the measurement)
float t2;                      //End time (time at the end of the measurement)
float total;                   //t2-t1 Time interval (positive)
boolean green = false;         //Check variable. If true the red sensor has been triggered, therefore the green can be triggered
boolean currentOn = false;     //True: the current to the light sensors is on

//Setup function
void setup() 
{
  //Initialize serial port at 9600 baud
  Serial.begin(9600);
  
  //Initialize LED pins
  pinMode(ledRed,OUTPUT);
  pinMode(ledGreen,OUTPUT);
  pinMode(sensorCurrent,OUTPUT);
}

//Main loop
void loop()
{
  //Turn sensor current on
  if(!currentOn)
  {
    digitalWrite(sensorCurrent,HIGH);
    currentOn = true;
  }
  
  //Read sensor values
  sensorRed = analogRead(A0);
  sensorGreen = analogRead(A1);
  
  //Debugging//
  //Serial.println(sensorRed);
  
  //If red sensor is triggered start counting time
  //and light the red LED (pin 8)
  if(sensorRed > 1000)
  {
    t1 = micros();
    green = true;
    digitalWrite(ledRed,HIGH);
  }
  
  //If green sensor is triggered stop counting and
  //print out the time. Light the green LED (pin 9)
  if((sensorGreen > 900) && (green))
  {
    t2 = micros();
    total = (t2 - t1);
    Serial.println(total);
    digitalWrite(ledGreen,HIGH);
    
    //Wait 1 sec
    delay(1000);

    //Turn LEDs off and increment the number of measurements done
    digitalWrite(ledRed,LOW);
    digitalWrite(ledGreen,LOW);
    green = false;
    measurements = measurements + 1;
    
    //If the number of measurements done is equal to the number of the required, the current
    //to the light sensors is cut off.
    if(measurements >= numberOfMeasurements)   //Only one measurement is done in this case, 
    {                                          //then the current to the sensors is cut off
      digitalWrite(sensorCurrent,LOW);
    }   
  }
}
