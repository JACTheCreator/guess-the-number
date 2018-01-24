import logging
import os
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
	init()
	print ('#############launch#############')
	print ('Alexa Number: ', Global.myNumber)
	print ('My Attempts: ',Global.attempts)
	print ('#################################')
	speech_text = render_template('welcome')
	return question(speech_text)

@ask.intent('GetNumberIntent')
def get_number(number):
	print ('#########GetNumberIntent#########')
	print ('Alexa Number: ', Global.myNumber)
	print ('My Attempts: ',Global.attempts)
	print ('My Number: ',number)
	print ('#################################')	
	try:	
		if int(number) < 1 or int(number) > 10:
			speech_text = render_template('outofrange')
			return question(speech_text)
		elif int(number) == Global.myNumber:
			speech_text = render_template('correct')
			init()
			return statement(speech_text)
		if Global.attempts == 1:
			speech_text = render_template('outoftries', mynumber = Global.myNumber)
			init()
			return statement(speech_text)
		Global.attempts -= 1
		if Global.attempts == 1:
			attempt_text = 'attempt'
		else:
			attempt_text = 'attempts'	
		if int(number) < Global.myNumber:
			positon_text = 'lower'
		else:
			positon_text = 'higher'
		speech_text = render_template('wrong', positon = positon_text, attempt_word = attempt_text, attempts = Global.attempts)
		return question(speech_text)
	except:
		speech_text = render_template('notnumber')
		return question(speech_text)
@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text).reprompt(help_text)


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop():
	init()
	speech_text = render_template('bye')
	return statement(speech_text)

def init():
	Global.myNumber = randint(1, 10)
	Global.attempts = 3

class Global(object):
	myNumber = randint(1, 10)
	attempts = 3
	
@ask.session_ended
def session_ended():
	init()
	return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)