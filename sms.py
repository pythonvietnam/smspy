#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import requests
import smssettings
import sys
import webbrowser

login_url = 'https://www.telenor.no/privat/minesider/logginnfelles.cms'
minside_url = 'https://www.telenor.no/privat/minesider/minside/minSidePage.cms'
smspage_url = 'https://www.telenor.no/privat/minesider/abonnement/mobil/umstjeneste/initUmsTjeneste.cms?setCurrentLocationToReturnOfFlow=true&umsUrl=SEND_SMS'
sendsms_url = 'https://telenormobil.no/norm/win/sms/send/process.do'

parser = argparse.ArgumentParser(description='Send an SMS')
parser.add_argument('phonenumber', type=int,
                   help='One 6 digit norwegian phone number: XXXXXXXX')
parser.add_argument('message', type=str,
                   help='Your message in double or single quotes, example: \"Hey mum\" ')
args = parser.parse_args()


def show(content):
    """Write HTML to file and open in browser"""
    
    with open('respons.html', 'w') as fil:
        fil.write(content.content)
    webbrowser.open('respons.html')


login_payload = {   
                'controller': 'com.telenor.consumer.web.action.login.LogginnfellesAction',\
                'lbAction': 'Logg inn',\
                'usr_name': smssettings.username,\
                'usr_password': smssettings.password, \
                '__checkbox_loginForm.rememberUsername': 'true',\
                'useAjax': 'true',\
                'loginForm.screenSize' : '1366x768',\
                'loginForm.windowSize' :' 1302x682',\
                'nyBrukerPersonaliaNameForm.firstName':'',\
                'nyBrukerPersonaliaNameForm.lastName':''}

sms_payload = { 'toAddress' : args.phonenumber, 
                'message' : args.message, 
                'b_send' : 'Send+SMS'}


sessionID = requests.Session()

login_get_response = sessionID.get(login_url)
show(login_get_response)

login_post_response = sessionID.post(login_url, login_payload)
show(login_post_response)

minside_response = sessionID.get(minside_url)
show(minside_response)

smspage_response = sessionID.get(smspage_url)
show(smspage_response)

sms_response = sessionID.post(sendsms_url, sms_payload)
show(smspage_response)
