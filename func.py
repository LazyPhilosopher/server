from logging import NullHandler
import mysql.connector
from mysql.connector import errorcode

VERBOSE = 1

def commence_db_connection(
    host, user, password 
    ):
    try:
        print("Connecting...")
        cnx =mysql.connector.connect(
        host="localhost",
        user="admin",
        password="Sharicho_3718"
    )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Connection to ", host+'@'+user ," was successful" )
    return cnx

def search_db(
    cursor, db_name
    ):
    cursor.execute("SHOW DATABASES")

    for x in cursor:
        if(x[0] == db_name):
            return 1 
            
    return 0

def clean_cursor(
    cursor, verbose
    ):
    if(verbose == 1):
        for x in cursor:
            print(x)
    else:
        for x in cursor:
            pass

def delete_database(cursor, db_name):
    try:
        cursor.execute(
            "DROP DATABASE  {} ".format(db_name))
    except mysql.connector.Error as err:
        print("Failed deleting database: {}".format(err))
        exit(1)
    if(VERBOSE):
        print("Successfully deleted", db_name)
        return 0

def create_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    if(VERBOSE):    
        print("Successfully created", db_name)

def show_databases(cursor):
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x[0]) 

def add_employee(cursor, first_name, last_name, hire_date, gender, birth_date):
    add_employee = ("INSERT INTO employees "
                   "(first_name, last_name, hire_date, gender, birth_date) "
                   "VALUES (%s, %s, %s, %s, %s)")
    data_employee = (first_name, last_name, hire_date, gender, birth_date)

    # Insert new employee
    cursor.execute(add_employee, data_employee)
    return cursor.lastrowid

def create_tables(cursor, database, TABLES):
    cursor.execute("USE "+ database)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    #cursor.close()

def get_employee_by_job(cursor, job):
    cursor.execute("USE sql_hr")
    response = []
    column_names = []

    # Getting column names with SQL Query
    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = 'employees' "
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        column_names.append(x[0])

    # Receiving employers
    sql = "SELECT * FROM employees WHERE job_title = %s"
    job = (job, )
    cursor.execute(sql, job)
    myresult = cursor.fetchall()


    for x in myresult:
        tmp_dict = {}
        for idx in range(len(column_names)):
            tmp_dict[column_names[idx]] = x[idx]
        response.append(tmp_dict)
        print(x)
        #result = str(x)
    return response


