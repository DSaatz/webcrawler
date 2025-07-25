from crawler import crawl
from storage import init_db

PAGE_LIMIT = 1000
TOKEN_LIMIT = 500

seed_url = None

def main():

    seed_url = input("Enter your seed URL: ")

    if not seed_url:
        print("Seed URL cannot be empty.")
        return
    
    init_db()

    crawl(seed_url, page_limit=PAGE_LIMIT, token_limit=TOKEN_LIMIT)

if __name__ == "__main__":
    main()