from flask import Flask,render_template, session,redirect, request,  abort
import mysql.connector

app = Flask(__name__)
conn = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password ='',
    database ='qlnhansu'
)

cursor = conn.cursor()

app.secret_key = "11212"    




# in ra dữ liệu từ các bảng
@app.route('/nhansu') 
def nhansu():
    if not session.get("gmail"):
        return redirect ("/")
    cursor.execute("SELECT * FROM quanlynhansu")
    data = cursor.fetchall()
    return render_template('nhansu.html', data=data)

@app.route('/congviec')
def congviec():
    if not session.get("gmail"):
        return redirect("/")
    cursor.execute("SELECT * FROM quanlycongviec")
    data = cursor.fetchall()
    return render_template('congviec.html', data=data)
# đăng ký
@app.route("/dangki")
def signup():
    return render_template("sign_up.html")

# đăng nhập
@app.route("/")
def dangnhap():
    return render_template("login.html")
# tìm kiếm thông tin
@app.route('/searchnhansu')
def search():
    keyword = request.args.get('keyword')
    cursor.execute("SELECT * FROM quanlynhansu WHERE Cc LIKE %s", ("%" + keyword + "%",))
    results = cursor.fetchall()
    return render_template('timkiemns.html', results=results)

@app.route('/searchcv')
def searchcv():
    keyword = request.args.get('keyword')
    cursor.execute("SELECT * FROM quanlycongviec WHERE Ten LIKE %s", ("%" + keyword + "%",))
    results = cursor.fetchall()
    return render_template('timkiemcv.html', results=results)

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
        Nganh = request.form.get("Nganh")
        Sdt = request.form.get("Sdt")
        
        cursor.execute("SELECT * FROM quanlynhansu WHERE Cc = %s OR Sdt = %s", (Cc, Sdt))
        quanlynhansu = cursor.fetchall()

        if quanlynhansu:
            return "Thêm thông tin thất bại"
        
        else:
            cursor.execute("INSERT INTO quanlynhansu (Ten, Cc, Ngaysinh, Nganh, Sdt) VALUES (%s, %s, %s, %s, %s)",
                           (Ten, Cc, Ngaysinh, Nganh, Sdt))
            conn.commit()
            return redirect("nhansu")
@app.route("/congviec/themcv")
def themcv():
    if not session.get("gmail"):
        return redirect ("/") 
    return render_template("themcv.html")

@app.route('/themcvt', methods=["POST"])
def themcvt():
    if request.method == 'POST':
        Ten = request.form.get("Ten")
        soluongnhanluc = request.form.get("soluongnhanluc")
        Tuoi = request.form.get("Tuoi")
        mucluong = request.form.get("mucluong")
        thoigian = request.form.get("thoigian")

        cursor.execute("SELECT * FROM quanlycongviec WHERE Ten = %s", (Ten,))
        quanlycongviec = cursor.fetchall()

        if quanlycongviec:
            return "Thêm thông tin thất bại"
        
        else:
            cursor.execute("INSERT INTO quanlycongviec (Ten, soluongnhanluc, Tuoi, mucluong, thoigian) VALUES (%s, %s, %s, %s, %s)",
                           (Ten, soluongnhanluc, Tuoi, mucluong, thoigian))
            conn.commit()
            return redirect("congviec")
        
# sửa thông tin      
@app.route("/update_ns/<item_id>", methods=["POST"])
def update_ns(item_id):
    Ten = request.form.get("Ten")
    Cc = request.form.get("Cc")
    Ngaysinh = request.form.get("Ngaysinh")
    Nganh = request.form.get("Nganh")
    Sdt = request.form.get("Sdt")
    
    cursor.execute("UPDATE quanlynhansu SET Ten = %s, Cc = %s, Ngaysinh = %s, Nganh = %s, Sdt = %s WHERE id = %s",
                   (Ten, Cc, Ngaysinh, Nganh, Sdt, item_id))
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
@app.route("/update_cv/<item_id>", methods=["POST"])
def update_cv(item_id):
    Ten = request.form.get("Ten")
    soluongnhanluc = request.form.get("soluongnhanluc")
    Tuoi = request.form.get("Tuoi")
    mucluong = request.form.get("mucluong")
    thoigian = request.form.get("thoigian")

    cursor.execute("UPDATE quanlycongviec SET Ten = %s, soluongnhanluc = %s, Tuoi = %s, mucluong = %s, thoigian = %s WHERE id = %s",
                   (Ten, soluongnhanluc, Tuoi, mucluong, thoigian, item_id))
    conn.commit()
    return redirect("/congviec")

@app.route("/edit_cv/<item_id>", methods=["GET"])
def edit_cv(item_id):
    cursor.execute("SELECT * FROM quanlycongviec WHERE id = %s", (item_id,))
    congviec = cursor.fetchone()

    if congviec:
        return render_template("updatecv.html", congviec=congviec)
    else:
        return redirect("/congviec")
    
# xoá thông tin
@app.route('/delete_ns/<item_id>', methods=['GET'])
def delete(item_id):
    cursor.execute(f"DELETE FROM quanlynhansu WHERE id = {item_id}")
    conn.commit()
    return redirect('/nhansu')

@app.route('/delete_cv/<item_id>', methods=['GET'])
def deletecv(item_id):
    cursor.execute(f"DELETE FROM quanlycongviec WHERE id = {item_id}")
    conn.commit()
    return redirect('/congviec')
# kiểm tra dữ liệu đầu vào với dữ liệu trên sql để đăng nhập
@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        gmail = request.form.get("gmail")
        matkhau = request.form.get("matkhau")

        query = "SELECT * FROM taikhoan WHERE gmail = %s AND matkhau = %s"
        cursor.execute(query, (gmail, matkhau))
        taikhoan = cursor.fetchall()

        if taikhoan:
            session["gmail"] = gmail
            return redirect('nhansu')
        else:
            return "Đăng nhập thất bại, vui lòng thử lại"
    
# kiểm tra thông tin taikhoan đã tồn tại chưa, nếu chưa thì đăng ký
@app.route('/sign_up', methods=["POST"])
def sign_up():
    if request.method == 'POST':
        tendangnhap = request.form.get("tendangnhap")
        matkhau = request.form.get("matkhau")
        gmail = request.form.get("gmail")

        cursor.execute("SELECT * FROM taikhoan WHERE tendangnhap = %s OR gmail = %s", (tendangnhap, gmail))
        taikhoan = cursor.fetchall()

        if taikhoan:
            return "Đăng kí thất bại"
        else:
            cursor.execute("INSERT INTO taikhoan (tendangnhap, matkhau, gmail) VALUES (%s, %s, %s)", (tendangnhap, matkhau, gmail))
            conn.commit()
            return redirect("/")
    taikhoan
app.run()





