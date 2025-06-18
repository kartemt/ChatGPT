# Telegram Navigator

This project contains a small website and scripts to collect posts from a Telegram channel and arrange them into sections based on the first hashtag of each post.

## Requirements

- Python 3.11+
- [Telethon](https://github.com/LonamiWebs/Telethon)
- [Flask](https://flask.palletsprojects.com/)

## Usage

1. Set the following environment variables:
   - `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` &ndash; credentials from [my.telegram.org](https://my.telegram.org/).
   - `TELEGRAM_CHANNEL` &ndash; username or ID of the channel to fetch posts from.
   - `NAVIGATOR_DB` (optional) &ndash; path to the SQLite database, default is `posts.db`.
2. Run `python navigator/telefetch.py` to download recent posts into the database.
3. Start the web application with `python navigator/app.py` and open `http://localhost:5000`.
4. Use the **edit** links to manually change the section of a post if the automatic classification was incorrect.
