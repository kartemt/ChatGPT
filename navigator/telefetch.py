import os
import re
import sqlite3
from telethon import TelegramClient
from telethon.tl.types import Message

API_ID = int(os.getenv('TELEGRAM_API_ID', '0'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
CHANNEL = os.getenv('TELEGRAM_CHANNEL')
DB_PATH = os.getenv('NAVIGATOR_DB', 'posts.db')

HASHTAG_RE = re.compile(r'#(\w+)')


def get_first_hashtag(text: str) -> str:
    match = HASHTAG_RE.search(text or '')
    return match.group(1).lower() if match else 'general'


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        'CREATE TABLE IF NOT EXISTS posts ('
        'id INTEGER PRIMARY KEY, '
        'channel TEXT, '
        'url TEXT, '
        'section TEXT, '
        'text TEXT, '
        'date TEXT'
        ')'
    )
    conn.commit()


def save_post(conn: sqlite3.Connection, message: Message) -> None:
    section = get_first_hashtag(message.message or '')
    url = f"https://t.me/{CHANNEL}/{message.id}"
    conn.execute(
        'INSERT OR REPLACE INTO posts (id, channel, url, section, text, date) '
        'VALUES (?, ?, ?, ?, ?, ?)',
        (
            message.id,
            CHANNEL,
            url,
            section,
            message.message,
            message.date.isoformat(),
        ),
    )


def fetch():
    client = TelegramClient('navigator', API_ID, API_HASH)
    client.start()
    with client, sqlite3.connect(DB_PATH) as conn:
        ensure_db(conn)
        for message in client.iter_messages(CHANNEL, limit=100):
            if message.message:
                save_post(conn, message)
        conn.commit()


if __name__ == '__main__':
    fetch()
