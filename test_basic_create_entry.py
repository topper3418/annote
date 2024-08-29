from src.db.controller import create_entry

if __name__ == "__main__":
    print('sanity check')
    entry = create_entry("Do stuff today")
    print(entry)

