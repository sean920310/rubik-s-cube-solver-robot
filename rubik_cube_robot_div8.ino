#define U_DIR      12
#define U_STEP     15
#define R_DIR      10
#define R_STEP     11
#define F_DIR      8
#define F_STEP     9
#define D_DIR      6
#define D_STEP     7
#define L_DIR      4
#define L_STEP     5
#define B_DIR      2
#define B_STEP     3
#define DISABLE    16

#define STEPS_PER_090    400
#define STEPS_PER_180    800

#define M_F 0
#define M_B 1
#define M_L 2
#define M_R 3
#define M_D 4
#define M_U 5

#define CCW     1
#define CW      0

int move_and_move_delay = 0 ;

#define motor_div 8

byte delay90[50*motor_div+1];
byte delay180[100*motor_div+1];

int get_DIR_PIN(int motor ){
  switch( motor ) {
       case M_F: return F_DIR;
       case M_B: return B_DIR;
       case M_L: return L_DIR;
       case M_R: return R_DIR;
       case M_D: return D_DIR;
       case M_U: return U_DIR;
    }
}
    
int get_STEP_PIN(int motor ){
  switch( motor ) {
       case M_F: return F_STEP;
       case M_B: return B_STEP;
       case M_L: return L_STEP;
       case M_R: return R_STEP;
       case M_D: return D_STEP;
       case M_U: return U_STEP;
    }
}

int getDelay90(int n){
   return delay90[n]+50;
}

int getDelay180(int n){
  return delay180[n]+50;
}


void turn090( int motor, int dir ) {
    digitalWrite( get_DIR_PIN( motor ), dir );
    int stepPin = get_STEP_PIN( motor );
    for( int i = 0; i < STEPS_PER_090; i++ ) {
        digitalWrite( stepPin, 1 );
        digitalWrite( stepPin, 0 );
        delayMicroseconds( getDelay90(i) );
    }
    delay( move_and_move_delay );
}

void turn180( int motor, int dir ) {
    digitalWrite( get_DIR_PIN( motor ), dir );
    int stepPin = get_STEP_PIN( motor );
    for( int i = 0; i < STEPS_PER_180; i++ ) {
        digitalWrite( stepPin, 1 );
        digitalWrite( stepPin, 0 );
        delayMicroseconds( getDelay180(i) );
    }
    delay( move_and_move_delay );
}

void turn090_180( int motor1, int dir1, int motor2, int dir2 ) {
    digitalWrite( get_DIR_PIN( motor1 ), dir1 );
    digitalWrite( get_DIR_PIN( motor2 ), dir2 );

    int stepPin1 = get_STEP_PIN( motor1 );
    int stepPin2 = get_STEP_PIN( motor2 );
    for( int i = 0; i < STEPS_PER_180; i++ ) {
        if( i % 2 == 0 ) {//tricky part, only step half the time
            digitalWrite( stepPin1, 1 );
            digitalWrite( stepPin1, 0 );
        }
        digitalWrite( stepPin2, 1 );
        digitalWrite( stepPin2, 0 );
        delayMicroseconds( getDelay180(i) );
    }
    delay( move_and_move_delay );
}

void turn180_090( int motor1, int dir1, int motor2, int dir2 ) {
    turn090_180( motor2, dir2, motor1, dir1 );
    delayMicroseconds( move_and_move_delay );
}

void turn180_180( int motor1, int dir1, int motor2, int dir2 ) {
    digitalWrite( get_DIR_PIN( motor1 ), dir1 );
    digitalWrite( get_DIR_PIN( motor2 ), dir2 );

    int stepPin1 = get_STEP_PIN( motor1 );
    int stepPin2 = get_STEP_PIN( motor2 );
    for( int i = 0; i < STEPS_PER_180; i++ ) {
        digitalWrite( stepPin1, 1 );
        digitalWrite( stepPin1, 0 );
        digitalWrite( stepPin2, 1 );
        digitalWrite( stepPin2, 0 );
        delayMicroseconds( getDelay180(i) );
    }
    delay( move_and_move_delay );
}

void turn090_090( int motor1, int dir1, int motor2, int dir2 ) {
    digitalWrite( get_DIR_PIN( motor1 ), dir1 );
    digitalWrite( get_DIR_PIN( motor2 ), dir2 );

    int stepPin1 = get_STEP_PIN( motor1 );
    int stepPin2 = get_STEP_PIN( motor2 );
    for( int i = 0; i < STEPS_PER_090; i++ ) {
        digitalWrite( stepPin1, 1 );
        digitalWrite( stepPin1, 0 );
        digitalWrite( stepPin2, 1 );
        digitalWrite( stepPin2, 0 );
        delayMicroseconds( getDelay90(i) );
    }
    delay( move_and_move_delay );
}

