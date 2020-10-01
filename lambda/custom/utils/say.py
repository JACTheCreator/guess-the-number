from constants.intents import (LAUNCH_REQUEST, GET_GUESS_ALEXA_NUMBER_INTENT,
                               GET_GUESS_MY_NUMBER_INTENT, GET_ATTEMPTS_INTENT,
                               GET_RANGE_INTENT, GET_HIGHER_INTENT,
                               GET_LOWER_INTENT, GET_NUMBER_INTENT, 
                               AMAZON_YES_INTENT, AMAZON_NO_INTENT,
                               AMAZON_HELP_INTENT, AMAZON_CANCEL_INTENT,
                               AMAZON_STOP_INTENT, SESSION_ENDED_REQUEST, GET_USER_GUESS_INTENT) 

class say(object):
	@staticmethod
	def welcome():
		return """
			Welcome to Guess the number. I have two modes. 
			In the first mode, I will attempt to guess the number 
			that you are thinking of. In the second mode, you can attempt 
			to guess the number I am thinking of. What mode would you like
			to play.
    		If you need any assistance, just say help.
	  	"""

	@staticmethod
	def getrange():
		return """ 
    		What is the guessing range of the numbers in this game? An example is 1 to 10.
  		"""

	@staticmethod
	def getattempts():
  		return """
    		How many attempts are needed in this game?
  		"""

	@staticmethod
	def guessalexanumber(min, max, attempts):
		return """
			I am thinking of a number between {} and {}! 
			What number am I thinking of? 
			You have {} attempts! 
			Go!
		""".format(min, max, attempts)

	@staticmethod
	def guessyournumberprompt(attempts , min , max):
		return """
			I will use {} attempts to guess the number that you are thinking of.
			Your number is between {} and {}. I will go now! 
		""".format(attempts, min, max)

	@staticmethod
	def guessyournumber(alexa_guess):
		return """
			Are you thinking of {}?
		""".format(alexa_guess)

	@staticmethod
	def notnumber():
		return """
	    	Please say a number. Try again.
	  	"""

	@staticmethod
	def outofrange(min, max):
		return """
			Silly! That number is not between {} and {}.
		""".format(min, max)

	@staticmethod
	def correct():
		return """
			Yay! You got it!
		"""

	@staticmethod
	def wrong(guessed_number, positon, attempts, attempt_word):
		return """
			Nope!
			{} is {} than my number.
			You need to go {}.
			You got {} {} left
		""".format(guessed_number, positon[0], positon[1], attempts, attempt_word)

	@staticmethod
	def outoftries(alexa_number):
		return """
			You are out of tries!
			I was thinking of {}.
			Better luck next time.
		""".format(alexa_number)
	
	@staticmethod
	def didnothear():
		return """
			I did not get that. 
		"""

	@staticmethod
	def help(prev_msg):
		return """
			This game contains two modes. In both modes, alexa will ask
			for the amount of attempts needed, and the guessing range. The value for 
			the attempts should be greater than 0. The numbers used for the guessing range 
			should be positive. An example of this 1 to 10 or, 1 to 15. 
			In the first mode, I will attempt to guess the number 
			that you are thinking of. In the second mode, you can attempt 
			to guess the number I am thinking of. I will now continue from where I left off.
		""" + prev_msg

	@staticmethod
	def bye():
		return """
			GoodBye
		"""

	@staticmethod
	def exceptionerror():
		return """
			Sorry, there was some problem. Please try again Later!!
		"""

	@staticmethod
	def unabletoguess():
		return """
			This is weird! I am unable to guess another number!
		"""

	@staticmethod
	def numberthinkingof():
		return """
			What number were you thinking of?
		"""

	@staticmethod
	def next_intent_error_handle(intent, handler_input):
		invalid_speech = 'Silly! That is not right! I was expecting you to tell me'
		
		if set(intent) == set([GET_GUESS_MY_NUMBER_INTENT, GET_GUESS_ALEXA_NUMBER_INTENT]):
			return invalid_speech + """
			the game mode. Just say guess your number 
			if you want to guess my number, or, say guess my secret number 
			if you want me to guess your secret number.
			"""
		
		if set(intent) == set([GET_ATTEMPTS_INTENT, GET_NUMBER_INTENT]):
			return invalid_speech + """
			how many guessing attempts are in this game.
			"""
		
		if set(intent) == set([GET_RANGE_INTENT]):
			return invalid_speech + """
			the range of the numbers to guess. 
			"""
		
		if set(intent) == set([GET_NUMBER_INTENT]):
			return invalid_speech + """
			a number that I am thinking of.
			"""
		
		if set(intent) == set([GET_LOWER_INTENT, GET_HIGHER_INTENT]):
			return invalid_speech + """
			if the number I guess is higher or lower than yours.
			"""
		
		if set(intent) == set([AMAZON_YES_INTENT, AMAZON_NO_INTENT]):
			alexa_guess = handler_input.attributes_manager.session_attributes['alexa_guesses'][-1]
			return invalid_speech + """
			YES or NO. Are you thinking of {}? 
			""".format(alexa_guess)
		
		if set(intent) == set([GET_HIGHER_INTENT, GET_LOWER_INTENT]):
			alexa_guess = handler_input.attributes_manager.session_attributes['alexa_guesses'][-1]
			return invalid_speech + """
			To go High or Low! Is your number higher or lower that {} 
			""".format(alexa_guess)
		
		if set(intent) == set([GET_NUMBER_INTENT, GET_USER_GUESS_INTENT]):
			return invalid_speech + """
			the number that i was thinking.	
			""" 