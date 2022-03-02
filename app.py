from flask import Flask, flash, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
import io
import csv
import xlwt


app = Flask(__name__)
app.secret_key = 'super secret key'

# Development vs. Production Environment
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/wells'
    
    DB_HOST = 'localhost'
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASS = 'password'
    
    conn = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USER, 
                            password=DB_PASS, 
                            host=DB_HOST)
else:
    app.debug = False
    DATABASE_URL = ('postgres://kdvrrlftxwwnny:59a80e2f97dc965e22eeb79b67a15462b7a96494fc5b7f6e5b5515f04ba5ccc9@ec2-3-228-222-169.compute-1.amazonaws.com:5432/db8pq96jum6v55')
    
    
    DB_HOST = 'ec2-3-228-222-169.compute-1.amazonaws.com'
    DB_NAME = 'db8pq96jum6v55'
    DB_USER = 'kdvrrlftxwwnny'
    DB_PASS = '59a80e2f97dc965e22eeb79b67a15462b7a96494fc5b7f6e5b5515f04ba5ccc'
    
    conn = psycopg2.connect(dbname=DB_NAME, 
                        user=DB_USER, 
                        password=DB_PASS, 
                        host=DB_HOST)
    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#### I'm lazy and refuse to create a Routes folder ####

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def adminPanel():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM results"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('admin.html', list_users = list_users)


@app.route('/index.html')
def home():
    return render_template('index.html')


@app.route('/submit', methods=["POST"])
def submit():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        collection_date = request.form['collection_date']
        well_one_reading = request.form['well_one_reading']
        well_one_free = request.form['well_one_free']
        well_two_reading = request.form['well_two_reading']
        well_two_free = request.form['well_two_free']
        outside_reading = request.form['outside_reading']
        outside_total = request.form['outside_total']
        outside_free = request.form['outside_free']


        if collection_date == '' or well_one_reading == '' or well_one_free == '' or well_two_reading == '' or well_two_free == '':
               return render_template('index.html', message="Please fill all required fields.")
        cur.execute("INSERT INTO results (collection_date, well_one_reading, well_one_free, well_two_reading, well_two_free, outside_reading, outside_total, outside_free) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (collection_date, well_one_reading, well_one_free, well_two_reading, well_two_free, outside_reading, outside_total, outside_free))
        conn.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods= ['POST','GET'])
def deleteUser(id):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DELETE FROM results WHERE id = {0}'.format(id))
        conn.commit()
        flash('Record deleted.')
        return redirect(url_for('admin'))

### CSV DOWNLOAD 
@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/download/report/excel')
def download_report():
    curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    curr.execute("SELECT * FROM results")
    result = curr.fetchall()
    #for row in result:
        #print(row)

        #output in bytes
    output = io.BytesIO()
        #create WorkBook object
    workbook = xlwt.Workbook()
        #add sheet
    sh = workbook.add_sheet('Clever Well Water Report')

        #add headers
    sh.write(0, 0, 'ID')
    sh.write(0, 1, 'Collection Date')
    sh.write(0, 2, 'Well One Reading')
    sh.write(0, 3, 'Well One Free')
    sh.write(0, 4, 'Well Two Reading')
    sh.write(0, 5, 'Well Two Free')
    sh.write(0, 6, 'Outside Reading')
    sh.write(0, 7, 'Outside Total')
    sh.write(0, 8, 'Outside Free')


    id = 0
    for row in result:
        sh.write(id+1,0, str(row['id']))
        sh.write(id+1,1, row['Collection Date'])
        sh.write(id+1,2, row['Well One Reading'])
        sh.write(id+1,3, row['Well One Free'])
        sh.write(id+1,4, row['Well Two Reading'])
        sh.write(id+1,5, row['Well Two Free'])
        sh.write(id+1,6, row['Outside Reading'])
        sh.write(id+1,7, row['Outside Total'])
        sh.write(id+1,8, row['Outside Free'])
        id += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=power_rankings.xls"})

if __name__ == "__main__":
    app.run()
