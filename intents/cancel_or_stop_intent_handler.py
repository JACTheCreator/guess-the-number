from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from utils.say import say

from constants.intents import AMAZON_CANCEL_INTENT, AMAZON_STOP_INTENT

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name(AMAZON_CANCEL_INTENT)(handler_input) or
                is_intent_name(AMAZON_STOP_INTENT)(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Tell the user farewell
        speech_text = say.bye()
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response
