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

'''
db = SQLAlchemy()
with app.app_context():
    db.create_all()
'''

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
    DATABASE_URL = ('postgres://zndzxoluvjahwq:d097adcaa8f06b8413a926edcc8376230da5ab1eb5cc03ed9f4b533ed7a910c0@ec2-52-87-123-108.compute-1.amazonaws.com:5432/de788dbpun4d63')
    DB_HOST = 'ec2-52-87-123-108.compute-1.amazonaws.com'
    DB_NAME = 'de788dbpun4d63'
    DB_USER = 'zndzxoluvjahwq'
    DB_PASS = 'd097adcaa8f06b8413a926edcc8376230da5ab1eb5cc03ed9f4b533ed7a910c0'
    
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
    s = "SELECT * FROM wells"
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
        date = request.form['date']
        well_one_reading = request.form['well_one_reading']
        well_one_free = request.form['well_one_free']
        well_two_reading = request.form['well_two_reading']
        well_two_free = request.form['well_two_free']
        outside_total = request.form['outside_total']
        outside_free = request.form['outside_free']


        if date == '' or well_one_reading == '' or well_one_free == '' or well_two_reading == '' or well_two_free == '' or outside_free == '' or outside_total == '':
               return render_template('index.html', message="Please fill all required fields.")
        cur.execute("INSERT INTO wells (date, well_one_reading, well_one_free, well_two_reading, well_two_free, outside_total, outside_free) VALUES (%s,%s,%s,%s,%s,%s,%s)", (date, well_one_reading, well_one_free, well_two_reading, well_two_free, outside_total, outside_free))
        conn.commit()
        curs = conn.cursor()
        curs.execute("ROLLBACK")
        conn.commit()
        
        


@app.route('/delete/<string:id>', methods= ['POST','GET'])
def deleteUser(id):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DELETE FROM wells WHERE id = {0}'.format(id))
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
    curr.execute("SELECT * FROM wells")
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
        sh.write(id+1,7, row['Outside Total'])
        sh.write(id+1,8, row['Outside Free'])
        id += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=power_rankings.xls"})

if __name__ == "__main__":
    app.run()
