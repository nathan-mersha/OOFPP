from tracker import HabbitJAL, HabbitController, Period, Log
import sys
from os import path, system, name


# converted to dir name instead of the ./habbits.json because depending on where you run the script you may get file not found, you usualy have to run it in the project file itself, but this way you can run it from anywhere
habbits_json_path = path.join(path.dirname(__file__), "habits.json")
predefined_habbits_json_path = path.join(path.dirname(__file__),"predefined_habbits.json")


habbitJAL = HabbitJAL(habbits_json_path=habbits_json_path, predefined_habbits_json_path=predefined_habbits_json_path)
habbitController = HabbitController(habbitJAL=habbitJAL)


# habbitController.create_habbit("test", "description", Period.weekly)
# habbitController.delete_habbit("test")
# habbitController.create_habbit("test2", "description", Period.daily)
# habbitController.mark_completion("test2")
# habbitController.delete_habbit("test")

user_name:str = habbitController.get_user_name()
menu: str = '''
    1 : Create a habbit
    2 : View your habbits
    3 : Delete a habbit
    4 : Mark off your habbit
    5 : View analytics
    6 : Update your name
    7 : Exit, you can type exit at anytime to exit the program
    8 : About developer & the project
    9 : Help
'''
def main():
    intro_completed: bool = False
    main_menu: str = f'''
    Hello {user_name},
    Welcome back to habbit tracker
    ==============================
    {menu}
    '''
    
    while True:

        if not intro_completed:
            Log.green(main_menu)

        
        user_input = input(f"Pick a menu {user_name} (press 9 for options): ").strip()
        intro_completed = True

        
        if user_input == "1":
            create_habbit()
        elif user_input == "2":
            view_habbit()
        elif user_input == "3":
            delete_habbit()
        elif user_input == "4":
            mark_off_habbit()
        elif user_input == "5":
            view_analytics()
        elif user_input == "6":
            update_name()
        elif user_input == "7" or user_input == "exit":
            exit_from_the_app()
        elif user_input == "8" or user_input == "about":
            about_the_developer_and_the_project()
        elif user_input == "9" or user_input == "help":
            show_options()
        elif user_input == "clear" or user_input == "cls":
            clear_ui()
        else:
            Log.red(f"Please input a valid command, print 9 or help for available options ")

def show_options():
    Log.green(menu)

def clear_ui():
    system('cls' if name=='nt' else 'clear')

def create_habbit():
    name:str = input("Habbit name : ")
    description:str = input("Habbit description : ")
    period = input(f"Period ({Period.daily.value}, {Period.weekly.value}) : ")
    parsed_period: Period
    if period == Period.daily.value:
        parsed_period = Period.daily
    elif period == Period.weekly.value:
        parsed_period = Period.weekly
    else:
        Log.red(f"Allowed values for input values are daily or weekly, aborting creating habbit...")
        return
    
    habbitController.create_habbit(name, description, parsed_period)
    

def view_habbit():
    menu:str = '''
Pick the one you want to view
=============================

'''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

    picked_habbit_index: int
    try:
        picked_habbit_index = int(input(menu))
    except ValueError as e:
        Log.yellow(f"Please input number only")
        return

    if picked_habbit_index < 0 or picked_habbit_index > len(all_habits):
        Log.yellow(f"Please pick a number between 0 and {len(all_habits)}")
        return
    
    picked_habbit = all_habits[picked_habbit_index]

    # note that i have my habbit, show all the completions
    parsed_message_for_the_user = f'''
    Name : {picked_habbit["name"]} , {picked_habbit["period"]}
    Description : {picked_habbit["description"]}
    Created at : {picked_habbit["created_at"]}
    Completions : You did {picked_habbit["name"]} {len(picked_habbit["completions"])} times, '''

    
    if len(picked_habbit["completions"]) > 0 : 
        parsed_message_for_the_user += "Congra!\n"
    else: 
        parsed_message_for_the_user += "Dont be lazy!\n"
        
    Log.green(parsed_message_for_the_user)
    

def delete_habbit():
    menu:str = '''
    Pick the one you want to delete

    '''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

    picked_habbit_index: int
    try:
        picked_habbit_index = int(input(menu))
    except ValueError as e:
        Log.yellow(f"Please input number only")
        return

    if picked_habbit_index < 0 or picked_habbit_index > len(all_habits):
        Log.yellow(f"Please pick a number between 0 and {len(all_habits)}")
        return
    
    picked_habbit = all_habits[picked_habbit_index]

    # the reason this works is because the name of the habit is actually unique
    habbitController.delete_habbit(picked_habbit["name"])

def mark_off_habbit():
    menu:str = '''
    Pick the one you want to mark as completed

    '''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

    picked_habbit_index: int
    try:
        picked_habbit_index = int(input(menu))
    except ValueError as e:
        Log.yellow(f"Please input number only")
        return

    if picked_habbit_index < 0 or picked_habbit_index > len(all_habits):
        Log.yellow(f"Please pick a number between 0 and {len(all_habits)}")
        return
    
    picked_habbit = all_habits[picked_habbit_index]

    # the reason this works is because the name of the habit is actually unique
    habbitController.mark_completion(picked_habbit["name"])


def filter_by_periodicity(period: str, habbits: list) -> list:
    # the reason i am using a lambda here is because this function will not be reused, it's just a simple filtering func
    filter_logic = lambda habbit : True if habbit["period"] == period else False
    filtered = filter(filter_logic, habbits)
    return list(filtered)    

def filter_by_period():
    while True:
        user_input = input("Choose period (daily, weekly)").strip()
        if user_input not in ["daily", "weekly"]:
            Log.red("Input incorrect, please enter daily or weekly")
            return
        
        all_habbits:list = habbitController.get_all_habits()
        filtered_habbit = filter_by_periodicity(user_input, all_habbits)
        message: str = f'''
        Your {user_input} habbits
'''
        for i, habbit in enumerate(filtered_habbit):
            message = message + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

        Log.green(message)
        return
            

def longest_streak_from_all_habbits():
    pass

def longest_streak_from_a_habbit():
    pass
            
def view_analytics():
    analytics_message = '''
        1. Show all my habbits
        2. Filter by period (daily, weekly)
        3. What is my longest streak from all my habbits?
        4. What is my longest streak of a habbit?
        5. Return to main menu
'''
    while True:
        Log.green(analytics_message)
        user_input = input(f"Choose a menu, {user_name}: ")

        if user_input == "1":
            view_habbit()
        elif user_input == "2":
            filter_by_period()
        elif user_input == "3":
            longest_streak_from_all_habbits()
        elif user_input == "4":
            longest_streak_from_a_habbit()
        elif user_input == "5":
            return
        else:
            Log.red("Wrong option")

def update_name():
    name: str = input("What do you want me to call you? : ")
    update_data = habbitController.update_user_name(name)

    # the resason i am declariing user name as globaal here is because, 
    # i want to modify it in memory, even though i have modified the json, 
    # i ddidnt want to read the json everytime for a simple username call
    global user_name 
    user_name = update_data["user"]["name"]
    Log.green(f"Great!! name updated to : {user_name}")

def exit_from_the_app():
    Log.green("Good bye {habbitController.get_user_name()}")
    sys.exit()

def about_the_developer_and_the_project():
    Log.green(f'''
         I      UUU     UUU
                UUU     UUU
        III     UUU     UUU
        III     UUU     UUU
        III     UUU     UUU
        III     UUUU   UUUU
        III      UUUUUUUUU
        ====================================================
        Project : Object Oriented and Functional Programming
        Student id : 102303079
        Phase 2 assignment
''')
    
if __name__ == "__main__":
    main()