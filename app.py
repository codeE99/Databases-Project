#! /usr/bin/python3

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, redirect, flash
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)
app.secret_key = 'dog_dayz_super_secret'

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

# Route to show the "Customer" form
@app.route('/customer_management')
def customer_management():
    return render_template('customer_management.html')  

#Route to show the "Add Customer" form
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()

            Owner_ID = request.form['Owner_ID']
            First_Name = request.form['First_Name']
            Last_Name = request.form['Last_Name']
            Add_Line1 = request.form['Add_Line1']
            Add_Line2 = request.form['Add_Line2']
            City = request.form['City']
            State = request.form['State']
            Zip = request.form['Zip']
            Contact_Phone = request.form['Contact_Phone']
            Contact_Email = request.form['Contact_Email']

            cur.execute(""" 
                INSERT INTO OWNER 
                (Owner_ID, First_Name, Last_Name, Add_Line1, Add_Line2, City, State, Zip, Contact_Phone, Contact_Email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (Owner_ID, First_Name, Last_Name, Add_Line1, Add_Line2, City, State, Zip, Contact_Phone, Contact_Email))

            mysql.connection.commit()
            cur.close()

            flash('Customer added successfully!', 'success')

            return redirect('/customer_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/customer_management')

    return render_template('add_customer.html')



#Route to show the "Remove Customer" form
@app.route('/remove_customer', methods=['GET', 'POST'])
def remove_customer():
    if request.method == 'POST':
        try:
            cur = mysql.connection.cursor()

            Owner_ID = request.form['Owner_ID']

            cur.execute("DELETE FROM OWNER WHERE Owner_ID = %s", (Owner_ID,))
            mysql.connection.commit()
            cur.close()

            flash(f"Customer with Owner ID {Owner_ID} removed successfully.", 'success')

            return redirect('/customer_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/customer_management')

    return render_template('remove_customer.html')
    

if __name__ == '__main__':
    app.run(debug=True)


