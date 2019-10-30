# Interface a Stepper Motor with Raspberry Pi and L298N 
#pip install RPi.GPIO

import RPi.GPIO as GPIO
import time 


out1 = 13
out2 = 11
out3 = 15
out4 = 12
speed = .03 # Higher values equal slower speeds. 1 is slow, .001 is very fast
            # Lower speeds have higher torque. High speeds have a tendency to strip the motor. 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)




def motor_dispense_candy(num_candy):

    i=0
    positive=0
    negative=0
    y=0

    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)

    x = abs(200 * num_candy) # A complete rotation is 400; 180 degree rotation is 200

    for y in range(x,0,-1):
        if i==0:
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(speed)
            
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(speed)
        elif i==2:  
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(speed)
        elif i==3:    
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(speed)
        elif i==4:  
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(speed)
        elif i==5:
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(speed)
        elif i==6:    
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(speed)
        elif i==7:    
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(speed)
        if i==7:
            i=0
            continue
        i=i+1
          

def cleanup(): 
  GPIO.cleanup()

def motor_main():
  try:
    motor_dispense_candy(1)
  except KeyboardInterrupt: 
    cleanup()

if __name__ == "__main__":
  motor_main()


