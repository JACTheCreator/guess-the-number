from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say
from utils.common import get_prev_msg

from constants.intents import AMAZON_HELP_INTENT

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(AMAZON_HELP_INTENT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Giving the user help
        prev_msg = get_prev_msg(handler_input)
        speech_text = say.help(prev_msg = prev_msg)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response
