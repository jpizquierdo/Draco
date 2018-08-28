#ifndef Draco_h
#define Draco_h
#include "Arduino.h"
#include <TimeLib.h>
#include <Wire.h>
#include <DS1307RTC.h>
#include <DHT.h>
class Draco {
	public:
		Draco(String name="Plant 1",
			  int Water_pin=2,
			  int RelativeHumidity_Temperature_pin=3,
			  int SoilHumidityDigitalPin=4,
			  int SoilHumidityAnalogPin=A1,
			  int water_time=300,
			  int water_threshold=300,
			  int min_temperature=5,
			  int max_temperature=40);
		void Setup();
		int getSoilHumidity();
		int getSoilStatus();
		float getRelativeHumidity();
		float getTemperature();
		String getName();
		void setName(String new_name);
		int getWaterTime();
		void setWaterTime(int value);
		void water();
		void check_watering();
		void water_off();
		int getWaterThreshold();
		void setWaterThreshold(int value);
		int getMinTemperature();
		void setMinTemperature(int value);
		int getMaxTemperature();
		void setMaxTemperature(int value);
	private:
		String _name;
		int _Water_pin;
		int _RelativeHumidity_Temperature_pin;
		int _SoilHumidityDigitalPin;
		int _SoilHumidityAnalogPin;
		int _water_time;
		int _water_threshold;
		int _min_temperature;
		int _max_temperature;	
		time_t _watering_time_init;
		DHT dht;
};
#endif

