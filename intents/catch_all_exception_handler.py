from ask_sdk_core.dispatch_components import AbstractExceptionHandler

from utils.say import say

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        # Tells the user an error has occured and then exits.
        speech = say.exceptionerror()
        handler_input.response_builder.speak(speech).set_should_end_session(True)
        return handler_input.response_builder.response
