import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

DB_PATH = os.getenv('NAVIGATOR_DB', 'posts.db')

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db()
    sections = conn.execute(
        'SELECT section, COUNT(*) as count FROM posts GROUP BY section ORDER BY section'
    ).fetchall()
    return render_template('index.html', sections=sections)


@app.route('/section/<section>')
def section_view(section: str):
    conn = get_db()
    posts = conn.execute(
        'SELECT id, url, text, date FROM posts WHERE section=? ORDER BY date DESC',
        (section,),
    ).fetchall()
    return render_template('section.html', section=section, posts=posts)


@app.route('/admin/<int:post_id>', methods=['GET', 'POST'])
def admin(post_id: int):
    conn = get_db()
    if request.method == 'POST':
        new_section = request.form['section']
        conn.execute('UPDATE posts SET section=? WHERE id=?', (new_section, post_id))
        conn.commit()
        return redirect(url_for('section_view', section=new_section))
    post = conn.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    sections = conn.execute('SELECT DISTINCT section FROM posts').fetchall()
    return render_template('admin.html', post=post, sections=sections)


if __name__ == '__main__':
    app.run(debug=True)
