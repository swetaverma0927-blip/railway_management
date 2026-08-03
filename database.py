import mysql.connector
from mysql.connector import Error

from config import HOST, USER, PASSWORD, DATABASE, PORT


def create_database():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DATABASE}"
        )

        print("Database created successfully")

    except Error as error:
        print("Database creation error:", error)

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def create_tables():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT
        )

        cursor = connection.cursor()

        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
        """

        passengers_table = """
        CREATE TABLE IF NOT EXISTS passengers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            passenger_name VARCHAR(100) NOT NULL,
            father_name VARCHAR(100),
            gender VARCHAR(20),
            age INT,
            mobile VARCHAR(15),
            address VARCHAR(255),
            train_number VARCHAR(30),
            train_name VARCHAR(100),
            source_station VARCHAR(100),
            destination_station VARCHAR(100),
            journey_date VARCHAR(30),
            coach VARCHAR(30),
            seat_number VARCHAR(30),
            ticket_price DECIMAL(10, 2)
        )
        """

        cursor.execute(users_table)
        cursor.execute(passengers_table)

        cursor.execute(
            """
            INSERT IGNORE INTO users (username, password)
            VALUES (%s, %s)
            """,
            ("admin", "admin123")
        )

        connection.commit()

        print("Tables created successfully")
        print("Default username: admin")
        print("Default password: admin123")

    except Error as error:
        print("Table creation error:", error)

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    create_database()
    create_tables()