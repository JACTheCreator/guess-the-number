from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.common import (set_next_intent, is_next_intent_error, 
                         handle_next_intent_error, set_prev_msg)

from constants.intents import (GET_ATTEMPTS_INTENT,
                               GET_RANGE_INTENT)

class GetAttemptsIntentHandler(AbstractRequestHandler):
    """Handler for Get Attempts Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(GET_ATTEMPTS_INTENT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Checking if this intent should play now.
        if is_next_intent_error(handler_input = handler_input, current_intent = [GET_ATTEMPTS_INTENT]):
            return handle_next_intent_error(handler_input = handler_input) 

        # Getting the attempts from the user.
        attempts = handler_input.request_envelope.request.intent.slots["attempts"].value

         # Validing the attempts the user gives.
        if not attempts or attempts == '0':
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_ATTEMPTS_INTENT, GET_NUMBER_INTENT])

            # Reprompt user on number of attempts
            speech_text = say.notnumber() + say.getattempts()
            set_prev_msg(handler_input, msg = say.getattempts())
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Converting attempts(str) to an integer.
        session_attr['max_attempts'] = session_attr['attempts'] = int(attempts)

        # Setting the next intent.
        set_next_intent(handler_input = handler_input, 
                        next_intent = [GET_RANGE_INTENT])

        # Asking the user the range of the numbers in a game. 
        speech_text = say.getrange()
        reprompt_text = say.didnothear() + speech_text
        set_prev_msg(handler_input, msg = speech_text)
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response