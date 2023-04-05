from taro.data.database import create_write_dict_db
import psycopg2
import os

def test_clean_db():
    connection = None
    try:
    
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        try:
            cursor.execute(f'DROP TABLE dummy;')
        except:
            pass
        try:
            cursor.execute(f'DROP TABLE dummy_BACKUP;')
        except:
            pass
        
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')

def test_dummy_table():
    
    # create dummy data
    data = [{'Field1': 'bla', 'Field2': 2, 'Field3': 3.141}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]
    
    # Write dummy data to db
    create_write_dict_db('dummy', data, verbose=True)
    
    
    connection = None
    try:
    
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        cursor.execute(f'select * from dummy;')
        result = cursor.fetchall()
        
        assert result == [('bla', 2, 3.141), ('blafdf', 42, 3.1431), ('blfsa', 4, 3.431)]
        
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
    
def test_dummy_backup():
    # create dummy data
    new_data = [{'Field1': 'blub', 'Field2': 3, 'Field3': 3.1421}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]
    
    # Write dummy data to db
    create_write_dict_db('dummy', new_data, verbose=True)
    
    connection = None
    try:
    
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        cursor.execute(f'select * from dummy_BACKUP;')
        result = cursor.fetchall()
        
        assert result == [('bla', 2, 3.141), ('blafdf', 42, 3.1431), ('blfsa', 4, 3.431)]
        
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
            
                
def test_dummy_backup_restore():
    
    # Create bad data
    bad_data = [{'Field1': 'blub', 'Field2': 3, 'Field3': 'BAD_DATA'}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]

    # Write bad dummy data to db
    create_write_dict_db('dummy', bad_data, verbose=True)
    
    try:

        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        cursor.execute(f'select * from dummy;')
        result = cursor.fetchall()
        
        assert result == [('bla', 2, 3.141), ('blafdf', 42, 3.1431), ('blfsa', 4, 3.431)]
        
    finally:
        if connection:
            connection.close()
            print('SQLite Connection closed')
            
    