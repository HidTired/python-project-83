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
from . import utils
from . import db
import os


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.post("/urls")
def add_url():
    url = request.form.get("url")
    errors = utils.validate(url) or {}
    conn = db.connect_db(app)
    if errors:
        flash(errors, "danger")
        conn.close()
        return render_template('index.html'), 422
    result = utils.normalize_url(url)
    if existed := db.check_url(conn, result):
        flash("Страница уже существует", "info")
        conn.close()
        return redirect(url_for("show_url", id_=existed["id"]))
    else:
        id_ = db.insert_url(conn, result)
        conn.commit()
        flash("Страница успешно добавлена", "success")
    conn.close()
    return redirect(url_for("show_urls"))


@app.route("/urls")
def show_urls():
    conn = db.connect_db(app)
    urls = db.get_all_urls(conn)
    conn.close()
    return render_template("urls.html", all_urls_checks=urls)


@app.route("/urls/<int:id_>")
def show_url(id_):
    conn = db.connect_db(app)
    url = db.find(conn, id_)
    conn.close()
    if not url:
        abort(404, description="URL не найден")
    return render_template("url.html",
                          url_info=url,
                          url_checks=url["checks"])


@app.post("/urls/<int:id_>/checks")
def check_url(id_):
    conn = db.connect_db(app)
    url_data = db.find(conn, id_)
    if not url_data:
        conn.close()
        abort(404)

    url = url_data["name"]
    try:
        parsed = utils.check_website(url)
        if parsed is None:
            raise Exception("Parsing failed")
    except Exception:  # ✅ НЕ bare except!
        conn.close()
        flash("Произошла ошибка при проверке", "danger")  # ✅ без пробела
        return redirect(url_for("show_url", id_=id_))

    db.insert_check(
        conn, id_, parsed["status_code"],
        parsed["h1"],
        parsed["title"],
        parsed["description"]
    )
    conn.commit()
    conn.close()
    flash("Страница успешно проверена", "success")
    return redirect(url_for("show_url", id_=id_))


@app.route("/clear")
def clear_db():
    conn = db.connect_db(app)
    with conn.cursor() as cur:
        cur.execute("TRUNCATE urls, url_checks RESTART IDENTITY")
    conn.commit()
    conn.close()
    flash("✅ База данных очищена!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)