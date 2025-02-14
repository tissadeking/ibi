from __future__ import print_function, unicode_literals
import regex
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt

style = style_from_dict({
            Token.QuestionMark: '#E91E63 bold',
            Token.Selected: '#673AB7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#2196f3 bold',
            Token.Question: '',
        })
print('Welcome to HORSE IBI Intent Entry')

question_entry = [

        {
            'type': 'list',
            'qmark': '',
            'name': 'intent_entry',
            'message': 'How do you want to enter your intents?',
            'choices': ['Write intents', 'Select from lists',
                        'Receive Intents from Another Module',
                        'Use AI/ML-Recommended Intents'],
            'filter': lambda val: val.lower()
        }

    ]
answer_entry = prompt(question_entry, style=style)
sf = answer_entry['intent_entry']
print('sf: ', sf)






cas_policy = {
    'intent_type': 'str',
    'threat': 'str',
    'attacked_host': 'str',
    'action': 'str',
    'duration': int,
    'intent_id': 'str',
    'mitigation_host': 'str',
}


a_list = [1, 2, 3, 4, 5]

# Checks if the variable "a_list" is a list
if type(a_list) == list:
    print("Variable is a list.")
else:
    print("Variable is not a list.")


























import json
#import bpy

# Class definition
class Person(object):
    def __init__(self, name, surname, age) -> None:
        self.person_name = name
        self.person_surname = surname
        self.person_age = age

    def to_custom_json(self):
        mapping = {'person_name': 'person-name', 'person_surname': 'person-surname-with-hyphen',
                   'person_age': 'the-name-that-you-want'}
        result = json.dumps({mapping.get(k, k): v for k, v in self.__dict__.items()})
        return result

# Creating the object (instantiate the class Person)
p1 = Person("Bill", "Gates", 68)
p2 = Person("Obama", "Barack", 63)
#bpy.context.p1.name = bpy.context.p1.name.replace("_name", "_LP")
p1.nameee = 'ajimpa'
delattr(p1,'person_name')

print("Printing the dictionary of the object")
print(p1.__dict__)
print(p2.__dict__)

print("Using json dumps over the dictionary with underscores")
print(json.dumps(p1.__dict__))
print(json.dumps(p2.__dict__))

print("Using custom encoder method...")
#print(p1.to_custom_json())
#print(p2.to_custom_json())

import numpy as np
# Assuming you have defined the number of states and actions
num_states = 10  # Example number of states
num_actions = 5  # Example number of actions
# Initialize Q-table with zeros
Q_table = np.zeros((num_states, num_actions))
# Print initial Q-table
print("Initial Q-Table:")
print(Q_table)

import yaml
import pandas as pd
states_arr = ['3gh','4a','4s','sd5']
actions_arr = ['g','f','t']
q_labels_dict = {}
q_labels_dict['state_labels'] = states_arr
q_labels_dict['action_labels'] = actions_arr
with open('data.yml', 'w') as outfile:
    yaml.dump(q_labels_dict, outfile, default_flow_style=False)
with open('data.yml') as f:
    parameters = yaml.safe_load(f)
print(parameters['state_labels'])

n_states = len(states_arr)  # Number of states in the grid world
n_actions = len(actions_arr)
# Initialize Q-table with zeros
Q_table_values = np.ones((n_states, n_actions))
print('initial q table: ', Q_table_values)
#print(Q_table_values[10][2])
# convert array into dataframe
Q_table_df = pd.DataFrame(Q_table_values)
# save the dataframe as a csv file
Q_table_df.to_csv("q_table.csv", index=False)

df = pd.read_csv('q_table.csv')
arr = df.to_numpy()
#arr = np.transpose(arr)
print(arr)
action = np.argmax(arr[1])
print('max action: ', action)


# Python code to convert string to list
def Convert(string):
    li = list(string.split(" "))
    return li
# Driver code
str1 = "Geeks"
print(Convert(str1))
