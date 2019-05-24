
class say(object):
	def welcome():
		return """
	    	I am thinking of a number between 1 and 10... 
      		What number am i thinking of?
      		You have three attempts. Go!
	  	"""

	def getrange():
		return """ 
    		What is the range of the numbers to guess?
  		"""

	def getattempts():
  		return """
    		How many attempts are needed?
  		"""

	def guessalexanumber(min, max, attempts):
		return """
			I am thinking of a number between {} and {}! 
			What number am I thinking of? 
			You have {} attempts! 
			Go!
		""".format(min, max, attempts)

	def notnumber():
		return """
	    	Please say a number. Try again
	  	"""

	def outofrange(min, max):
		return """
			Silly! That number is not between {} and {}.
		""".format(min, max)

	def correct():
		return """
			Yay! You got it!
		"""

	def wrong(guessed_number, positon, attempts, attempt_word):
		return """
			Nope!
			{} is {} than my number.
			You need to go {}.
			You got {} {} left
		""".format(guessed_number, positon[0], positon[1], attempts, attempt_word)

	def outoftries(alexa_number):
		return """
			Oh No! You are out of tries.
			I was thinking of {}.
			Better luck next time.
		""".format(alexa_number)

	def help():
		return """
			I will pick a secret number between 1 and 10 
			and then tell you to start guessing.
			You should guess one number and say it out loud.
			If the guess was high, I will inform you that your number is high. 
			If the guess was low, I will inform you that your number is low. 
			You will have three attempts to get the correct number. 
			If you have run out of attempts I will tell you the secret number.
		"""

	def bye():
		return """
			GoodBye
		"""