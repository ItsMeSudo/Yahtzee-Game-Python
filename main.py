import random, os

username, difficulty, player_data, table_header, debug_mode = "", 0, [
    ["Tetszőleges kombináció", None, None],
    ["Pár", None, None],
    ["Drill", None, None],
    ["Két Pár", None, None],
    ["Kis póker", None, None],
    ["Full", None, None],
    ["Kis sor", None, None],
    ["Nagy sor", None, None],
    ["Nagy póker", None, None]
], ["Érvényes kombinációk", "PlayerPont", "AI Pont"], False

def main_menu():
    global username
    clearscreen()
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


def clearscreen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def start_configuration():
    global username, difficulty
    clearscreen()
    
    while True:
        print("> Add meg a felhasználó nevedet:")
        username = input("> ")
        if username:
            break
        else:
            print("Hibás bemenet. Kérlek, adj meg egy érvényes felhasználónevet.")

    clearscreen()
    
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
        clearscreen()
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

def check_conditions(numbers, game_runs):
    id = playerfield(game_runs)
    unique_numbers = set(numbers)
    global unique_list, counts, generated_numbers
    generated_numbers = numbers
    unique_list = list(unique_numbers)
    counts = [numbers.count(num) for num in unique_numbers]

    conditions = []
    if counts in ([2, 3], [3, 2]) and player_data[5][id] is None:
        conditions.append("Full")
    if 4 in counts and player_data[4][id] is None:
        conditions.append("Kis póker")
    if 3 in counts and player_data[2][id] is None:
        conditions.append("Drill")
    if 2 in counts:
        if counts.count(2) == 2 and player_data[3][id] is None:
            conditions.append("Két Pár")
        elif player_data[1][id] is None:
            conditions.append("Pár")
    if set(numbers) == {1, 2, 3, 4, 5} and player_data[6][id] is None:
        conditions.append("Kis sor")
    if set(numbers) == {2, 3, 4, 5, 6} and player_data[7][id] is None:
        conditions.append("Nagy sor")
    if len(unique_numbers) == 1 and player_data[8][id] is None:
        conditions.append("Nagy póker")
    if not conditions and player_data[0][id] is None:
        conditions.append("Tetszőleges kombináció")

    return conditions

def get_unused_fields(playerfield):
    array = [field[0] for field in player_data if field[playerfield] is None]
    return array

def playerfield(game_runs):
    if game_runs%2 != 0:
        return 2
    else:
        return 1

