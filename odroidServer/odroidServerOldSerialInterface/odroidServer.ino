

#define digitalWrite_ 0
#define digitalRead_ 1
#define analogWrite_ 2
#define analogRead_ 3
int num_cmds = 3;

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

  Serial.begin(9600);
}

void getString(char *buf, int bufsize)
{
 int i;
 for (i=0; i<bufsize - 1; ++i)
 {
   while (Serial.available() == 0); // wait for character to arrive
   buf[i] = Serial.read();
   
//   if(i=0){
//    Serial.println("in start");
//      while(buf[0] != 62 && Serial.available()>0)
//        buf[0] = Serial.read();   
//    }
   
   
   if (buf[i] == 0){
    break;
    }
   buf[i] == 0;
 }
 
}


void respond(char **cmds){
  Serial.print(";");
  for (int i=1; i<=num_cmds; i++)
  {
    Serial.print(atoi(cmds[i]));
    Serial.print(";");
          
  }    
  Serial.println();
}

void loop() {
  char buf[32];
  getString(buf, sizeof(buf));
  Serial.println(buf);
  char *p = buf;
  char *str;
  int i=0;
  
  char *cmds[num_cmds];
  while ((str = strtok_r(p, ";", &p)) != NULL){ // delimiter is the semicolon
    
    cmds[i]=str;
    i++;
  }
  
    switch(atoi(cmds[1])){
      case digitalWrite_:
        digitalWrite(atoi(cmds[2]), atoi(cmds[3]));
        
        break;
      case digitalRead_:
        cmds[3] = "0" ;
        sprintf (cmds[3], "%03i", digitalRead(atoi(cmds[2])));
        
        break;
      case analogWrite_:
        analogWrite(atoi(cmds[2]), atoi(cmds[3]));
        break;
      case analogRead_:
        
        Serial.print("result: ");
        Serial.println(analogRead(atoi(cmds[2])));
        cmds[3] = "0" ;
        sprintf (cmds[3], "%03i", analogRead(atoi(cmds[2])));
        Serial.println(cmds[3]);
        break;
      default:
        cmds[0] = ">";
        cmds[1] = "0";
        cmds[2] = "0";
        cmds[3] = "0";
        Serial.println(F("unknown command;"));
        break;
    };
    respond(cmds);
  
      
    delete cmds;
    delete p;
    delete str;
 
}
  
  
  

