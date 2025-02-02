import pandas as pd
import json
import random

class Ais:
    forms_file = "static/forms.json"
    def __init__(self):
        self.forms = json.load(open(self.forms_file, 'r'))['forms']
        self.current_form_num = 12
        self.available_forms = list(range(1,12))
        self.leg_resist = 8
        self.HP = 1000
    
    def change_form(self):
        if len(self.available_forms) < 1:
            self.available_forms = list(range(1,13))
        self.current_form_num = random.choice(self.available_forms)
        self.available_forms.remove(self.current_form_num) # avoid repeats
        return self.get_form()

    def get_form(self):
        return self.forms[self.current_form_num-1]
        
    def set_HP(self, newHP):
        self.HP = newHP

    def set_leg_resist(self, newLegResist):
        self.leg_resist = newLegResist

    def get_HP(self):
        return self.HP
    
    def get_leg_resist(self):
        return self.leg_resist
    
    def set_form(self, form_dict):
        self.forms[self.current_form_num-1] = form_dict

    def reset_leg(self):
        self.forms[self.current_form_num-1]['leg_action_rem'] = self.get_form()['leg_action_num']


class Combat:
    def __init__(self, initiative_dict, ais):
        self.init_dict = initiative_dict
        self.initiative = list(dict(sorted(initiative_dict.items(),reverse=True, key=lambda item: int(item[1]))).keys())
        self.reactions = dict.fromkeys(self.initiative, False)
        self.current_index = 0 # first player in the initiative array
        self.ais = ais
    
    def reset_initiative(self, initiative_dict):
        self.init_dict = initiative_dict
        if len(initiative_dict.items()) > 1:
            temp_current = self.initiative[self.current_index]
            self.initiative = list(dict(sorted(initiative_dict.items(), reverse=True, key=lambda item: int(item[1]))).keys())
            self.current_index = self.initiative.index(temp_current)
    
    def next_turn(self, reactions):
        self.reactions = reactions
        if self.current_index >= len(self.initiative) - 1:
            # last player in the array
            self.current_index = 0
        else:
            self.current_index += 1
        self.reactions[self.get_current_player()] = False

        return self.get_current_player()

    def get_current_player(self):
        return self.initiative[self.current_index]
    
    def get_initiative(self):
        return self.initiative
    
    def get_raw_init(self):
        return self.init_dict
    
    def get_reactions(self):
        return self.reactions
    def set_reactions(self, react_dict):
        self.reactions = react_dict