import psycopg2


# Making a connection to a database
def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="adeel",
        password="1234",
        port=5432
    )
    return conn

conn = connect_db()
cur = conn.cursor()
print('Connection Successful')

def create_tables():
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
    cur.execute('''
                
                CREATE TABLE IF NOT EXISTS prices (
                    id SERIAL PRIMARY KEY,
                    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                    price VARCHAR(50),
                    original_price VARCHAR(50),
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                
                ''')
    cur.execute('''
                
                CREATE TABLE IF NOT EXISTS variants (
                    id SERIAL PRIMARY KEY,
                    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
                    variant_name VARCHAR(255),
                    stock_status VARCHAR(100)
                )
                
                ''')

    conn.commit()
    print('Tables created successfully')
    
create_tables()


def get_product_by_url(url):
    cur.execute('''
                
                SELECT id FROM products WHERE url = %s
                
                ''', (url,))
    return cur.fetchone()

def insert_product(name, url, description, category):
    cur.execute('''
                
                INSERT INTO products (name, url, description, category)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                
                ''', (name, url, description, category))
    product_id = cur.fetchone()[0]
    
    conn.commit()
    return product_id

def update_product(product_id, name, description, category):
    cur.execute('''
                
                UPDATE products
                SET name = %s, description = %s, category = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                
                ''', (name, description, category, product_id))
    conn.commit()
    return product_id

def insert_price(product_id, price, original_price):
    cur.execute('''
                
                INSERT INTO prices (product_id, price, original_price)
                VALUES (%s, %s, %s)
                
                ''', (product_id, price,original_price))
    conn.commit()
    return product_id

def insert_variant(product_id, variant_name, stock_status):
    cur.execute('''
                
                INSERT INTO variants (product_id, variant_name, stock_status)
                VALUES (%s, %s, %s)
                
                ''', (product_id, variant_name, stock_status))
    conn.commit()
    return product_id

def delete_variants(product_id):
    cur.execute('''
                
                DELETE FROM variants WHERE product_id = %s
                
                ''', (product_id,))
    conn.commit()
    return product_id

def db_close():
    cur.close()
    conn.close()