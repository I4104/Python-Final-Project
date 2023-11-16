from flask import Flask, render_template, request, redirect, session
import mysql.connector

# Khởi tạp kết nối tới MySQL
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root', 
    password = '',
    database = 'quanlynhahang'
)

# Tạo cursor để thao tác với MySQL
cursor = conn.cursor()

# Khởi tạo Flask App
app = Flask(__name__)

# Tạo key cho app để sử dụng session
app.secret_key = "1234567"

# Trang chủ
@app.route("/", methods=['GET'])
def index():
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    # Lấy danh sách bàn ăn
    cursor.execute(f"SELECT * FROM ban_an")
    ban_an = cursor.fetchall()
    return render_template("index.html", ban_an = ban_an)

# Đặt bàn
@app.route("/dat_ban/<ban_id>", methods=['GET', "POST"])
def datban(ban_id):
    # Kiểm tra session xem đã đăng nhập tài khoản hay chưa
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    if (ban_id is None):
        # Nếu bàn ăn không tồn tại
        return redirect("/")

    # Kiểm tra xem bàn ăn có tồn tại trong MySQL hay không và đã được đặt trước hay chưa
    cursor.execute(f"SELECT * FROM ban_an WHERE id = {ban_id} AND dat_truoc = 0")
    ban_an = cursor.fetchall()
    if (len(ban_an) > 0):
        if (request.method == "GET"):
            # Lấy danh sách món ăn
            cursor.execute(f"SELECT * FROM mon_an WHERE trangthai = 1")
            mon_an = cursor.fetchall()
            return render_template("datban.html", ban_id = ban_id, mon_an = mon_an)

        if request.method == "POST":
            username = session.get("username")
            mon_an = []
            for item in request.form:
                if int(request.form[item]) > 0:
                    mon_an.append(f"{item}: {request.form[item]} đĩa")

            if (len(mon_an) > 0):
                # Tạo thực đơn cách nhau bở dấu ','
                thuc_don = ", ".join(mon_an) 

                # Thêm thông tin vào bảng orders
                cursor.execute(f"INSERT INTO orders(username, ban_id, mon_an) VALUES ('{username}', '{ban_id}', '{thuc_don}')")

                # Chuyển trạng thái bàn ăn thành đã đặt trước
                cursor.execute(f"UPDATE ban_an SET dat_truoc = 1 WHERE id = {ban_id}")

                # Commit Changes
                conn.commit()

                # Khách đặt bàn thành công, chuyển khách về trang chủ
                return """
                    <script>
                        alert('Đặt bàn thành công'); 
                        window.location.href = '/'
                    </script>
                """;
            else:
                # Nếu khách đặt bàn nhưng ko đặt món ăn nào, thông báo và chuyển khách về trang chọn món
                return """
                    <script>
                        alert('Vui lòng đặt chọn món'); 
                        window.history.go(-1)
                    </script>
                """;
            return mon_an
    else:
        # Bàn không tồn tại, chuyển người dùng về trang chủ
        return """
            <script>
                alert('Bàn không tồn tại hoặc đã có người đặt trước'); 
                window.location.href = '/'
            </script>
        """;

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
                return """
                    <script>
                        alert('Tài khoản đã tồn tại'); 
                        window.history.go(-1)
                    </script>
                """;
            else:
                session["username"] = username
                cursor.execute(f"INSERT INTO users(username, password) VALUES ('{username}', '{password}')")
                conn.commit()
                return """
                    <script>
                        alert('Đăng ký thành công!'); 
                        window.location.href = '/'
                    </script>
                """;
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
                return """
                    <script>
                        alert('Đăng nhập thành công!'); 
                        window.location.href = '/'
                    </script>
                """;
            else:
                return """
                    <script>
                        alert('Đăng nhập thất bại! Tài khoản hoặc mật khẩu không chính xác'); 
                        window.history.go(-1)
                    </script>
                """;
    else:
        # Nếu người dùng đã đăng nhập, chuyển về trang chủ
        return redirect("/")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    if (request.method == "GET"):
        cursor.execute(f"SELECT * FROM ban_an")
        ban_an = cursor.fetchall()
        return render_template("admin/index.html", ban_an = ban_an)

    if (request.method == "POST"):
        soluong = request.form.get("soluong")

        cursor.execute(f"INSERT INTO ban_an(soluong) VALUES ('{soluong}')")
        conn.commit()
        return """
            <script>
                alert('Thêm bàn ăn thành công!'); 
                window.location.href = '/admin'
            </script>
        """;

