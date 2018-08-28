FROM rasa_local_settings

ENV RASA_DOCKER="YES" \
    RASA_HOME=/app \
    RASA_PYTHON_PACKAGES=/usr/local/lib/python2.7/dist-packages

# Run updates, install basics and cleanup
# - build-essential: Compile specific dependencies
# - git-core: Checkout git repos
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends build-essential git-core openssl libssl-dev libffi6 libffi-dev curl  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR ${RASA_HOME}

COPY . ${RASA_HOME}

# use bash always
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN pip install rasa_nlu==0.13.1

RUN pip install flask

RUN git clone https://github.com/RasaHQ/rasa_core.git

RUN cd rasa_core \
&& pip install -r requirements.txt \
&& pip install -e .

EXPOSE 5000 5005

CMD python ./bot.py --port 5005