//////////////////////////////setup()//////////////////
void setup() {
  Serial.begin(115200);
  gen_delay90(3);
  gen_delay180(3);
  for(int i = 2 ; i<=16 ; i++){
    pinMode(i , OUTPUT);
  }
  Serial.println("ok");
  for(int i = 0 ; i<STEPS_PER_090 ; i++){
   Serial.println(getDelay90(i));
  }
}//setup


unsigned long start_time;
/////////////////////////////loop//////////////////////
void loop() {
  char cmd;
    if(Serial.available()>0){cmd = Serial.read();}
    else{start_time = millis();}
      
    switch(cmd){
          
      
       //F/B
/*F   */  case 'a': turn090       ( M_F,  CW           ); Serial.print('a'); break;
/*F2  */  case 'b': turn180       ( M_F,  CW           ); Serial.print('b'); break;
/*F'  */  case 'c': turn090       ( M_F, CCW           ); Serial.print('c'); break;
/*F B */  case 'd': turn090_090   ( M_F,  CW, M_B,  CW ); Serial.print('d'); break;
/*F2B */  case 'e': turn180_090   ( M_F,  CW, M_B,  CW ); Serial.print('e'); break;
/*F'B */  case 'f': turn090_090   ( M_F, CCW, M_B,  CW ); Serial.print('f'); break;
/*  B */  case 'g': turn090       (           M_B,  CW ); Serial.print('g'); break;
/*F B2*/  case 'h': turn090_180   ( M_F,  CW, M_B,  CW ); Serial.print('h'); break;
/*F2B2*/  case 'i': turn180_180   ( M_F,  CW, M_B,  CW ); Serial.print('i'); break;
/*F'B2*/  case 'j': turn090_180   ( M_F, CCW, M_B,  CW ); Serial.print('j'); break;
/*  B2*/  case 'k': turn180       (           M_B, CCW ); Serial.print('k'); break;
/*F B'*/  case 'l': turn090_090   ( M_F,  CW, M_B, CCW ); Serial.print('l'); break;
/*F2B'*/  case 'm': turn180_090   ( M_F,  CW, M_B, CCW ); Serial.print('m'); break;
/*F'B'*/  case 'n': turn090_090   ( M_F, CCW, M_B, CCW ); Serial.print('n'); break;
/*  B'*/  case 'o': turn090       (           M_B, CCW ); Serial.print('o'); break;

        //L/R
/*  L */  case 'p': turn090       ( M_L,  CW           ); Serial.print('p'); break;
/*  L2*/  case 'q': turn180       ( M_L,  CW           ); Serial.print('q'); break;
/*  L'*/  case 'r': turn090       ( M_L, CCW           ); Serial.print('r'); break;
/*R L */  case 's': turn090_090   ( M_L,  CW, M_R,  CW ); Serial.print('s'); break;
/*R L2*/  case 't': turn180_090   ( M_L,  CW, M_R,  CW ); Serial.print('t'); break;
/*R L'*/  case 'u': turn090_090   ( M_L, CCW, M_R,  CW ); Serial.print('u'); break;
/*R   */  case 'v': turn090       (           M_R,  CW ); Serial.print('v'); break;
/*R2L */  case 'w': turn090_180   ( M_L,  CW, M_R,  CW ); Serial.print('w'); break;
/*R2L2*/  case 'x': turn180_180   ( M_L,  CW, M_R,  CW ); Serial.print('x'); break;
/*R2L'*/  case 'y': turn090_180   ( M_L, CCW, M_R,  CW ); Serial.print('y'); break;
/*R2  */  case 'z': turn180       (           M_R, CCW ); Serial.print('z'); break;
/*R'L */  case 'A': turn090_090   ( M_L,  CW, M_R, CCW ); Serial.print('A'); break;
/*R'L2*/  case 'B': turn180_090   ( M_L,  CW, M_R, CCW ); Serial.print('B'); break;
/*R'L'*/  case 'C': turn090_090   ( M_L, CCW, M_R, CCW ); Serial.print('C'); break;
/*R'  */  case 'D': turn090       (           M_R, CCW ); Serial.print('D'); break;

        //U/D
/*U   */  case 'E': turn090       ( M_U,  CW           ); Serial.print('E'); break;
/*U2  */  case 'F': turn180       ( M_U,  CW           ); Serial.print('F'); break;
/*U'  */  case 'G': turn090       ( M_U, CCW           ); Serial.print('G'); break;
/*U D */  case 'H': turn090_090   ( M_U,  CW, M_D,  CW ); Serial.print('H'); break;
/*U2D */  case 'I': turn180_090   ( M_U,  CW, M_D,  CW ); Serial.print('I'); break;
/*U'D */  case 'J': turn090_090   ( M_U, CCW, M_D,  CW ); Serial.print('J'); break;
/*  D */  case 'K': turn090       (           M_D,  CW ); Serial.print('K'); break;
/*U D2*/  case 'L': turn090_180   ( M_U,  CW, M_D,  CW ); Serial.print('L'); break;
/*U2D2*/  case 'M': turn180_180   ( M_U,  CW, M_D,  CW ); Serial.print('M'); break;
/*U'D2*/  case 'N': turn090_180   ( M_U, CCW, M_D,  CW ); Serial.print('N'); break;
/*  D2*/  case 'O': turn180       (           M_D, CCW ); Serial.print('O'); break;
/*U D'*/  case 'P': turn090_090   ( M_U,  CW, M_D, CCW ); Serial.print('P'); break;
/*U2D'*/  case 'Q': turn180_090   ( M_U,  CW, M_D, CCW ); Serial.print('Q'); break;
/*U'D'*/  case 'R': turn090_090   ( M_U, CCW, M_D, CCW ); Serial.print('R'); break;
/*  D'*/  case 'S': turn090       (           M_D, CCW ); Serial.print('S'); break;
              //啟用和停用馬達
          case '7':digitalWrite( DISABLE, 1 ); break; //停用
          case '8':digitalWrite( DISABLE, 0 ); break; //啟用
              //計時功能
          case 13 :Serial.print("pass time is : ");
                   Serial.print((millis()-start_time)/1000.0000);
                   Serial.println("second") ;
                   break;
          case '0':gen_delay90(0);
                   gen_delay180(0);
                   for(int i = 0 ; i<STEPS_PER_090 ; i++){Serial.println(getDelay90(i));}
                   break;
          case '1':gen_delay90(1);
                   gen_delay180(1);
                   for(int i = 0 ; i<STEPS_PER_090 ; i++){Serial.println(getDelay90(i));}
                   break;
          case '2':gen_delay90(2);
                   gen_delay180(2);
                   for(int i = 0 ; i<STEPS_PER_090 ; i++){Serial.println(getDelay90(i));}
                   break;
          case '3':gen_delay90(3);
                   gen_delay180(3);
                   for(int i = 0 ; i<STEPS_PER_090 ; i++){Serial.println(getDelay90(i));}
                   break;
                   
    }
      
}//loop



