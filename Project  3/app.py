from flask import Flask, render_template, request, redirect, session
import mysql.connector

# Khởi tạp kết nối tới MySQL
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root', 
    password = '',
    database = 'quanlydonhang'
)

# Tạo cursor để thao tác với MySQL
cursor = conn.cursor()

# Khởi tạo Flask App
app = Flask(__name__)

# Tạo key cho app để sử dụng session
app.secret_key = "1234567"

# Trang chủ
@app.route("/", methods=['GET', 'POST'])
def index():
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy danh sách đơn hàng
    cursor.execute(f"SELECT * FROM orders")
    orders = cursor.fetchall()
    return render_template("index.html", orders = orders)

# Xem chi tiết đơn hàng
@app.route("/view/<order_id>", methods=['GET', 'POST'])
def view(order_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy thông tin hàng hóa
    cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")
    orders = cursor.fetchall()

    # Lấy danh sách hàng hóa
    cursor.execute(f"SELECT * FROM product")
    product = cursor.fetchall()

    if (request.method == "GET"):
        if (len(orders) > 0):
            cursor.execute(f"SELECT * FROM orders_detail WHERE orders_id = {order_id}")
            orders_detail = cursor.fetchall()
            return render_template("view.html", orders = orders[0], orders_detail = orders_detail, product = product)
        else:
            # Nếu đơn hàng không tồn tại, chuyển người dùng về trang product
            return "<script>alert('Mặt hàng không tồn tại'); window.location.href = '/product' </script>";

    if (request.method =="POST"):
        status = request.form.get("status")
        if (len(orders) > 0):
            cursor.execute(f"UPDATE orders SET status = {status} WHERE id = {order_id}")
            conn.commit()
            return f"<script>alert('Lưu thông tin thành công'); window.location.href = '/view/{order_id}' </script>";
        else:
            # Nếu đơn hàng không tồn tại, chuyển người dùng về trang product
            return "<script>alert('Mặt hàng không tồn tại'); window.location.href = '/product' </script>";

# Thêm đơn hàng
@app.route("/add/orders", methods=['POST'])
def add_orders():
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    name = request.form.get("name")
    status = request.form.get("status")
    cursor.execute(f"INSERT INTO orders(name, status) VALUES ('{name}', '{status}')")
    conn.commit()
    return f"<script>alert('Lưu thông tin thành công'); window.location.href = '/' </script>";

# Xóa hàng hóa
@app.route("/delete/orders/<orders_id>", methods=['GET'])
def delete_orders(orders_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy thông tin hàng hóa
    cursor.execute(f"SELECT * FROM orders WHERE id = {orders_id}")
    orders = cursor.fetchall()
    if (len(orders) > 0):
        cursor.execute(f"DELETE FROM orders WHERE id = {orders_id}")
        conn.commit()
        return "<script>alert('Xóa đơn hàng thành công!'); window.location.href = '/' </script>";
    else:
        # Nếu mặt hàng không tồn tại, chuyển người dùng về trang product
        return "<script>alert('Đơn hàng không tồn tại'); window.location.href = '/' </script>";
    
# Thêm mặt hàng vào đơn hàng
@app.route("/view/add/<order_id>", methods=['POST'])
def add_view(order_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy thông tin hàng hóa
    cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")
    orders = cursor.fetchall()
    
    name = request.form.get("name")
    soluong = request.form.get("soluong")
    if (len(orders) > 0):
        cursor.execute(f"SELECT * FROM product WHERE name = '{name}'")
        product = cursor.fetchall()[0]

        cursor.execute(f"INSERT INTO orders_detail(orders_id, product, soluong, price) VALUES ('{order_id}', '{name}', '{soluong}', '{product[2]}')")
        conn.commit()
        return f"<script>alert('Lưu thông tin thành công'); window.location.href = '/view/{order_id}' </script>";
    else:
        # Nếu đơn hàng không tồn tại, chuyển người dùng về trang product
        return "<script>alert('Mặt hàng không tồn tại'); window.location.href = '/product' </script>";

# Xóa mặt hàng trong đơn hàng
@app.route("/view/delete/<order_id>/<detail_id>", methods=['GET'])
def delete_view(order_id, detail_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy thông tin hàng hóa
    cursor.execute(f"SELECT * FROM orders_detail WHERE id = {detail_id} AND orders_id = {order_id}")
    orders = cursor.fetchall()
    
    if (len(orders) > 0):
        cursor.execute(f"DELETE FROM orders_detail WHERE id = {detail_id}")
        conn.commit()
        return f"<script>alert('Xóa mặt hàng thành công!'); window.location.href = '/view/{order_id}' </script>";
    else:
        # Nếu mặt hàng không tồn tại, chuyển người dùng về trang product
        return f"<script>alert('Mặt hàng không tồn tại'); window.location.href = '/view/{order_id}' </script>";

# Hàng hóa
@app.route("/product", methods=['GET', 'POST'])
def product():
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy danh sách hàng hóa
    cursor.execute(f"SELECT * FROM product")
    product = cursor.fetchall()
    return render_template("product.html", product = product)

# Thêm hàng hóa
@app.route("/add/product", methods=['POST'])
def add_product():
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    name = request.form.get("name")
    price = request.form.get("price")
    status = request.form.get("status")

    cursor.execute(f"SELECT * FROM product WHERE name = '{name}'")
    product = cursor.fetchall()
    if (len(product) > 0):
        return "<script>alert('Mặt hàng đã tồn tại'); window.location.href = '/product' </script>";
    else:
        cursor.execute(f"INSERT INTO product(name, price, status) VALUES ('{name}', '{price}', '{status}')")
        conn.commit()
        return "<script>alert('Thêm mặt hàng thành công!'); window.location.href = '/product' </script>";

# Sửa hàng hóa
@app.route("/edit/product/<product_id>", methods=['GET', 'POST'])
def edit_product(product_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    if (request.method == "GET"):
        # Lấy thông tin hàng hóa
        cursor.execute(f"SELECT * FROM product WHERE id = {product_id}")
        product = cursor.fetchall()
        if (len(product) > 0):
            return render_template("edit_product.html", product = product[0])
        else:
            # Nếu mặt hàng không tồn tại, chuyển người dùng về trang product
            return "<script>alert('Mặt hàng không tồn tại'); window.location.href = '/product' </script>";
    
    if (request.method =="POST"):
        name = request.form.get("name")
        price = request.form.get("price")
        status = request.form.get("status")

        cursor.execute(f"SELECT * FROM product WHERE id = '{product_id}'")
        product = cursor.fetchall()
        if (len(product) > 0):
            cursor.execute(f"UPDATE product SET name = '{name}', price = '{price}', status = '{status}' WHERE id = '{product_id}'")
            conn.commit()
            return "<script>alert('Lưu thông tin thành công!'); window.location.href = '/product' </script>";
        else:
            return "<script>alert('Mặt hàng không tồn tại'); window.location.href = '/product' </script>";

# Xóa hàng hóa
@app.route("/delete/product/<product_id>", methods=['GET'])
def delete_product(product_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy thông tin hàng hóa
    cursor.execute(f"SELECT * FROM product WHERE id = {product_id}")
    product = cursor.fetchall()
    if (len(product) > 0):
        cursor.execute(f"DELETE FROM product WHERE id = {product_id}")
        conn.commit()
        return "<script>alert('Xóa mặt hàng thành công!'); window.location.href = '/product' </script>";
    else:
        # Nếu mặt hàng không tồn tại, chuyển người dùng về trang product
        return "<script>alert('Mặt hàng không tồn tại'); window.location.href = '/product' </script>";

@app.route("/register", methods=['GET', 'POST'])
def register():
    if not session.get("username"):
        if (request.method == "GET"):
            return render_template("register.html")

        if (request.method == "POST"):
            username = request.form.get("username")
            password = request.form.get("password")

            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            users = cursor.fetchall()
            if (len(users) > 0):
                return "<script>alert('Tài khoản đã tồn tại');window.history.go(-1)</script";
            else:
                session["username"] = username
                cursor.execute(f"INSERT INTO users(username, password) VALUES ('{username}', '{password}')")
                conn.commit()
                return "<script>  alert('Đăng ký thành công!');  window.location.href = '/' </script>";
    else:
        # Nếu người dùng đã đăng nhập, chuyển về trang chủ
        return redirect("/")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if not session.get("username"):
        if (request.method == "GET"):
            return render_template("login.html")

        if (request.method == "POST"):
            username = request.form.get("username")
            password = request.form.get("password")

            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            users = cursor.fetchall()
            if (len(users) > 0):
                session["username"] = username
                return "<script>alert('Đăng nhập thành công!'); window.location.href = '/'</script>";
            else:
                return "<script>alert('Đăng nhập thất bại! Tài khoản hoặc mật khẩu không chính xác'); window.history.go(-1)</script>";
    else:
        # Nếu người dùng đã đăng nhập, chuyển về trang chủ
        return redirect("/")

app.run()