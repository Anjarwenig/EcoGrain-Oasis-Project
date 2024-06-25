from tabulate import tabulate

def string_validation(title):
    while True:
        value = input(title)
        if value.replace(" ", "").isalpha():
            return value.capitalize()
        else:
            print("Please only enter text.")

def integer_validation(title, minval=0, maxval=1000000):
    while True:
        user_input = input(title)
        if user_input.strip() == "":  
            return None
        try:
            num = int(user_input)
            if minval <= num <= maxval:
                return num
            else:
                print(f"Number out of range ({minval}-{maxval}). Please try again or press enter to keep current.")
        except ValueError:
            print("That's not a valid number. Please try again or press enter to keep current.")


def show_menu(database):
    while True:
        print('''Menu:
        1. Show Entire Database
        2. Show Details by Code
        3. Back to Main Menu''')
        sub_choice = input("Enter your choice: ")

        if sub_choice == "1":
            # Displaying the entire database as a table
            print(tabulate(list(database.values()), headers=["ID", "Name", "Type", "Quantity", "Price", "Code"], tablefmt="grid"))
        elif sub_choice == "2":
            code = input("Enter the code of the grain to view details: ")
            found = False
            for grain in database.values():
                if grain[-1] == code:
                    print(f"Details for code {code}:")
                    print(tabulate([grain], headers=["ID", "Name", "Type", "Quantity", "Price", "Code"], tablefmt="grid"))
                    found = True
                    break
            if not found:
                print(f"No grain found with the code: {code}")
                        
        elif sub_choice == "3":
            break  
        else:
            print("Invalid choice, please try again.")



def generate_code(database):
    existing_codes = [int(entry[5]) for entry in database.values()]
    new_code = max(existing_codes) + 1 if existing_codes else 1
    return f"{new_code:04d}"

def add_grain(database):
    while True:
        print('''
                1. Add new grain
                2. Back to main menu''')
        
        choice = input('Enter your choice: ')
        if choice == '1':
            
            db_data = [[entry[5], entry[1], entry[2], entry[3], entry[4]] for entry in database.values()]
            print(tabulate(db_data, headers=["Code", "Name", "Type", "Stock", "Price"], tablefmt="grid"))
            
            code_str = generate_code(database)
            print(f"The new code is {code_str}")
            
            name = input("Enter grain name: ").title()
            existing_entries = [entry for entry in database.values() if entry[1].lower() == name.lower()]
            existing_types = {entry[2] for entry in existing_entries}
            
            if existing_entries:
                print(f"{name} exists in the database.")
                types = ["Organic", "Non Organic"]
                availability_table = [(i + 1, t, "In database" if t in existing_types else "Not in database") for i, t in enumerate(types)]
                print(tabulate(availability_table, headers=["No", "Type", "Availability"], tablefmt="grid"))
                
                missing_types = [t for t in types if t not in existing_types]
                if not missing_types:
                    print(f"All types of {name} are already in the database.")
                    continue

                for _type in missing_types:
                    while True:
                        confirmation = input(f"{name} as {_type} does not exist. Do you want to add {name} as {_type}? (yes/no): ").lower()
                        if confirmation in ["yes", "y"]:
                            while True:
                                try:
                                    quantity = int(input("Enter quantity: "))
                                    if quantity <= 0:
                                        raise ValueError
                                    break
                                except ValueError:
                                    print("Invalid input, try again.")

                            while True:
                                try:
                                    price = int(input("Enter price: "))
                                    if price <= 0:
                                        raise ValueError
                                    break
                                except ValueError:
                                    print("Invalid input, try again.")

                            index = max([entry[0] for entry in database.values()], default=0) + 1
                            new_entry = [index, name, _type, quantity, price, code_str]
                            print(tabulate([new_entry], headers=["Index", "Name", "Type", "Quantity", "Price", "Code"], tablefmt="grid"))

                            while True:
                                print(f"Do you want to add {name} as {_type}?")
                                print("1. Yes, add to database")
                                print("2. No, add different grain")
                                print("3. Back to main menu")
                                confirmation = input("Enter your choice: ").strip()
                                if confirmation == '1':
                                    database[f"{name} ({_type})"] = new_entry
                                    print(f"{name} as {_type} added successfully!")
                                    break
                                elif confirmation == '2':
                                    break
                                elif confirmation == '3':
                                    return
                                else:
                                    print("Invalid choice, please try again.")
                            break
                        elif confirmation in ["no", "n"]:
                            break
                        else:
                            print("Please only answer 'yes' or 'no'.")
            else:
                while True:
                    _type = input("Enter type (Organic/Non Organic): ").capitalize()
                    if _type in ["Organic", "Non Organic"]:
                        break
                    print("Incorrect input. Please enter 'Organic' or 'Non Organic'.")

                while True:
                    try:
                        quantity = int(input("Enter quantity: "))
                        if quantity <= 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid input, try again.")

                while True:
                    try:
                        price = int(input("Enter price: "))
                        if price <= 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid input, try again.")

                index = max([entry[0] for entry in database.values()], default=0) + 1
                new_entry = [index, name, _type, quantity, price, code_str]
                print(tabulate([new_entry], headers=["Index", "Name", "Type", "Quantity", "Price", "Code"], tablefmt="grid"))

                while True:
                    print(f"Do you want to add {name} as {_type}?")
                    print("1. Yes, add to database")
                    print("2. No, add different grain")
                    print("3. Back to main menu")
                    confirmation = input("Enter your choice: ").strip()
                    if confirmation == '1':
                        database[f"{name} ({_type})"] = new_entry
                        print(f"{name} as {_type} added successfully!")
                        break
                    elif confirmation == '2':
                        break
                    elif confirmation == '3':
                        return
                    else:
                        print("Invalid choice, please try again.")
        elif choice == '2':
            break
        else:
            print("Invalid choice, please try again.")


