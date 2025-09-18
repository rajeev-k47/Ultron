#include <SoftwareSerial.h>

const int tp1 = 8;
const int ep1 = 9;
const int tp2 = 10;
const int ep2 = 11;

const int dist_threshold = 100;
const int sequence_timeout = 800;
unsigned long t1 = 0, t2 = 0;
bool istrig1 = false, istrig2 = false;

float dr1, ds1, dr2, ds2;

int peoplein=0;

void setup() {
  Serial.begin(9600);
  pinMode(tp1, OUTPUT);
  pinMode(ep1, INPUT);
  pinMode(tp2, OUTPUT);
  pinMode(ep2, INPUT);

}

void loop() {
  digitalWrite(tp1, LOW);
  delayMicroseconds(2);
  digitalWrite(tp1, HIGH);
  delayMicroseconds(10);
  digitalWrite(tp1, LOW);
  dr1 = pulseIn(ep1, HIGH);
  ds1 = (dr1*.0343)/2;

  digitalWrite(tp2, LOW);
  delayMicroseconds(2);
  digitalWrite(tp2, HIGH);
  delayMicroseconds(10);
  digitalWrite(tp2, LOW);
  dr2 = pulseIn(ep2, HIGH);
  ds2 = (dr2*.0343)/2;

  unsigned long now = millis();

  if(ds1>0 && ds1<dist_threshold){
      if(!istrig1){
        istrig1=!istrig1;
        t1=now;
      }
  }
  if(ds2>0 && ds2<dist_threshold){
    if(!istrig2){
      istrig2=!istrig2;
      t2=now;
    }
  }
  if(istrig1&&istrig2){
    if(t1<t2 && (t2-t1)<sequence_timeout){
        peoplein++;
    }else if(t1>t2 && (t1-t2)<sequence_timeout){
      peoplein--;
      if(peoplein<0)peoplein=0;
    }
    istrig1=false;
    istrig2=false;
  }

  if(istrig1 && (now-t1)>sequence_timeout){
    istrig1=false;
  }
  if(istrig2 && (now-t2)>sequence_timeout){
    istrig2=false;
  }
  if(peoplein==0){
      Serial.println(peoplein);
  }else{
      Serial.println(peoplein);
  }
}

