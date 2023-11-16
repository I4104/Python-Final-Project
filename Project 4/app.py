from flask import Flask,render_template, session,redirect, request,  abort
import mysql.connector

app = Flask(__name__)
conn = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='',
    database ='nhansu'
)

cursor = conn.cursor()

app.secret_key = "123223"    

# đăng ký
@app.route("/dangki")
def signup():
    return render_template("sign_up.html")

# đăng nhập
@app.route("/")
def dangnhap():
    return render_template("login.html")


# in ra dữ liệu từ các bảng
@app.route('/nhansu') 
def nhansu():
    if not session.get("gmail"):
        return redirect ("/")
    cursor.execute("SELECT * FROM quanlynhansu")
    data = cursor.fetchall()
    return render_template('nhansu.html', data=data)

@app.route('/thuctap')
def thuctap():
    if not session.get("gmail"):
        return redirect("/")
    cursor.execute("SELECT * FROM danhsachthuctap")
    data = cursor.fetchall()
    return render_template('thuctap.html', data=data)

# tìm kiếm thông tin
@app.route('/searchnhansu')
def search():
    keyword = request.args.get('keyword')
    cursor.execute("SELECT * FROM quanlynhansu WHERE Cc LIKE %s", ("%" + keyword + "%",))
    results = cursor.fetchall()
    return render_template('timkiemns.html', results=results)

@app.route('/searchtt')
def searchcv():
    keyword = request.args.get('keyword')
    cursor.execute("SELECT * FROM danhsachthuctap WHERE Cc LIKE %s", ("%" + keyword + "%",))
    results = cursor.fetchall()
    return render_template('timkiemtt.html', results=results)

# thêm thông tin
@app.route("/nhansu/themns")
def themsv():
   if not session.get("gmail"):
      return redirect ("/")
   return render_template("themns.html")

@app.route('/themnss', methods=["POST"])
def themnss():
    if request.method == 'POST':
        Ten = request.form.get("Ten")
        Cc = request.form.get("Cc")
        Ngaysinh = request.form.get("Ngaysinh")
        Que = request.form.get("Que")
        Sdt = request.form.get("Sdt")
        
        cursor.execute("SELECT * FROM quanlynhansu WHERE Cc = %s OR Sdt = %s", (Cc, Sdt))
        quanlynhansu = cursor.fetchall()

        if quanlynhansu:
            return "Thêm thông tin thất bại"
        
        else:
            cursor.execute("INSERT INTO quanlynhansu (Ten, Cc, Ngaysinh, Que, Sdt) VALUES (%s, %s, %s, %s, %s)",
                           (Ten, Cc, Ngaysinh, Que, Sdt))
            conn.commit()
            return redirect("nhansu")
@app.route("/thuctap/themtt")
def themtt():
    if not session.get("gmail"):
        return redirect ("/") 
    return render_template("themtt.html")

@app.route('/themttt', methods=["POST"])
def themttt():
    if request.method == 'POST':
        Ten = request.form.get("Ten")
        Cc = request.form.get("Cc")
        Tuoi = request.form.get("Tuoi")
        home = request.form.get("home")
        Sdt = request.form.get("Sdt")

        cursor.execute("SELECT * FROM danhsachthuctap WHERE Cc = %s OR Sdt = %s", (Cc, Sdt))
        danhsachthuctap = cursor.fetchall()

        if danhsachthuctap:
            return "Thêm thông tin thất bại"
        
        else:
            cursor.execute("INSERT INTO danhsachthuctap (Ten, Cc, Tuoi, home, Sdt) VALUES (%s, %s, %s, %s, %s)",
                           (Ten, Cc, Tuoi, home, Sdt))
            conn.commit()
            return redirect("thuctap")
        
# sửa thông tin      
@app.route("/update_ns/<item_id>", methods=["POST"])
def update_ns(item_id):
    Ten = request.form.get("Ten")
    Cc = request.form.get("Cc")
    Ngaysinh = request.form.get("Ngaysinh")
    Que = request.form.get("Que")
    Sdt = request.form.get("Sdt")
    
    cursor.execute("UPDATE quanlynhansu SET Ten = %s, Cc = %s, Ngaysinh = %s, Que = %s, Sdt = %s WHERE id = %s",
                   (Ten, Cc, Ngaysinh, Que, Sdt, item_id))
    conn.commit()
    return redirect("/nhansu")

@app.route("/edit_ns/<item_id>", methods=["GET"])
def edit_ns(item_id):
    cursor.execute("SELECT * FROM quanlynhansu WHERE id = %s", (item_id,))
    nhansu = cursor.fetchone()
    
    if nhansu:
        return render_template("update.html", nhansu=nhansu)
    else:
        return redirect("/nhansu")
    

@app.route("/update_tt/<item_id>", methods=["POST"])
def update_tt(item_id):
    Ten = request.form.get("Ten")
    Cc = request.form.get("Cc")
    Tuoi = request.form.get("Tuoi")
    home = request.form.get("home")
    Sdt = request.form.get("Sdt")

    cursor.execute("UPDATE danhsachthuctap SET Ten = %s, Cc = %s, Tuoi = %s, home = %s, Sdt = %s WHERE id = %s",
                   (Ten, Cc, Tuoi, home, Sdt, item_id))
    conn.commit()
    return redirect("/thuctap")

@app.route("/edit_tt/<item_id>", methods=["GET"])
def edit_tt(item_id):
    cursor.execute("SELECT * FROM danhsachthuctap WHERE id = %s", (item_id,))
    thuctap = cursor.fetchone()

    if thuctap:
        return render_template("updatett.html", thuctap=thuctap)
    else:
        return redirect("/thuctap")
    
# xoá thông tin
@app.route('/delete_ns/<item_id>', methods=['GET'])
def delete(item_id):
    cursor.execute(f"DELETE FROM quanlynhansu WHERE id = {item_id}")
    conn.commit()
    return redirect('/nhansu')

@app.route('/delete_tt/<item_id>', methods=['GET'])
def deletett(item_id):
    cursor.execute(f"DELETE FROM danhsachthuctap WHERE id = {item_id}")
    conn.commit()
    return redirect('/thuctap')
# kiểm tra dữ liệu đầu vào với dữ liệu trên sql để đăng nhập
@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        gmail = request.form.get("gmail")
        password = request.form.get("password")

        query = "SELECT * FROM admin WHERE gmail = %s AND password = %s"
        cursor.execute(query, (gmail, password))
        admin = cursor.fetchall()

        if admin:
            session["gmail"] = gmail
            return redirect('nhansu')
        else:
            return "Đăng nhập thất bại, vui lòng thử lại"
    
# kiểm tra thông tin admin đã tồn tại chưa, nếu chưa thì đăng ký
@app.route('/sign_up', methods=["POST"])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        gmail = request.form.get("gmail")

        cursor.execute("SELECT * FROM admin WHERE username = %s OR gmail = %s", (username, gmail))
        admin = cursor.fetchall()

        if admin:
            return "Đăng kí thất bại"
        else:
            cursor.execute("INSERT INTO admin (username, password, gmail) VALUES (%s, %s, %s)", (username, password, gmail))
            conn.commit()
            return redirect("/")
    admin
app.run()