def print_colored(text, color):
    colors = {
        "blue": "\033[94m",
        "green": "\033[92m",
        "end": "\033[0m"
    }
    return f"{colors[color]}{text}{colors['end']}"

def update_grain(database):
    while True:
        print('''
                1. Update Grain
                2. Back to main menu''')
        
        choice = input('Enter your choice: ')
        if choice == '1':
           
            db_data = [[entry[5], entry[1], entry[2], entry[3], entry[4]] for entry in database.values()]
            print(tabulate(db_data, headers=["Code", "Name", "Type", "Stock", "Price"], tablefmt="grid"))
            
            code_str = input("Enter the code of the grain to update: ").zfill(4)
            if not any(entry[5] == code_str for entry in database.values()):
                print("Invalid input. The code does not exist.")
                continue
            
            grain_to_update = None
            for key, value in database.items():
                if value[5] == code_str:
                    grain_to_update = key
                    break

            current_details = [[database[grain_to_update][5], database[grain_to_update][1], database[grain_to_update][2], database[grain_to_update][3], database[grain_to_update][4]]]
            print(print_colored("Current details:", 'blue'))
            print(tabulate(current_details, headers=["Code", "Name", "Type", "Quantity", "Price"], tablefmt="grid"))

            new_quantity = integer_validation(f"Enter new quantity for {grain_to_update} (current {database[grain_to_update][3]}): ", database[grain_to_update][3])
            new_price = integer_validation(f"Enter new price for {grain_to_update} (current {database[grain_to_update][4]}): ", database[grain_to_update][4])

            updated_details = database[grain_to_update].copy()
            updated_details[3] = new_quantity
            updated_details[4] = new_price
            updated_display_details = [[updated_details[5], updated_details[1], updated_details[2], updated_details[3], updated_details[4]]]

            print(print_colored("Current details:", 'blue'))
            print(tabulate(current_details, headers=["Code", "Name", "Type", "Quantity", "Price"], tablefmt="grid"))
            
            print(print_colored("Updated details:", 'green'))
            print(tabulate(updated_display_details, headers=["Code", "Name", "Type", "Quantity", "Price"], tablefmt="grid"))

            while True:
                print("Are you sure you want to update the grain?")
                print("1. Yes, update database")
                print("2. No, update another grain")
                print("3. Back to main menu")
                confirmation = input("Enter your choice: ").strip()
                if confirmation == '1':
                    database[grain_to_update] = updated_details
                    print(f"{grain_to_update} updated successfully!")
                    
                    while True:
                        print('''
                                1. Update Grain
                                2. Back to main menu''')
                        post_update_choice = input("Enter your choice: ").strip()
                        if post_update_choice == '1':
                            break
                        elif post_update_choice == '2':
                            return
                        else:
                            print("Invalid choice, please try again.")
                elif confirmation == '2':
                    break
                elif confirmation == '3':
                    return
                else:
                    print("Invalid choice, please try again.")
        elif choice == '2':
            break
        else:
            print("Invalid choice, please try again.")





