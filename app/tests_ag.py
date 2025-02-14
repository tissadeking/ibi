import numpy as np, pandas as pd
from numpy.array_api import argmax

df = pd.read_csv('q_table.csv')
arr = df.to_numpy()
#arr = np.transpose(arr)
print(arr)
action = np.argmax(arr[1])
print('max action: ', action)
print(type(arr[1]))
print(arr[1][1])

action_dict = {}
for i in range(len(arr[1])):
    action_dict[str(i)] = arr[1][i]
print('dict: ', action_dict)
val_list = list(action_dict.values())
action_value_for_max = np.argmax(val_list)
del action_dict[str(action_value_for_max)]
print('dict: ', action_dict)

action = np.argmax(Q_table[current_state])  # Exploit

#APPLY CONFLICT CHECK WITH QOS AND SELECT ACTION THAT DOESN'T CONFLICT WITH QOS
#check constraint of selected action in df_policy, extract problem constraints
#if constraint of selected action is in problem constraints,
# then make np.argmax ignore the value with that action label and redo np.argmax
action_dict = {}
for i in range(len(Q_table[current_state])):
    action_dict[str(i)] = Q_table[current_state][i]
print('dict: ', action_dict)

def select_action(problem_constraints, action_dict):
    val_list = list(action_dict.values())
    action_value_for_max = np.argmax(val_list)
    action_label = retrieve_action_label(action_value_for_max)
    del action_dict[str(action_value_for_max)]
    print('dict: ', action_dict)
    val_list = list(action_dict.values())
    action_value_for_max = np.argmax(val_list)
    action_label = retrieve_action_label(action_value_for_max)
    qos_check(problem_constraints, action_dict, action_label)
    #return action_dict

def qos_check(problem_constraints, action_dict, action_label):
    global constraint
    for ind in df_policy.index:
        if df_policy['intent_type'][ind] == reco_dict['intent_type'] and \
                df_policy['threat'][ind] == reco_dict['threat'] and \
                df_policy['action'][ind] == action_label:
            constraint = df_policy['constraint'][ind]
    #for i in range(len(problem_constraints)):
    if constraint in problem_constraints:
        select_action(problem_constraints, action_dict)
    else:
        val_list = list(action_dict.values())
        action_value_for_max = np.argmax(val_list)
        action_label = retrieve_action_label(action_value_for_max)
        return action_label


