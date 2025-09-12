import requests
import json
import os
import random


class Pokemon:
    POKEMON_FILENAME = "pokemon.json"
    EFFECTIVENESS = {
        "Normal":    {"Rock": 0.5, "Ghost": 0},
        "Fire":      {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
        "Water":     {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
        "Electric":  {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
        "Grass":     {"Fire": 0.5, "Water": 2, "Ice": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
        "Ice":       {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Rock": 0.5, "Steel": 0.5},
        "Fighting":  {"Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Ghost": 0, "Fairy": 0.5},
        "Poison":    {"Grass": 2, "Fairy": 2, "Poison": 0.5, "Ground": 0.5, "Bug": 2, "Rock": 0.5, "Ghost": 0.5, "Steel": 0},
        "Ground":    {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
        "Flying":    {"Grass": 2, "Electric": 0.5, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
        "Psychic":   {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
        "Bug":       {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Rock": 1, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
        "Rock":      {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
        "Ghost":     {"Normal": 0, "Ghost": 2, "Psychic": 0, "Dark": 0.5},
        "Dragon":    {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
        "Dark":      {"Psychic": 2, "Ghost": 2, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
        "Steel":     {"Ice": 2, "Rock": 2, "Fairy": 2, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
        "Fairy":     {"Fighting": 2, "Dragon": 2, "Dark": 2, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5}
    }
    library = []

    def __init__(self, name, height, weight, types, family):
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.family = family
        self.hit_points = 100 # For simplicity, all pokemon have 100HP

    # The __str__ is a special method
    # that gets called automatically when we print an object.
    def __str__(self):
        text = self.name
        
        if self.name != self.family:
            text += f", an evolution of {self.family},"
        
        text += f" is {self.height}m tall and weighs {self.weight}kg."
        
        if len(self.types) > 1:
            last = self.types[-1]
            previous = self.types[:len(self.types)-1]
            text += f" It is of types {', '.join(previous)} and {last}"
        else:
            text += f" It is of type {self.types[0]}."
        
        return text
    
    def attack(self, other): 
        # Randomly select attack type
        attack_type = random.choice(self.types)
        print(f"{self.name} ({self.hit_points}HP) is attacking {other.name} ({other.hit_points}HP) with an attack of type {attack_type}.")

        # Calculate effectiveness
        effectiveness = 1
        effectiveness_factors = self.EFFECTIVENESS[attack_type]
        for type in other.types:
            if type in effectiveness_factors:
                effectiveness *= effectiveness_factors[type]
                print(effectiveness)
        
        if (effectiveness > 1):
            print(f"That is very effective!")
        elif (effectiveness > 0 and effectiveness < 1):
            print(f"That is not very effective.")
        elif (effectiveness == 0):
            print(f"The attack has no effect!")

        other.hit_points -= effectiveness*25
        if other.hit_points <= 0:
            print(f"{self.name} wins!")

    def has_fainted(self): 
        return self.hit_points <= 0

    # create_library is a class method, meaning it is called on the Class, not on the object.
    @classmethod
    def create_library(cls): #cls is a reference to the Class
        '''
        Read a library of Pokemon from a local file or fetch Pokemon from the Internet
        Set the class attribute "library".
        '''
        data = None
        # Try to get the available pokemon from a JSON file
        if os.path.exists(cls.POKEMON_FILENAME): # Check if the JSON file already exists
            print("Local Pokemon file exists. Trying to read from file...")
            try: # Try reading the JSON file
                with open(cls.POKEMON_FILENAME, "r") as file:
                    data = json.load(file)
            except (json.JSONDecodeError, IOError): # Handle errors
                print("No local Pokemon library available.")

        if data is None: # If we couldn't get the Pokemon library from a local file
            print("Could not read Pokemon from file. Trying to fetch from API...")
            try:
                response = requests.get("https://softwium.com/api/pokemons") # Try querying Pokemon from the Internet
                response.raise_for_status() # Raise an error if the request was not successful
                data = response.json() # Get the response content as JSON

                print(f"Fetched list of {len(data)} Pokemon from API. Saving to file...")

                # Save Pokemon data to file for next time
                with open(cls.POKEMON_FILENAME, "w") as file: 
                    json.dump(data, file)
            except requests.RequestException as e: # Handle errors
                print(f"Could not fetch Pokemon from API: {e}")
        
        if data is not None: 
            cls.library = data
            print(f"Saved {len(data)} Pokemon to the library.")
        else:
            print(f"Oups, something went wrong.")

    # create_random is a class method, meaning it is called on the Class, not on the object.
    # The following method is a so called Factory Method
    # The Factory Method Pattern is one of many Software Design Patterns
    # See also https://en.wikipedia.org/wiki/Software_design_pattern
    # The factory method can be called on a Class to have it create an object automatically
    # without needing to use the constructor
    @classmethod
    def create_random(cls):
        '''
        Create a Pokemon object from a random library entry
        '''
        if not cls.library:
            raise ValueError("Libray empty. Please create library first.")
        
        library_entry = random.choice(cls.library)

        # Create new Pokemon based on library entry
        return cls(
            name=library_entry.get("name"),
            height=library_entry.get("height"),
            weight=library_entry.get("weight"),
            types=library_entry.get("types"),
            family=library_entry.get("family")
        )