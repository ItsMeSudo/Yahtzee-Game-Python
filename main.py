import random, os, time, json

username, difficulty, player_data, table_header, debug_mode, gamesavefile, gamedatas = None, 0, [
    ["Tetszőleges kombináció", None, None],
    ["Pár", None, None],
    ["Drill", None, None],
    ["Két Pár", None, None],
    ["Kis póker", None, None],
    ["Full", None, None],
    ["Kis sor", None, None],
    ["Nagy sor", None, None],
    ["Nagy póker", None, None]
], ["Érvényes kombinációk", "PlayerPont", "AI Pont"], False, "./gamesave.csv", [["IsRunning", False], ["Diff", None], ["Runs", None]]

def save_table_to_file(table_data):
    if table_data == None:
        for row in player_data:
            row[1] = None
            row[2] = None
        table_header[1] = "PlayerPont"
        gamedatas[0][1], gamedatas[1][1] = False, None


    with open(gamesavefile, mode='w', newline='') as file:
        for row in [table_header] + gamedatas + player_data :
            file.write(','.join(map(str, row)) + '\n')
        file.close()

def load_prev_game():
    global player_data, table_header, username, difficulty, gamedatas
    table_data = []
    if os.path.exists(gamesavefile):
        with open(gamesavefile, mode='r') as file:
            lines = file.readlines()
            header = lines[0].strip().split(',')
            gamestate = lines[1].strip().split(',')+lines[2].strip().split(',')+lines[3].strip().split(',')
            table_data = [line.strip().split(',') for line in lines[4:]]
            gamestateresult = []
            for i in range(0, len(gamestate), 2):
                key = gamestate[i]
                value = gamestate[i + 1]
                if value.lower() == 'true' or value.lower() == 'false':
                    value = value.lower() == 'true'
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                gamestateresult.append([key, value])
            tabledatares = []
            for inner_list in table_data:
                innerlistres = []
                for value in inner_list:
                    if value.lower() == 'none':
                        innerlistres.append(None)
                    elif value.isdigit():
                        innerlistres.append(int(value))
                    else:
                        innerlistres.append(value)

                tabledatares.append(innerlistres)

        print(header, gamestateresult, tabledatares)
        clearscreen()
        player_data = tabledatares
        table_header = header
        gamedatas = gamestateresult
        username = table_header[1]
        difficulty = gamedatas[1][1]
        print("Mentés sikeresen betöltve!")
        print("A játék 3másodperc múlva indul.")
        time.sleep(3)
        main()
         
    else:
        print("err")

def getprevgame():
    if os.path.exists(gamesavefile):
        with open(gamesavefile, mode='r') as file:
            lines = file.readlines()
            isrun = lines[1].strip().split(",")[1]
            if isrun == "True":
                return True
    else:
        return False
    
def gettopstat():
    clearscreen()
    try:
        with open('toplist.txt', 'r') as file:
            toplist = [line.strip().split(',') for line in file]
            print("Toplista:")
            for idx, entry in enumerate(toplist, 1):
                print(f"{idx}. {entry[0]} - {entry[1]} pont")
            print("\n\n\n\n")
    except FileNotFoundError:
        print("Nincs elmentett toplista.")

def save_to_top(name, score):
    try:
        with open('toplist.txt', 'r') as file:
            toplist = [line.strip().split(',') for line in file]
    except FileNotFoundError:
        toplist = []

    toplist.append([name, str(score)])
    toplist.sort(key=lambda x: int(x[1]), reverse=True)
    toplist = toplist[:10]

    with open('toplist.txt', 'w') as file:
        for entry in toplist:
            file.write(f"{entry[0]},{entry[1]}\n")


def main_menu():
    global username
    clearscreen()
    try:
        while True:
            print("> Menu:")
            if getprevgame():
                print("1. Játék indítása")
                print("2. Előző játékmenet betöltése")
                print("3. Toplista megnézése")
                print("4. Kilépés")
                choice = input("Enter your choice (1/2/3/4): ")
                if choice == "1":
                    start_configuration()
                    main()
                elif choice == "2":
                    load_prev_game()
                elif choice == "3":
                    gettopstat()
                elif choice == "4":
                    print("Kilépés---")
                    break
                else:
                    print("Ez nem egy lehetőség.")
            else:
                print("1. Játék indítása")
                print("2. Toplista megnézése")
                print("x. Előző játékmenet betöltése (Nem elérhető, nem található mentés.)")
                print("3. Kilépés")
                choice = input("Enter your choice (1/2/3): ")
                if choice == "1":
                    start_configuration()
                    main()
                elif choice == "2":
                    gettopstat()
                elif choice == "3":
                    print("Kilépés---")
                    break
                else:
                    print("Ez nem egy lehetőség.")
    except KeyboardInterrupt or EOFError:
        print("\nProgram megszakítva!")
        exit(1)



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
    table_header[1] = username

    clearscreen()
    for row in player_data:
        row[1] = None
        row[2] = None
    
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

    gamedatas[1][1], gamedatas[0][1] = difficulty, True


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
    if gamedatas[2][1]:
        game_runs = gamedatas[2][1]
    else:
        game_runs = 1
    try:
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
                    if difficulty == 1:
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
                    for index, sublist in enumerate(player_data):
                        if sublist[0] == unused_fields[len(unused_fields)-1]:
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
                playervalue = row[1]
                aivalue = row[2]

                if playervalue is not None:
                    playervalue_sum += playervalue

                if aivalue is not None:
                    aivalue_sum += aivalue

            if username:
                print(f"{username} sum:", playervalue_sum)
            else:
                print("PlayerValue sum:", playervalue_sum)
            print("AIValue sum:", aivalue_sum)
            if (playervalue_count+aivalue_count)==18:
                if playervalue_sum > aivalue_sum:
                    save_to_top(username, playervalue_sum)
                    print(f"Győztes: {username}")
                elif aivalue_sum > playervalue_sum:
                    save_to_top("Gép", aivalue_sum)
                    print("A gép legyőzött téged :D")
                else:
                    save_to_top(f"Gép+{username}", playervalue_sum)
                    print("Döntetlen!")

            game_runs += 1
            game_run = any(None in sublist for sublist in player_data)
            gamedatas[2][1] = game_runs
            save_table_to_file(player_data)
            input("\nNyomj egy entert a folytatáshoz\n vagy ctrl+c-t a menübe való visszalépéshez (a játékállás mentve lesz)\n")
            # if game_runs > 8:
            #     game_run = False
        save_table_to_file(None)
    except KeyboardInterrupt or EOFError:
        clearscreen()
        print("Játét mentve!\n") 

def can_insert_data(combination, value, gamerunsnum, debug):
    id = playerfield(gamerunsnum)
    if player_data[combination][id] is None or debug:
        player_data[combination][id] = value
        return True
    else:
        return False

if __name__ == "__main__":
    main_menu()
