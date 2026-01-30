#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
Servo s;

#define ENA 7
#define IN1 8
#define IN2 9

#define SS_PIN 10
#define RST_PIN 5

#define SERVO_PIN A0

MFRC522 mfrc522(SS_PIN, RST_PIN);

byte readCard[4];
String tag_UID1 = "6E8EAB4";
String tag_UID2 = "6FDD75";
String tagID = "";

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
}

void stopMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

boolean readID() {
  if (!mfrc522.PICC_IsNewCardPresent()) return false;
  if (!mfrc522.PICC_ReadCardSerial()) return false;

  tagID = "";
  for (uint8_t i = 0; i < 4; i++) {
    tagID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  tagID.toUpperCase();

  mfrc522.PICC_HaltA();
  return true;
}

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  analogWrite(ENA, 255);
  stopMotor();

  s.attach(SERVO_PIN);
  s.write(65);

  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (readID()) {
    if (tagID == tag_UID1 || tagID == tag_UID2) {
      Serial.println("Authorized");
      forward();
      delay(2000);
      stopMotor();
    } else {
      Serial.println("Access denied");
      Serial.println(tagID);
      stopMotor();
    }
  }
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == 'B') {      
      s.write(65);
    }
    else if (cmd == 'F'){ 
      s.write(0);
    }
  }
}
