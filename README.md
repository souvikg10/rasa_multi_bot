# Rasa chatbot example
This is an example rasa chatbot implementation that can be connected to your Facebook page.

## Proof of Concept
The project was a quick one week implementation to demonstrate a desired architecture of Rasa components using the latest tensforflow embeddings

Feel free to make the project your own. 

## How to start

Requirements - Docker

### First Step
Build 3 images 

```sh
cd rasa_local_settings
docker build -t rasa_local_settings .
cd ..
cd rasa_nlu_setting
docker build -t rasa_nlu_setting .
cd ..
docker-compose build
docker-compose up
```

### Traning
Models for NLU are not pre-trained, 

To train
```sh
docker-compose up
docker exec -it rasabotexample_rasa_nlu_setting_1 bash
python -m rasa_nlu.train --config config.yaml --data nlu/training_data.json --path nlu --project bot1
```
## Run chatbot
```sh
docker exec -it rasabotexample_rasa_core_test_1 bash
python bot.py --port 5005
/usr/local/lib/python2.7/site-packages/h5py/__init__.py:36: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.
  from ._conv import register_converters as _register_converters
Using TensorFlow backend.
2018-04-22 18:05:08.859702: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
Bot loaded. Type a message and press enter:

```


#### Note
I am no longer supporting this project. This was just an example. 

