import psycopg2


# Making a connection to a database
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="adeel",
    password="1234",
    port=5432
)

cur = conn.cursor()
print('Connection Successful')