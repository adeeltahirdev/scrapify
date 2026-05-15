# Scrapify

A Python-based web scraping system built with Selenium and Postgre to scrape product data from multiple e-commerce websites and store it in a relational database.

Currently supported stores:

- RadStore
- Konfor
- Surteez

---

# Features

* Multi-store scraping architecture
* Scrapes product categories
* Scrapes product URLs
* Scrapes product names
* Scrapes sale and original prices
* Scrapes product variants
* Tracks stock status for each variant
* Scrapes product descriptions
* Stores product data in Postgre
* Updates existing products automatically
* Maintains price history over time
* Automatic database table creation
* Centralized scraper runner
* Error handling with safe database closing

---

# Technologies Used

* Python
* Selenium
* Postgre
* psycopg2
* ChromeDriver

---

# Project Structure

```
project/
│
├── main.py
├── model.py
├── requirements.txt
├── README.md
│
├── scrapers/
│   ├── radstore.py
│   ├── konfor.py
│   └── surteez.py
│
└── chromedriver
```

---

# Database Schema

## Products Table

Stores the main product information.

| Column      | Type               |
| ------------ | ------------------ |
| id          | SERIAL PRIMARY KEY |
| name        | VARCHAR(255)       |
| url         |  UNIQUE        |
| description |                |
| category    | VARCHAR(100)       |
| source      | VARCHAR(100)       |
| created_at  | TIMESTAMP          |
| updated_at  | TIMESTAMP          |

---

## Prices Table

Stores product price history.

| Column         | Type               |
| -------------- | ------------------ |
| id             | SERIAL PRIMARY KEY |
| product_id     | INTEGER (FK)       |
| price          | VARCHAR(50)        |
| original_price | VARCHAR(50)        |
| scraped_at     | TIMESTAMP          |

---

## Variants Table

Stores variant stock information.

| Column       | Type               |
| ------------ | ------------------ |
| id           | SERIAL PRIMARY KEY |
| product_id   | INTEGER (FK)       |
| variant_name | VARCHAR(255)       |
| stock_status | VARCHAR(100)       |

---

# Installation

## 1. Clone the Repository

```
git clone <https://github.com/adeeltahirdev/scrapify>
cd <project-folder>
```

---

## 2. Create Virtual Environment

```
pytho3 -m venv .venv
```

OR
```
uv venv
```

Activate the virtual environment:

### Linux/macOS

```
source .venv/bin/activate
```

### Windows

```
.venv\Scripts\activate
```

---

## 3. Install Dependencies

Install all required packages:

```
pip install -r requirements.txt
```

Or manually:

```
pip install selenium psycopg2
```

---

## 4. Install Postgre

Install Postgre and create a database user.

Example:

```
Database Name: your-database-name
Username: your-user-name
Password: your-password
```

---

# Postgre Access

Login to Postgre:

```
p -h localhost -U your-user-name -d yoour-database-name
```

---

# Useful Postgre Commands

## Show Tables

```
\dt
```

## View Products

```
SELECT * FROM products;
```

## View Prices

```
SELECT * FROM prices;
```

## View Variants

```
SELECT * FROM variants;
```

## Exit Postgre

```
\q
```

---

# Running the Scraper

Run all scrapers using:

```
python main.py
```

The system will:

1. Connect to Postgres
2. Create tables automatically if they do not exist
3. Run all store scrapers
4. Scrape and store product data
5. Update existing products automatically
6. Save price history
7. Close the database connection safely

---

# Data Flow

```
E-Commerce Websites
        ↓
 Selenium Scrapers
        ↓
     Python
        ↓
 Postgre Database
```

---

# Notes

* Selenium is used because most target websites render content dynamically.
* Product URLs are used as unique identifiers.
* Price history is stored separately for tracking price changes over time.
* Variants are refreshed on every scrape.
* Database connections are automatically closed even if an error occurs.

---

# Future Improvements

* Add image scraping
* Add REST API
* Add dashboard for analytics

---

# Author

Adeel Tahir