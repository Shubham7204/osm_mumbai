import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="os_mumbai",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )