from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings
import os
from rasa_core import utils
from rasa_core.actions import Action
from agent import Agent
from rasa_core.channels import HttpInputChannel
from rasa_core.channels.facebook import FacebookInput
from rasa_core.channels.console import ConsoleInputChannel
from interpreter import RasaNLUHttpInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)


class RestaurantPolicy(KerasPolicy):
    def model_architecture(self, num_features, num_actions, max_history_len):
        """Build a Keras model and return a compiled model."""
        from keras.layers import LSTM, Activation, Masking, Dense
        from keras.models import Sequential

        n_hidden = 32  # size of hidden layer in LSTM
        # Build Model
        batch_shape = (None, max_history_len, num_features)

        model = Sequential()
        model.add(Masking(-1, batch_input_shape=batch_shape))
        model.add(LSTM(n_hidden, batch_input_shape=batch_shape))
        model.add(Dense(input_dim=n_hidden, output_dim=num_actions))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        logger.debug(model.summary())
        return model


def train_dialogue(domain_file="data/bengalibot/domain.yml",
                   model_path="data/bengalibot/dialogue",
                   training_data_file="data/bengalibotbot/story/stories.md"):
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


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu.config import RasaNLUModelConfig
    from rasa_nlu.model import Trainer
    from rasa_nlu import config

    training_data = load_data('data/bengalibot/nlu/training_data.json')
    trainer = Trainer(config.load("configs/config.yaml"))
    trainer.train(training_data)
    model_directory = trainer.persist('./data/bengalibot/nlu')
    return model_directory


def run(serve_forever=True,port=5002):
    #train_nlu()
    #train_dialogue()
    interpreter = RasaNLUHttpInterpreter(server="http://rasa_nlu_setting:5000",project = "bot1")
    agent = Agent.load("data/bengalibot/dialogue", interpreter=interpreter)
    
   # input_channel = FacebookInput(
    #                              fb_verify="rasa_bot",  # you need tell facebook this token, to confirm your URL
     #                             fb_secret="",  # your app secret
      #                            fb_tokens={"": ""},   # page ids + tokens you subscribed to
       #                           debug_mode=True    # enable debug mode for underlying fb library
   #                               )
    if serve_forever:
        agent.handle_channel(ConsoleInputChannel()) ## Remove this console input with the input channel
    return agent


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide the port')
    parser.add_argument('--port', type=int, help='Port number', required=True)
    port = parser.parse_args().port
    run(port=port)
    exit(1)
