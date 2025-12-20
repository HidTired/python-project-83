from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort
)
from dotenv import load_dotenv
from page_analyzer import utils, db
import os
import requests


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route("/")
def index():
    url = {"name": ""}
    errors = {}
    return render_template("index.html", url=url, errors=errors)


@app.post("/urls")
def add_url():
    url = request.form.get("url")
    errors = utils.validate(url)
    conn = db.connect_db(app)
    if errors:
        flash(errors, "danger")
        return render_template('index.html'), 422
    result = utils.normalize_url(url)
    if existed := db.check_url(conn, result):
        id = existed.get("id")
        flash("Страница уже существует", "info")
    else:
        id = db.insert_url(conn, result)
        conn.commit()
        conn.close()
        flash("Страница успешно добавлена", "success")
    return redirect(url_for("show_url", id=id))


@app.route("/urls")
def show_urls():
    conn = db.connect_db(app)
    urls = db.get_all_urls(conn)
    db.close(conn)
    return render_template("/url.html", urls=urls, id=id)


@app.route("/urls/<int:id>")
def show_url(id):
    conn = db.connect_db(app)
    url = db.find(conn, id)
    if not url:
        db.close(conn)
        abort(404, description="URL не найден")
    db.close(conn)
    return render_template("/urls.html", url=url)


@app.post("/urls/<int:id>/checks")
def check_url(id):
    conn = db.connect_db(app)
    url_data = db.find(conn, id)
    url = url_data["name"]

    if not url_data:
        db.close(conn)
        abort(404, description="URL для проверки не найден")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        db.close(conn)
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("show_url", id=id))

    status_code = response.status_code
    parsed_html = utils.parse_html(response)

    db.insert_check(
        conn,
        id,
        status_code,
        parsed_html["h1"],
        parsed_html["title"],
        parsed_html["description"],
    )
    db.close(conn)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("show_url", id=id))


if __name__ == "__main__":
    app.run(debug=True)
