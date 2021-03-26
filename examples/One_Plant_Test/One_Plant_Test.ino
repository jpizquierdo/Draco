
#include <Draco.h>
#include <TimeLib.h>
#include <TimeAlarms.h>
#include <Wire.h>
#include <DS1307RTC.h>

//Connect the SCL pin to the I2C clock SCL pin on your Arduino.
//On an UNO & '328 based Arduino, this is also known as A5, on a Mega it is also known as digital 21 and on a Leonardo/Micro, digital 3
const int RTC_SCL_pin = 21;

//Connect the SDA pin to the I2C data SDA pin on your Arduino.
//On an UNO & '328 based Arduino, this is also known as A4, on a Mega it is also known as digital 20 and on a Leonardo/Micro, digital 2
const int RTC_SDA_pin = 20;

//Plant 1 Configuration:
String name="Dragui";
const int Water_pin=22;
const int relay=24;
const int RelativeHumidity_Temperature_pin=2;
const int SoilHumidityDigitalPin=3;
const int SoilHumidityAnalogPin=A0;
int water_time=120;//in seconds
int water_threshold=60;
int min_temperature=15;
int max_temperature=40;

Draco Dragui(name,Water_pin,RelativeHumidity_Temperature_pin,SoilHumidityDigitalPin,SoilHumidityAnalogPin);
Draco Draguita("Draguita",Water_pin,RelativeHumidity_Temperature_pin,SoilHumidityDigitalPin,SoilHumidityAnalogPin);
Draco Pinzas("Pinzas",Water_pin,RelativeHumidity_Temperature_pin,SoilHumidityDigitalPin,SoilHumidityAnalogPin);
Draco *plants[3] = {&Dragui, &Draguita, &Pinzas};
const int plantsSize = sizeof(plants)/sizeof(plants[0]);

void setup() {
  // put your setup code here, to run once:
  pinMode(relay, OUTPUT);
  //Dragui.Setup();
  //Draguita.Setup();
  //Pinzas.Setup();
  for (int i=0; i < plantsSize; i++) {
    plants[i]->Setup();//Note the use of -> instead of . because you are using a pointer to the object.
    plants[i]->setWaterTime(water_time);
    plants[i]->setWaterThreshold(water_threshold);
    plants[i]->setMinTemperature(min_temperature);
    plants[i]->setMaxTemperature(max_temperature);
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
  Alarm.alarmRepeat(22,39,0,clock_testing);  // 21:00 every day
  Alarm.timerRepeat(5, clock_testing);// timer for every two weeks in seconds
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //Dragui.getName();
  
  for (int i=0; i < 1; i++) {
    //plants[i]->check_watering();//Note the use of -> instead of . because you are using a pointer to the object.
    Serial.println("******************");
    Serial.println("New reading debug");
    Serial.print("numero de plantas= ");
    Serial.println(plantsSize);

    Serial.println("******************\n");
  }

  for (int i=0; i < plantsSize; i++) {
      Serial.println("####################");
      Serial.println(plants[i]->getName());
      Serial.println("####################\n");
      Serial.print("Soil status: ");
      Serial.println(plants[i]->getSoilStatus());
      Serial.print("Soil humidity: ");
      Serial.print(plants[i]->getSoilHumidity());
      Serial.println("%");

      Serial.print("Air temperature: ");
      Serial.print(plants[i]->getTemperature());
      Serial.println("ºC");

      Serial.print("Relative Humidity: ");
      Serial.print(plants[i]->getRelativeHumidity());
      Serial.println("%");

      Serial.print("The water time is ");
      Serial.println(plants[i]->getWaterTime());

      Serial.print("The water threshold is ");
      Serial.println(plants[i]->getWaterThreshold());

      Serial.print("The minimum temperature is ");
      Serial.println(plants[i]->getMinTemperature());

      Serial.print("The maximum temperature is ");
      Serial.println(plants[i]->getMaxTemperature());
      Serial.println("\n");
      digitalWrite(relay,LOW);

    }
    //Dragui.water();

    tmElements_t tm;
  if (RTC.read(tm)) {
    Serial.print("Ok, Time = ");
    print2digits(tm.Hour);
    Serial.write(':');
    print2digits(tm.Minute);
    Serial.write(':');
    print2digits(tm.Second);
    Serial.print(", Date (D/M/Y) = ");
    Serial.print(tm.Day);
    Serial.write('/');
    Serial.print(tm.Month);
    Serial.write('/');
    Serial.print(tmYearToCalendar(tm.Year));
    Serial.println();
  } else {
    if (RTC.chipPresent()) {
      Serial.println("The DS1307 is stopped.  Please run the SetTime");
      Serial.println("example to initialize the time and begin running.");
      Serial.println();
    } else {
      Serial.println("DS1307 read error!  Please check the circuitry.");
      Serial.println();
    }
    delay(9000);
  }
  delay(4000);
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

void clock_testing() {
  //Serial.println("15 second timer");
  Dragui.water();
  //digitalWrite(relay,HIGH);
  delay(4000);
  //digitalWrite(relay,LOW);
  Dragui.water_off();
}

void print2digits(int number) {
  if (number >= 0 && number < 10) {
    Serial.write('0');
  }
  Serial.print(number);
}
