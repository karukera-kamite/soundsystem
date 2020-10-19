import mysql.connector
from passlib.hash import sha256_crypt

mydb = mysql.connector.connect(
  host="localhost",
  user="jonathan",
  passwd="gnipod8*",
  database="soundsystem"
)
mycursor = mydb.cursor()

sql = "INSERT INTO users (login, password, firstname, lastname, birth, sex) VALUES (%s, %s,%s, %s, %s, %s)"
val = ('koup.bo@nintendo.jp',sha256_crypt.hash('qsdfgh'),'bowzer','koupa','1970-05-09',1)

mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")
