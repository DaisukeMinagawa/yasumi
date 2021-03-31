# -*- coding: utf-8 -*-

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def yasumiLaunch():
    message='やすみちゃん起動しました。ご主人様、お疲れ様です。'
    #今日もご一緒させていただきます。'
    f = open('yasumi_voice.txt', 'w')
    f.write(message)
    f.close()
    os.system('python yasumi_voice.py yasumi_voice.txt')

def startTimer():
    message='五十二分間お仕事頑張ってください。'
    f = open('yasumi_voice.txt', 'w')
    f.write(message)
    f.close()
    os.system('python yasumi_voice.py yasumi_voice.txt')

def restTimer():
    message='デスクから十七分間離れて休憩してください'
    f = open('yasumi_voice.txt', 'w')
    f.write(message)
    f.close()
    os.system('python yasumi_voice.py yasumi_voice.txt')

def endTimer():
    message='お仕事再会のお時間です。一緒に頑張りましょう、ご主人様'
    f = open('yasumi_voice.txt', 'w')
    f.write(message)
    f.close()
    os.system('python yasumi_voice.py yasumi_voice.txt')


if __name__ == '__main__':

  #yasumiLaunch()

  # get the countdown time in seconds
  setWorktime = 40 #52min = 3120
  setResttime = 20 #17min = 1020

  startTime = time.time()
  finishTime52 = startTime + setWorktime

  # loop until the current system time
  # is greater than the finishTime52
  currentSec=0
  cnt=0
  while GPIO.input(8)== GPIO.HIGH:
    print"I am waiting for response by button"
    if GPIO.input(8)== GPIO.LOW:
      while TRUE:
        cnt += 1
        time.sleep(0.1)
        if cnt <=10:
          print"Button is pushed short"
          print "Let's work 52min"
          startTimer()
          break
        elif cnt >10:
          print"You have pused 1+sec"
          print "Let's work 52min"
          startTimer()
          break

  while time.time() < finishTime52:

    # show loop is running
    currentSec += 1
    print currentSec
    # wait for one second
    time.sleep(1)
  
    print "Rest 17min"

    startTime = time.time()
    finishTime17 = startTime + setResttime

    print "Let's rest 17min"
    currentSec2=0
      
  while time.time() < finishTime17:

    # show loop is running
    currentSec2 += 1
    print currentSec

    # wait for one second
    time.sleep(1)

    print "You have rested 17min!"

