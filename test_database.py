from database import get_connection


connection = get_connection()

if connection is not None and connection.is_connected():
    print("MySQL database connected successfully")

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE()")

    database_name = cursor.fetchone()

    print("Connected database:", database_name[0])

    cursor.close()
    connection.close()

    print("Database connection closed")

else:
    print("Database connection failed")