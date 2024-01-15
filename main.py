import random, os

username, difficulty, player_data, computer_data, table_header, debug_mode = "", 0, [
    ["Tetszőleges kombináció", None],
    ["Pár", None],
    ["Drill", None],
    ["Két Pár", None],
    ["Kis póker", None],
    ["Full", None],
    ["Kis sor", None],
    ["Nagy sor", None],
    ["Nagy póker", None]
], [
    ["Tetszőleges kombináció", None],
    ["Pár", None],
    ["Drill", None],
    ["Két Pár", None],
    ["Kis póker", None],
    ["Full", None],
    ["Kis sor", None],
    ["Nagy sor", None],
    ["Nagy póker", None]
], ["Érvényes kombinációk", "Pontérték"], False

def main_menu():
    global username
    os.system("cls")
    while True:
        print("> Menu:")
        print("1. Játék indítása")
        print("2. Előző játékmenet betöltése")
        print("3. Kilépés")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            start_configuration()
            main()
        elif choice == "2":
            load_prev_game()
        elif choice == "3":
            print("Kilépés---")
            break
        else:
            print("Ez nem egy lehetőség.")

def start_configuration():
    global username, difficulty
    os.system("cls")
    
    while True:
        print("> Add meg a felhasználó nevedet:")
        username = input("> ")
        if username:
            break
        else:
            print("Hibás bemenet. Kérlek, adj meg egy érvényes felhasználónevet.")

    os.system("cls")
    
    while True:
        print("> Add meg az ellenfeled nehézségét:")
        print("1. Könnyű")
        print("2. Nehéz")
        defined_difficulty = input("Enter your choice (1/2): ")

        if defined_difficulty.isdigit() and 1 <= int(defined_difficulty) <= 2:
            difficulty = 0 if int(defined_difficulty) == 1 else 1
            break
        else:
            print("Hibás választás. Kérlek, válassz 1-t vagy 2-t.")

    if not 1 <= int(defined_difficulty) <= 2:
        print("Hibás választás UwU")
        os.system("cls")
        main_menu()

def tabulate_data(data, headers):
    col_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
    table = "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+\n"
    header_str = "| " + " | ".join(
        f"{header}".ljust(col_width) for header, col_width in zip(headers, col_widths)
    ) + " |\n"
    table += header_str
    table += "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+\n"
    for row in data:
        row_str = "| " + " | ".join(
            f"{value}".ljust(col_width) if value is not None else "".ljust(col_width)
            for value, col_width in zip(row, col_widths)
        ) + " |\n"
        table += row_str

    table += "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+"

    return table

def generate_random_numbers():
    return [random.randint(1, 6) for _ in range(5)]

def check_conditions(numbers):
    unique_numbers = set(numbers)
    global unique_list, counts, generated_numbers
    generated_numbers = numbers
    unique_list = list(unique_numbers)
    counts = [numbers.count(num) for num in unique_numbers]

    conditions = []
    if counts in ([2, 3], [3, 2]) and player_data[5][1] is None:
        conditions.append("Full")
    if 4 in counts and player_data[4][1] is None:
        conditions.append("Kis póker")
    if 3 in counts and player_data[2][1] is None:
        conditions.append("Drill")
    if 2 in counts:
        if counts.count(2) == 2 and player_data[3][1] is None:
            conditions.append("Két Pár")
        elif player_data[1][1] is None:
            conditions.append("Pár")
    if set(numbers) == {1, 2, 3, 4, 5} and player_data[6][1] is None:
        conditions.append("Kis sor")
    if set(numbers) == {2, 3, 4, 5, 6} and player_data[7][1] is None:
        conditions.append("Nagy sor")
    if len(unique_numbers) == 1 and player_data[8][1] is None:
        conditions.append("Nagy póker")
    if not conditions and player_data[0][1] is None:
        conditions.append("Tetszőleges kombináció")

    return conditions

def get_unused_fields():
    array = [field[0] for field in player_data if field[1] is None]
    return array

