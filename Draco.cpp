#include "Arduino.h"
#include "Draco.h"
#include <TimeLib.h>
#include <Wire.h>
#include <DS1307RTC.h>
#include <DHT.h>
#define DHTTYPE DHT11
//http://polygondoor.com.au/creating-classes-in-c-for-arduino/
Draco::Draco (
	String name,
	int Water_pin,
	int RelativeHumidity_Temperature_pin,
	int SoilHumidityDigitalPin,
	int SoilHumidityAnalogPin,
	int water_time,
	int water_threshold,
	int min_temperature,
	int max_temperature)
{
	_name=name;
	_Water_pin=Water_pin;
	_RelativeHumidity_Temperature_pin=RelativeHumidity_Temperature_pin;
	_SoilHumidityDigitalPin=SoilHumidityDigitalPin;
	_SoilHumidityAnalogPin=SoilHumidityAnalogPin;
	_water_time=water_time;
	_water_threshold=water_threshold;
	_min_temperature=min_temperature;
	_max_temperature=max_temperature;
	DHT dht(RelativeHumidity_Temperature_pin, DHTTYPE);
}

void Draco::Setup()
{
	pinMode(_Water_pin, OUTPUT);
	pinMode(_SoilHumidityDigitalPin, INPUT);
	dht.begin();
}

int Draco::getSoilHumidity()
{
	return analogRead(_SoilHumidityAnalogPin);
}

int Draco::getSoilStatus()
{
	return digitalRead(_SoilHumidityDigitalPin);
}

float Draco::getRelativeHumidity()
{
	return dht.readHumidity();
}

float Draco::getTemperature()
{
	//return dht.readTemperature(true);//Fahrenheit
	return dht.readTemperature();
}

String Draco::getName()
{
	return _name;
}

void Draco::setName(String new_name)
{
	_name=new_name;
}

int Draco::getWaterTime()
{
	return _water_time;
}

void Draco::setWaterTime(int value)
{
	_water_time=value;
}

int Draco::getWaterThreshold()
{
	return _water_threshold;
}

void Draco::setWaterThreshold(int value)
{
	_water_threshold=value;
}

int Draco::getMinTemperature()
{
	return _min_temperature;
}

void Draco::setMinTemperature(int value)
{
	_min_temperature=value;
}

int Draco::getMaxTemperature()
{
	return _max_temperature;
}

void Draco::setMaxTemperature(int value)
{
	_max_temperature=value;
}

void Draco::water()
{	
	_watering_time_init = now();
	digitalWrite(_Water_pin, HIGH);
}

void Draco::check_watering()
{
	if ((digitalRead(_Water_pin) == true) && (now() - _watering_time_init >=_water_time)){	
		digitalWrite(_Water_pin, LOW);
	}
	//For future improvements
	/*if ((digitalRead(_Water_pin) == false) && (getSoilHumidity()<_water_threshold)){	
		digitalWrite(_Water_pin, HIGH);
	}*/
}

void Draco::water_off()
{
	digitalWrite(_Water_pin, LOW);
}
	
