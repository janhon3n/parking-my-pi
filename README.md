# Raspberry pi peruutuskamera

Tietotekniikan laboratorio kurssi

Mikael Janhonen ja Adrian Borzyszkowski

## Projektin yleiskatsaus

Projektissa käytimme

* Rapsberry Pi 2 B
* HC-SR04 ultraääni läheisyysmittari
* joku Buzzeri

Käytössämme oli eri ultraäänimittari kuin tehtävänannossa. Kyseinen mittari ei käytä I2C väylää vaan kommunikaatio toimii 2 pinnin yli. Meillä ei myöskään ollut PWM:mää käyttävää buzzeria vaan tasajännitteellä toimiva vakiotaajuinen (ääni) buzzer.

Ultraäänimittarin etäisyysmittaus toimii kytkemällä Trigger pinnin ylös ja mittaamalla tämän jälkeen Echo pinniin tulevan pulssin pituuden. Echo pinni on kytketty pull down resistorilla myös maahan, jotta varaus ei jää leijumaan. Käyttämämme Buzzer toimii hyvin yksinkertaisesti pitäen ääntä vain, jos sen läpi on jännite.

Ultraäänimittari toimii hyvin ja etäisyydet ovat tarkkoja (tarkastettu viivottimella). Pitkän käytön jälkee jos etäisyyttä hakee liian tiheään mittari kuitenkin lakkaa toimimasta. Tämän vuoksi laitoimme koodiin pienille viivelle monta piippausta ennen kuin uusi etäisyys haetaan mittarista. Mittari antaa myös outoja lukemia, jos sen edessä on todella lähellä jotain (alle 2cm).

Piippausten viiveitä laskimme hieman eri tavalla kuin tehtävänannossa. Yli 60cm etäisyyksillä piippausta ei ole ja sitä matalammilla etäisyyksillä piippaustiheys nousee etäisyyden laskiessa piippausten pysyen kuitenkin saman pituisina (0.2s). Kuitenkin kun piippausten välillä oleva viive laskee alle 0.2 sekunnin alkaa myös piippausten kesto laskea. Teimme tämän siksi että buzzerin ääni on erittäin ärsyttävä ja mielestämme kyseinen toiminta on pienillä etäisyyksillä hyvin miellytävää.

## Python scripti

```Python

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
   print ("Pulssin kesto on %.111f sekunttia" % TimeElapsed)

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
      
```
