import sqlite3

conn = sqlite3.connect("news.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS news(
id INTEGER PRIMARY KEY,
title TEXT,
summary TEXT,
link TEXT
)
""")

conn.commit()


def save_news(article):

    cursor.execute(
        "INSERT INTO news(title,summary,link) VALUES(?,?,?)",
        (article["title"], article["summary"], article["link"])
    )

    conn.commit()


def get_all_news():

    cursor.execute("SELECT title,summary,link FROM news")

    return cursor.fetchall()