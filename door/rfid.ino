#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
Servo s;

#define ENA 7
#define IN1 8
#define IN2 9

#define SS_PIN 10
#define RST_PIN 5

#define SERVO_PIN 6

#define PUSH_BUTTON 2

unsigned long buttonPressStart = 0;
bool buttonHandled = false;

MFRC522 mfrc522(SS_PIN, RST_PIN);

#define OPEN 65
#define CLOSE 0

int DOOR_STATE = CLOSE;

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

void toggleDoor() {
  if (DOOR_STATE == OPEN) {
    s.write(CLOSE);
    DOOR_STATE = CLOSE;
  } else {
    s.write(OPEN);
    DOOR_STATE = OPEN;
  }
}

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  analogWrite(ENA, 255);
  stopMotor();

  pinMode(PUSH_BUTTON, INPUT_PULLUP);

  s.attach(SERVO_PIN);
  s.write(DOOR_STATE);

  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (readID()) {
    if (tagID == tag_UID1 || tagID == tag_UID2) {
      Serial.println("Authorized access");
      //forward();
      //delay(2000);
      //stopMotor();
      if(DOOR_STATE == OPEN){
        Serial.println("1");
        s.write(CLOSE);
        DOOR_STATE = CLOSE;
      }
      else{
        Serial.println("0");
        s.write(OPEN);
        DOOR_STATE = OPEN;
      }
    } else {
      Serial.println("Access denied");
      Serial.println(tagID);
      stopMotor();
    }
  }

bool currentState = digitalRead(PUSH_BUTTON);
if (currentState == LOW) {
  if (buttonPressStart == 0) {
    buttonPressStart = millis();   
  } else if (!buttonHandled && millis() - buttonPressStart >= 500) {
    toggleDoor();                 
    buttonHandled = true;        
  }
}

if (currentState == HIGH) {
  buttonPressStart = 0;
  buttonHandled = false;
}

  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == 'B') {      
      s.write(OPEN);
      DOOR_STATE = OPEN;
    }
    else if (cmd == 'F'){ 
      s.write(CLOSE);
      DOOR_STATE = CLOSE;
    }
  }
}
