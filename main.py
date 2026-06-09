from tracker import HabbitJAL, HabbitController
from helper import Period, Log, to_completion_format
import sys
from os import path, system, name
import datetime as dt

date = dt.date

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
    """the main loop, just keeps requesting the user and calling the right function based on what they type"""

    intro_completed: bool = False
    main_menu: str = f'''
Hello {user_name},
Welcome back to habbit tracker
==============================
{menu}
'''
    
    while True:
        if not intro_completed:
            Log.blue(main_menu)

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
            Log.yellow(f"Please input a valid command, print 9 or help for available options ")

def show_options():
    """just prints the menu options"""
    Log.blue(menu)

def clear_ui():
    """clears the terminal screen, this will call the sytems cls, i have tested this on ubuntu, not so sure if it works on windows"""
    system('cls' if name=='nt' else 'clear')

def create_habbit():
    """asks the user for the habit name, description and period then creates it"""
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
    """shows the user a list of all habits and lets them pick one to see more detail"""
    menu:str = '''
Pick the one you want to view
=============================

'''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

    picked_habbit_index: int
    try:
        Log.blue(menu)
        picked_habbit_index = int(input("Select the one you want to view : "))
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
    """shows the habit list and deletes whichever one the user picks"""
    menu:str = '''
Pick the one you want to delete
===============================

'''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

    picked_habbit_index: int
    try:
        Log.blue(menu)
        picked_habbit_index = int(input("Pick a habbit to delete : "))
    except ValueError as e:
        Log.red(f"Please input number only")
        return

    if picked_habbit_index < 0 or picked_habbit_index > len(all_habits):
        Log.yellow(f"Please pick a number between 0 and {len(all_habits)}")
        return
    
    picked_habbit = all_habits[picked_habbit_index]

    # the reason this works is because the name of the habit is actually unique
    habbitController.delete_habbit(picked_habbit["name"])

def mark_off_habbit():
    """shows the habit list and marks whichever one the user picks as completed"""
    menu:str = '''
Pick the one you want to mark as completed
==========================================

'''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

    picked_habbit_index: int
    try:
        Log.blue(menu)
        picked_habbit_index = int(input("Pick a habbit: "))
    except ValueError as e:
        Log.red(f"Please input number only")
        return

    if picked_habbit_index < 0 or picked_habbit_index > len(all_habits):
        Log.yellow(f"Please pick a number between 0 and {len(all_habits)}")
        return
    
    picked_habbit = all_habits[picked_habbit_index]

    # the reason this works is because the name of the habit is actually unique
    habbitController.mark_completion(picked_habbit["name"])
    Log.green(f"Habbit : {habbit["name"]} marked as completed.")


def filter_by_periodicity(period: str, habbits: list) -> list:
    """filters the habit list by period (daily or weekly), i used a lambda here since it's just a one liner filter"""
    # the reason i am using a lambda here is because this function will not be reused, it's just a simple filtering func
    filter_logic = lambda habbit : True if habbit["period"] == period else False
    filtered = filter(filter_logic, habbits)
    return list(filtered)    

def filter_by_period():
    """asks the user for a period and shows only habits matching that period"""
    while True:
        user_input = input("Choose period (daily, weekly): ").strip()
        if user_input not in ["daily", "weekly"]:
            Log.red("Input incorrect, please enter daily or weekly")
            return
        
        all_habbits:list = habbitController.get_all_habits()
        filtered_habbit = filter_by_periodicity(user_input, all_habbits)
        message: str = f'''
Your {user_input} habbits
=========================

'''
        for i, habbit in enumerate(filtered_habbit):
            message = message + f"{i} - {habbit["name"]} ({habbit["period"]}) - {habbit["description"]}\n"

        Log.green(message)
        return
            

# this will return a unique week starting from jan 1, 2000 as 1 and will go above after this.
# the reason i am doing this is to get a unique week starting from some point, so that when i 
# do my weekly analysis i could use this.
def convert_date_to_unique_week(date : date) -> int:
    """converts a date to a unique week number starting from year 2000,
    this way i can compare weekly completions by just doing w2 - w1 == 1
    """
    starting_year = 2000
    week = date.isocalendar().week
    year = date.isocalendar().year

    year_diff = year - starting_year
    offset = year_diff * 54
    return week + offset
    
def map_completions_to_unique_weeks(unformated_completions: list[str]) -> list[int]:
    """takes a list of completion date strings and returns a sorted list of unique week numbers"""
    formated_completion_dates: list[date] = to_completion_format(unformated_completions)
    formated_completion_dates.sort()
    unique_weeks: list[int] = []
    for comp_date in formated_completion_dates:
        conv_unq_week = convert_date_to_unique_week(comp_date)
        if conv_unq_week not in unique_weeks:
            unique_weeks.append(conv_unq_week)

    unique_weeks.sort()         
    return unique_weeks

