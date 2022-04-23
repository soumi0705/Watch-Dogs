#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define Status D0
#define Sensor D7
const char *ssid = "Life_1101";
const char *password = "Mataji2oz";
const char *mqtt_server = "broker.mqttdashboard.com";
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(espClient);
void setup()
{
  Serial.begin(115200);
  pinMode(Sensor, INPUT);  // declare sensor as input
  pinMode(Status, OUTPUT); // declare LED as output
  Serial.print("PIR Setup Completed!");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.print("Connected to WiFi :");
  Serial.println(WiFi.SSID());
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(MQTTcallback);
  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266"))
    {
      Serial.println("Connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe("smart_home_mcu/healthCheck");
}
void MQTTcallback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message received in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  String message;
  for (int i = 0; i < length; i++)
  {
    message = message + (char)payload[i];
  }
  Serial.print(message);
  Serial.println();
  Serial.println("-----------------------");
}
void loop()
{
  long state = digitalRead(Sensor);
  delay(1000);
  if (state == HIGH)
  {
    digitalWrite(Status, LOW);
    Serial.println("Motion detected!");
    client.publish("sensors/bed-room/control", "HIGH");
     client.publish("sensors/bed-room/control", "ON");
    delay(1000);
  }
  else
  {
    digitalWrite(Status, HIGH);
    Serial.println("Motion absent!");
    client.publish("sensors/bed-room/control", "LOW");
    delay(1000);
  }
  client.loop();
}
