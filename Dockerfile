FROM rasa/rasa_core

ENV RASA_DOCKER="YES" \
    RASA_HOME=/app \
    RASA_PYTHON_PACKAGES=/usr/local/lib/python2.7/dist-packages

WORKDIR ${RASA_HOME}

COPY . ${RASA_HOME}

EXPOSE 5000 5005 5006

CMD python bot.py --port 5005
