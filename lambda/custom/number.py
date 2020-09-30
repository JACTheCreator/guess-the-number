from flask import Flask
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.skill_builder import SkillBuilder

from intents.launch_request_handler import LaunchRequestHandler
from intents.get_guess_alexa_number_or_my_number_intent_handler import GetGuessAlexaNumberorGetGuessMyNumberIntentHandler
from intents.get_attempts_intent_handler import GetAttemptsIntentHandler
from intents.get_range_intent_handler import GetRangeIntentHandler
from intents.get_lower_or_higher_intent_handler import GetLowerorHigherIntentHandler
from intents.yes_intent_handler import YesIntentHandler
from intents.no_intent_handler import NoIntentHandler
from intents.get_number_intent_handler import GetNumberIntentHandler
from intents.get_user_guess_intent_handler import GetUserGuessIntentHandler
from intents.help_intent_handler import HelpIntentHandler
from intents.cancel_or_stop_intent_handler import CancelOrStopIntentHandler
from intents.session_ended_request_handler import SessionEndedRequestHandler
from intents.catch_all_exception_handler import CatchAllExceptionHandler


sb = SkillBuilder()

# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetGuessAlexaNumberorGetGuessMyNumberIntentHandler())
sb.add_request_handler(GetAttemptsIntentHandler())
sb.add_request_handler(GetRangeIntentHandler())
sb.add_request_handler(GetLowerorHigherIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(GetNumberIntentHandler())
sb.add_request_handler(GetUserGuessIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()