#!/usr/bin/env bash
set -eo pipefail

# Устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Загружаем настройки uv
source "$HOME/.local/bin/env"

# Синхронизация и установка зависимостей
pip3 install gunicorn

make install && psql -a -d $DATABASE_URL -f database.sql