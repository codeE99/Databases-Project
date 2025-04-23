#!user/bin/python3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app=Flask(__name__)
app.secret_key='your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def login():
    #output a message if something goes wrong
    msg=''
    #check if "username" and "password" POST requests exist(user submitted form)
    if request.method=='POST' and 'username' in  request.form and 'password' in request.form:
    #create variables for easy access
        username=request.form['username']
        password=request.form['password']

        hash=password+app.secret_key
        hash=hashlib.sha1(hash.encode())
        password=hash.hexdigest()

        #check is account exists using MySQL
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username =%s AND password=%s', (username, password,))
        #Fetch one record and return the result
        account=cursor.fetchone()
        #if account exists in accounts table in our database
        if account:
            #create session data to access in other routes
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            #Redirect to home page
            return redirect(url_for('home'))
        else:
            #Account doesn't exist or username/password incorrect
            msg='Incorrect username and/or password!'
    #show the login form with message (if any)
    return render_template('index.html',msg=msg)