def longest_streak_from_all_habbits() -> map:
    """goes through all habits and calculates the streak for each one,
    for daily habits it checks consecutive days, for weekly it checks consecutive weeks
    """
    habbits = habbitController.get_all_habits()

    message = '''
Habbit Analysis
==============

'''
    for j,habbit in enumerate(habbits):
        period = habbit["period"]
        unformated_completions : list[str] = habbit["completions"]
        formated_completion_dates: list[date] = to_completion_format(unformated_completions)
        formated_completion_dates.sort()

        habbit_streak = 0
        if period == "daily":
            
            for i,d1 in enumerate(formated_completion_dates):
                next_date =  i + 1
                if next_date >= len(formated_completion_dates):
                    break
                d2 = formated_completion_dates[next_date]
                date_diff = d2 - d1
                date_diff_days = date_diff.days
                
                if date_diff_days <= 1:
                    habbit_streak += 1
                else:
                    habbit_streak = 0 # resteting the streak
                habbit["streak"] = habbit_streak

        elif period == "weekly":
            # map the completion dates to a year and weekly concetnated number (year0weekday)
            formated_weeks = map_completions_to_unique_weeks(habbit["completions"])
            for i,w1 in enumerate(formated_weeks):
                    w2i =  i + 1
                    if w2i >= len(formated_weeks):
                        break
                    w2 = formated_weeks[w2i]
                    week_diff = w2 - w1
                    if week_diff == 1:
                        habbit_streak += 1
            habbit["streak"] = habbit_streak
        message += f"{j}. {habbit["name"]} ({habbit["period"]}) longest streak is : {habbit_streak}\n"
   
    
    return {"message" : message, "habbits" : habbits}


def streak_for_a_specific_habbit():
    """lets the user pick a specific habit from the list and shows that habit's streak"""
    menu:str = '''
Pick the one you want to check the streak for
=============================================

'''
    all_habits:list = habbitController.get_all_habits()
    for i, habbit in enumerate(all_habits):
        menu = menu + f"{i} - {habbit['name']} ({habbit['period']}) - {habbit['description']}\n"

    picked_habbit_index: int
    try:
        Log.blue(menu)
        picked_habbit_index = int(input("Pick a habbit: "))
    except ValueError as e:
        Log.red(f"Please input number only")
        return

    if picked_habbit_index < 0 or picked_habbit_index > len(all_habits):
        Log.yellow(f"Please pick a number between 0 and {len(all_habits)}")
        return

    picked_habbit = all_habits[picked_habbit_index]
    period = picked_habbit["period"]
    unformated_completions : list[str] = picked_habbit["completions"]
    formated_completion_dates: list[date] = to_completion_format(unformated_completions)
    formated_completion_dates.sort()

    habbit_streak = 0
    if period == "daily":
        for i,d1 in enumerate(formated_completion_dates):
            next_date = i + 1
            if next_date >= len(formated_completion_dates):
                break
            d2 = formated_completion_dates[next_date]
            date_diff = d2 - d1
            if date_diff.days <= 1:
                habbit_streak += 1
            else:
                habbit_streak = 0

    elif period == "weekly":
        formated_weeks = map_completions_to_unique_weeks(picked_habbit["completions"])
        for i,w1 in enumerate(formated_weeks):
            w2i = i + 1
            if w2i >= len(formated_weeks):
                break
            w2 = formated_weeks[w2i]
            if w2 - w1 == 1:
                habbit_streak += 1

    Log.green(f"""
Streak for : {picked_habbit['name']} ({period})
============================================
Streak : {habbit_streak}
""")


def longest_streak_from_a_habbit():
    """finds which habit has the longest streak, separately for daily and weekly"""
    response = longest_streak_from_all_habbits()
    habbit_with_streaks = response["habbits"]
    longest_streak_daily: dict = {}
    longest_streak_weekly: dict = {}
   
    for habbit in habbit_with_streaks:
        period = habbit.get("period", "daily")
        streak = habbit.get("streak", 0)
        if period == "daily":
            if "streak" not in longest_streak_daily or longest_streak_daily["streak"] < streak:
                longest_streak_daily = habbit
            
        if period == "weekly":
            if "streak" not in longest_streak_weekly or longest_streak_weekly["streak"] < streak:
                longest_streak_weekly = habbit

     
    longest_counts =  {
        "daily" : longest_streak_daily,
        "weekly" : longest_streak_weekly
    }

    message = f'''
Longest streak
==============
Daily : {longest_counts["daily"]["name"]}, Streak : {longest_counts["daily"]["streak"]}
Weekly : {longest_counts["weekly"]["name"]}, Streak : {longest_counts["weekly"]["streak"]}
'''
    
    Log.green(message)
    return longest_counts

            
def view_analytics():
    """shows the analytics sub-menu and keeps looping until the user goes back"""
    analytics_message = '''
Analytics Menu
==============

1. Show all my habbits
2. Filter by period (daily, weekly)
3. What is my longest streak from all my habbits?
4. What is the streak for a specific habbit?
5. What is my longest streak of a habbit?
6. Return to main menu
'''
    while True:
        Log.blue(analytics_message)
        user_input = input(f"Choose a menu, {user_name}: ")

        if user_input == "1":
            view_habbit()
        elif user_input == "2":
            filter_by_period()
        elif user_input == "3":
            streak = longest_streak_from_all_habbits()
            message = streak["message"]
            Log.green(message)
        elif user_input == "4":
            streak_for_a_specific_habbit()
        elif user_input == "5":
            longest_streak_from_a_habbit()
        elif user_input == "6":
            Log.green("Returning to main menu")
            return
        else:
            Log.red("Wrong option")

def update_name():
    """asks the user for a new name and saves it, also updates the in-memory variable so it shows right away"""
    name: str = input("What do you want me to call you? : ")
    update_data = habbitController.update_user_name(name)

    # the resason i am declariing user name as globaal here is because, 
    # i want to modify it in memory, even though i have modified the json, 
    # i ddidnt want to read the json everytime for a simple username call
    global user_name 
    user_name = update_data["user"]["name"]
    Log.green(f"Great!! name updated to : {user_name}")

def exit_from_the_app():
    """prints a goodbye message and exits"""
    Log.green(f"Good bye {habbitController.get_user_name()}")
    sys.exit()

def about_the_developer_and_the_project():
    """shows a little ascii art with the project and student info"""
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