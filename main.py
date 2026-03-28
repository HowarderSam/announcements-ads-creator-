import sqlite3
from flask import (Flask,render_template,
                   request,jsonify,url_for,
                   redirect,url_for,
                   abort,g)


app = Flask(__name__)
DATABASE = "ads.db"

@app.route("/")
def index():
    return redirect(url_for("create_ad"))



@app.route('/create/', methods=['GET', 'POST'])
def create_ad():
    if request.method == 'POST':
        title = request.form["title"]
        text = request.form["text"]
        phone = request.form["phone"]
        email = request.form["email"]

        db = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO ads (title, text, phone, email)
            VALUES (?, ?, ?, ?)
        """, (title, text, phone, email))
        db.commit()

        return redirect(url_for('show_ads'))

    return render_template('create.html')


@app.route('/ads/')
def show_ads():
    db = get_db()
    cur = db.cursor()
    res = cur.execute("""SELECT * FROM ads""").fetchall()
    return render_template('ads.html', data=res)


def get_db():
    """Функція підключення до бази даних"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE) 
    return g.db  

@app.teardown_appcontext
def close_db(exception):
    """Функція, яка закриває підключення до бази після завершення запиту"""
    db = g.pop('db', None)  
    if db is not None:
        db.close()  



def create_table():
    db = get_db()
    cur = db.cursor()
    # cur.execute("""DROP TABLE users""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL,
            text VARCHAR(255) NOT NULL,
            phone VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)
    db.commit()



if __name__ == "__main__":
    with app.app_context():
        create_table()
    app.run(debug=True)