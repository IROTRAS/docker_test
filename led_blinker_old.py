import RPi.GPIO as GPIO # always needed with RPi.GPIO  
from time import sleep  # pull in the sleep function from time module  

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  

GPIO.setup(17, GPIO.OUT)# set GPIO 17 for blue LED
GPIO.setup(18, GPIO.OUT)# set GPIO 18 for blue LED

blue17 = GPIO.PWM(17, 100)    # create object blue17 for PWM on port 25 at 100 Hertz  
blue18 = GPIO.PWM(18, 100)      # create object blue18 for PWM on port 24 at 100 Hertz  

blue17.start(0)              # start blue17 led on 0 percent duty cycle (off)  
blue18.start(100)              # blue18 fully on (100%)  

# now the fun starts, we'll vary the duty cycle to   
# dim/brighten the leds, so one is bright while the other is dim  

pause_time = 0.02           # you can change this to slow down/speed up  

try:
    # while True:  
    #     for i in range(0,101):      # 101 because it stops when it finishes 100  
    #         blue17.ChangeDutyCycle(i)  
    #         blue18.ChangeDutyCycle(100 - i)  
    #         sleep(pause_time)  
    #     for i in range(100,-1,-1):      # from 100 to zero in steps of -1  
    #         blue17.ChangeDutyCycle(i)  
    #         blue18.ChangeDutyCycle(100 - i)  
    #         sleep(pause_time) 
    while True:
        for i in range(0,101):      # 101 because it stops when it finishes 100  
            blue17.ChangeDutyCycle(i)
            blue18.ChangeDutyCycle(100 - i)
            sleep(pause_time)
        sleep(.07)
        for i in range(100,-1,-1):      # from 100 to zero in steps of -1  
            blue17.ChangeDutyCycle(i)
            blue18.ChangeDutyCycle(100 - i)
            sleep(pause_time)
        sleep(.07)
except KeyboardInterrupt:
    blue17.stop()            # stop the blue17 PWM output  
    blue18.stop()              # stop the blue18 PWM output  
    GPIO.output(17,False)
    GPIO.output(18,False)
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit  
