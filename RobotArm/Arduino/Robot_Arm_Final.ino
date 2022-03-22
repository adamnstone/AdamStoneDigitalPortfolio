#include <Servo.h>

Servo base;
Servo forward;
Servo up;
Servo grab;

int quit = 0;
const int millisBeforeQuit = 2000;

void setup() {
  Serial.begin(9600);
  up.attach(3);
  forward.attach(5);
  base.attach(7);
  grab.attach(9);
  
  up.write(0);
  forward.write(160);
  base.write(0);
  grab.write(0);
}

int getSpaces(String s){
  int j = 0;
  for (int i = 0; i < s.length(); i++){
    if (s[i] == ' '){
      j++;
    }
  }
  return(j);
}

String recieveString(int len){
  int startMillis = millis();
  int millisWaited = 0;
  Serial.println("waiting");
  String toReturn = "";
  for (int j = 0; j < len; j++){
    toReturn += " ";
  }
  int i = 0;
  while (getSpaces(toReturn) > 0){
    if (Serial.available() > 0){
      toReturn[i] = Serial.read();
      i++;
    }
    millisWaited = millis() - startMillis;
    if (millisWaited >= millisBeforeQuit){
      quit = 1;
      return("0");
    }
  }
  Serial.println("RECIEVED: " + toReturn);
  return(toReturn);
}

void grabBox() {
  grab.write(90);
  delay(500);
  base.write(20);
  forward.write(10);
  up.write(20);
  delay(500);
  grab.write(0);
  delay(500);
  up.write(40);
  delay(500);
  base.write(40);
  delay(1000);
}

void rotateMotors(int g, int u, int f, int b){
  if (quit == 1){
    quit = 0;
    Serial.println("Quitting...");
    return;
  }
  base.write(b);
  forward.write(f);
  up.write(u);
  grab.write(g);
}

void loop() {
  Serial.println("Waiting for Signal");
  while (true){
    if (Serial.available() > 0){
      char msg = Serial.read();
      if (msg == 's'){
        break;
      }
    }
  }
  Serial.println("Signal Start Recieved");
  int is[4] = {0, 0, 0, 0};
  for (int i = 0; i < 4; i++){
    is[i] = recieveString(3).toInt();
    if (quit){
      break;
      Serial.println("Quit Identified");
    }
  }
  rotateMotors(is[0], is[1], is[2], is[3]);
  Serial.println("Movement Complete!");
  /*
  rotateMotors(0, 0, 0, 0);
  delay(1000);
  rotateMotors(10, 0, 0 ,0);
  delay(1000);
  rotateMotors(10, 10, 0, 0);
  delay(1000);
  rotateMotors(10, 10,10,0);
  delay(1000);
  rotateMotors(10,10,10,10);
  delay(1000);
  */
}
