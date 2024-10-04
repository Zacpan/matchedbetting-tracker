import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        # Replace with your MySQL database credentials
        connection = mysql.connector.connect(
            host='localhost',          
            user='root',      
            password='1234',  
            database='MatchedBetting'  
        )
        if connection.is_connected():
            print("Connection to MySQL database was successful.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def main():
    # Create the connection
    connection = create_connection()
    
    # Perform any database operations here
    # For now, just close the connection
    if connection:
        connection.close()
        print("MySQL connection is closed.")

if __name__ == "__main__":
    main()