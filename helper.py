# this will be my helper functions, and helper classes, and enums, const and all those stuff
from enum import Enum
import datetime as dt
from dateutil import parser
date = dt.date
time_format: str = "%Y-%m-%dT%H:%M:%S"

class Log:
    """just a helper class to print stuff in colour in the terminal,
    yellow = warning, red = error, green = success, blue = menu
    """

    yellow_color = '\033[93m' # i will use this for warning
    green_color = '\033[92m' # i will use this for success message
    red_color = '\033[91m' # i will use this for error message
    reset_color = '\033[0m' # this is just white, used for reset
    blue_color = '\033[94m' # i will use this for menu color
    
    @staticmethod
    def yellow(text: str):
        """print the text in yellow, i use this for warnings"""
        print(f"{Log.yellow_color}{text}{Log.reset_color}")
    
    @staticmethod
    def red(text: str):
        """print the text in red, i use this for errors"""
        print(f"{Log.red_color}{text}{Log.reset_color}")

    @staticmethod
    def green(text: str):
        """print the text in green, i use this for success messages"""
        print(f"{Log.green_color}{text}{Log.reset_color}")

    @staticmethod
    def blue(text: str):
        """print the text in blue, i use this for the menus"""
        print(f"{Log.blue_color}{text}{Log.reset_color}")    

    
#defining some enums for periods
class Period(Enum):
    """just an enum for the two habit periods, daily or weekly"""

    daily = "daily"
    weekly = "weekly"

def date_to_string(date: date)-> str:
    """just converts a date to a string so i can save it to the json"""
    return str(date)

def string_to_date(date_string: str) -> date:
    """parses a date string back to a datetime object"""
    return  dt.datetime.fromisoformat(date_string)

def now()-> date:
    """just returns the current datetime"""
    return dt.datetime.now()


def to_completion_format(completions: list[str]) -> list[date]:
    """takes the list of completion date strings from the json and converts them to datetime objects,
    i use dateutil here because the date strings can be in slightly different formats
    """
    completion_dates: list[date] = []
    for completion in completions:
        parsed_date = parser.isoparse(completion.strip())
        completion_dates.append(parsed_date)
    return completion_dates