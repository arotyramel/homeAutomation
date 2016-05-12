

#define digitalWrite_ 0
#define digitalRead_ 1
#define analogWrite_ 2
#define analogRead_ 3
bool serialInComplete_ = false;
unsigned short maxStringLength_= 50;
String serialIn_;




void setup() {
  //relay 1-4
  for(int i=4;i<8;i++){
    pinMode(i,OUTPUT);
    digitalWrite(i,HIGH);
  }

  // Temp Sensor
  // VCC VOUT
  pinMode(A0,OUTPUT);
  digitalWrite(A0,HIGH);
  // Sensor VIN
  pinMode(A1,INPUT);

  //RF I/O
  // RX Module
  pinMode(A2,INPUT);
  // TX Module
  pinMode(A3,OUTPUT);
  digitalWrite(A3,LOW);

  //RF Power
  // Power RX Module
  pinMode(A6,OUTPUT);
  digitalWrite(A6,LOW);
  // Power TX Module
  pinMode(A7,OUTPUT);
  digitalWrite(A7,LOW);


  serialIn_.reserve(maxStringLength_);
  Serial.begin(9600);
}

void done(){
  
    // clear the string:
  serialIn_ = "";
  serialInComplete_ = false;
}

String getValue(String data, char separator, int index)
{
 int found = 0;
  int strIndex[] = {
0, -1  };
  int maxIndex = data.length()-1;
  for(int i=0; i<=maxIndex && found<=index; i++){
  if(data.charAt(i)==separator || i==maxIndex){
  found++;
  strIndex[0] = strIndex[1]+1;
  strIndex[1] = (i == maxIndex) ? i+1 : i;
  }
 }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void processSerialIn(){
  if (serialInComplete_){
    
      if(!serialIn_.startsWith(">")){
        Serial.println("unknown command");
        Serial.println(serialIn_);
        done();
        return;
      }
    
      int func = getValue(serialIn_, ';', 1).toInt();
      int pin = getValue(serialIn_, ';', 2).toInt();
  
      //Serial.println(func);
      //Serial.println(pin);
      
      int val;
      switch(func){
        case digitalWrite_:
          val = getValue(serialIn_, ';', 3).toInt();
          digitalWrite(pin, val);        
          break;
        case digitalRead_:
          val = digitalRead(pin);
          break;
        case analogWrite_:
          val = getValue(serialIn_, ';', 3).toInt();
          analogWrite(pin , val);
          break;
        case analogRead_:
          val = analogRead(pin);
          break;
        default:
          Serial.println(F("unknown func"));
          break;
      };

    Serial.print(">");
    Serial.print(";");
    Serial.print(func);
    Serial.print(";");
    Serial.print(pin);
    Serial.print(";");
    Serial.println(val);
    Serial.flush();

  done();
  }


}

void loop() {
processSerialIn();
}



void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    if (inChar == '\r') {
      serialInComplete_ = true;
      return;
    }
    if(serialIn_.length() > maxStringLength_)
    {
      serialInComplete_ = true;
      return;
     }
    serialIn_ += inChar;
  }
  
}
  
  