def main():
    game_run = True
    game_runs = 0
    while game_run:
        os.system("cls")
        nullazo_id = None
        random_numbers = generate_random_numbers()
        print("Dobott számok:", *random_numbers)
        
        matching_conditions = check_conditions(random_numbers)
        unused_fields = get_unused_fields()
        if matching_conditions == []:
            print("Már minden olyan mező fel van használva ahova beírhatnád ezt a kombinációt.")
        else :
            print("Lehetőségek:", ", ".join(str(condition) for condition in matching_conditions))

        if len(matching_conditions) > 1:
            errorhandle = True
            while errorhandle:
                try:
                    print("Több lehetőség is van. Válassz egyet:")
                    for i, condition in enumerate(matching_conditions, 1):
                        print(f"{i}. {condition}")

                    user_input = input("Írd be az általad választott lehetőség számát: ")

                    if user_input.strip():
                        choice_index = int(user_input) - 1

                        if 0 <= choice_index < len(matching_conditions):
                            final_result = matching_conditions[choice_index]
                            print("Végső érték:", final_result)
                            errorhandle = False
                        else:
                            print("Hibás választás, kilépés")
                    else:
                        print("Hiba: Üres bemenet. Próbáld újra.")
                except ValueError:
                    print("Hiba: Nem érvényes egész számot adtál meg. Próbáld újra.")

        elif len(matching_conditions) == 1:
            final_result = matching_conditions[0]
            print("Végső érték:", final_result)
        elif len(matching_conditions) == 0:
            while True:
                try:
                    print("Jelölj meg egy üres kombinációt, amit a továbbiakban már nem tudsz elérni.")
                    for i, condition in enumerate(unused_fields, 1):
                        print(f"{i}. {condition}")
                    choice_index = int(input("Válassz egyet: ")) - 1
                    print(f"Kiválasztottad a: {unused_fields[choice_index]}")
                    final_result = "nullazo"
                    break
                except ValueError:
                    print("Hiba: Nem érvényes egész számot adtál meg. Próbáld újra.")
            for index, sublist in enumerate(player_data):
                if sublist[0] == unused_fields[choice_index]:
                    nullazo_id = index
                    break
        
        if final_result == "Tetszőleges kombináció":
            ertek = sum(generated_numbers)
            if can_insert_data(0, ertek, 1, debug_mode) == False:
                print("Error lol 1")

        if final_result == "Pár":
            global par_index
            par_index = next((i for i, count in enumerate(counts) if count == 2), None)
            ertek = 2 * unique_list[par_index]
            if can_insert_data(1, ertek, 1, debug_mode) == False:
                print("Error lol 2")

        if final_result == "Drill":
            global drill_index
            drill_index = next((i for i, count in enumerate(counts) if count == 3), None)
            ertek = 3 * unique_list[drill_index]
            if can_insert_data(2, ertek, 1, debug_mode) == False:
                print("Error lol 3")

        if final_result == "Két Pár":
            global par1_index, par2_index
            par1_index = next((i for i, count in enumerate(counts) if count == 2), None)
            par2_index = next((i for i, count in enumerate(counts[par1_index+1:]) if count == 2), None) + par1_index + 1
            ertek = 2 * unique_list[par1_index] + 2 * unique_list[par2_index]
            if can_insert_data(3, ertek, 1, debug_mode) == False:
                print("Error lol 4")
        
        if final_result == "Kis póker":
            global kispoker_index
            kispoker_index = next((i for i, count in enumerate(counts) if count == 4), None)
            ertek = 4 * unique_list[kispoker_index]
            if can_insert_data(4, ertek, 1, debug_mode) == False:
                print("Error lol 5")

        if final_result == "Full":
            ertek = sum(generated_numbers)
            if can_insert_data(5, ertek, 1, debug_mode) == False:
                print("Error lol 6")

        if final_result == "Kis sor":
            ertek = 15
            if can_insert_data(6, ertek, 1, debug_mode) == False:
                print("Error lol 7")

        if final_result == "Nagy sor":
            ertek = 20
            if can_insert_data(7, ertek, 1, debug_mode) == False:
                print("Error lol 8")

        if final_result == "Nagy póker":
            ertek = 50
            if can_insert_data(8, ertek, 1, debug_mode) == False:
                print("Error lol 9")
        if final_result == "nullazo":
            if can_insert_data(nullazo_id, 0, 1, debug_mode) == False:
                print("Error lol 10")

        print(tabulate_data(player_data, table_header))
        game_runs += 1
        input("Nyomj egy entert a folytatáshoz")
        if game_runs > 8:
            game_run = False

def can_insert_data(combination, value, is_player, debug):
    if is_player:
        data_list = player_data
    else:
        data_list = computer_data

    if data_list[combination][1] is None or debug:
        data_list[combination][1] = value
        return True
    else:
        return False

if __name__ == "__main__":
    main_menu()
