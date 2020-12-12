
#define CLOCK 8
#define MANUAL 9
#define ANA 0
#define DIR 7
#define ADP 3
#define ADM 2


#define SIDERAL_SPEED 14.95902778
//#define SIDERAL_SPEED 4.986342593


double cor[21];
int Time=0;
int IndexErreur=0;


volatile long int Compteur = 0;  //Compteur pour interruption
double Step=0.016;
double Target=SIDERAL_SPEED;
//double Target;
double Erreur=0.0;
byte TrigCalc=0;
long int Valeur;
long int CorValeur;
boolean ManualMode=false;
int Joy0;
byte AdpRead,AdmRead; 


 void(* resetFunc) (void) = 0;//declare reset function at address 0
 
 void setup()
 {
    pinMode(CLOCK, OUTPUT);
    pinMode(DIR, OUTPUT);
    pinMode(MANUAL,INPUT);
    pinMode(ADP,INPUT);
    pinMode(ADM,INPUT);
    Joy0=analogRead(0);
    digitalWrite(DIR,1);
    digitalWrite(CLOCK,1);
    Valeur=round((Target+Erreur)/Step);
    Time=0;
    IndexErreur=0;
    // Initialise le Timer 2 pour déclencher les interruptions à intervalle régulier
    TCCR2A = 0; //default 
    TCCR2B = 0b00000001; // clk/256 est incrémenté toutes les 16uS  
    TIMSK2 = 0b00000001; // TOIE2 
    sei();               // autorise les interruptions


cor[0]=1.0;
cor[1]=1.0;
cor[2]=1.0;
cor[3]=1.0;
cor[4]=1.0;
cor[5]=1.0;
cor[6]=1.0;
cor[7]=1.0;
cor[8]=1.0;
cor[9]=1.0;
cor[10]=1.0;
cor[11]=1.0;
cor[12]=1.0;
cor[13]=1.0;
cor[14]=1.0;
cor[15]=1.0;
cor[16]=1.0;
cor[17]=1.0;
cor[18]=1.0;
cor[19]=1.0;

cor[20]=cor[0];

   Serial.begin(115200);
  }
   
  // Boucle principale
  void loop() 
  {
  int Val;
  int Joystick;
  int Delay;
  double Interpo=0.0;

 
  if (!ManualMode)
  {
    if ((TrigCalc) && (Compteur>10))
    {
      //Serial.println(Target);
      digitalWrite(CLOCK,1);
      Valeur=round((Target+Erreur)/Step);
      Erreur=Target-(double)Valeur*Step;
      TrigCalc=0;
      if (Time>2005)
      { 
         IndexErreur++;
         Time=0;
      }
      if (IndexErreur>19) IndexErreur=0;
      Interpo=(double)Time/2005.0;
    //Serial.println(Target);
    }


    digitalWrite(DIR,1);
    AdpRead=digitalRead(ADP);
    AdmRead=digitalRead(ADM);
    if (AdpRead==0) 
    {
	   Target=SIDERAL_SPEED/2;
    }
    else
    {

	   Target=SIDERAL_SPEED*(cor[IndexErreur]*(1-Interpo)+cor[IndexErreur+1]*Interpo);
    }
    //Serial.println(CorValeur);
  }
  else
  {
       Joystick=analogRead(0);
       //Serial.println(Joystick);
       Joystick=Joystick-Joy0;
       
  if (Joystick<-180) Joystick=-350;
  if (Joystick>180) Joystick=350;
  
       if (abs(Joystick)<16) Joystick=0;
       if (Joystick>0)    
       {
          digitalWrite(DIR,0); 
       }
       else
       {
          digitalWrite(DIR,1);
       }
       
       Joystick=abs(Joystick);
       //Serial.println(Joystick);
       if (Joystick!=0)
       {
          digitalWrite(CLOCK,0);
          delayMicroseconds(10);
          digitalWrite(CLOCK,1);
          if (Joystick>300) 
            Delay=50;
          else
            Delay=(-32*Joystick+16390)/10;
          delayMicroseconds(Delay);
       }
  }
  
  
  if (digitalRead(MANUAL)==0)
  {
    ManualMode=true;
  }
  else
  {
    if (ManualMode) resetFunc(); //call reset 
  }
}
     
// routine d'interruption du timer
ISR (TIMER2_OVF_vect) 
{  



  if ((Compteur++ == Valeur) && (!ManualMode))
  {
    //Valeur=round((Target+Erreur)/Step);
    //Erreur=Target-(double)Valeur*Step;
    //Valeur=730;
    Time++;
    if (AdmRead==1)
    {
       digitalWrite(CLOCK,0);
       TrigCalc=1;
   }
    Compteur=0;  

  }  
} 
