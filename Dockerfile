# docker build . --tag pidroidbot-discord
FROM python:3.8-slim

LABEL version="1.0.1" maintainer="Pidroid-B" url="https://github.com/PiDroid-B/pidroidbot-discord"

ARG USER_ID="10001"
ARG USER_NAME="app"
ARG GROUP_ID="10001"
ARG GROUP_NAME="app"

ARG HOME="/app/"

ENV PYTHONPATH="${HOME}"
ENV USER_NAME="${USER_NAME}"
ENV DEFAULT_UID="${USER_ID}"
ENV GROUP_NAME="${GROUP_NAME}"
ENV DEFAULT_GID="${GROUP_ID}"

RUN \
  groupadd -g ${GROUP_ID} -o ${GROUP_NAME} && \
  useradd --create-home --home-dir ${HOME} -s /bin/bash -o -u ${USER_ID} -g ${GROUP_ID} ${USER_NAME}

COPY . ${HOME}
WORKDIR ${HOME}

RUN \
  apt-get update && \
  apt-get install -y --no-install-recommends dumb-init sudo && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --no-cache-dir -r requirements.txt

VOLUME /app/log /app/settings /app/data

RUN chmod +x /app/.docker/entrypoint.sh

ENTRYPOINT [ "/app/.docker/entrypoint.sh" ]
CMD ["sudo", "-n", "-u", "app", "dumb-init", "-v", "--", "python3", "/app/pidroidbot_discord/__init__.py"]