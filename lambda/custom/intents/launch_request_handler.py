from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type

from utils.say import say
from utils.common import set_next_intent, set_prev_msg

from constants.intents import (LAUNCH_REQUEST, 
                               GET_GUESS_ALEXA_NUMBER_INTENT, 
                               GET_GUESS_MY_NUMBER_INTENT)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type(LAUNCH_REQUEST)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Setting the next intent.
        set_next_intent(handler_input = handler_input, 
                        next_intent = [GET_GUESS_ALEXA_NUMBER_INTENT, 
                                       GET_GUESS_MY_NUMBER_INTENT],
                        is_launch_request = True)
       
        # Welcoming the user.
        speech_text = say.welcome()
        reprompt_text = say.didnothear() + speech_text
        set_prev_msg(handler_input, msg = 'What mode would you like to play?')
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)        
        return handler_input.response_builder.response
