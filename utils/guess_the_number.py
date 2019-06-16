from  random import randint
from math import floor, ceil

from utils.say import say
from utils.common import set_next_intent, set_prev_msg

from constants.intents import (AMAZON_YES_INTENT,
                               AMAZON_NO_INTENT)

def guess_your_number(handler_input):
    # Getting session attributes
    session_attr = handler_input.attributes_manager.session_attributes
    
    attempts = session_attr['attempts']
    max_attempts = session_attr['max_attempts']
    guessing_range = session_attr['guessing_range']
    position = session_attr['position']
    alexa_guesses = session_attr['alexa_guesses']
    alexa_guess = None
    min = session_attr['min']
    max = session_attr['max']

    if attempts == max_attempts:
        guessing_range = [session_attr['min'], session_attr['max']]

    if position == 'LOWER':
        guessing_range[1] = (alexa_guesses[-1] - 1)
    elif position == 'HIGHER':
        guessing_range[0] = (alexa_guesses[-1] + 1)

    # Ensure that the guess doesn't go below min or above max  
    if guessing_range[0] < min or guessing_range[1] < min:
        return None
    if guessing_range[0] > max or guessing_range[1] > max:
        return None
    
    try:
        if attempts == 1:
            alexa_guess = randint(guessing_range[0], guessing_range[1])
        else:
            guess = (guessing_range[0] + guessing_range[1]) / 2
            alexa_guess = randint(int(floor(guess)), int(ceil(guess)))
    except:
        return None
    
    alexa_guesses.append(alexa_guess)


    session_attr['guessing_range'] = guessing_range
    session_attr['position'] = position
    session_attr['alexa_guesses'] = alexa_guesses

    attempts -= 1
    session_attr['attempts'] = attempts

    return alexa_guesses[-1]


def guess_alexa_number(handler_input):
    # Getting session attributes
    session_attr = handler_input.attributes_manager.session_attributes
    
    alexa_number = session_attr["alexa_number"]
    min = session_attr['min']
    max = session_attr['max']

    guessed_number = handler_input.request_envelope.request.intent.slots["number"].value
    if not guessed_number:
        speech_text = say.notnumber()
        set_prev_msg(handler_input, msg = speech_text)
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response


    if int(guessed_number) < 1 or int(guessed_number) > 10:
        speech_text = say.outofrange(min = 1, max = 10)
        set_prev_msg(handler_input, msg = speech_text)
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response

    elif int(guessed_number) == alexa_number:
        set_next_intent(handler_input,
                        next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])
        speech_text = say.correct() + 'Do you want a rematch?'
        reprompt_text = say.didnothear() + speech_text
        set_prev_msg(handler_input, msg = 'Do you want a rematch?')
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response

    attempts = session_attr['attempts']
    attempts -= 1

    if attempts == 0:
        set_next_intent(handler_input,
                        next_intent = [AMAZON_YES_INTENT, AMAZON_NO_INTENT])
        speech_text = say.outoftries(alexa_number = alexa_number) + 'Do you want a rematch?'
        set_prev_msg(handler_input, msg = 'Do you want a rematch?')
        handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
        return handler_input.response_builder.response


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
    reprompt_text = say.didnothear() + speech_text
    set_prev_msg(handler_input, msg = speech_text)
    handler_input.response_builder.speak(speech_text).ask(reprompt_text).set_should_end_session(False)
    return handler_input.response_builder.response
