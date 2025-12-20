### Hexlet tests and linter status:
[![Actions Status](https://github.com/HidTired/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/HidTired/python-project-83/actions)

.\.venv\Scripts\activate
python -m pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 page_analyzer:app
waitress-serve --port=8000 page_analyzer:app

pip install -r ./requirements.txt