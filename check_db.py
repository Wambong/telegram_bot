from database import check_database, print_all_data

if __name__ == '__main__':
    print("Checking database status...")
    if check_database():
        print("\nPrinting all data:")
        print_all_data()
    else:
        print("Database check failed!")