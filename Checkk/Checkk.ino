#include <Wire.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);  

void setup() {
  Serial.begin(9600);  
  lcd.begin();         
  lcd.backlight();     
  pinMode(4, OUTPUT); // Red light
  pinMode(5, OUTPUT);  // green light
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();  
    
    
    lcd.clear();

    
    switch (received) {


      
      case '1':
        lcd.print("Object: Person");
        digitalWrite(4, LOW); 
         delay(1500);
        break;
      case '2':
        lcd.print("Object: car");
        digitalWrite(4, HIGH); 
        digitalWrite(5, LOW); 
        delay(1500); 
        break;
      case '3':
        lcd.print("Object: truck");
        digitalWrite(4, HIGH); 
        digitalWrite(5, LOW); 
        delay(1500); 
        break;
      case '4':
        lcd.print("Object: bus");
        digitalWrite(4, HIGH);  
        digitalWrite(5, LOW); 
        delay(1500);
        break;
        case '5':
        lcd.print("Object: train");
        digitalWrite(4, HIGH);  
        digitalWrite(5, LOW); 
        delay(1500);
        break;

      case '6':
        lcd.print("Object: motorcycle");
        digitalWrite(4, HIGH);  
        digitalWrite(5, LOW); 
        delay(1500);
        break;

      case '7':
        lcd.print("Object:bicycle");
        digitalWrite(4, HIGH); 
        digitalWrite(5, LOW); 
        delay(1500); 
        break;
      
      
      case '0':
        lcd.print("No Object Detected");
        digitalWrite(4, LOW);  
        digitalWrite(5, HIGH);  
        
        break;
      default:
        lcd.print("Unknown Object");
        digitalWrite(4, LOW);  
        digitalWrite(5, HIGH); 
        delay(1500);
        break;
    }

    
  }
}
