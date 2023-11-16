from flask import Flask, render_template, request, redirect, session
import mysql.connector

# Khởi tạp kết nối tới MySQL
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root', 
    password = '',
    database = 'quanly'
)

# Tạo cursor để thao tác với MySQL
cursor = conn.cursor()


# Khởi tạo Flask App
app = Flask(__name__)

# Tạo key cho app để sử dụng session
app.secret_key = "1234567"

# User UI
@app.route("/", methods=['GET'])
def index():
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy danh sách sản phẩm
    cursor.execute(f"SELECT * FROM product")
    product = cursor.fetchall()
    return render_template("index.html", product = product)

@app.route("/category", methods=['GET'])
def category():
    if not session.get("username"):
        return redirect("/login")

    cursor.execute(f"SELECT * FROM category")
    data = cursor.fetchall() 
    return render_template("category.html", data = data)

@app.route("/add", methods=['GET'])
def add():
    if not session.get("username"):
        return redirect("/login")

    cursor.execute(f"SELECT * FROM category")
    category = cursor.fetchall()
    return render_template("add.html", category = category)

@app.route("/search", methods=['GET'])
def search():
    if not session.get("username"):
        return redirect("/login")

    search = request.args.get("search")

    cursor.execute(f"SELECT * FROM product WHERE name LIKE '%{search}%'")
    search = cursor.fetchall()
    return render_template("index.html", product = search)


@app.route("/edit/<id>", methods=['GET'])
def edit(id):
    if not session.get("username"):
        return redirect("/login")

    # Lấy toàn bộ các loại sản phẩm hiện có
    cursor.execute(f"SELECT * FROM category")
    category = cursor.fetchall()

    # Lấy thông tin sản phẩm bằng id của nó
    cursor.execute(f"SELECT * FROM product WHERE id = '{id}'")
    data = cursor.fetchall()
    if (len(data) > 0):
        # Khi lấy dữ liệu từ sql, ta nhận được 1 list, vì vậy [0] để lấy phần tử đầu tiên
        return render_template("edit.html", category = category, data = data[0])
    else:
        # Nếu sản phẩm đang sửa không còn tồi tại, chuyển lại trang sản phẩm
        return redirect("/")

@app.route("/register", methods=['GET'])
def register():
    if not session.get("username"):
        return render_template("register.html")
    else:
        # Nếu người dùng đã đăng nhập, chuyển về trang chủ
        return redirect("/")

@app.route("/login", methods=['GET'])
def login():
    if not session.get("username"):
        return render_template("login.html")
    else:
        # Nếu người dùng đã đăng nhập, chuyển về trang chủ
        return redirect("/")

@app.route("/logout", methods=['GET'])
def logout():
    session.pop("username")
    return redirect("/login")

# CURD API 
@app.route("/curd/register", methods=['POST'])
def a_register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'")
    users = cursor.fetchall()
    if (len(users) > 0):
        return f"Tài khoản đã tồn tại";
    else:
        session["username"] = username
        cursor.execute(f"INSERT INTO users(username, password, email) VALUES ('{username}', '{password}', '{email}')")
        conn.commit()
        return f"Đăng ký thành công!";

@app.route("/curd/login", methods=['POST'])
def a_login():
    username = request.form.get("username")
    password = request.form.get("password")

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    users = cursor.fetchall()
    if (len(users) > 0):
        session["username"] = username
        return f"Đăng nhập thành công!";
    else:
        return f"Đăng nhập thất bại! Tài khoản hoặc mật khẩu không chính xác";

@app.route("/curd/add/<item>", methods=['POST'])
def ajax_add(item):
    if (item == "category"):
        name = request.form.get('name') 
        if (name == ""):
            return f"Vui lòng nhập đủ thông tin"
        else:
            cursor.execute(f"INSERT INTO category(name) VALUES ('{name}')")
            conn.commit()
            return "Thêm danh mục thành công!"

    if (item == "product"):
        name = request.form.get('name')
        category = request.form.get('category')
        amount = request.form.get('amount')
        price = request.form.get('price')

        if (name == "" or category == "" or amount  == "" or price == ""):
            return f"Vui lòng nhập đủ thông tin"
        else:
            cursor.execute(f"INSERT INTO product(name, category, amount, price) VALUES ('{name}', '{category}', '{amount}', '{price}')")
            conn.commit()
            return "Thêm sản phẩm thành công!"


@app.route("/curd/edit/<id>", methods=['POST'])
def ajax_edit(id):
    cursor.execute(f"SELECT * FROM product WHERE id = '{id}'")
    product = cursor.fetchall()
    if (len(product) > 0):
        name = request.form.get('name')
        category = request.form.get('category')
        amount = request.form.get('amount')
        price = request.form.get('price')

        if (name == "" or category == "" or amount  == "" or price == ""):
            return f"Vui lòng nhập đủ thông tin"
        else:
            cursor.execute(f"UPDATE product SET name = '{name}', category = '{category}', amount = '{amount}', price = '{price}'")
            conn.commit()
            return "Sửa sản phẩm thành công!"
    else:
        return "Sản phẩm không còn tồn tại!"

@app.route("/curd/delete/<item>/<id>", methods=['GET'])
def ajax_delete(item, id):
    if (item == "category"):
        cursor.execute(f"SELECT * FROM category WHERE id = '{id}'")
        category = cursor.fetchall()
        if (len(category) > 0):
            cursor.execute(f"DELETE FROM category WHERE id = '{id}'")
            conn.commit()
            return "Xóa danh mục thành công!"
        else:
            return f"Danh mục không còn tồn tại"
            
    if (item == "product"):
        cursor.execute(f"SELECT * FROM product WHERE id = '{id}'")
        product = cursor.fetchall()
        if (len(product) > 0):
            cursor.execute(f"DELETE FROM product WHERE id = '{id}'")
            conn.commit()
            return "Xóa sản phẩm thành công!"
        else:
            return f"Sản phẩm không còn tồn tại"

app.run()