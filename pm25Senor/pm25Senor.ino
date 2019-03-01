//當ardunio 接收到python 端發送訊號，Ardunio才讀取感測器的值，再傳給App繪圖

const byte dustPin=A0;
float dustVal=0;
int ledPower=2; //　to set pin2 which is LED of sensor controler
int delayTime=280;
int delayTime2=40;
float offTime=9680;
int receive = 0;
int relay = 10;

// initialize pin mode and fan status
void setup(){
  Serial.begin(9600);
  pinMode(ledPower,OUTPUT);
  pinMode(relay, OUTPUT);
  pinMode(dustPin, INPUT); // read data from dustPin pin
  
  digitalWrite(relay,LOW); // fan is off at the beginning 
}


void loop(){

  
  // to control sensor 
  digitalWrite(ledPower,LOW);
  delayMicroseconds(delayTime);
  dustVal=analogRead(dustPin);
  delayMicroseconds(delayTime2);
  digitalWrite(ledPower,HIGH);
  delayMicroseconds(offTime);


  
  
  // to read commands from python program 
  if (Serial.available())
  {
    /*如果接收到python 偵測的命令時 開始傳送感測器資料,*/
      receive = Serial.read();
      if (receive == 49) //字元'1'　ASCII code = 49
      {
            if (dustVal>36)
            {
              float value = (dustVal/1024-0.0356)*120000*0.035;
              Serial.println(value); // send PM2.5 value to python promgram
            }        
      }
      /*判斷命令是什麼？*/
      if (receive == 50) // read '2' from python, then turn on fan
      {
         digitalWrite(relay,HIGH); // HIGH is on , LOW is off
      }
      if (receive == 51) // read '3' from python, then turn off fan
      {
         digitalWrite(relay,LOW); // HIGH is on , LOW is off
      }
  }
}
