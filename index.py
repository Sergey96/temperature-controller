#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import serial
import requests
from os.path import join, dirname
from time import localtime, strftime

import os
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BOT_ID = os.getenv("BOT_ID")
MAX_TEMPERATURE = os.getenv("MAX_TEMPERATURE")
MIN_TEMPERATURE = os.getenv("MIN_TEMPERATURE")
COM_PORT = os.getenv("COM_PORT")
LOG_FILE = os.getenv("LOG_FILE")

if  TOKEN is None or CHAT_ID is None or BOT_ID is None or MAX_TEMPERATURE is None or MIN_TEMPERATURE is None or COM_PORT is None:
    print("Не могу найти настройки в файле .env: TOKEN, CHAT_ID, BOT_ID, MAX_TEMPERATURE, MIN_TEMPERATURE, COM_PORT")
    exit()

if  len(TOKEN) == 0 or  len(CHAT_ID) == 0 or len(BOT_ID) == 0 or len(MAX_TEMPERATURE) == 0 or len(MAX_TEMPERATURE) == 0 or len(COM_PORT) == 0:
    print("Настройки в файле .env не должны иметь пустое значение: TOKEN, CHAT_ID, BOT_ID, MAX_TEMPERATURE, MIN_TEMPERATURE, COM_PORT")
    exit()

ser = serial.Serial(COM_PORT, 9600)

logFile = LOG_FILE if LOG_FILE is not None else 'log.txt'
fp = open(logFile ,'a+') 

def  getIcon (oldTerm, termRadiator): 
    if  oldTerm < termRadiator and termRadiator >= int(MAX_TEMPERATURE): 
        return "\u25B2🔥"
    if  oldTerm < termRadiator: 
        return "\u25B2"
    
    if  oldTerm > termRadiator and termRadiator <= int(MIN_TEMPERATURE): 
        return "\u25BC❄"
    
    return "\u25BC"

def sendTelegram (msg):
    requests.get("https://api.telegram.org/" + BOT_ID + ":" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + msg)

def log (termRadiator, termRoom, humidity):
    file_line = strftime("%Y-%m-%d\t%H:%M:%S", localtime()) + "\tR:\t" + str(termRadiator) + "\t\xb0С\t" + "\tT:\t" + str(termRoom) + "\t\xb0С\tH:\t" + str(humidity) + "%\n"
    fp.write(file_line)  

def telegram (termRadiator, oldTerm, termRoom, humidity):
    answer = str(termRadiator) + "\xb0С " + getIcon(oldTerm, termRadiator)
    answer += " T:" + str(termRoom) + "\xb0С  H:" + str(humidity) + "%"
    sendTelegram (answer)

startTerm = 10
oldTerm = startTerm

while True:
    line = ser.readline()
    print(line)

    termRadiator = float(line[0:5])
    humidity = float(line[8:14])+5
    termRoom = float(line[16:21])+1

    log(termRadiator, termRoom, humidity)

    if abs(termRadiator-oldTerm) > 1: 
        telegram (termRadiator, oldTerm, termRoom, humidity)
        oldTerm = termRadiator
    sleep(60) 