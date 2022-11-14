from markupsafe import escape
from flask import Flask,render_template, request, redirect, url_for, session
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=llq09122;PWD=lIYfyUWXo8ZKGrxp",'','')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('/index.html')

@app.route('/signin')
def signin():
    return render_template('/signin.html')
    
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    address = request.form['email']
    city = request.form['phoneno']
    pin = request.form['pswd']

    sql = "SELECT * FROM students WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('index.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO students VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phoneno)
      ibm_db.bind_param(prep_stmt, 4, pswd)
      ibm_db.execute(prep_stmt)
    
    return render_template('index.html', msg="Student Data saved successfuly..")

@app.route('/signup')
def signup():
    return render_template('/signup.html')

@app.route('/about')
def about():
    return render_template('/about.html')

    
