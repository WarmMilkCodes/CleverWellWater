from flask import Flask, flash, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras
import io
import csv
#import xlwt


app = Flask(__name__)
app.secret_key = 'super secret key'

# Development vs. Production Environment
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/wells'
    
    DB_HOST = 'localhost'
    DB_NAME = 'wells'
    DB_USER = 'postgres'
    DB_PASS = 'password'
    
    conn = psycopg2.connect(dbname=DB_NAME, 
                            user=DB_USER, 
                            password=DB_PASS, 
                            host=DB_HOST)
else:
    app.debug = False
    #DATABASE_URL = HEROKU URL HERE
    
    
    DB_HOST = NULL
    DB_NAME = NULL
    DB_USER = NULL
    DB_PASS = NULL
        
    conn = psycopg2.connect(dbname=DB_NAME, 
                        user=DB_USER, 
                        password=DB_PASS, 
                        host=DB_HOST)
    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#### I'm lazy and refuse to create a Routes folder ####

@app.route('/')
def index():
    return render_template('index.html')

'''
@app.route('/admin')
def adminPanel():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM voting"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('admin.html', list_users = list_users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['loginName'] != 'PowerRankings' or request.form['password'] != 'roguevotes':
            error = 'Invalid credentials. Please ensure username and password are correct.'
        else:
            return redirect(url_for('adminPanel'))
    return render_template('login.html')
'''

@app.route('/index.html')
def home():
    return render_template('index.html')
'''
@app.route('/success.html')
def success():
    return render_template('success.html')
'''

@app.route('/submit', methods=["POST"])
def submit():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        date = request.form['date']
        wellonereading = request.form['well-one-reading']
        wellonefree = request.form['well-one-free']
        welltworeading = request.form['well-two-reading']
        welltwofree = request.form['well-two-free']
        outsidereading = request.form['outsideeading']
        outsidetotal = request.form['outsidetotal']
        outsidefree = request.form['outsidefree']


        if date == '' or wellonereading == '' or wellonetotal == '' or wellonefree == '' or welltworeading == '' or welltwototal == '' or welltwofree == '':
               return render_template('index.html', message="Please fill all required fields.")
        cur.execute("INSERT INTO voting (username, league, team1, team2, team3, team4, team5, team6, team7, team8, team9, team10) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (username, league, team1, team2, team3, team4, team5, team6, team7, team8, team9, team10))
        conn.commit()
        return redirect(url_for('success'))


@app.route('/delete/<string:id>', methods= ['POST','GET'])
def deleteUser(id):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DELETE FROM voting WHERE id = {0}'.format(id))
        conn.commit()
        flash('Record deleted.')
        return redirect(url_for('adminPanel'))

### CSV DOWNLOAD 
@app.route('/download_csv')
def download():
    return render_template('download_csv.html')

@app.route('/download_csv/report/excel')
def download_report():
    curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    curr.execute("SELECT * FROM voting")
    result = curr.fetchall()
    #for row in result:
        #print(row)

        #output in bytes
    output = io.BytesIO()
        #create WorkBook object
    workbook = xlwt.Workbook()
        #add sheet
    sh = workbook.add_sheet('Power Rankings Report')

        #add headers
    sh.write(0, 0, 'ID')
    sh.write(0, 1, 'Username')
    sh.write(0, 2, 'League')
    sh.write(0, 3, 'Team 1')
    sh.write(0, 4, 'Team 2')
    sh.write(0, 5, 'Team 3')
    sh.write(0, 6, 'Team 4')
    sh.write(0, 7, 'Team 5')
    sh.write(0, 8, 'Team 6')
    sh.write(0, 9, 'Team 7')
    sh.write(0, 10, 'Team 8')
    sh.write(0, 11, 'Team 9')
    sh.write(0, 12, 'Team 10')

    id = 0
    for row in result:
        sh.write(id+1,0, str(row['id']))
        sh.write(id+1,1, row['username'])
        sh.write(id+1,2, row['league'])
        sh.write(id+1,3, row['team1'])
        sh.write(id+1,4, row['team2'])
        sh.write(id+1,5, row['team3'])
        sh.write(id+1,6, row['team4'])
        sh.write(id+1,7, row['team5'])
        sh.write(id+1,8, row['team6'])
        sh.write(id+1,9, row['team7'])
        sh.write(id+1,10, row['team8'])
        sh.write(id+1,11, row['team9'])
        sh.write(id+1,12, row['team10'])
        id += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=power_rankings.xls"})

if __name__ == "__main__":
    app.run()
