from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.common import (set_next_intent, is_next_intent_error, 
                          handle_next_intent_error, is_prev_intent, 
                          set_game_state, is_current_game_state, set_prev_msg)

from constants.game_state import GAME_IN_PROGRESS, GAME_RESTARTED 
from constants.game_state import GAME_IN_PROGRESS, GAME_NOT_IN_PROGRESS

from constants.intents import (AMAZON_NO_INTENT, GET_HIGHER_INTENT,
                               GET_LOWER_INTENT, GET_RANGE_INTENT,
                               GET_NUMBER_INTENT, AMAZON_YES_INTENT,
                               GET_GUESS_ALEXA_NUMBER_INTENT, GET_GUESS_MY_NUMBER_INTENT,
                               GET_USER_GUESS_INTENT)

class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(AMAZON_NO_INTENT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response       

        # Checking if this intent should play now.
        if is_next_intent_error(handler_input = handler_input, current_intent = [AMAZON_NO_INTENT]):
            return handle_next_intent_error(handler_input = handler_input)

        is_prev_low_high_intent = is_prev_intent(handler_input, intents = [GET_LOWER_INTENT, GET_HIGHER_INTENT])
        is_prev_range_intent = is_prev_intent(handler_input, intents = [GET_RANGE_INTENT])
        is_prev_yes_no_intent = is_prev_intent(handler_input, intents = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])
        is_prev_number_intent = is_prev_intent(handler_input, intents = [GET_NUMBER_INTENT])
        is_prev_user_guess_number_intent = is_prev_intent(handler_input, intents = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])

        is_game_in_progress = ((is_current_game_state(handler_input, state = GAME_IN_PROGRESS) or 
                                is_current_game_state(handler_input, state = GAME_RESTARTED)) and 
                                is_prev_yes_no_intent)

        if is_prev_yes_no_intent or is_prev_number_intent or is_prev_user_guess_number_intent:
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_GUESS_ALEXA_NUMBER_INTENT, 
                                           GET_GUESS_MY_NUMBER_INTENT])
            
            set_game_state(handler_input, state = GAME_NOT_IN_PROGRESS)

            speech_text = 'What mode would you like to play?'
            reprompt_text = say.didnothear() + speech_text
            set_prev_msg(handler_input, msg = speech_text)
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
            return handler_input.response_builder.response

        elif is_prev_low_high_intent or is_prev_range_intent or is_game_in_progress:
            # Getting session attributes.
            session_attr = handler_input.attributes_manager.session_attributes

            if session_attr['attempts'] == 0:
                # Setting the next intent.
                set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_NUMBER_INTENT])
                speech_text = 'What number were you thinking of?'
                set_prev_msg(handler_input, msg = speech_text)
                reprompt_text = say.didnothear() + speech_text
                handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
                return handler_input.response_builder.response            

            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_HIGHER_INTENT, GET_LOWER_INTENT])

            set_game_state(handler_input, state = GAME_IN_PROGRESS)

            speech_text = 'Should I go lower or higher?'
            set_prev_msg(handler_input, msg = speech_text)
            reprompt_text = say.didnothear() + speech_text
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
            return handler_input.response_builder.response

        