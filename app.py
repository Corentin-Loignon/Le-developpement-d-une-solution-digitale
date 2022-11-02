from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3

from coinmarket import getInfo

app=Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'dgzerg51greg1'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '95776454-2389-4bca-ba79-6cb0e0c87104',
}

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_crypto_value(crypto_value_id):
    conn = get_db_connection()
    crypto_value = conn.execute('SELECT * FROM crypto_value WHERE id = ?',
                                (crypto_value_id,)).fetchone()
    conn.close()
    if crypto_value is None:
        abort(404)
    return crypto_value

@app.route('/home')
def home():
    conn = get_db_connection()
    crypto_value = conn.execute('SELECT * FROM crypto_value').fetchall()
    sum_price = conn.execute('SELECT SUM(price) FROM crypto_value').fetchall()
    conn.close()
    crypto_list = getInfo(headers)
    return render_template('home.html', crypto_value=crypto_value, sum_price=sum_price, crypto_list=crypto_list)

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/add', methods=('GET', 'POST'))
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        date = request.form['date']

        if not name:
            flash('Le nom de la crypto est requis')
        elif not quantity:
            flash('La quantité est requise')
        elif not price:
            flash('Le prix est requis')
        elif not date:
            flash('La date est requise')
        else:
            conn = get_db_connection()
            conn.execute('insert into crypto_value (name, price, quantity, date) VALUES (?, ?, ?, ?)',
                         (name, price, quantity, date))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit')
def modify():
    conn = get_db_connection()
    crypto_value = conn.execute('SELECT * FROM crypto_value').fetchall()
    conn.close()
    return render_template('edit.html', crypto_value=crypto_value)


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    crypto_value = get_crypto_value(id)

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        date = request.form['date']

        if not name:
            flash('Le nom de la crypto est requis')
        elif not quantity:
            flash('La quantité est requise')
        elif not price:
            flash('Le prix est requis')
        elif not date:
            flash('La date est requise')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE crypto_value SET name = ?, price = ?, quantity = ?, date = ? WHERE id = ?',
                         (name, price, quantity, date, id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('edit.html', crypto_value=crypto_value)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    crypto_value = get_crypto_value(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM crypto_value WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" a été supprimé'.format(crypto_value['name']))
    return redirect(url_for('home'))

if __name__ == "__main__":
   app.run()