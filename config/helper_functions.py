from datetime import datetime
from rich.console import Console

def get_valid_date(prompt, allow_blank=False):
    console = Console()
    while True:
        date_input = input(prompt)
        if allow_blank and date_input == "":
            return None
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            console.print("Invalid date format. Please enter the date in YYYY-MM-DD format.", style="bold red")

def get_valid_int(prompt, allow_blank=False):
    console = Console()
    while True:
        input_value = input(prompt)
        if allow_blank and input_value == "":
            return None
        if input_value.isdigit():
            return int(input_value)
        console.print("Please enter a valid numeric value.", style="bold red")

def get_valid_id(session, prompt, get_function, entity_name, allow_blank=False, current_id=None):
    console = Console()
    while True:
        get_function()
        input_id = input(prompt)
        if allow_blank and input_id == "":
            return current_id
        if input_id.isdigit():
            entity_id = int(input_id)
            entity = session.query(entity_name).get(entity_id)
            if entity:
                return entity_id
            else:
                console.print(f"{entity_name.__name__} ID not found. Please choose an existing ID from the list.", style="bold red")
        else:
            console.print("Please enter a valid numeric ID.", style="bold red")
