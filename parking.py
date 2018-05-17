# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Käytetyt pinnit
GPIO_TRIGGER = 4
GPIO_ECHO = 17
GPIO_BUZZER = 19

# Aseta pinnien mode
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
GPIO.output(GPIO_BUZZER, False)

def distance():
   # Togglaa triggeri
   GPIO.output(GPIO_TRIGGER, True)
   time.sleep(0.00001)
   GPIO.output(GPIO_TRIGGER, False)

   StartTime = time.time()
   StopTime = time.time()

   # Päivitä StartTimea kunnes pulssi alkaa
   while GPIO.input(GPIO_ECHO) == 0:
      StartTime = time.time()

   # Päivitä StopTimea kunnes pulssi päättyy
   while GPIO.input(GPIO_ECHO) == 1:
      StopTime = time.time()

   # Laske ero
   TimeElapsed = StopTime - StartTime
   print ("Pulssin kesto on %.3f ms" % TimeElapsed*1000)

   # Kerro äänen nopeudella (34300 cm/s)
   # Jaa kahdella koska ääni menee edes takas
   return (TimeElapsed * 34300) / 2

while 1:
   dist = distance()
   print ("Mitattu pituus on %.1f cm" % dist)

   if dist > 60.0:
      time.sleep(1)
      continue

   # laske timeDelay ja buzzerDelay (30 tuntu hyvältä kertoimelta)
   timeDelay = dist * 30
   buzzerDelay = 0.2
   beepAmount = 1

   if timeDelay < 200: # pienillä viiveillä pieni buzzerDelay
      buzzerDelay = timeDelay / 1000
      beepAmount = 2

   if timeDelay < 50:
      beepAmount = 4

   for i in range(0,beepAmount):
      # Kytke buzzeria
      GPIO.output(GPIO_BUZZER, True)
      time.sleep(buzzerDelay)
      GPIO.output(GPIO_BUZZER, False)

      time.sleep(timeDelay / 1000)