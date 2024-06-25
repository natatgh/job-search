from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_jobs_from_db():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, link, description FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

@app.route('/')
def index():
    jobs = get_jobs_from_db()
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
