
from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Database folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database", "travel.db")

# Create database folder
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)


# Create database table
def create_table():
    con = sqlite3.connect(DATABASE)

    con.execute("""
        CREATE TABLE IF NOT EXISTS travellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            contact TEXT,
            email TEXT,
            dob TEXT,
            gender TEXT,
            start_date TEXT,
            end_date TEXT,
            place TEXT,
            trip TEXT,
            services TEXT,
            agree TEXT,
            health TEXT
        )
    """)

    con.commit()
    con.close()


# Open HTML form
@app.route("/")
def home():
    return render_template("index.html")


# Receive form data
@app.route("/submit", methods=["POST"])
def submit():

    first_name = request.form.get("first_name")
    middle_name = request.form.get("middle_name")
    last_name = request.form.get("last_name")
    contact = request.form.get("contact")
    email = request.form.get("email")
    dob = request.form.get("dob")
    gender = request.form.get("gender")

    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    place = request.form.get("place")

    trip = request.form.get("trip")
    services = ", ".join(request.form.getlist("services"))

    agree = request.form.get("agree")
    health = request.form.get("health")

    # Save data into database
    con = sqlite3.connect(DATABASE)

    con.execute("""
        INSERT INTO travellers
        (first_name, middle_name, last_name, contact,
         email, dob, gender, start_date, end_date,
         place, trip, services, agree, health)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        first_name, middle_name, last_name, contact,
        email, dob, gender, start_date, end_date,
        place, trip, services, agree, health
    ))

    con.commit()
    con.close()

    return "Travel Details Saved Successfully!"


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
