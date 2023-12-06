import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect("test.db")

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

def getOrdersByDateRange(startDate, endDate):
    cursor.execute('SELECT * FROM Orders WHERE DeliveryDate BETWEEN ? AND ?', (startDate, endDate))
    return cursor.fetchall()

def getOrdersByDate(date):
    cursor.execute('SELECT * FROM Orders WHERE DeliveryDate = ?', (date,))
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

def getMilesForWeek(week):
    query = '''
        SELECT 
            SUM(LoadedMiles) as TotalLoadedMiles,
            SUM(EmptyMiles) as TotalEmptyMiles,
            SUM(TotalMiles) as TotalTotalMiles,
            COUNT(*) as TotalOrders
        FROM Orders
        WHERE Week = ?
    '''
    cursor.execute(query, (week,))
    columns = [desc[0] for desc in cursor.description]
    result = cursor.fetchone()

    if result:
        return dict(zip(columns, result))
    else:
        return None


def weekToDateRange(str):
    # weeks is a list of tuples
    #dBWeeks = getAvailableWeeks()

    year, week_number = map(int, str.split(" W"))
    # Assuming the week starts on Sunday
    start_date = datetime.strptime(f"{year}-W{week_number}-0", "%Y-W%W-%w")
    # Assuming the week ends on Saturday
    end_date = start_date + timedelta(days=6)
    return start_date.strftime("%m/%d/%y"), end_date.strftime("%m/%d/%y")

def dateRangeToWeeK(startDate, endDate):
    # weeks is a list of tuples
    #dBWeeks = getAvailableWeeks()

    start_date = datetime.strptime(startDate, "%m/%d/%y")
    end_date = datetime.strptime(endDate, "%m/%d/%y")
    # Assuming the week starts on Sunday
    week_number = start_date.strftime("%W")
    year = start_date.strftime("%Y")
    return f"{year} W{week_number}"

def monthlyMilesReport(startWeek, endWeek):
    # month is a string in the format of "2023 W40" and "2023 W50"

    #returns loaded miles, empty miles, total miles, and total orders for each week 
    #in the range of startWeek to endWeek

    #get orders for each week in the range
    orders = []
    for week in range(startWeek, endWeek):
        orders.append(getOrdersByWeek(week))

def getDestinationCountsFromUtahByMonth(month):
    # returns a list of dictionarys for each destination state
    #[{'Destination': 'AZ', 'DestinationCount': 1, 'avgRev': 5.0}]
    query = '''
        SELECT DestinationState, COUNT(*) as DestinationCount, 
            ROUND(AVG(RevTotalMile), 2) as AvgMiles
        FROM Orders
        WHERE OriginState = 'UT' AND Month = ?
        GROUP BY DestinationState 
    '''
    cursor.execute(query, (month,))
    dbData = cursor.fetchall()

    myData = []

    for row in dbData:
        dict = {}
        dict['Destination'] = row[0]
        dict['DestinationCount'] = row[1]
        dict['avgRev'] = row[2]
        myData.append(dict)

    return myData

def getMonthyRevenue(month):
    # returns the total revenue for the month
    query = '''
        SELECT SUM(TotalRevenue) as TotalRevenue
        FROM Orders
        WHERE Month = ?
    '''
    cursor.execute(query, (month,))
    return cursor.fetchone()[0]

def getWeeklyRevenue(week):
    # returns the total revenue for the week by delivery date
    query = '''
        SELECT DeliveryDate, SUM(TotalRevenue) as TotalRevenue
        FROM Orders
        WHERE Week = ?
        GROUP BY DeliveryDate
    '''
    cursor.execute(query, (week,))
    dbData = cursor.fetchall()

    data = []
    for date in dbData:
        dict = {}
        dict['DeliveryDate'] = date[0]
        dict['TotalRevenue'] = date[1]
        data.append(dict)
    return data
        



    







