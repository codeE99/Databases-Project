#! /usr/bin/python3

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   
app.config['MYSQL_DB'] = 'dog_dayz_salon'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pet', methods=['GET','POST'])
def pet():
    msg=''

    if request.method == 'GET':
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM pet')
        cursor.close()
        return render_template('pet.html')
    
    if request.method == 'POST':
        name=request.form['name']
        breed=request.form['breed']
        rabies_vacc = 1 if request.form['rabies_vacc'] == 'yes' else 0
        current_meds=request.form['medications']
        med_conditions=request.form['conditions']
        behavior=request.form['behavior']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO pet (Name, Breed, Medical_RabiesVac,Current_Meds, Medical_Conditions,Behavior) VALUES(%s,%s,%s,%s,%s,%s)", [name, breed, rabies_vacc,current_meds, med_conditions, behavior])
        mysql.connection.commit()
        cursor.close()
        msg='Pet added!'
        return render_template ('pet.html',msg=msg)
    

if __name__ == '__main__':
    app.run(debug=True)


