from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.guess_the_number import guess_your_number
from utils.common import set_next_intent, is_next_intent_error, handle_next_intent_error

from constants.intents import (GET_HIGHER_INTENT, GET_LOWER_INTENT,
                               AMAZON_YES_INTENT, AMAZON_NO_INTENT,
                               GET_NUMBER_INTENT)

from constants.position import (HIGHER,
                                LOWER)

class GetLowerorHigherIntentHandler(AbstractRequestHandler):
    """Handler for High Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes

        # Setting the position based on the user input.
        if is_intent_name(GET_HIGHER_INTENT)(handler_input):
            session_attr['position'] = HIGHER
            return True
        if is_intent_name(GET_LOWER_INTENT)(handler_input):
            session_attr['position'] = LOWER
            return True
        return False

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Checking if this intent should play now.
        current_intent = [GET_LOWER_INTENT, GET_HIGHER_INTENT]
        if is_next_intent_error(handler_input = handler_input, current_intent = current_intent):
            return handle_next_intent_error(handler_input = handler_input)

        # Attempts to guess the user number
        alexa_guess = guess_your_number(handler_input = handler_input)

        # Checking if is possible for alexa to guess a number
        if alexa_guess is None:
            speech_text = say.unabletoguess() + say.numberthinkingof()
            next_intent = [GET_NUMBER_INTENT]
        else:
            speech_text = say.guessyournumber(alexa_guess = alexa_guess)
            next_intent =  [AMAZON_YES_INTENT, AMAZON_NO_INTENT]

        # Setting the next intent.
        set_next_intent(handler_input = handler_input, 
                        next_intent = next_intent)
        
        # Speaking to the user
        reprompt_text = say.didnothear() + speech_text
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response