def main():
    game_run = True
    game_runs = 1
    while game_run:
        isPlayer = None
        clearscreen()
        nullazo_id = None
        random_numbers = generate_random_numbers()
        print(f"Ez a(z) {game_runs}. kör.")
        print("Dobott számok:", *random_numbers)

        if game_runs%2 != 0:
            print("Ez a gép köre!")
            isPlayer = False
        else: 
            isPlayer = True

        
        matching_conditions = check_conditions(random_numbers, game_runs)
        unused_fields = get_unused_fields(playerfield(game_runs))
        if isPlayer:
            if matching_conditions == []:
                print("Már minden olyan mező fel van használva ahova beírhatnád ezt a kombinációt.")
            else :
                print("Lehetőségek:", ", ".join(str(condition) for condition in matching_conditions))

        if len(matching_conditions) > 1:
            if isPlayer:
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
                                if isPlayer:
                                    print("Végső érték:", final_result)
                                else:
                                    print("A gép választása:", final_result)
                                errorhandle = False
                            else:
                                print("Hibás választás, kilépés")
                        else:
                            print("Hiba: Üres bemenet. Próbáld újra.")
                    except ValueError:
                        print("Hiba: Nem érvényes egész számot adtál meg. Próbáld újra.")
            else:
                if difficulty == 0:
                    final_result = matching_conditions[0]
                else:
                    maxid = 0
                    for i in range(len(matching_conditions)):
                        maxid = i
                    final_result = matching_conditions[maxid]

        elif len(matching_conditions) == 1:
            final_result = matching_conditions[0]
            if isPlayer:
                print("Végső érték:", final_result)
            else:
                print("A gép választása:", final_result)
        elif len(matching_conditions) == 0:
            if isPlayer:
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
            else:
                final_result = "nullazo"
                choice_index = 0
                for index, sublist in enumerate(player_data):
                    if sublist[0] == unused_fields[choice_index]:
                        nullazo_id = index
                        break
        
        if final_result == "Tetszőleges kombináció":
            ertek = sum(generated_numbers)
            if can_insert_data(0, ertek, game_runs, debug_mode) == False:
                print("Error lol 1")

        if final_result == "Pár":
            global par_index
            par_index = next((i for i, count in enumerate(counts) if count == 2), None)
            ertek = 2 * unique_list[par_index]
            if can_insert_data(1, ertek, game_runs, debug_mode) == False:
                print("Error lol 2")

        if final_result == "Drill":
            global drill_index
            drill_index = next((i for i, count in enumerate(counts) if count == 3), None)
            ertek = 3 * unique_list[drill_index]
            if can_insert_data(2, ertek, game_runs, debug_mode) == False:
                print("Error lol 3")

        if final_result == "Két Pár":
            global par1_index, par2_index
            par1_index = next((i for i, count in enumerate(counts) if count == 2), None)
            par2_index = next((i for i, count in enumerate(counts[par1_index+1:]) if count == 2), None) + par1_index + 1
            ertek = 2 * unique_list[par1_index] + 2 * unique_list[par2_index]
            if can_insert_data(3, ertek, game_runs, debug_mode) == False:
                print("Error lol 4")
        
        if final_result == "Kis póker":
            global kispoker_index
            kispoker_index = next((i for i, count in enumerate(counts) if count == 4), None)
            ertek = 4 * unique_list[kispoker_index]
            if can_insert_data(4, ertek, game_runs, debug_mode) == False:
                print("Error lol 5")

        if final_result == "Full":
            ertek = sum(generated_numbers)
            if can_insert_data(5, ertek, game_runs, debug_mode) == False:
                print("Error lol 6")

        if final_result == "Kis sor":
            ertek = 15
            if can_insert_data(6, ertek, game_runs, debug_mode) == False:
                print("Error lol 7")

        if final_result == "Nagy sor":
            ertek = 20
            if can_insert_data(7, ertek, game_runs, debug_mode) == False:
                print("Error lol 8")

        if final_result == "Nagy póker":
            ertek = 50
            if can_insert_data(8, ertek, game_runs, debug_mode) == False:
                print("Error lol 9")
        if final_result == "nullazo":
            if can_insert_data(nullazo_id, 0, game_runs, debug_mode) == False:
                print("Error lol 10")

        print(tabulate_data(player_data, table_header))
        # playerscore = sum(player_data[1])
        # computerscore = sum(player_data[2])
        # print(playerscore, computerscore)

        playervalue_count = 0
        aivalue_count = 0

        for row in player_data:
            playervalue = row[1]
            aivalue = row[2]

            if playervalue is not None:
                playervalue_count += 1

            if aivalue is not None:
                aivalue_count += 1

                playervalue_sum = 0
                aivalue_sum = 0

        for row in player_data:
            definition = row[0]
            playervalue = row[1]
            aivalue = row[2]

            if playervalue is not None:
                playervalue_sum += playervalue

            if aivalue is not None:
                aivalue_sum += aivalue

        print("PlayerValue sum:", playervalue_sum)
        print("AIValue sum:", aivalue_sum)
        if (playervalue_count+aivalue_count)==18:
            if playervalue_sum > aivalue_sum:
                print(f"Győztes: {username}")
            elif aivalue_sum > playervalue_sum:
                print("A gép legyőzött téged :D")
            else:
                print("Döntetlen!")

        game_runs += 1
        game_run = any(None in sublist for sublist in player_data)
        input("Nyomj egy entert a folytatáshoz")
        # if game_runs > 8:
        #     game_run = False

def can_insert_data(combination, value, gamerunsnum, debug):
    id = playerfield(gamerunsnum)
    if player_data[combination][id] is None or debug:
        player_data[combination][id] = value
        return True
    else:
        return False

if __name__ == "__main__":
    main_menu()
