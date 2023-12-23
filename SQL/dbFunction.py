import pyodbc

def dbConnect():
    try:
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                    'SERVER=TUTU;'
                                    'DATABASE=Test;'
                                    'UID=sa;'
                                    'PWD=abcd123456')
        print("Connection successful")
        return connection
    except pyodbc.Error as e:
        print("Error in connection", e)


