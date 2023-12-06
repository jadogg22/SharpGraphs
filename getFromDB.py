import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect("test.db")

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

def getOrdersByDateRange(startDate, endDate):
    cursor.execute('SELECT * FROM Orders WHERE DeliveryDate BETWEEN ? AND ?', (startDate, endDate))
    return cursor.fetchall()

def getOrdersByWeek(week):
    # week is a string in the format of "2023 W40"
    cursor.execute('SELECT * FROM Orders WHERE Week = ?', (week,))
    return cursor.fetchall()

def getOrdersByMonth(month):
    # month is a string in the format of "2023 M10"
    cursor.execute('SELECT * FROM Orders WHERE Month = ?', (month,))
    return cursor.fetchall()

def getOrdersByQuarter(quarter):
    # quarter is a string in the format of "2023 Q04"
    cursor.execute('SELECT * FROM Orders WHERE Quarter = ?', (quarter,))
    return cursor.fetchall()

def getAvailableWeeks():
    cursor.execute('SELECT DISTINCT Week FROM Orders')
    return cursor.fetchall()

def getAvailableMonths():
    cursor.execute('SELECT DISTINCT Month FROM Orders')
    return cursor.fetchall()

def getAvailableQuarters():
    cursor.execute('SELECT DISTINCT Quarter FROM Orders')
    return cursor.fetchall()






