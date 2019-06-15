from  random import randint

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.guess_the_number import guess_your_number
from utils.common import (set_next_intent, is_next_intent_error, 
                          handle_next_intent_error, is_prev_intent, 
                          set_game_state, is_current_game_state)

from constants.mode import GUESS_ALEXA_NUMBER, GUESS_MY_NUMBER
from constants.game_state import GAME_IN_PROGRESS, GAME_RESTARTED 
from constants.intents import (AMAZON_YES_INTENT, AMAZON_NO_INTENT,
                               GET_LOWER_INTENT, GET_HIGHER_INTENT,
                               GET_RANGE_INTENT, GET_NUMBER_INTENT,
                               GET_USER_GUESS_INTENT)
	                          
class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(AMAZON_YES_INTENT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Checking if this intent should play now.
        if is_next_intent_error(handler_input = handler_input, current_intent = [AMAZON_YES_INTENT]):
            return handle_next_intent_error(handler_input = handler_input)

        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes

        is_prev_low_high_intent = is_prev_intent(handler_input, intents = [GET_LOWER_INTENT, GET_HIGHER_INTENT])
        is_prev_range_intent = is_prev_intent(handler_input, intents = [GET_RANGE_INTENT])
        is_prev_yes_no_intent = is_prev_intent(handler_input, intents = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])
        is_prev_number_intent = is_prev_intent(handler_input, intents = [GET_NUMBER_INTENT])
        is_prev_user_guess_number_intent = is_prev_intent(handler_input, intents = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])

        should_game_restart = is_current_game_state(handler_input, state = GAME_RESTARTED) and is_prev_yes_no_intent

        if (is_prev_low_high_intent or is_prev_range_intent or should_game_restart):
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])

            speech_text = 'Yay! Do you want a rematch?'
            reprompt_text = say.didnothear() + speech_text
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
            return handler_input.response_builder.response 

        elif is_prev_yes_no_intent or is_prev_number_intent or is_prev_user_guess_number_intent:
            min = session_attr["min"]
            max = session_attr["max"]
            attempts = session_attr['attempts'] = session_attr['max_attempts'] 
            set_game_state(handler_input, state = GAME_RESTARTED)

            if session_attr["mode"] == GUESS_ALEXA_NUMBER:
                # Setting the next intent.
                set_next_intent(handler_input = handler_input, 
                                next_intent = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])
                session_attr["alexa_number"] = randint(int(min), int(max))
                
                speech_text = say.guessalexanumber(min = min, max = max, attempts = attempts)
                reprompt_text = say.didnothear() + speech_text
                handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
                return handler_input.response_builder.response

            if session_attr["mode"] == GUESS_MY_NUMBER:
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
                handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
                return handler_input.response_builder.response