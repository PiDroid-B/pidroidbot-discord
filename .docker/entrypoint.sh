#!/usr/bin/env bash
command=( "${@}" )

PUID=${PUID:-${DEFAULT_UID}}
PGID=${PGID:-${DEFAULT_GID}}

sed -i -e "s/^${GROUP_NAME}:\([^:]*\):[0-9]*/${GROUP_NAME}:\1:${PGID}/" /etc/group
sed -i -e "s/^${USER_NAME}:\([^:]*\):\([0-9]*\):\([0-9]*\)/${USER_NAME}:\1:${PUID}:${PGID}/" /etc/passwd

chown -R "${USER_NAME}":"${GROUP_NAME}" /app/

#Defaults env_keep += "ftp_proxy http_proxy https_proxy no_proxy"
echo "Defaults env_keep += \"PYTHONPATH\"" >> /etc/sudoers

exec "${command[@]}"
