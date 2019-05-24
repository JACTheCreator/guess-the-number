import random

from flask import Flask
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from say import say

sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["alexa_number"] = random.randint(1,10)
        session_attr["attempts"] = 3

        speech_text = say.welcome()
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class GetNumberIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GetNumberIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes

        if not session_attr:
            session_attr["alexa_number"] = random.randint(1,10)
            session_attr["attempts"] = 3

        alexa_number = session_attr["alexa_number"]
        guessed_number = handler_input.request_envelope.request.intent.slots["number"].value
        if not guessed_number:
            speech_text = say.notnumber()
            return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

        if int(guessed_number) < 1 or int(guessed_number) > 10:
            speech_text = say.outofrange(min = 1, max = 10)
            return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

        elif int(guessed_number) == alexa_number:
            speech_text = say.correct()
            return handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(True).response

        attempts = session_attr['attempts']
        attempts -= 1

        if attempts == 0:
            speech_text = say.outoftries(alexa_number = alexa_number)
            return handler_input.response_builder.speak(speech_text).ask(speech_text).set_should_end_session(True).response

        if attempts == 1:
            attempt_text = 'attempt'
        else:
            attempt_text = 'attempts'

        if int(guessed_number) < alexa_number:
            positon_text = ['lower', 'higher']
        else:
            positon_text = ['higher', 'lower']

        session_attr['attempts'] = attempts

        speech_text = say.wrong(guessed_number = guessed_number, positon = positon_text, attempt_word = attempt_text, attempts = attempts)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).
                return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = say.bye()

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


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

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).set_should_end_session(True)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetNumberIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

app = Flask(__name__)
skill_response = SkillAdapter(
    skill=sb.create(), skill_id='amzn1.ask.skill.8f5e63c8-62f3-4cf7-9bc4-87a1d3b44e4c', app=app)

skill_response.register(app=app, route="/")

if __name__ == '__main__':
    app.run(threaded=True)