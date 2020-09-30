from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.common import (set_next_intent, is_next_intent_error, 
                          handle_next_intent_error, set_prev_msg)

from constants.mode import GUESS_ALEXA_NUMBER, GUESS_MY_NUMBER

from constants.game_state import GAME_NOT_IN_PROGRESS

from constants.intents import (GET_GUESS_ALEXA_NUMBER_INTENT, GET_GUESS_MY_NUMBER_INTENT,
                               GET_ATTEMPTS_INTENT, GET_NUMBER_INTENT,
                               GET_USER_GUESS_INTENT)


class GetGuessAlexaNumberorGetGuessMyNumberIntentHandler(AbstractRequestHandler):
    """Handler for Get Guess Alexa Number Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Setting the mode based on the user input.
        if is_intent_name(GET_GUESS_ALEXA_NUMBER_INTENT)(handler_input):
            session_attr["mode"] = GUESS_ALEXA_NUMBER
            return True           
        if is_intent_name(GET_GUESS_MY_NUMBER_INTENT)(handler_input):
            session_attr["mode"] = GUESS_MY_NUMBER
            return True           
        return  False

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Checking if this intent should play now.
        current_intent = [GET_GUESS_ALEXA_NUMBER_INTENT, GET_GUESS_MY_NUMBER_INTENT]
        if is_next_intent_error(handler_input = handler_input, current_intent = current_intent):
            return handle_next_intent_error(handler_input = handler_input)            

        # Setting the next intent.
        set_next_intent(handler_input = handler_input, 
                        next_intent = [GET_ATTEMPTS_INTENT, GET_NUMBER_INTENT, GET_USER_GUESS_INTENT])

        # Setting game state (to game not in progress)
        handler_input.attributes_manager.session_attributes['game_state'] = GAME_NOT_IN_PROGRESS

        # Asking the user for the amount of attempts in a game. 
        speech_text = say.getattempts() 
        reprompt_text = say.didnothear() + speech_text
        set_prev_msg(handler_input, msg = speech_text)
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response