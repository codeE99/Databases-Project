#! /usr/bin/python3

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, redirect, flash
from flask_mysqldb import MySQL
import json
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from datetime import datetime


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
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(pet_id, 4) AS UNSIGNED)) FROM pet WHERE pet_id LIKE 'PET%'")
        result = cursor.fetchone()
        max_id = result[0] if result[0] else 0
        new_pet_id = f"PET{max_id + 1}"

        name=request.form['name']
        breed=request.form['breed']
        rabies_vacc = 1 if request.form['rabies_vacc'] == 'yes' else 0
        current_meds=request.form['medications']
        med_conditions=request.form['conditions']
        behavior=request.form['behavior']
        owner_id=request.form['owner_id']
        #cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO pet (Pet_ID, Name, Breed, Medical_RabiesVac, Current_Meds, Medical_Conditions, Behavior, Owner_ID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", 
                       [new_pet_id, name, breed, rabies_vacc, current_meds, med_conditions, behavior, owner_id])
        mysql.connection.commit()
        cursor.close()
        msg=f"Pet added with ID {new_pet_id}!"
        flash(msg)
        print(f"Inserting: {new_pet_id}, {name}, {breed}, {rabies_vacc}, {current_meds}, {med_conditions}, {behavior}, {owner_id}")
        return render_template ('pet.html')

# Customer routes
#=======================================================
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
    
# Staff routes
#=======================================================
# Staff Management Menu
@app.route('/staff_management')
def staff_management():
    return render_template('staff_management.html')

# View all staff
@app.route('/view_staff')
def view_staff():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Staff_ID, First_Name, Last_Name FROM STAFF")
    staff_list = cur.fetchall()
    cur.close()
    return render_template('view_staff.html', staff_list=staff_list)

# Add new staff
@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        try:
            Staff_ID = request.form['Staff_ID']
            First_Name = request.form['First_Name']
            Last_Name = request.form['Last_Name']
            Role = request.form['Role']
            Salary = request.form['Salary']
            Date_Started = request.form['Date_Started']
            Qualifications = request.form['Qualifications']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO STAFF (Staff_ID, First_Name, Last_Name, Role, Salary, Date_Started, Qualifications)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (Staff_ID, First_Name, Last_Name, Role, Salary, Date_Started, Qualifications))
            mysql.connection.commit()
            cur.close()

            flash('Staff member added successfully!', 'success')
            return redirect('/staff_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/staff_management')

    return render_template('add_staff.html')

# Remove a staff member
@app.route('/remove_staff', methods=['GET', 'POST'])
def remove_staff():
    if request.method == 'POST':
        try:
            Staff_ID = request.form['Staff_ID']

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM STAFF WHERE Staff_ID = %s", (Staff_ID,))
            mysql.connection.commit()
            cur.close()

            flash(f"Staff member with ID {Staff_ID} removed successfully.", 'success')
            return redirect('/staff_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/staff_management')

    return render_template('remove_staff.html')