////////////////////////////  make delay time ///////////////////

/////final/ start_w_set 2300 / MAX_speed_set 3500 / acc_set 37000 

///////////////////////sat mode:      **0**    **1**   **2**   **3**
//////////////////////mode type:      show     slow    safe    fast
const int     start_w_set[5]         { 750   , 1800  , 2000  , 2300  ,        };
const int     MAX_speed_set[5]       { 800   , 3500  , 3400  , 3500  ,        };
const float   acc_set[5]             { 5000  , 20000 , 28000 , 37000 ,        };
const int move_and_move_delay_set[5] { 300   , 40     , 0     , 0     ,        };

void gen_delay90(int speed_mode){
    move_and_move_delay = move_and_move_delay_set[speed_mode];
    const int start_w = start_w_set[speed_mode];   //起始速度
    const double deg = 1.8/motor_div;     //每次旋轉的角度
    const int MAX_speed = MAX_speed_set[speed_mode]; //最高速度
    
    double acc = acc_set[speed_mode]; //加速度(只看大小)
    double w = 0; //角速度 deg/sec
    int t ;       //延遲時間
    
    w = start_w;
    for (int n = 0 ; n<50*motor_div ; n++){
        if (n> STEPS_PER_090 /2 & acc>0){acc*=-1;}
        if (!n> STEPS_PER_090 /2 & acc<0){acc*=-1;}
        t = deg/w*1000000;
        if (w > MAX_speed){t = deg/MAX_speed*1000000;}
        delay90[n] = t-50;
        w = sqrt(pow(w , 2 ) + acc*2*deg);
    }  
}

void gen_delay180(int speed_mode){
    move_and_move_delay = move_and_move_delay_set[speed_mode];
    const int start_w = start_w_set[speed_mode];   //起始速度
    const double deg = 1.8/motor_div;     //每次旋轉的角度
    const int MAX_speed = MAX_speed_set[speed_mode]; //最高速度
    
    double acc = acc_set[speed_mode];//加速度
    double w = 0; //角速度 deg/sec
    int t ;       //延遲時間
    
    w = start_w;
    for (int n = 0 ; n<100*motor_div ; n++){
        if (n> STEPS_PER_180 /2 & acc>0){acc*=-1;}
        if  (!n> STEPS_PER_180 /2 & acc<0){acc*=-1;}
        t = deg/w*1000000;
        if (w > MAX_speed){t = deg/MAX_speed*1000000;}
        delay180[n] = t-50;
        w = sqrt(pow(w , 2 ) + acc*2*deg);
     }  
}
        
