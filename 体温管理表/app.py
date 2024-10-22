from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# データベースを初期化
def init_db():
    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS temperatures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    date TEXT,
                    time TEXT
                )''')
    conn.commit()
    conn.close()

# データの追加
def add_temperature(temperature, date, time):
    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO temperatures (temperature, date, time) VALUES (?, ?, ?)",
              (temperature, date, time))
    conn.commit()
    conn.close()

# すべてのデータを取得
def get_all_temperatures():
    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM temperatures")
    data = c.fetchall()
    conn.close()
    return data

# データの削除
def delete_temperature(record_id):
    conn = sqlite3.connect('temperature_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM temperatures WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        temperature = request.form['temperature']
        date = request.form['date']
        time = request.form['time']
        if temperature and date and time:
            add_temperature(temperature, date, time)
        return redirect(url_for('index'))

    temperatures = get_all_temperatures()
    return render_template('index.html', temperatures=temperatures)

@app.route('/delete/<int:record_id>')
def delete(record_id):
    delete_temperature(record_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # アプリ起動時にデータベースを初期化
    app.run(debug=True)