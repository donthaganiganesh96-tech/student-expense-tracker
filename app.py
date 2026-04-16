from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT, amount REAL, category TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    
    # Calculate totals for the chart
    categories = ['Food', 'Travel', 'Shopping', 'Other']
    values = [sum(e[2] for e in expenses if e[3] == c) for c in categories]
    
    conn.close()
    return render_template('index.html', expenses=expenses, labels=categories, values=values)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')
    
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)", 
                   (title, amount, category))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
