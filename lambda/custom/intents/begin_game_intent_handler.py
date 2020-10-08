from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from random import randint

from utils.say import say
from utils.guess_the_number import guess_your_number
from utils.common import set_next_intent, is_next_intent_error, handle_next_intent_error, set_prev_msg

from constants.mode import GUESS_ALEXA_NUMBER, GUESS_MY_NUMBER
from constants.game_state import GAME_IN_PROGRESS
from constants.intents import (GET_RANGE_INTENT, GET_NUMBER_INTENT, GET_RANGE_INTENT,
                               AMAZON_YES_INTENT, AMAZON_NO_INTENT, 
                               GET_USER_GUESS_INTENT, BEGIN_GAME_INTENT)

class BeginGameIntentHandler(AbstractRequestHandler):
    """Handler for Get Range Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(BEGIN_GAME_INTENT)(handler_input)
    
    def handle(self, handler_input):
        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes

        min = int(session_attr['min'])
        max = int(session_attr['max'])
        attempts = int(session_attr['attempts'])

        if min > max:
            min, max = max, min

        if session_attr['mode'] == GUESS_ALEXA_NUMBER:
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_NUMBER_INTENT])

            session_attr['alexa_number'] = randint(int(min), int(max))
            speech_text = say.guessalexanumber(min = min, max = max, attempts = attempts)
            reprompt_text = say.didnothear() + speech_text
            set_prev_msg(handler_input, msg = speech_text)
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False) 
            return handler_input.response_builder.response      

        else: # session_attr['mode'] == GUESS_MY_NUMBER:
            set_next_intent(handler_input = handler_input, 
                            next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT]) 
                            
            alexa_guess = guess_your_number(handler_input = handler_input)
            speech_text = (say.guessyournumberprompt(attempts = attempts, min = min, max = max) +
                           say.guessyournumber(alexa_guess = alexa_guess))

            reprompt_text = say.didnothear() + 'speech_text'
            set_prev_msg(handler_input, msg = speech_text)
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False) 
            return handler_input.response_builder.response      
