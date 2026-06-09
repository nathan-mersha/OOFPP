
import json
from helper import Log,Period, now, date_to_string

class HabbitJAL:
    """this is my data layer, I called it JAL (JSON Access Layer) since there's no database,
    all reads and writes to habits.json go through here so nowhere else in the app touches the file directly
    """

    def __init__(self, habbits_json_path, predefined_habbits_json_path) -> None:
        """just takes the paths to both json files and stores them"""
        self.habbits_json_path = habbits_json_path
        self.predefined_habbits_json_path = predefined_habbits_json_path


    def load_predefined_habbits_to_habbit(self) -> dict:
        """if something goes wrong with habits.json this will overwrite it with the predefined seed data"""
        with open(self.predefined_habbits_json_path , "r+") as pf:
            predefined_data = json.load(pf)
            with open(self.habbits_json_path, "r+") as f:
                json.dump(predefined_data, f)
                return predefined_data
            
    def get_all_habbits(self) -> list:
        """returns all habits from the json file, if the json is broken it restores from predefined first"""
        with open(self.habbits_json_path, "r+") as f:
            try:
                data = json.load(f)
                return data["habbits"]
            except json.JSONDecodeError: # if the user deleted everything for some reason, i will restore everything from scratch, this only happens if there is no valid json
                all_data: dict =  self.load_predefined_habbits_to_habbit()
                return all_data["habbits"]

    def get_user_data(self) -> dict:
        """returns the user data from the json file (just the name for now)"""
        with open(self.habbits_json_path, "r+") as f:
            try:
                data = json.load(f)
                return data["user"]
            except json.JSONDecodeError: # if the user deleted everything for some reason, i will restore everything from scratch, this only happens if there is no valid json
                Log.red("Data is corrupted, resetting everything...")
                all_data:dict = self.load_predefined_habbits_to_habbit()
                return all_data["user"]
            
    def append_to_habbits(self, new_doc:dict) -> dict:
        """adds a new habit to the json file"""
        with open(self.habbits_json_path, "r+") as f:
            data = json.load(f)
            data["habbits"].append(new_doc)
            f.seek(0)
            json.dump(data, f, indent=4)
            return data
        
    def update_habbit(self, updated_habbit: dict):
        """finds a habit by name and replaces it with the updated version"""
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
        """removes a habit from the json file"""
        with open(self.habbits_json_path, "r+") as f:
            data = json.load(f)
            data["habbits"].remove(new_doc)

            with open(self.habbits_json_path, "w+") as fp:
                fp.seek(0)
                json.dump(data, fp, indent=4)
                json.dump
                return data    

    def update_user_data(self, user_data: dict) -> dict:
        """saves the updated user data back to the json file"""
        with open(self.habbits_json_path, "r+") as fp:
            data = json.load(fp)
            with open(self.habbits_json_path, "w+") as f:
                
                data["user"] = user_data
                f.seek(0)
                json.dump(data, f, indent=4)
                return data
            
class HabbitController:
    """this is the main logic layer, it handles creating, deleting, completing habits
    and also the analytics, it talks to HabbitJAL for all the data stuff
    """

    def __init__(self, habbitJAL: HabbitJAL) -> None:
        """takes a HabbitJAL instance and stores it"""
        self.habbitJAL = habbitJAL

    def create_habbit(self, name: str, description: str, period: Period):
        """creates a new habit, checks that the period is valid and the name isn't already taken"""
        # check if period is valid enum
        if period not in [Period.daily, Period.weekly]:
            Log.yellow("Period not a valid value, it should be {Period.daily.value} or {Period.weekly.value}")
            
        
        # first i will check if there is an existing habgit with that name, if so i will return the user some error
        habbits = self.habbitJAL.get_all_habbits()

    
        for habbit in habbits:
            if habbit["name"].lower() == name.lower():
                Log.red("Habbit already exists, please use a different name, or add entry to the existing habbit")
                
                return
                
            
        # create the habbit here.
        new_habbit = {
            "name" : name,
            "description" : description,
            "period" : period.value,
            "created_at" : date_to_string(now()),
            "completions" : []
        }

        self.habbitJAL.append_to_habbits(new_habbit)
        Log.green(f"Habbit {new_habbit['name']} succesfully created")

    def get_all_habits(self) -> list:
        """just returns all habits"""
        all_habbits:list = self.habbitJAL.get_all_habbits()
        return all_habbits 
                   
    def mark_completion(self, name: str) -> dict:
        """finds the habit by name and adds the current time to its completions list"""
        habbits: list = self.habbitJAL.get_all_habbits()
        updated_habbit: dict = {}

        for habbit in habbits:
            if(habbit["name"].lower() == name.lower()):
                completions: list[str] = habbit["completions"]
                completions.append(date_to_string(now()))
                updated_habbit = habbit
                #update to the actual json here
                self.habbitJAL.update_habbit(updated_habbit)
                
        return updated_habbit


    def delete_habbit(self, name: str) -> dict:
        """finds and deletes the habit by name, returns an empty dict if not found"""
        # first i will check if there is an existing habgit with that name, if so i will return the user some error
        habbits: list = self.habbitJAL.get_all_habbits()
        removed_habbit: dict = {}
        
        # just in case there are multiple habbits by the same name, although i handled it when creating new habbit.
        for habbit in habbits:
            if(habbit["name"].lower() == name.lower()):
                removed_habbit = habbit
                habbits.remove(habbit)

        if(removed_habbit):
            Log.green(f"Removed habbit is : {removed_habbit["name"]}")
            self.habbitJAL.remove_from_habbits(removed_habbit)
        return removed_habbit

    def update_user_name(self, name: str) -> dict:
        """saves a new display name for the user"""
        return self.habbitJAL.update_user_data({"name" : name})

    def get_user_name(self) -> str:
        """returns the user's display name from the json file"""
        user_data = self.habbitJAL.get_user_data()
        return user_data["name"]