def filter_by_type(database):
    while True:
        print(f'''
                1. Filter by type
                2. Back to main menu''')
        
        choice = input('Enter your choice: ')
        
        if choice == '1':


            unique_types = list(set(entry[2] for entry in database.values())) 
            if not unique_types:
                print("No grain types found in the database.")
                return

            print("Available Grain Types:")
            for i, type in enumerate(unique_types, start=1):
                print(f"{i}. {type}")

            while True:
                type_choice = input("Select the type number to filter by: ")
                if type_choice.isdigit() and 1 <= int(type_choice) <= len(unique_types):
                    selected_type = unique_types[int(type_choice) - 1]
                    break
                else:
                    print("Invalid input, please enter only the number for available choices.")

            filtered_data = [entry for entry in database.values() if entry[2] == selected_type]

            if filtered_data:
                print(f"Displaying all grains of type: {selected_type}")
                print(tabulate(filtered_data, headers=["ID", "Name", "Type", "Quantity", "Price", "Code"], tablefmt="grid"))
            else:
                print("No grains found of the specified type.")

        elif choice == '2':
            break
        else:
            print("Invalid choice, please try again.")




def delete_grain(database):
    while True:
        print(f'''
                1. Delete menu
                2. Back to main menu''')

        choice = input('Enter your choice: ')
        if choice == '1':
            while True:
                simplified_data = [[value[5], value[1], value[2]] for value in database.values()]
                print(tabulate(simplified_data, headers=["ID", "Name", "Type"], tablefmt="grid"))

                code_todelete = integer_validation("Enter code of the grain to delete: ", (database))

                grain_to_delete = None
                for key, value in database.items():
                    if value[0] == code_todelete:
                        grain_to_delete = key
                        break

                if not grain_to_delete:
                    print("No grain found with that ID.")
                    continue

                print("Details of the grain to be deleted:")
                print(tabulate([database[grain_to_delete]], headers=["ID", "Name", "Type", "Other details..."], tablefmt="grid"))
                
                confirmation_choice = input('Do you want to delete the item?\n1. Yes, delete\n2. No, delete another item\n3. Back to main menu\nEnter your choice: ')

                if confirmation_choice == '1':
                    del database[grain_to_delete]
                    print("Grain deleted successfully.")
                    break
                elif confirmation_choice == '2':
                    continue
                elif confirmation_choice == '3':
                    break
                else:
                    print("Invalid choice, please try again.")
        elif choice == '2':
            break
        else:
            print("Input invalid! Please input choice 1 or 2.")

     

def view_statistics(database):
    if not database:
        print("The database is currently empty.")
        return

    stats_data = []
    total_quantity = 0
    total_value = 0
    for entry in database.values():
        quantity = entry[3]
        price = entry[4]
        total = quantity * price
        total_quantity += quantity
        total_value += total
        stats_data.append([entry[1], entry[2], quantity, price, total])

    print("Statistics:")
    print(tabulate(stats_data, headers=["Name", "Type", "Quantity", "Price", "Total Value"], tablefmt="grid"))
    print(f"Total Quantity of All Grains: {total_quantity}")
    print(f"Overall Total Value of All Grains: {total_value}")


