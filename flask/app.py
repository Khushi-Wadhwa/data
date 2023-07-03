from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import csv
from datetime import datetime
from decimal import Decimal
  
app = Flask(__name__)
  
  
@app.route('/')
def index():
    return render_template('index.html')
  
  
@app.route('/create', methods=['POST'])
def create(): 
    CONNECTION = "postgres://khushi:12345@localhost:5432/khushi"
    conn = psycopg2.connect(CONNECTION)
    cur = conn.cursor()
    name = request.form['contract_name']
    start = request.form['start_date']
    stop = request.form['stop_date']
    filepath = request.form['file']
    query = f"""SELECT * FROM data
        WHERE contract_name = '{name}'
        AND chunk_start_time::date BETWEEN '{start}' AND '{stop}';"""
    cur.execute(query)
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        for row in cur.fetchall():
            row = list(row)
            row[0] = row[0].strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(row)

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))
  

  
  
if __name__ == '__main__':
    app.run(debug=True)