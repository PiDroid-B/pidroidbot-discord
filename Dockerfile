FROM python:3.8-slim

LABEL version="v0.0.65" maintainer="Pidroid-B" url="https://github.com/PiDroid-B/pidroidbot-discord"

ARG USER_ID="10001"
ARG GROUP_ID="app"
ARG HOME="/app/"

ENV HOME=${HOME}
ENV PYTHONPATH=${HOME}

RUN \
  groupadd --gid ${USER_ID} ${GROUP_ID} && \
  useradd --create-home --uid ${USER_ID} --gid ${GROUP_ID} --home-dir ${HOME} ${GROUP_ID}

ADD . ${HOME}
WORKDIR ${HOME}

RUN \
  chown -R ${USER_ID}:${GROUP_ID} ${HOME} && \
  pip install --no-cache-dir -r requirements.txt

USER ${USER_ID}

VOLUME /app/log
VOLUME /app/settings
VOLUME /app/data

CMD python pidroidbot_discord/__main__.py