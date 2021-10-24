import mysql.connector

def getConn():
    mydb = mysql.connector.connect(
      host="in8.fcomet.com",
      user="dtcorpsc_user",
      password="dtcorpsc_password",
      database="dtcorpsc_mp"
    )
    return mydb


def getCustomer(AM_PM):
    conn = getConn()
    mycursor = conn.cursor()
    query = "SELECT * FROM customers ORDER BY hfn_orderno"
    #if AM_PM != "PM":
    #	query = "SELECT * FROM customers where Qty_AM !=0"
    #else:
    #	query = "SELECT * FROM customers where Qty_PM !=0"
    mycursor.execute(query)
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

def getCustHist(cust):
    cust_hist = {}
    conn = getConn()
    mycursor = conn.cursor()
    for c in cust:
        query = '''
        SELECT date, SUM(lineAM) Morning, SUM(linePM) Evening FROM 
        (SELECT 
         date(upd_ts) AS date
         ,CASE WHEN line = 'AM' then qty ELSE 0 END AS lineAM
         ,CASE WHEN line = 'PM' then qty ELSE 0 END AS linePM
         FROM line l 
         JOIN (SELECT MAX(upd_ts) AS mupd_ts FROM line WHERE cust_id = '''+str(c[0])+''' GROUP BY date(upd_ts),line) d
         ON l.upd_ts =d.mupd_ts
         AND cust_id = '''+str(c[0])+''') agg
        GROUP BY date
        '''
        mycursor.execute(query)
        c_hist = mycursor.fetchall()
        cust_hist[c[0]] = c_hist
    mycursor.close()
    conn.close()
    return cust_hist

