from random import randint

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, is_request_type

from utils.say import say
from utils.common import set_next_intent, is_next_intent_error, handle_next_intent_error, set_prev_msg

from constants.mode import GUESS_ALEXA_NUMBER, GUESS_MY_NUMBER

from constants.game_state import GAME_IN_PROGRESS

from constants.intents import (GET_GUESS_ALEXA_NUMBER_INTENT, GET_GUESS_MY_NUMBER_INTENT,
                               GET_ATTEMPTS_INTENT, GET_NUMBER_INTENT,
                               GET_USER_GUESS_INTENT, AMAZON_YES_INTENT, AMAZON_NO_INTENT)

class ModeRangeAttemptsIntentHandler(AbstractRequestHandler):
    """Single handler."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type('Dialog.API.Invoked')(handler_input) and
                handler_input.request_envelope.request.api_request.name == 'GetGameSettings')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes

        api_request = handler_input.request_envelope.request.api_request

        min = api_request.arguments['min']
        max = api_request.arguments['max']
        attempts = api_request.arguments['attempts']

        session_attr['min'] = int(min)
        session_attr['max'] = int(max)
        session_attr['game_state'] = GAME_IN_PROGRESS

        if session_attr['mode'] == GUESS_ALEXA_NUMBER:
            # # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_NUMBER_INTENT])
            session_attr["alexa_number"] = randint(int(min)-1, int(max))
        
        elif session_attr['mode'] == GUESS_MY_NUMBER:
            set_next_intent(handler_input = handler_input, 
                            next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT]) 
            session_attr['guessing_range'] = []
            session_attr['position'] = ''
            session_attr['alexa_guesses'] = []
        
        # Converting attempts(str) to an integer.
        session_attr['max_attempts'] = session_attr['attempts'] = int(attempts)

        return {
            'directives' : [
                {
                    'type': 'Dialog.DelegateRequest',
                    'target': 'skill',
                    'period': {
                        'until': 'EXPLICIT_RETURN'
                    },
                    'updatedRequest': {
                        'type': 'IntentRequest',
                        'intent': {
                            'name': 'BeginGameIntent',
                        }
                    }
                }
            ],
            'apiResponse': {}
        }
