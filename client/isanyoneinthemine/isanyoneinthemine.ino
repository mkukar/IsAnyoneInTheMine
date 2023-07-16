/*
 * Is Anyone in the Mine?
 * Lights up when someone is playing minecraft!
 * 
 * Created by Michael Kukar 2023
 * 
 * 
 * TIPS and TRICKS
 * 
 * Note - I am using HiLetgo ESP-WROOM-32
 * 
 * Board Type: Node32s
 * To Program: Hold "IOO" (or whatever it says) button until "Hard resetting via RTS pin" appears
 * To Run: Press "EN" button
 */

#include <WiFi.h>
#include <HTTPClient.h>


const int LED_PIN = 2; // LED_PIN = 2 is board-included LED
const char* ssid = "My home wifi"; // wifi network
const char* pass = "hunter2"; // wifi password
const String REQUEST_URL = "https://YOURSERVERHERE.com/api/isanyoneinthemine"; // your server endpoint
const int DELAY_BETWEEN_REQUESTS_MS = 10000;

String responseText;
int responseStatus;

bool isAnyoneInTheMine() {
  HTTPClient httpclient;
  httpclient.begin(REQUEST_URL);
  responseStatus = httpclient.GET();
  if (responseStatus != HTTP_CODE_OK) {
    Serial.print("Failed to connect to API, status code: ");
    Serial.println(responseStatus);
    return false;
  }
  // response is {"isanyoneinthemine":true or false}, so we just search for "true" instead of parsing anything
  responseText = httpclient.getString();
  Serial.print("Response from server: ");
  Serial.println(responseText);
  httpclient.end();
  if (responseText.indexOf("true") > 0) {
    return true;
  }
  else {
    return false;
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  Serial.println("Is anyone in the mine?");
  Serial.println("Created by Michael Kukar 2023");
  Serial.println("Connecting to wifi...");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (isAnyoneInTheMine()) {
    digitalWrite(LED_PIN, HIGH);
  }
  else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(DELAY_BETWEEN_REQUESTS_MS);
}
