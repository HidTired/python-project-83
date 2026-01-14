set -eo pipefail

chmod +x build.sh

curl -LsSf https://astral.sh/uv/install.sh | sh

source "$HOME/.local/bin/env"

pip3 install gunicorn

make install && psql -a -d $DATABASE_URL -f database.sql