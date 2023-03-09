import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def write_dicst_db(db_path, csv_path, verbose = False):
    
    
    try:
 
        # Import csv and extract data
        with open(csv_path, 'r') as fin:
            dr = csv.DictReader(fin)
            country_info = [(i['country name'], i['ruling party'], i['url'], i['position']) for i in dr]
            #print(country_info)
    
        # Connect to SQLite
        #sqliteConnection = sqlite3.connect(f"{os.path.dirname(__file__)}/../data/databases/wiki.db")
        sqliteConnection = sqlite3.connect(database=db_path)
        cursor = sqliteConnection.cursor()
    
        # Create country table 
        cursor.execute('drop table country')
        cursor.execute('create table country(country TEXT, party TEXT, url TEXT, position TEXT);') 
    
        # Insert data into table
        cursor.executemany(
            "insert into country (country, party, url, position) VALUES (?, ?, ?, ?);", country_info)
    
        # Show student table
        if verbose:
            cursor.execute('select * from country;')
    
        # View result
        result = cursor.fetchall()
        print(result)
    
        # Commit work and close connection
        sqliteConnection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')

def insert_country(db_path, country):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    try:
        # Connect to SQLite
        conn = sqlite3.connect(database=db_path)
        
        
        sql = ''' INSERT INTO country(country, party, url, position)
                VALUES(?,?,?,?) '''
        
        cur = conn.cursor()
        cur.execute(sql, country)
        conn.commit()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if conn:
            conn.close()
            print('SQLite Connection closed')
    
    return cur.lastrowid
