
import Library


# Define the database
grain_database = {
    "Brown rice": [1, "Brown rice", "Organic", 780, 16000, "0001"],
    "Jasmine": [2, "Jasmine", "Non Organic", 1000, 15000, "0002"],
    "Long Grain": [3, "Long Grain", "Organic", 790, 50000, "0003"],
    "Shirataki": [4, "Shirataki", "Organic", 4000, 80000, "0004"],
    "White rice": [5, "White rice", "Non Organic", 870, 12000, "0005"]
}


def main():
    MenuList='''
Welcome to EcoGrain Oasis !
Menu List:
1. Show
2. Add
3. Update Database
4. Delete
5. View Statistics
6. Filter by type
7. Exit
'''
    while True:
        print(MenuList)
        choice = input("Enter your choice: ")
        if choice == "1":
            Library.show_menu(grain_database)
        elif choice == "2":
            Library.add_grain(grain_database)
        elif choice == "3":  
            Library.update_grain(grain_database)
        elif choice == "4":
            Library.delete_grain(grain_database)
        elif choice == "5":
            Library.view_statistics(grain_database)
        elif choice == "6":
            Library.filter_by_type(grain_database)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


main()
