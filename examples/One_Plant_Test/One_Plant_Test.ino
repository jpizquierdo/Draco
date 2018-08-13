
#include <Draco.h>
#include <TimeLib.h>
#include <TimeAlarms.h>
#include <Wire.h>
#include <DS1307RTC.h>

//Connect the SCL pin to the I2C clock SCL pin on your Arduino.
//On an UNO & '328 based Arduino, this is also known as A5, on a Mega it is also known as digital 21 and on a Leonardo/Micro, digital 3
int RTC_SCL_pin = 21;

//Connect the SDA pin to the I2C data SDA pin on your Arduino.
//On an UNO & '328 based Arduino, this is also known as A4, on a Mega it is also known as digital 20 and on a Leonardo/Micro, digital 2
int RTC_SDA_pin = 20;

//Plant 1 Configuration:
String name="Dragui";
int Water_pin=22;
int RelativeHumidity_Temperature_pin=2;
int SoilHumidityDigitalPin=3;
int SoilHumidityAnalogPin=A0;
int water_time=120;//in seconds
int water_threshold=300;
int min_temperature=5;
int max_temperature=40;

Draco Dragui(name,Water_pin,RelativeHumidity_Temperature_pin,SoilHumidityDigitalPin,SoilHumidityAnalogPin,water_time,water_threshold,min_temperature,max_temperature);
Draco Draguita("Draguita",Water_pin,RelativeHumidity_Temperature_pin,SoilHumidityDigitalPin,SoilHumidityAnalogPin,water_time,water_threshold,min_temperature,max_temperature);
Draco Pinzas("Pinzas",Water_pin,RelativeHumidity_Temperature_pin,SoilHumidityDigitalPin,SoilHumidityAnalogPin,water_time,water_threshold,min_temperature,max_temperature);
Draco *things[3] = {&Dragui, &Draguita, &Pinzas};

void setup() {
  // put your setup code here, to run once:
  //Dragui.Setup();
  //Draguita.Setup();
  //Pinzas.Setup();
  for (int i=0; i < 3; i++) {
    things[i]->Setup();//Note the use of -> instead of . because you are using a pointer to the object.
  }

  //RTC Setup
  Serial.begin(9600);
  while (!Serial) ; // wait until Arduino Serial Monitor opens
  setSyncProvider(RTC.get);   // the function to get the time from the RTC
  if(timeStatus()!= timeSet) 
     Serial.println("Unable to sync with the RTC");
  else
     Serial.println("RTC has set the system time");  
   
  //setTime(hour(),minute(),second(),day(),month(),year()); // set time to RTC time. dont needed
  //setTime(8,30,0,1,1,18); // set time to Saturday 8:30:00am Jan 1 2018
  Alarm.timerRepeat(1209600, two_weeks_water);// timer for every two weeks in seconds
  Alarm.alarmRepeat(21,0,0,all_days_water);  // 21:00 every day
  
}

void loop() {
  // put your main code here, to run repeatedly:
  Dragui.getName();
  for (int i=0; i < 3; i++) {
    things[i]->check_watering();//Note the use of -> instead of . because you are using a pointer to the object.
  }
  Alarm.delay(1000); // wait one second between clock display

}

void two_weeks_water() {
  //Serial.println("15 second timer");
  Dragui.water();
  Draguita.water();
}

void all_days_water() {
  //Serial.println("15 second timer");
  Pinzas.water();
}
