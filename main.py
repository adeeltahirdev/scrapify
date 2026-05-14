from scrapers.radstore import scrape_radstore
from scrapers.surteez import scrape_surteez
from scrapers.konfor import scrape_konfor

from model import connect_db, create_tables, db_close

def main():
    connect_db()
    create_tables()

    scrape_radstore()
    scrape_konfor()
    scrape_surteez()

    db_close()
    
if __name__ == "__main__":
    main()