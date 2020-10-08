from flask import Flask
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.skill_builder import SkillBuilder

import sys
sys.path.append('../custom/')
from constants.skill_id import skill_id
from number import sb

app = Flask(__name__)
skill_response = SkillAdapter(skill = sb.create(), 
                              skill_id = skill_id, 
                              app = app)

skill_response.register(app = app, route = "/")

if __name__ == '__main__':
    app.run(debug = True, threaded = True)