# docker build . --tag pidroidbot-discord
FROM python:3.8-slim

LABEL version="v0.0.66" maintainer="Pidroid-B" url="https://github.com/PiDroid-B/pidroidbot-discord"

ARG USER_ID="10001"
ARG GROUP_ID="app"
ARG HOME="/app/"

ENV \
  HOME=${HOME} \
  PYTHONPATH=${HOME}

RUN \
  groupadd --gid ${USER_ID} ${GROUP_ID} && \
  useradd --create-home --uid ${USER_ID} --gid ${GROUP_ID} --home-dir ${HOME} ${GROUP_ID}

COPY . ${HOME}
# COPY .docker/ /
WORKDIR ${HOME}

RUN \
  apt-get update && \
  apt-get install dumb-init && \
  chown -R ${USER_ID}:${GROUP_ID} ${HOME} && \
  pip install --no-cache-dir -r requirements.txt

USER ${USER_ID}

VOLUME /app/log /app/settings /app/data

# CMD python pidroidbot_discord/__init__.py
ENTRYPOINT ["dumb-init", "-v", "--", "python3", "/app/pidroidbot_discord/__init__.py"]