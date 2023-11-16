from flask import Flask, render_template, request, redirect, session
from db_config import conn, cursor

# Khởi tạo Flask App
app = Flask(__name__)

# Tạo key cho app để sử dụng session
app.secret_key = "1234567"

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    if (request.method == "GET"):
        return render_template("booking.html")
    else:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        table_type = request.form.get("type")
        amount = request.form.get("amount")
        placement = request.form.get("placement")
        date = request.form.get("date")
        time = request.form.get("time")
        note = request.form.get("note")

        cursor.execute(f"INSERT INTO booking SET name = '{name}', phone = '{phone}', email = '{email}', type = '{table_type}', amount = '{amount}', placement = '{placement}', date = '{date}', time = '{time}', note = '{note}'")
        conn.commit()

        cursor.execute(f"SELECT * FROM customer WHERE name = '{name}' AND email = '{email}'")
        customer = cursor.fetchall()
        if (len(customer) == 0):
            cursor.execute(f"INSERT INTO customer SET name = '{name}', email = '{email}', phone = '{phone}'")
            conn.commit()

        return f"Bạn đã đặt bàn vào ngày {date}, thời gian: {time} thành công";


@app.route("/menu", methods=['GET'])
def menu():
    return render_template("menu.html")

@app.route("/contact", methods=['GET'])
def contact():
    return render_template("contact.html")

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/admin", methods=['GET'])
def admin():
    cursor.execute("SELECT * FROM booking")
    booking = cursor.fetchall()
    return render_template("admin/index.html", booking = booking)

@app.route("/admin/person", methods=['GET'])
def admin_person():
    cursor.execute("SELECT * FROM customer")
    customer = cursor.fetchall()
    return render_template("admin/person.html", customer = customer)

@app.route("/admin/delete/<booking_id>", methods=['GET'])
def admin_delete(booking_id):
    cursor.execute(f"SELECT * FROM booking WHERE id = {booking_id}")
    booking = cursor.fetchone()
    if (len(booking) > 0):
        cursor.execute(f"DELETE FROM booking WHERE id = '{booking_id}'")
        conn.commit()

@app.route("/admin/edit/<booking_id>", methods=['GET', 'POST'])
def admin_edit(booking_id):
    cursor.execute(f"SELECT * FROM booking WHERE id = {booking_id}")
    booking = cursor.fetchone()
    if (len(booking) > 0):
        if (request.method == "GET"):
            return render_template("admin/edit.html", booking = booking)
        else:
            name = request.form.get("name")
            phone = request.form.get("phone")
            email = request.form.get("email")
            table_type = request.form.get("type")
            amount = request.form.get("amount")
            placement = request.form.get("placement")
            cursor.execute(f"UPDATE booking SET name = '{name}', phone = '{phone}', email = '{email}', type = '{table_type}', amount = '{amount}', placement = '{placement}' WHERE id = '{booking_id}'")
            conn.commit()
            return redirect("/admin")
    else:
        return redirect("/admin")

@app.route("/login", methods=['GET', "POST"])
def login():
    if not session.get("username"):
        if (request.method == "GET"):   
            return render_template("login.html")
        else:
            username = request.form.get("username")
            password = request.form.get("password")

            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            users = cursor.fetchall()
            if (len(users) > 0):
                session["username"] = username
                return f"Đăng nhập thành công!";
            else:
                return f"Đăng nhập thất bại! Tài khoản hoặc mật khẩu không chính xác";
    else:
        return redirect("/")

app.run()