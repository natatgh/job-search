from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

class Config:
    DATABASE = 'jobs.db'
    DEBUG = True

app.config.from_object(Config)

def get_jobs_from_db():
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, company, location, link, html_description, company_logo, tags
                FROM jobs
            """)
            jobs = cursor.fetchall()
        return jobs
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return []

@app.route('/')
def index():
    jobs = get_jobs_from_db()
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
