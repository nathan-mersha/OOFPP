# this will be my helper functions, and helper classes, and enums, const and all those stuff
from enum import Enum
import datetime as dt
from dateutil import parser
date = dt.date
time_format: str = "%Y-%m-%dT%H:%M:%S"

class Log:
    yellow_color = '\033[93m' # i will use this for warning
    green_color = '\033[92m' # i will use this for success message
    red_color = '\033[91m' # i will use this for error message
    reset_color = '\033[0m' # this is just white, used for reset
    blue_color = '\033[94m' # i will use this for menu color
    
    @staticmethod
    def yellow(text: str):
        print(f"{Log.yellow_color}{text}{Log.reset_color}")
    
    @staticmethod
    def red(text: str):
        print(f"{Log.red_color}{text}{Log.reset_color}")

    @staticmethod
    def green(text: str):
        print(f"{Log.green_color}{text}{Log.reset_color}")

    @staticmethod
    def blue(text: str):
        print(f"{Log.blue_color}{text}{Log.reset_color}")    

    
#defining some enums for periods
class Period(Enum):
    daily = "daily"
    weekly = "weekly"

def date_to_string(date: date)-> str:
    return str(date)

def string_to_date(date_string: str) -> date:
     return  dt.datetime.fromisoformat(date_string)

def now()-> date:
     return dt.datetime.now()


def to_completion_format(completions: list[str]) -> list[date]:
        completion_dates: list[date] = []
        for completion in completions:
            parsed_date = parser.isoparse(completion.strip())
            completion_dates.append(parsed_date)
        return completion_dates