# View individual staff profile
@app.route('/staff/<staff_id>')
def staff_profile(staff_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM STAFF WHERE Staff_ID = %s", (staff_id,))
    staff = cur.fetchone()
    cur.close()

    if staff:
        return render_template('staff_profile.html', staff=staff)
    else:
        flash('Staff member not found.', 'warning')
        return redirect('/view_staff')

# Appointment routes
#=======================================================
# Appointment Management Menu
@app.route('/appointment_management')
def appointment_management():
    return render_template('appointment_management.html')

# View Appointments by Date
@app.route('/view_appointments_by_date', methods=['GET', 'POST'])
def view_appointments_by_date():
    if request.method == 'POST':
        date_day = request.form['Date_Day']
        date_month = request.form['Date_Month']
        date_year = request.form['Date_Year']

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                A.Appointment_ID,
                A.Time,
                S.First_Name AS Staff_FirstName,
                S.Last_Name AS Staff_LastName,
                O.First_Name AS Owner_FirstName,
                O.Last_Name AS Owner_LastName,
                P.Name AS Pet_Name,
                A.Status
            FROM APPOINTMENT A
            JOIN STAFF S ON A.Staff_ID = S.Staff_ID
            JOIN OWNER O ON A.Owner_ID = O.Owner_ID
            JOIN PET P ON A.Pet_ID = P.Pet_ID
            WHERE A.Date_Day = %s AND A.Date_Month = %s AND A.Date_Year = %s
            ORDER BY A.Time
        """, (date_day, date_month, date_year))
        appointments = cur.fetchall()
        cur.close()

        return render_template('view_appointments_by_date.html', appointments=appointments, search_date=f"{date_month}/{date_day}/{date_year}")

    return render_template('view_appointments_by_date.html', appointments=None)

# Create Appointment
@app.route('/create_appointment', methods=['GET', 'POST'])
def create_appointment():
    if request.method == 'POST':
        try:
            Appointment_ID = request.form['Appointment_ID']
            Date_Day = request.form['Date_Day']
            Date_Month = request.form['Date_Month']
            Date_Year = request.form['Date_Year']
            Time = request.form['Time']
            Staff_ID = request.form['Staff_ID']
            Owner_ID = request.form['Owner_ID']
            Pet_ID = request.form['Pet_ID']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO APPOINTMENT
                (Appointment_ID, Date_Day, Date_Month, Date_Year, Time, Staff_ID, Owner_ID, Pet_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (Appointment_ID, Date_Day, Date_Month, Date_Year, Time, Staff_ID, Owner_ID, Pet_ID))
            mysql.connection.commit()
            cur.close()

            flash('Appointment created successfully!', 'success')
            return redirect('/appointment_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/appointment_management')

    return render_template('create_appointment.html')

# Delete Appointment
@app.route('/delete_appointment', methods=['GET', 'POST'])
def delete_appointment():
    if request.method == 'POST':
        try:
            Appointment_ID = request.form['Appointment_ID']

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM APPOINTMENT WHERE Appointment_ID = %s", (Appointment_ID,))
            mysql.connection.commit()
            cur.close()

            flash(f"Appointment {Appointment_ID} deleted successfully.", 'success')
            return redirect('/appointment_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/appointment_management')

    return render_template('delete_appointment.html')

# Update Appointment Status
@app.route('/update_appointment_status', methods=['GET', 'POST'])
def update_appointment_status():
    if request.method == 'POST':
        try:
            Appointment_ID = request.form['Appointment_ID']
            Status = request.form['Status']

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE APPOINTMENT 
                SET Status = %s 
                WHERE Appointment_ID = %s
            """, (Status, Appointment_ID))
            mysql.connection.commit()
            cur.close()

            flash(f"Appointment {Appointment_ID} status updated to {Status}.", 'success')
            return redirect('/appointment_management')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect('/appointment_management')

    return render_template('update_appointment_status.html')
    
@app.route('/stats')
def stats():
    # use a dict cursor so we can reference columns by name
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # 1) Appointment Status Summary
    cur.execute("""
        SELECT Status, COUNT(*) AS count
        FROM APPOINTMENT
        GROUP BY Status
    """)
    rows = cur.fetchall()
    status_summary = {'Scheduled': 0, 'Completed': 0, 'Cancelled': 0}
    for row in rows:
        status_summary[row['Status']] = row['count']

    # 2) Total Revenue (assumes you have SERVICE & APPOINTMENT_SERVICES tables)
    cur.execute("""
        SELECT COALESCE(SUM(s.Price), 0) AS revenue
        FROM APPOINTMENT a
        JOIN APPOINTMENT_SERVICES aps ON a.Appointment_ID = aps.Appointment_ID
        JOIN SERVICE s              ON aps.Service_ID     = s.Service_ID
        WHERE a.Status = 'Completed'
    """)
    total_revenue = cur.fetchone()['revenue']

    # 3) Top Staff Members by completed appts
    cur.execute("""
        SELECT s.First_Name, s.Last_Name, COUNT(*) AS completed_count
        FROM APPOINTMENT a
        JOIN STAFF s ON a.Staff_ID = s.Staff_ID
        WHERE a.Status = 'Completed'
        GROUP BY a.Staff_ID
        ORDER BY completed_count DESC
        LIMIT 5
    """)
    top_staff = cur.fetchall()

    # 4) Appointments This Month
    now = datetime.now()
    cur.execute("""
        SELECT COUNT(*) AS count
        FROM APPOINTMENT
        WHERE Date_Month = %s AND Date_Year = %s
    """, (str(now.month), str(now.year)))
    current_month_appointments = cur.fetchone()['count']

    cur.close()

    return render_template('stats.html',
        status_summary=status_summary,
        total_revenue=total_revenue,
        top_staff=top_staff,
        current_month_appointments=current_month_appointments,
        now=now
    )





if __name__ == '__main__':
    app.run(debug=True)


