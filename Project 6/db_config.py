import mysql.connector

# Khởi tạp kết nối tới MySQL
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root', 
    password = '',
    database = 'booking_table'
)

# Tạo cursor để thao tác với MySQL
cursor = conn.cursor()