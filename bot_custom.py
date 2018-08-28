cfrom __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import argparse
import logging
import warnings
import json
from rasa_core import utils
from rasa_core.actions import Action
from agent import Agent
from rasa_core.domain import TemplateDomain
from rasa_core.tracker_store import InMemoryTrackerStore
from rasa_core.channels.rest import HttpInputChannel
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.channels.channel import UserMessage, OutputChannel
from rasa_core.channels.rest import HttpInputComponent
from rasa_core.channels.custom import CustomInput
from interpreter import RasaNLUHttpInterpreter
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)

class BotOutput(OutputChannel):
    """A bot that uses rest to communicate."""
    def __init__(self):
        pass
    
    def send_text_message(self, recipient_id, elements):
        self.message = jsonify({"status": recipient_id, "result": elements})

class BotInput(HttpInputComponent):
    """Http input for trip bot."""

    def __init__(self):
        pass

    def blueprint(self, on_new_message):

        bot = Blueprint('bot', __name__)

        @bot.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @bot.route("/message", methods=['GET', 'POST'])
        def chat():
            if request.method == 'GET':
                return jsonify({"status": "ok"})
            if request.method == 'POST':
                output = request.stream.read()
                uid = request.args.get("uid", "default")
                output = json.loads(output)
                output_channel = BotOutput()
                user_message = UserMessage(output["text"], output_channel, uid)
                on_new_message(user_message)
                return output_channel.message
        return bot



def train_dialogue(domain_file="",
                   model_path="",
                   training_data_file=""):
    agent = Agent(domain_file,policies=[MemoizationPolicy(), KerasPolicy()])
    
    agent.train(
            training_data_file,
                max_history=3,
                epochs=100,
                batch_size=50,
                augmentation_factor=50,
                validation_split=0.2
            
    )

    agent.persist(model_path)
    return agent


def run(serve_forever=True,port=5002, debug = False):
    domain = os.path.abspath("")
    interpreter = RasaNLUHttpInterpreter(server="http://rasanlu:5000",token = "",model_name = "",project = "")
    tracker_domain = TemplateDomain.load(os.path.abspath(""))
    tracker_store = InMemoryTrackerStore(tracker_domain)
    chat_endpoint = BotInput()
    if debug:
        input_channel = ConsoleInputChannel()
    else:
        input_channel = HttpInputChannel(port, "/ai", chat_endpoint)
    agent = Agent.load(domain,
                    interpreter=interpreter,
                    tracker_store=tracker_store)

    if serve_forever:
        agent.handle_channel(input_channel)
    return agent


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide the port')
    parser.add_argument('--port', type=int, help='Port number', required=True)
    port = parser.parse_args().port
    train_dialogue()
    run(port=port)
    exit(1)
