from utils.say import say
from constants.intents import LAUNCH_REQUEST


def set_next_intent(handler_input, next_intent, is_launch_request = False):
    """Set the intent that should play next and the previously played intent"""

    # Getting session attributes.
    session_attr = handler_input.attributes_manager.session_attributes 

    # Setting the previous intent.
    if is_launch_request:
        session_attr['prev_intent'] = [LAUNCH_REQUEST]
    elif not is_launch_request:
        session_attr['prev_intent'] = session_attr['next_intent']

    # Setting the next intent.
    session_attr['next_intent'] = next_intent


def is_next_intent_error(handler_input, current_intent):
    """Checks if the current intent should play"""
    
    # Getting the value of the next value from the session attributes.
    next_intent = handler_input.attributes_manager.session_attributes['next_intent']

    # Returns True if the next intent does not contains the current intent.
    return not (True in [x in next_intent for x in current_intent])


def handle_next_intent_error(handler_input):
    """Handles the next intent error"""

    # Getting the value of the next value from the session attributes.
    next_intent = handler_input.attributes_manager.session_attributes['next_intent']

    # Tells the user the error that has occured.
    speech_text = say.next_intent_error_handle(intent = next_intent, handler_input = handler_input)        
    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response


def is_prev_intent(handler_input, intents):
    """Checks the previous intent"""

    # Getting the value of the next value from the session attributes.
    prev_intent = handler_input.attributes_manager.session_attributes['prev_intent']
    
    # Returns True if the previous intent is equivalent to the intents.
    return set(prev_intent) == set(intents)


def set_game_state(handler_input, state):
    """Setting the state of the game."""
    handler_input.attributes_manager.session_attributes['game_state'] = state


def is_current_game_state(handler_input, state):
    """Check the current game state"""
    return handler_input.attributes_manager.session_attributes['game_state'] == state