@app.route("/admin/view/<ban_id>", methods=['GET', 'POST'])
def view(ban_id):
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    cursor.execute(f"SELECT * FROM orders WHERE ban_id = {ban_id}")
    orders = cursor.fetchall()

    # Chuyển string Thực đơn đã lưu trong sql thành dạng list bằng split
    # 0 là lấy dòng đầu tiên, 3 là lấy cột thực đơn trong bảng orders
    orders = orders[0][3].split(", ")
    return render_template("admin/view.html", orders = orders, ban_id = ban_id)

@app.route("/admin/mon_an", methods=['GET', 'POST'])
def monan():
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    if (request.method == "GET"):
        cursor.execute(f"SELECT * FROM mon_an")
        mon_an = cursor.fetchall()
        return render_template("admin/monan.html", mon_an = mon_an)

    if (request.method == "POST"):
        name = request.form.get("name")
        price = request.form.get("price")

        cursor.execute(f"SELECT * FROM mon_an WHERE name = '{name}'")
        mon_an = cursor.fetchall()
        if (len(mon_an) > 0):
            return """
                <script>
                    alert('Món ăn đã tồn tại'); 
                    window.history.go(-1)
                </script>
            """;
        else:
            cursor.execute(f"INSERT INTO mon_an(name, price) VALUES ('{name}', '{price}')")
            conn.commit()
            return """
                <script>
                    alert('Thêm món ăn thành công!'); 
                    window.location.href = '/admin/mon_an'
                </script>
            """;

@app.route("/admin/edit/mon_an/<mon_id>", methods=['GET', 'POST'])
def edit_monan(mon_id):
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    if (request.method == "GET"):
        cursor.execute(f"SELECT * FROM mon_an WHERE id = {mon_id}")
        mon_an = cursor.fetchall()
        return render_template("admin/edit_mon.html", row = mon_an[0])

    if (request.method == "POST"):
        name = request.form.get("name")
        price = request.form.get("price")
        trangthai = request.form.get("trangthai")

        cursor.execute(f"SELECT * FROM mon_an WHERE id = '{mon_id}'")
        users = cursor.fetchall()
        if (len(users) > 0):
            cursor.execute(f"UPDATE mon_an SET name = '{name}', price = '{price}', trangthai = '{trangthai}' WHERE id = '{mon_id}'")
            conn.commit()
            return """
                <script>
                    alert('Sửa món ăn thành công!'); 
                    window.location.href = '/admin/mon_an'
                </script>
            """;
        else:
            return """
                <script>
                    alert('Món ăn ko tồn tại'); 
                    window.history.go(-1)
                </script>
            """;

@app.route("/admin/delete/mon_an/<mon_id>", methods=['GET'])
def delete_monan(mon_id):
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    cursor.execute(f"SELECT * FROM mon_an WHERE id = {mon_id}")
    mon_an = cursor.fetchall()

    if (len(mon_an) > 0):
        cursor.execute(f"DELETE FROM mon_an WHERE id = {mon_id}")
        conn.commit()
        return """
            <script>
                alert('Xóa món ăn thành công!'); 
                window.location.href = '/admin/mon_an'
            </script>
        """;
    else:
        return """
            <script>
                alert('Món ăn ko tồn tại'); 
                window.history.go(-1)
            </script>
        """;

@app.route("/admin/delete/ban_an/<ban_id>", methods=['GET'])
def delete_ban_an(ban_id):
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    cursor.execute(f"SELECT * FROM ban_an WHERE id = {ban_id}")
    ban_an = cursor.fetchall()

    if (len(ban_an) > 0):
        cursor.execute(f"DELETE FROM ban_an WHERE id = {ban_id}")
        conn.commit()
        return """
            <script>
                alert('Xóa bàn ăn thành công!'); 
                window.location.href = '/admin'
            </script>
        """;
    else:
        return """
            <script>
                alert('Bàn ăn ko tồn tại'); 
                window.history.go(-1)
            </script>
        """;

@app.route("/admin/return/<ban_id>", methods=['GET'])
def traban(ban_id):
    if not session.get("username"):
        # Nếu chưa đăng nhập, chuyển người dùng tới trang đăng nhập
        return redirect("/login")

    cursor.execute(f"SELECT * FROM ban_an WHERE id = {ban_id} AND dat_truoc = 1")
    ban_an = cursor.fetchall()

    if (len(ban_an) > 0):
        cursor.execute(f"UPDATE ban_an SET dat_truoc = 0 WHERE id = {ban_id}")
        cursor.execute(f"DELETE FROM orders WHERE ban_id = {ban_id}")
        conn.commit()
        return """
            <script>
                alert('Đã trả bàn thành công!'); 
                window.location.href = '/admin'
            </script>
        """;
    else:
        return """
            <script>
                alert('Bàn này không tồn tại hoặc chưa có ai đặt trước'); 
                window.history.go(-1)
            </script>
        """;

app.run()