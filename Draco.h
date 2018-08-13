#ifndef Draco_h
#define Draco_h
#include "Arduino.h"
#include <TimeLib.h>
#include <Wire.h>
#include <DS1307RTC.h>
#include <DHT.h>
class Draco {
	public:
		Draco(String name,
			  int Water_pin,
			  int RelativeHumidity_Temperature_pin,
			  int SoilHumidityDigitalPin,
			  int SoilHumidityAnalogPin,
			  int water_time,
			  int water_threshold,
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
		bool _watering;
		time_t _watering_time_init;
		DHT dht;
};
#endif

