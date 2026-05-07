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

cur.execute('''
            
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                url TEXT UNIQUE NOT NULL,
                description TEXT,
                category VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            
            ''')

conn.commit()
print('Table created successfully')

cur.execute('''
            
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                price VARCHAR(50),
                original_price VARCHAR(50),
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            
            ''')

conn.commit()
print('Table created successfully')

cur.execute('''
            
            CREATE TABLE IF NOT EXISTS variants (
                id SERIAL PRIMARY KEY,
                product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                variant VARCHAR(255),
                stock_status VARCHAR(100)
            )
            
            ''')

conn.commit()
print('Table created successfully')