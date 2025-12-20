### Hexlet tests and linter status:
[![Actions Status](https://github.com/HidTired/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/HidTired/python-project-83/actions)

.\.venv\Scripts\activate
python -m pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 page_analyzer:app
waitress-serve --port=8000 page_analyzer:app

pip install -r ./requirements.txt

base.html — базовый шаблон для всей страницы, он содержит общие стили и оформление.
index.html — главная страница, содержащая форму для ввода URL. Форма отправляет запрос методом POST.
url.html — страница детальной информации о конкретном URL и истории проверок. Там есть форма для запуска новой проверки.
urls.html — страница со списком всех зарегистрированных URL и историей проверок.