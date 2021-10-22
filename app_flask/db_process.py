import mysql.connector

def getConn():
    mydb = mysql.connector.connect(
      host="in8.fcomet.com",
      user="dtcorpsc_user",
      password="dtcorpsc_password",
      database="dtcorpsc_mp"
    )
    return mydb


def getCustomer():
    conn = getConn()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM customers")
    customers = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return customers

def putLine(sql,val):
    conn = getConn()
    mycursor = conn.cursor()
    mycursor.execute(sql, val)
    conn.commit()
    mycursor.close()
    conn.close()
