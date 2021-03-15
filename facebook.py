#!/usr/bin/env python
# -*- coding: utf-8 -*-


from settings.config_default import BASE_DIR, VERIFY, SECRET, PAGE_ACCESS_TOKEN
from rasa.core.channels.facebook import FacebookInput
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
import os
from rasa.utils.endpoints import EndpointConfig
# load your trained agent
interpreter = RasaNLUInterpreter(BASE_DIR+"/jady/models/nlu/nlu")
MODEL_PATH = BASE_DIR+"/jady/models/nlu/core"
action_endpoint = EndpointConfig(url="https://jady-server-actions.herokuapp.com/webhook")
agent = Agent.load(MODEL_PATH, interpreter=interpreter)
input_channel = FacebookInput(
        fb_verify=VERIFY,
        # you need tell facebook this token, to confirm your URL
        fb_secret=SECRET,  # your app secret
        fb_access_token=PAGE_ACCESS_TOKEN
        # token for the page you subscribed to
)
# set serve_forever=False if you want to keep the server running
s = agent.handle_channels([input_channel], int(os.environ.get('PORT',
5004)), serve_forever=True)
