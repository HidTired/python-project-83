import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


def connect_db(app): 
    DATABASE_URL = app.config['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)
    conn.cursor_factory = RealDictCursor
    return conn


def close(conn):
    conn.close()


def get_all_urls(conn):
    with conn.cursor() as curs:
        curs.execute("""
            SELECT
                urls.id,
                urls.name,
                last_checks.created_at,
                last_checks.status_code
            FROM urls
            LEFT JOIN (
                SELECT DISTINCT ON (url_id)
                    url_id,
                    created_at,
                    status_code
                FROM url_checks
                ORDER BY url_id, created_at DESC
            ) AS last_checks
            ON urls.id = last_checks.url_id
            ORDER BY urls.id;
        """)
        return curs.fetchall()

# Проверка
def insert_url(conn, url):
    now = datetime.now().date()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
            (url, now)
        )
        url_id = cursor.fetchone()["id"]
        conn.commit()
    return url_id


def find(conn, url_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
        url = cursor.fetchone()
        if url:
            cursor.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC",
                (url_id,)
            )
            url['checks'] = cursor.fetchall()
    return url


def check_url(conn, name):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM urls WHERE name = %s", (name,))
        return cursor.fetchone()


def insert_check(conn, url_id, status_code, h1=None, title=None, 
                 description=None):
    now = datetime.now().date()
    with conn.cursor() as curs:
        curs.execute("""
            INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (url_id, status_code, h1, title, description, now))
        conn.commit()