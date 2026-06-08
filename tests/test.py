import pytest
from tracker import HabbitJAL, HabbitController
from helper import Period
from os import path

def test_addition():
    assert 1 + 1 == 2

test_addition()

# converted to dir name instead of the ./habbits.json because depending on where you run the script you may get file not found, you usualy have to run it in the project file itself, but this way you can run it from anywhere
habbits_json_path = path.join(path.dirname(__file__), "habits_test.json")
predefined_habbits_json_path = path.join(path.dirname(__file__),"predefined_habbits_test.json")
habbitJAL = HabbitJAL(habbits_json_path=habbits_json_path, predefined_habbits_json_path=predefined_habbits_json_path)
habbitController = HabbitController(habbitJAL=habbitJAL)

# this is a test data
weekly_created_habbit: dict = {
    "name" : "weekly test",
    "description" : "just a description for weekly test",
    "period" : Period.weekly
}

daily_created_habbit: dict = {
    "name" : "daily test",
    "description" : "just a description for daily test",
    "period" : Period.daily
}

user_data = {
    "name" : "Update username"
}

def test_weekly_create_habbit():
    habbitController.create_habbit(weekly_created_habbit["name"], weekly_created_habbit["description"], weekly_created_habbit["period"])
    
    all_habbit = habbitController.get_all_habits()
    
    created_habbit = list(filter(lambda x: x["name"] == weekly_created_habbit["name"], all_habbit))[0]
    name = created_habbit["name"]
    description = created_habbit["description"]
    period = created_habbit["period"]

    assert name == weekly_created_habbit["name"]
    assert description == weekly_created_habbit["description"]
    assert period == Period.weekly.value


def test_daily_create_habbit():
    habbitController.create_habbit(daily_created_habbit["name"],daily_created_habbit["description"], daily_created_habbit["period"])

    all_habbit: list = habbitController.get_all_habits()
    
    created_habbit = list(filter(lambda x: x["name"] == daily_created_habbit["name"], all_habbit))[0]
    
    name = created_habbit["name"]
    description = created_habbit["description"]
    period = created_habbit["period"]

    assert name == daily_created_habbit["name"]
    assert description == daily_created_habbit["description"]
    assert period == Period.daily.value

def test_weekly_mark_completion():
    habbitController.mark_completion("weekly test")

    all_habbit = habbitController.get_all_habits()
    
    created_habbit = list(filter(lambda x: x["name"] == weekly_created_habbit["name"], all_habbit))[0]
    name = created_habbit["name"]
    description = created_habbit["description"]
    period = created_habbit["period"]
    completions = created_habbit["completions"]

    assert name == weekly_created_habbit["name"]
    assert description == weekly_created_habbit["description"]
    assert period == Period.weekly.value
    assert len(completions) > 0

def test_daily_mark_completion():
    habbitController.mark_completion("daily test")

    all_habbit = habbitController.get_all_habits()
    
    created_habbit = list(filter(lambda x: x["name"] == daily_created_habbit["name"], all_habbit))[0]
    name = created_habbit["name"]
    description = created_habbit["description"]
    period = created_habbit["period"]
    completions = created_habbit["completions"]

    assert name == daily_created_habbit["name"]
    assert description == daily_created_habbit["description"]
    assert period == Period.daily.value
    assert len(completions) > 0

def test_get_all_habbit():
    all_habbit = habbitController.get_all_habits()
    assert len(all_habbit) == 2 # why?? because i have created one deaily and on weekly, and not deleted yet.

def update_user_data():
    habbitController.update_user_name({"name": user_data["name"]})
    updated_user_name = habbitController.get_user_name()

    assert user_data["name"] == updated_user_name["name"]

def get_user_data():
    user_data = habbitController.get_user_name()
    assert type(user_data["name"]) is str

def test_daily_delete_habbit():
    habbitController.delete_habbit(daily_created_habbit["name"])
    all_habbit: list = habbitController.get_all_habits()
    deleted_habbit = list(filter(lambda x: x["name"] == daily_created_habbit["name"], all_habbit))
    assert len(deleted_habbit) == 0 #because i deleted it there, should not be a habbit by this name

def test_weekly_delete_habbit():
    habbitController.delete_habbit(weekly_created_habbit["name"])
    all_habbit: list = habbitController.get_all_habits()
    deleted_habbit = list(filter(lambda x: x["name"] == weekly_created_habbit["name"], all_habbit))
    assert len(deleted_habbit) == 0 #because i deleted it there, should not be a habbit by this name


# Running tests here
test_weekly_create_habbit()
test_daily_create_habbit()
test_weekly_mark_completion()
test_daily_mark_completion()
test_get_all_habbit()
update_user_data()
get_user_data()
test_daily_delete_habbit()
test_weekly_delete_habbit()