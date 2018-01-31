# import logging
# import os
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
# logging.getLogger('flask_ask').setLevel(logging.DEBUG)

myNumber = randint(1, 10)
attempts = 3

@ask.launch
def launch():
	init()
	print ('#############launch#############')
	print ('Alexa Number: ', myNumber)
	print ('My Attempts: ', attempts)
	print ('#################################')
	speech_text = render_template('welcome')
	return question(speech_text)

@ask.intent('GetNumberIntent')
def get_number(number):
	global myNumber
	global attempts
	print ('#########GetNumberIntent#########')
	print ('Alexa Number: ', myNumber)
	print ('My Attempts: ',attempts)
	print ('My Number: ',number)
	print ('#################################')	
	try:	
		if int(number) < 1 or int(number) > 10:
			speech_text = render_template('outofrange')
			return question(speech_text)
		elif int(number) == myNumber:
			speech_text = render_template('correct')
			init()
			return statement(speech_text)
		if attempts == 1:
			speech_text = render_template('outoftries', mynumber = myNumber)
			init()
			return statement(speech_text)
		attempts -= 1
		if attempts == 1:
			attempt_text = 'attempt'
		else:
			attempt_text = 'attempts'	
		if int(number) < myNumber:
			positon_text = 'lower'
		else:
			positon_text = 'higher'
		speech_text = render_template('wrong', positon = positon_text, attempt_word = attempt_text, attempts = attempts)
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
	global myNumber
	global attempts
	myNumber = randint(1, 10)
	attempts = 3

	
@ask.session_ended
def session_ended():
	return "{}", 200


if __name__ == '__main__':
    # if 'ASK_VERIFY_REQUESTS' in os.environ:
    #     verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
    #     if verify == 'false':
    #         app.config['ASK_VERIFY_REQUESTS'] = False
    # app.run(debug=True)
    app.run()