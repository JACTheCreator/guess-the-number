from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from random import randint

from utils.say import say
from utils.guess_the_number import guess_your_number
from utils.common import set_next_intent, is_next_intent_error, handle_next_intent_error, set_prev_msg

from constants.mode import GUESS_ALEXA_NUMBER, GUESS_MY_NUMBER
from constants.game_state import GAME_IN_PROGRESS
from constants.intents import (GET_RANGE_INTENT, GET_NUMBER_INTENT,
                               AMAZON_YES_INTENT, AMAZON_NO_INTENT, 
                               GET_USER_GUESS_INTENT)

class GetRangeIntentHandler(AbstractRequestHandler):
    """Handler for Get Range Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(GET_RANGE_INTENT)(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        if is_next_intent_error(handler_input = handler_input, current_intent = [GET_RANGE_INTENT]):
            return handle_next_intent_error(handler_input = handler_input)

        min = handler_input.request_envelope.request.intent.slots["min"].value
        max = handler_input.request_envelope.request.intent.slots["max"].value

        if not min or not max:
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_RANGE_INTENT])            
            speech_text =  "You said an invalid range. An example of a valid range is 1 to 10. Please try again. " + say.getattempts()
            reprompt_text = say.didnothear() + speech_text
            set_prev_msg(handler_input, msg = say.getrange())
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)            
            return handler_input.response_builder.response

        if min > max:
            min, max = max, min

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['min'] = int(min)
        session_attr['max'] = int(max)
        session_attr['game_state'] = GAME_IN_PROGRESS
        attempts = session_attr['max_attempts']

        if session_attr['mode'] == GUESS_ALEXA_NUMBER:
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_NUMBER_INTENT, GET_USER_GUESS_INTENT])
            session_attr["alexa_number"] = randint(int(min), int(max))
            
            speech_text = say.guessalexanumber(min = min, max = max, attempts = attempts)
            reprompt_text = say.didnothear() + speech_text
            set_prev_msg(handler_input, msg = speech_text)
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)            
            return handler_input.response_builder.response


        elif session_attr['mode'] == GUESS_MY_NUMBER:
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])         
            session_attr['guessing_range'] = []
            session_attr['position'] = ''
            session_attr['alexa_guesses'] = []

            alexa_guess = guess_your_number(handler_input = handler_input)

            speech_text = (say.guessyournumberprompt(attempts = attempts, min = min, max = max) +
                           say.guessyournumber(alexa_guess = alexa_guess))

            reprompt_text = say.didnothear() + speech_text
            set_prev_msg(handler_input, msg = speech_text)
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False) 
            return handler_input.response_builder.response      
