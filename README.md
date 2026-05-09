# Scrapify

A Python-based web scraper built with Selenium and Postgre to scrape product data from an e-commerce website and store it in a relational database.

## Features

- Scrapes product categories
- Scrapes product URLs
- Scrapes product names
- Scrapes sale and original prices
- Scrapes product variants
- Tracks stock status for each variant
- Scrapes product descriptions
- Stores product data in Postgre
- Updates existing products automatically
- Maintains price history over time

---

# Technologies Used

- Python
- Selenium
- Postgre
- psycopg2
- ChromeDriver

---

# Project Structure

```
project/
│
├── main.py
├── model.py
├── chromedriver
├── requirements.txt
└── README.md
```

---

# Database Schema

## Products Table

Stores the main product information.

| Column | Type |
|---|---|
| id | SERIAL PRIMARY KEY |
| name | VARCHAR(255) |
| url | TEXT UNIQUE |
| description | TEXT |
| category | VARCHAR(100) |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

## Prices Table

Stores product price history.

| Column | Type |
|---|---|
| id | SERIAL PRIMARY KEY |
| product_id | INTEGER (FK) |
| price | VARCHAR(50) |
| original_price | VARCHAR(50) |
| scraped_at | TIMESTAMP |

---

## Variants Table

Stores variant stock information.

| Column | Type |
|---|---|
| id | SERIAL PRIMARY KEY |
| product_id | INTEGER (FK) |
| variant_name | VARCHAR(255) |
| stock_status | VARCHAR(100) |

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
python3 -m venv .venv
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

```
pip install selenium psycopg2
```
OR

```
pip install -r requirements.txt
```

---

## 4. Install Postgre

Install Postgre and create a database user.

Example:

```
Database Name: your-db-name
Username: your-user-name
Password: your-db-passsword
```

---

# Postgre Access

Login to Postgres:

```
p -h localhost -U <your-user-name> -d <your-database-name>
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

Run the scraper using:

```
python3 main.py
```

The scraper will:

1. Open the RadStore website
2. Collect categories
3. Collect product URLs
4. Visit each product page
5. Scrape product data
6. Store data in Postgre
7. Update existing products automatically

---

# Data Flow

```
Website → Selenium Scraper → Python → Postgre Database
```

---

# Notes

- The scraper uses Selenium because the website content is dynamically rendered.
- Product prices are stored separately to maintain historical tracking.
- Variants are refreshed on every scrape.
- Product URLs are used as unique identifiers.

---

# Future Improvements

- Add image scraping
- Add REST API
- Add dashboard for analytics