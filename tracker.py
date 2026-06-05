import datetime
from dateutil import parser
import json
from enum import Enum
date = datetime.date
time_format: str = "%Y-%m-%dT%H:%M:%S"

habbits_json_path = "./habits.json"
predefined_habbits_json_path = "./predefined_habbits.json"

#defining some enums for periods
class Period(Enum):
    daily = "daily"
    weekly = "weekly"

# as in DAL (data access layer) but for json
class HabbitJAL:

    def __init__(self, habbits_json_path, predefined_habbits_json_path) -> None:
        self.habbits_json_path = habbits_json_path
        self.predefined_habbits_json_path = predefined_habbits_json_path


    # if something goes wrong, here i will repopuplate the main habits.json with a predefined json file
    def load_predefined_habbits_to_habbit(self) -> list:
        with open(predefined_habbits_json_path , "r+") as pf:
            predefined_data = json.load(pf)
            with open(habbits_json_path, "r+") as f:
                json.dump(predefined_data, f)
                return predefined_data
            
    def get_all_habbits(self) -> list:
        with open(self.habbits_json_path, "r+") as f:
            try:
                data = json.load(f)
                return data["habbits"]
            except json.JSONDecodeError: # if the user deleted everything for some reason, i will restore everything from scratch, this only happens if there is no valid json
                return self.load_predefined_habbits_to_habbit()

    def append_to_habbits(self, new_doc:dict) -> dict:
        with open(self.habbits_json_path, "r+") as f:
            data = json.load(f)
            data["habbits"].append(new_doc)
            f.seek(0)
            json.dump(data, f, indent=4)
            return data
        
    def update_habbit(self, updated_habbit: dict):
        all_habbits = self.get_all_habbits()
        
        for i, habbit in enumerate(all_habbits):
            if habbit["name"].lower() == updated_habbit["name"].lower():
                all_habbits[i] = updated_habbit

        with open(self.habbits_json_path, "r+") as f:
            data = json.load(f)
            data["habbits"] = all_habbits
            f.seek(0)
            json.dump(data, f, indent=4)
            return data
        
    def remove_from_habbits(self, new_doc: dict) -> dict:
        
        with open(habbits_json_path, "r+") as f:
            data = json.load(f)
            data["habbits"].remove(new_doc)
            print(f"data after removed : {data}")

            with open(habbits_json_path, "w+") as fp:
                fp.seek(0)
                json.dump(data, fp, indent=4)
                json.dump
                return data    

    
class HabbitController:

    def __init__(self, habbitJAL: HabbitJAL) -> None:
        self.habbitJAL = habbitJAL


    def to_completion_format(self, completions: list[str]) -> list[date]:
        completion_dates: list[date] = []
        for completion in completions:
            parsed_date = parser.isoparse(completion.strip());
            completion_dates.append(parsed_date)
        return completion_dates

    
    
    def create_habbit(self, name: str, description: str, period: Period):
        # check if period is valid enum
        if period not in [Period.daily, Period.weekly]:
            print(f"Period not a valid value, it should be {Period.daily} or {Period.weekly}")
        
        # first i will check if there is an existing habgit with that name, if so i will return the user some error
        habbits = self.habbitJAL.get_all_habbits()

    
        for habbit in habbits:
            if habbit["name"].lower() == name.lower():
                print("Habbit already exists, please use a different name, or add entry to the existing habbit")
                return
                
            
        # create the habbit here.
        new_habbit = {
            "name" : name,
            "description" : description,
            "period" : str(period),
            "created_at" : str(datetime.datetime.now()),
            "completions" : []
        }

        self.habbitJAL.append_to_habbits(new_habbit)
                    
    def mark_completion(self, name: str) -> dict:
        habbits: list = self.habbitJAL.get_all_habbits()
        updated_habbit: dict = {}

        for habbit in habbits:
            if(habbit["name"].lower() == name.lower()):
                completions: list[str] = habbit["completions"]
                completions.append(str(datetime.datetime.now()))
                updated_habbit = habbit
                #update to the actual json here
                self.habbitJAL.update_habbit(updated_habbit)
                
        return updated_habbit


    def delete_habbit(self, name: str) -> dict:
        # first i will check if there is an existing habgit with that name, if so i will return the user some error
        habbits: list = self.habbitJAL.get_all_habbits()
        removed_habbit: dict = {}
        
        # just in case there are multiple habbits by the same name, although i handled it when creating new habbit.
        for habbit in habbits:
            if(habbit["name"].lower() == name.lower()):
                removed_habbit = habbit
                habbits.remove(habbit)

        if(removed_habbit):
            print(f"Removed habbit is : {removed_habbit}")
            self.habbitJAL.remove_from_habbits(removed_habbit)
        return removed_habbit




habbitJAL = HabbitJAL(habbits_json_path=habbits_json_path, predefined_habbits_json_path=predefined_habbits_json_path)
habbitController = HabbitController(habbitJAL=habbitJAL)


habbitController.create_habbit("test", "description", Period.weekly)
habbitController.delete_habbit("test")
habbitController.create_habbit("test2", "description", Period.daily)
habbitController.mark_completion("test2")
habbitController.delete_habbit("test")


