from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import io
import csv
from collections import defaultdict

DB = 'expenses.db'

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# Create DB if not exists
@app.before_request
def ensure_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    );''')
    conn.commit()
    conn.close()

# Home page (list + filters)
@app.route('/')
def index():
    month = request.args.get('month')
    category = request.args.get('category')

    qs = "SELECT * FROM expenses"
    params = []
    conds = []

    if month:
        conds.append("substr(date,1,7)=?")
        params.append(month)

    if category:
        conds.append("category=?")
        params.append(category)

    if conds:
        qs += " WHERE " + " AND ".join(conds)

    qs += " ORDER BY date DESC"

    conn = get_db_connection()
    rows = conn.execute(qs, params).fetchall()

    total = sum(r["amount"] for r in rows)

    by_cat = defaultdict(float)
    for r in rows:
        by_cat[r['category']] += r['amount']

    conn.close()

    categories = ['Food', 'Transport', 'Groceries', 'Entertainment', 'Bills', 'Other']


    return render_template("index.html", expenses=rows, total=total, by_cat=by_cat, categories=categories)

# Add Expense
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == "POST":
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form.get('description')

        conn = get_db_connection()
        conn.execute("INSERT INTO expenses (date,category,amount,description) VALUES (?,?,?,?)",
                     (date, category, amount, description))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    categories = ['Food','Transport','Groceries','Entertainment','Bills','Other']
    return render_template("add_edit.html", categories=categories)

# Edit Expense
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form.get('description')

        conn.execute("UPDATE expenses SET date=?, category=?, amount=?, description=? WHERE id=?",
                     (date, category, amount, description, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    categories = ['Food','Transport','Groceries','Entertainment','Bills','Other']
    conn.close()
    return render_template("add_edit.html", expense=row, categories=categories)

# Delete Expense
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Export CSV
@app.route('/export')
def export():
    conn = get_db_connection()
    rows = conn.execute("SELECT date,category,amount,description FROM expenses ORDER BY date DESC").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date","category","amount","description"])

    for r in rows:
        writer.writerow([r["date"], r["category"], r["amount"], r["description"]])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="expenses.csv"
    )

# Run App
if __name__ == "__main__":
    app.run(debug=True)