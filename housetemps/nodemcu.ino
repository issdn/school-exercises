//        _                 _
//       | |               | |
//   __ _| |__   ___  _   _| |_
//  / _` | '_ \ / _ \| | | | __|
// | (_| | |_) | (_) | |_| | |_
//  \__,_|_.__/ \___/ \__,_|\__|
//
//  Temperature measurement with DHT11 Temperature and Humidity sensor,
//  Sending the data to asp.net api with LoL1n nodemcu v3.
//
//  Sources I used:
//  Asp.net intro: https://www.youtube.com/watch?v=2Ayfi7OJhBI&t=1103s
//  Elegoo Arduino Tut: https://www.elegoo.com/en-de/blogs/arduino-projects/elegoo-mega-2560-basic-starter-kit-tutorial
//  Asp.net uses HTTPS and other security but I didn't bother checking the certificate or fingerprint or whatever
//  so the line client.setInsecure(); is set.
//  Send every 30 seconds.

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include "DHT.h"

#define DHTTYPE DHT11
#define SSID "PLACEHOLDER"
#define WIFI_PASS "PLACEHOLDER"

uint8_t DHTPin = D4;
uint32_t port = 7145;
String ip = "localhost";
DHT dht(DHTPin, DHTTYPE);

// The data is being stored two times so that
// it only sends it when the temperature or humidity changes.
float lastTemperature = 22.00;
float lastHumidity = 50.00;
float temperature;
float humidity;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  pinMode(DHTPin, INPUT);
  dht.begin();
  WiFi.begin(SSID, WIFI_PASS);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) { delay(500); };
  Serial.println("Connected.");
}

void sendHttpsMessage(WiFiClientSecure client, float temperature, float humidity) {
  if (temperature == lastTemperature && humidity == lastHumidity) { return; };
  
  HTTPClient http;
  http.begin(client, "https://" + ip + "/api/Info");
  http.addHeader("Content-Type", "application/json");

  String request = "{\"temperature\":" + String(temperature) + ", \"humidity\":" + String(humidity) + "}";

  int responseCode = http.POST(request);

  if (responseCode < 0) {
    Serial.println(http.errorToString(responseCode));
  } else {
    Serial.println(responseCode);
    lastTemperature = temperature;
    lastHumidity = humidity;
  };
  http.end();
}


void loop() {
  if (WiFi.status() != WL_CONNECTED) { 
    Serial.println("Couldn't connect to WIFI.");
    return; 
  }
  
  WiFiClientSecure client;
  if(!client.connect(ip, port)) {
    Serial.println("Connection Failed!");
    client.stopAll();
    return;
  }

  temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  sendHttpsMessage(client, temperature, humidity);
  delay(30000);
}