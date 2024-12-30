from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
app = Flask(__name__)
#База данних реєєстрації
def get_db_conn():
    conn = sqlite3.connect('base.db')
    conn.row_factory = sqlite3.Row
    return conn
def create_table():
    conn = get_db_conn()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS registr(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

#База данних відгук
def get_db_vid():
    conn = sqlite3.connect('reviews.db')
    conn.row_factory = sqlite3.Row
    return conn
def create_table2():
    conn = get_db_vid()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    review TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/page1')
def page_1():
    return  render_template('infoslayd1.html')
@app.route('/form', methods=['GET', 'POST'])
def form_():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_conn()
        conn.execute('INSERT INTO registr(email, password) VALUES(?,?)',
                     (email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('forma.html')
@app.route('/thank')
def thank():
    return 'Дякую за фідбек'

@app.route('/rewiew1')
def rew():
    conn = get_db_vid()
    reviews = conn.execute('SELECT * FROM reviews').fetchall()
    conn.close()
    return render_template('pro_nas.html', reviews=reviews)


@app.route('/add_review', methods=['POST'])
def add_review():

    username = request.form['username']
    review = request.form['review']
    conn = get_db_vid()
    conn.execute('INSERT INTO reviews(username, review) VALUES(?,?)',
                     (username, review))
    conn.commit()
    conn.close()
    return redirect('/rewiew1')

if __name__ =='__main__':
    create_table()
    create_table2()
    app.run(debug=True)