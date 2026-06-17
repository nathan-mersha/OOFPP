# Habit Tracker App

Nathan Mersha Degineh, 102303079
Object Oriented and Functional Programming with Python (DLBDSOOFPP01)

GitHub Repository: https://github.com/nathan-mersha/OOFPP

This is a simple habit tracking app that runs on the command line. No fancy UI, no database, just a menu and a JSON file to save everything.
You can create daily and weekly habits, check them off, view your streaks, and delete habits you don't need anymore. The app also comes with 5 habits already loaded with 4 weeks of sample data so you can test the analytics right away.

# How to install

Make sure you have Python 3.10 or later, then go into the Phase 2 folder and run:

    pip install -r requirements.txt

# How to run

    python main.py

You will get a menu, just type the number and press enter. You can type exit at any prompt to quit.

The menu options are:

1. Create a habit
2. View a habit
3. Delete a habit
4. Mark a habit as done
5. Analytics menu
6. Update your name
7. Exit

# How it is structured

There are 3 files that do the main work. main.py has the CLI menu and all the user interaction. tracker.py has the logic and handles reading and writing to the JSON file. helper.py has some shared utilities like the Period enum and date helpers and some logging funcs.

All habit data is saved to habits.json. If that file gets corrupted for some reason it will automatically restore from predefined_habbits.json. ( this might lead to user loosing some data, in the worse case senario, it mainly happened when i devleop it, that sometimes i will miss right something without following the proper json format.)

# How to run the tests

    pytest tests/test.py -v

The tests use a separate JSON file so they never touch your actual habits, and by default will cleanup their test data once done, so you wont see anyting left.

# How streaks work

For daily habits it just checks if the completion dates are consecutive days. For weekly habits it converts each date to a unique week number and checks if the weeks are consecutive.
