from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.guess_the_number import guess_alexa_number
from utils.common import set_next_intent, is_next_intent_error, handle_next_intent_error

from constants.intents import (GET_USER_GUESS_INTENT, GET_NUMBER_INTENT)

class GetUserGuessIntentHandler(AbstractRequestHandler):
    """Handler for Get User Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(GET_USER_GUESS_INTENT)(handler_input)

    def handle(self, handler_input):
        #type: (HandlerInput) -> Response

        # Checking if this intent should play now.
        if is_next_intent_error(handler_input = handler_input, current_intent = [GET_USER_GUESS_INTENT]):
            return handle_next_intent_error(handler_input = handler_input)

        # Setting the next intent.
        set_next_intent(handler_input = handler_input, 
                        next_intent = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])

        return guess_alexa_number(handler_input)