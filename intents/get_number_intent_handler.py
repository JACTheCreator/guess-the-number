from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.convert_to_ordinal_number import convert_to_ordinal_number
from utils.say import say
from utils.common import (set_next_intent, is_next_intent_error, 
                          handle_next_intent_error, is_prev_intent)
from utils.guess_the_number import guess_alexa_number

from constants.mode import GUESS_ALEXA_NUMBER, GUESS_MY_NUMBER
from constants.intents import (GET_USER_GUESS_INTENT, GET_NUMBER_INTENT, 
                               GET_RANGE_INTENT, GET_GUESS_ALEXA_NUMBER_INTENT,
                               GET_GUESS_MY_NUMBER_INTENT, AMAZON_YES_INTENT,
                               AMAZON_NO_INTENT, GET_HIGHER_INTENT, GET_LOWER_INTENT)

class GetNumberIntentHandler(AbstractRequestHandler):
    """Handler for Get Number Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(GET_NUMBER_INTENT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Checking if this intent should play now.
        if is_next_intent_error(handler_input = handler_input, current_intent = [GET_NUMBER_INTENT]):
            return handle_next_intent_error(handler_input = handler_input)
        
        # Getting session attributes.
        session_attr = handler_input.attributes_manager.session_attributes

        # Checks if the previous state exists
        is_prev_guess_alexa_my_number_intent = is_prev_intent(handler_input, intents = [GET_GUESS_ALEXA_NUMBER_INTENT, GET_GUESS_MY_NUMBER_INTENT])
        is_prev_lower_or_higher_intent = is_prev_intent(handler_input, intents = [GET_HIGHER_INTENT, GET_LOWER_INTENT])
        is_prev_user_guess_intent = is_prev_intent(handler_input, intents = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])
        is_prev_number_intent = is_prev_intent(handler_input, intents = [GET_NUMBER_INTENT])
        is_prev_yes_no_intent = is_prev_intent(handler_input, intents = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])
        is_prev_range_intent = is_prev_intent(handler_input, intents = [GET_RANGE_INTENT])

        if is_prev_guess_alexa_my_number_intent:
            # Getting the attempts from the user.
            attempts = handler_input.request_envelope.request.intent.slots["number"].value

            # Validing the attempts the user gives.
            if not attempts or attempts == '0':
                # Setting the next intent.
                set_next_intent(handler_input = handler_input, 
                                next_intent = [GET_ATTEMPTS_INTENT, GET_NUMBER_INTENT])

                # Reprompt user on number of attempts
                speech_text = say.notnumber() + say.getattempts()
                reprompt_text = say.didnothear() + speech_text
                handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
                return handler_input.response_builder.response
            
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_RANGE_INTENT])  

            # Converting attempts(str) to an integer.
            session_attr['max_attempts'] = session_attr['attempts'] = int(attempts)

            # Asking the user the range of the numbers in a game. 
            speech_text = say.getrange()
            reprompt_text = say.didnothear() + speech_text
            handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
            return handler_input.response_builder.response

        elif is_prev_user_guess_intent or is_prev_range_intent:
            # Setting the next intent.
            set_next_intent(handler_input = handler_input, 
                            next_intent = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])

            return guess_alexa_number(handler_input)

        elif is_prev_yes_no_intent or is_prev_number_intent or is_prev_lower_or_higher_intent:
            if session_attr['mode'] == GUESS_ALEXA_NUMBER:
                set_next_intent(handler_input = handler_input, 
                                next_intent = [GET_USER_GUESS_INTENT, GET_NUMBER_INTENT])
                return guess_alexa_number(handler_input)

            elif session_attr['mode'] == GUESS_MY_NUMBER:
                # Getting the attempts from the user.
                user_number = handler_input.request_envelope.request.intent.slots["number"].value
                alexa_guesses = session_attr['alexa_guesses']
                # Validing the attempts the user gives.
                if not user_number:          
                    # Setting the next intent.
                    set_next_intent(handler_input = handler_input, 
                                    next_intent = [GET_NUMBER_INTENT])      
                    speech_text = say.notnumber() + say.numberthinkingof()
                    reprompt_text = say.didnothear() + speech_text
                    handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
                    return handler_input.response_builder.response

                # Setting the next intent.
                set_next_intent(handler_input = handler_input, 
                                next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])
                
                if user_number in alexa_guesses:
                    ordinal_number = convert_to_ordinal_number(alexa_guesses.index(user_number) + 1)
                    speech_text = ('Hey I guessed {} already on my {} attempt '.format(user_number, ordinal_number) +
                                   'Do you want a rematch?')
                    reprompt_text = say.didnothear() + speech_text
                    handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)                    
                    return handler_input.response_builder.response

                speech_text = ('Oh I see! I will get you next time!' + 
                               'Do you want a rematch?')
                reprompt_text = say.didnothear() + speech_text
                handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)          
                return handler_input.response_builder.response
