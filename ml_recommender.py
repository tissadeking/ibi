import csv
import os
import time
import tracemalloc

import numpy as np
import random
from elasticsearch import Elasticsearch
import config
import delete_intents_elasticsearch
import policy_configurator
import pandas as pd
import yaml

intents_url = config.intents_url
stored_intents_url = config.stored_intents_url
qos_intents_url = config.qos_intents_url
stored_qos_intents_url = config.stored_qos_intents_url
workflow_url = config.workflow_url
whatif_send_url = config.whatif_send_url
elasticsearch_url = config.elasticsearch_url
es = Elasticsearch(elasticsearch_url)

files_directory = '/code/app/'
df_policy = pd.read_csv(config.policy_store_directory)

# Define parameters
learning_rate = 0.8
discount_factor = 0.95
exploration_prob = 0.2
epochs = 1000

#REMEMBER TO ADD RECO AND REWARDING CALL AGAIN AT INTENT MANAGER WHEN IT RECEIVES ALREADY EXISTING
#INTENT, IT WOULD ADD ACTION TO THE DICTIONARY TO CALL

#function to populate q_table
def populate_q_labels():
    states_arr = []
    actions_arr = []
    for ind in df_policy.index:
        state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
        action_label = df_policy['action'][ind]
        if state_label not in states_arr:
            states_arr.append(state_label)
        if action_label not in actions_arr:
            actions_arr.append(action_label)
    for ind2 in df_policy.index:
        state_label = 'no_' + df_policy['threat'][ind2]
        #action = df_policy['action'][ind]
        if state_label not in states_arr:
            states_arr.append(state_label)
    q_labels_dict = {}
    q_labels_dict['states_labels'] = states_arr
    q_labels_dict['actions_labels'] = actions_arr
    #yml_file = files_directory + 'q_labels.yml'
    yml_file = config.q_labels_directory
    with open(yml_file, 'w') as outfile:
        yaml.dump(q_labels_dict, outfile, default_flow_style=False)
    print('q labels populated')
    #print(q_labels_dict)
#print('state labels arr: ', states_arr)
#print('action labels arr: ', actions_arr)

#function to create q_table
def create_q_table():
    #yml_file = files_directory + 'q_labels.yml'
    yml_file = config.q_labels_directory
    with open(yml_file) as f:
        paras = yaml.safe_load(f)
    states_arr = paras['states_labels']
    actions_arr = paras['actions_labels']
    # Define the environment
    n_states = len(states_arr)  # Number of states in the grid world
    n_actions = len(actions_arr) # Number of possible actions (up, down, left, right)
    #goal_state = 15  # Goal state

    # Initialize Q-table with ones
    Q_table_values = np.ones((n_states, n_actions))

    #states_arr = []
    mitigation_ddos_ntp_actions_arr = []
    mitigation_ddos_dns_actions_arr = []
    mitigation_ddos_pfcp_actions_arr = []
    prevention_ddos_ntp_actions_arr = []
    prevention_ddos_dns_actions_arr = []
    prevention_ddos_pfcp_actions_arr = []
    for ind in df_policy.index:
        if df_policy['intent_type'][ind] == 'mitigation':
            if df_policy['threat'][ind] == 'ddos_ntp':
                #state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
                action_label = df_policy['action'][ind]
                #if state_label not in states_arr:
                #    states_arr.append(state_label)
                if action_label not in mitigation_ddos_ntp_actions_arr:
                    mitigation_ddos_ntp_actions_arr.append(action_label)
            if df_policy['threat'][ind] == 'ddos_dns':
                #state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
                action_label = df_policy['action'][ind]
                #if state_label not in states_arr:
                #    states_arr.append(state_label)
                if action_label not in mitigation_ddos_dns_actions_arr:
                    mitigation_ddos_dns_actions_arr.append(action_label)
            if df_policy['threat'][ind] == 'ddos_pfcp':
                #state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
                action_label = df_policy['action'][ind]
                #if state_label not in states_arr:
                #    states_arr.append(state_label)
                if action_label not in mitigation_ddos_pfcp_actions_arr:
                    mitigation_ddos_pfcp_actions_arr.append(action_label)

        if df_policy['intent_type'][ind] == 'prevention':
            if df_policy['threat'][ind] == 'ddos_ntp':
                #state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
                action_label = df_policy['action'][ind]
                #if state_label not in states_arr:
                #    states_arr.append(state_label)
                if action_label not in prevention_ddos_ntp_actions_arr:
                    prevention_ddos_ntp_actions_arr.append(action_label)
            if df_policy['threat'][ind] == 'ddos_dns':
                #state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
                action_label = df_policy['action'][ind]
                #if state_label not in states_arr:
                #    states_arr.append(state_label)
                if action_label not in prevention_ddos_dns_actions_arr:
                    prevention_ddos_dns_actions_arr.append(action_label)
            if df_policy['threat'][ind] == 'ddos_pfcp':
                #state_label = df_policy['intent_type'][ind] + '_' + df_policy['threat'][ind]
                action_label = df_policy['action'][ind]
                #if state_label not in states_arr:
                #    states_arr.append(state_label)
                if action_label not in prevention_ddos_pfcp_actions_arr:
                    prevention_ddos_pfcp_actions_arr.append(action_label)
    for j in range(len(Q_table_values)):
        state_label = retrieve_state_label(j)
        if 'mitigation_ddos_ntp' in state_label:
            for k in range(len(Q_table_values[j])):
                action_label_check = retrieve_action_label(k)
                if action_label_check not in mitigation_ddos_ntp_actions_arr:
                    Q_table_values[j][k] = -100
        if 'mitigation_ddos_dns' in state_label:
            for k in range(len(Q_table_values[j])):
                action_label_check = retrieve_action_label(k)
                if action_label_check not in mitigation_ddos_dns_actions_arr:
                    Q_table_values[j][k] = -100
        if 'mitigation_ddos_pfcp' in state_label:
            for k in range(len(Q_table_values[j])):
                action_label_check = retrieve_action_label(k)
                if action_label_check not in mitigation_ddos_pfcp_actions_arr:
                    Q_table_values[j][k] = -100

        if 'prevention_ddos_ntp' in state_label:
            for k in range(len(Q_table_values[j])):
                action_label_check = retrieve_action_label(k)
                if action_label_check not in prevention_ddos_ntp_actions_arr:
                    Q_table_values[j][k] = -100
        if 'prevention_ddos_dns' in state_label:
            for k in range(len(Q_table_values[j])):
                action_label_check = retrieve_action_label(k)
                if action_label_check not in prevention_ddos_dns_actions_arr:
                    Q_table_values[j][k] = -100
        if 'prevention_ddos_pfcp' in state_label:
            for k in range(len(Q_table_values[j])):
                action_label_check = retrieve_action_label(k)
                if action_label_check not in prevention_ddos_pfcp_actions_arr:
                    Q_table_values[j][k] = -100
    #print('initial q table: ', Q_table_values)
    #print(Q_table_values[10][2])
    # convert array into dataframe
    Q_table_df = pd.DataFrame(Q_table_values)
    # save the dataframe as a csv file
    Q_table_df.to_csv(config.q_table_directory, index=False)
    print('q table created')

#function to retrieve the index of a particular state label
def retrieve_state_index(state_label):
    #yml_file = files_directory + 'q_labels.yml'
    yml_file = config.q_labels_directory
    with open(yml_file) as f:
        paras = yaml.safe_load(f)
    states_arr = paras['states_labels']
    state_index = states_arr.index(state_label)
    return state_index

#function to retrieve index of a particular action label
def retrieve_action_index(action_label):
    #yml_file = files_directory + 'q_labels.yml'
    yml_file = config.q_labels_directory
    with open(yml_file) as f:
        paras = yaml.safe_load(f)
    actions_arr = paras['actions_labels']
    action_index = actions_arr.index(action_label)
    return action_index

#function to retrieve label of a particular state with its index
def retrieve_state_label(ind):
    #yml_file = files_directory + 'q_labels.yml'
    yml_file = config.q_labels_directory
    with open(yml_file) as f:
        paras = yaml.safe_load(f)
    state_label = paras['states_labels'][ind]
    return state_label

#function to retrieve label of a particular action with its index
def retrieve_action_label(ind):
    #yml_file = files_directory + 'q_labels.yml'
    yml_file = config.q_labels_directory
    with open(yml_file) as f:
        paras = yaml.safe_load(f)
    #state_label = paras['state_labels'][ind]
    action_label = paras['actions_labels'][ind]
    return action_label

#function to retrieve entire q_table values
def retrieve_q_table():
    df = pd.read_csv(config.q_table_directory)
    arr = df.to_numpy()
    return arr

#function to check whether selected action conflicts with qos intents
def qos_check(problem_constraints, action_dict, action_label, reco_dict):
    global constraint
    #print('action label start qos check: ', action_label)
    for ind in df_policy.index:
        if df_policy['intent_type'][ind] == reco_dict['intent_type'] and \
                df_policy['threat'][ind] == reco_dict['threat'] and \
                df_policy['action'][ind] == action_label:
            constraint = df_policy['constraint'][ind]

    #print('constraints qos: ', constraint)
    #print('problem constraints: ', problem_constraints)
    #con = 0
    '''for i in range(len(problem_constraints)):
        if problem_constraints[i] == constraint:
            print('constraint found')
            con += 1'''
    if constraint in problem_constraints:
    #if con > 0:
        return select_action(problem_constraints, action_dict, reco_dict)
    else:
        #print('no constraint found')
        #print('action label end qos check: ', action_label)
        return action_label

#function to select suitable action from a list of actions
def select_action(problem_constraints, action_dict, reco_dict):
    val_list = list(action_dict.values())
    action_index_for_max = np.argmax(val_list)
    #print('action_index_for_max: ', action_index_for_max)
    #print('ACTION DICT: ', action_dict)
    #action_label = retrieve_action_label(action_index_for_max)
    del action_dict[str(action_index_for_max)]
    #print('dict: ', action_dict)
    val_list = list(action_dict.values())
    #print('val list: ', val_list)
    key_list = list(action_dict.keys())
    #print('key list: ', key_list)
    action_index_val = np.argmax(val_list)
    #act_ind = val_list.index(action_index_val)
    action_index_for_max = key_list[action_index_val]
    #print('action_index_for_max: ', action_index_for_max)
    action_label = retrieve_action_label(int(action_index_for_max))
    #print('action_label: ', action_label)
    return qos_check(problem_constraints, action_dict, action_label, reco_dict)
    #return action_dict

#function to call the ML recommender
def call_recommender(reco_dict):
    key_list = list(reco_dict.keys())
    if 'status' in key_list:
        next_state_label = 'no_' + reco_dict['threat']
        reco_dict['next_state_label'] = reco_dict['goal_state_label'] = next_state_label
        current_state_label = reco_dict['intent_type'] + '_' + reco_dict['threat']
        reco_dict['current_state_label'] = current_state_label
        rewarding(reco_dict)
        reco_index = es.exists(index="reco_store", id="1")
        if reco_index == True:
            resp = es.search(index="reco_store", size=100, query={"match_all": {}})
            for ind in range(len(resp['hits']['hits'])):
                hit1 = resp['hits']['hits'][ind]['_source']
                if hit1['intent_type'] == reco_dict['intent_type'] and hit1['threat'] == reco_dict['threat'] and \
                        str(hit1['host']) == reco_dict['host'] and \
                        str(hit1['duration']) == str(reco_dict['duration']):
                    delete_intents_elasticsearch.delete_intents_elasticsearch_fun(elasticsearch_url,
                                                                                  resp['hits']['hits'][ind]['_id'],
                                                                                  "reco_store")
    elif 'what_if_response' in key_list:
        current_state_label = reco_dict['intent_type'] + '_' + reco_dict['threat']
        goal_state_label = 'no_' + reco_dict['threat']
        reco_dict['goal_state_label'] = goal_state_label
        reco_dict['current_state_label'] = reco_dict['next_state_label'] = current_state_label
        rewarding(reco_dict)
        recommend(reco_dict)
    else:
        check_store(reco_dict)

#function to store the recommended intents inside reco_store
def store_recommended(reco_dict):
    reco_index = es.exists(index="reco_store", id="1")
    if reco_index == True:
        resp1 = es.search(index="reco_store", size=100, query={"match_all": {}})
        total = resp1['hits']['total']['value']
        id = total + 1
        es.index(index="reco_store", id=id, document=reco_dict)
    else:
        es.index(index="reco_store", id=str(1), document=reco_dict)

#function to check the reco_store for a particular intent
def check_store(intent_dict):
    #intent_dict contains: intent_type, threat, host, duration, and will be sent per host
    #current_state, goal_state,
    #current_state label = intent_type+threat
    #goal_state label example = no+threat
    current_state_label = intent_dict['intent_type'] + '_' + intent_dict['threat']
    goal_state_label = 'no_' + intent_dict['threat']
    reco_index = es.exists(index="reco_store", id="1")
    if reco_index == True:
        resp = es.search(index="reco_store", size=100, query={"match_all": {}})
        total = resp['hits']['total']['value']
        #THIS FOR LOOP HERE IS THE CAUSE OF THE PROBLEM OF CONTINUOUS RUNNING OF ML RECO
        for ind in range(len(resp['hits']['hits'])):
            hit1 = resp['hits']['hits'][ind]['_source']
            #for i in range(len(intent_dict['host'])):
            if hit1['intent_type'] == intent_dict['intent_type'] and hit1['threat'] == intent_dict['threat'] and \
                    str(hit1['host']) == intent_dict['host']:  #and \
                    #str(hit1['duration']) == str(intent_dict['duration']):
                intent_dict['current_state_label'] = current_state_label
                intent_dict['goal_state_label'] = goal_state_label
                #recommend(intent_dict)
                intent_dict['next_state_label'] = current_state_label
                rewarding(intent_dict)
                delete_intents_elasticsearch.delete_intents_elasticsearch_fun(elasticsearch_url, resp['hits']['hits'][ind]['_id'],
                                                            "reco_store")
            else:
                intent_dict['current_state_label'] = current_state_label
                intent_dict['goal_state_label'] = goal_state_label
                #recommend(intent_dict)
    else:
        intent_dict['current_state_label'] = current_state_label
        intent_dict['goal_state_label'] = goal_state_label
        #recommend(intent_dict)
    recommend(intent_dict)

# Q-learning algorithm
def recommend(reco_dict):
    #current_state, goal_state, host, duration, threat
    #current state is a number, each threat or no threat has a number

    #current_state = np.random.randint(0, n_states)  # Start from a random state
    #print(current_state)
    #data_dict = {}
    #tracemalloc.start()
    #start = time.time()
    current_state_label = reco_dict['current_state_label']
    goal_state_label = reco_dict['goal_state_label']
    if current_state_label != goal_state_label:
        # Choose action with epsilon-greedy strategy
        x = np.random.rand()
        #x = random.random()
        #x = 0.3
        print('np random rand: ', x)
        if x < exploration_prob or reco_dict['intent_type'] == 'prevention':
            '''if reco_dict['threat'] == 'dos_sig':
                data_dict['method'] = 'random'
            if reco_dict['threat'] == 'api_vul':
                data_dict['method'] = 'hitl'
            if reco_dict['threat'] == 'ddos_dns' or reco_dict['threat'] == 'ddos_ntp':
                data_dict['method'] = 'priority_based'
            '''
            #action = np.random.randint(0, n_actions)  # Explore
            policy_configurator.policy_configurator_fun(reco_dict, workflow_url, whatif_send_url,
                       stored_intents_url, elasticsearch_url)

        else:
            #data_dict['method'] = 'ml_reco'
            Q_table = retrieve_q_table()
            current_state_index = retrieve_state_index(current_state_label)
            action_index = np.argmax(Q_table[current_state_index])  # Exploit
            action_label = retrieve_action_label(action_index)
            action_dict = {}
            for i in range(len(Q_table[current_state_index])):
                action_dict[str(i)] = Q_table[current_state_index][i]
            print('dict: ', action_dict)
            #print('action label: ', action_label)
            #APPLY CONFLICT CHECK WITH QOS AND SELECT ACTION THAT DOESN'T CONFLICT WITH QOS
            #check constraint of selected action in df_policy, extract problem constraints
            #if constraint of selected action is in problem constraints,
            # then make np.argmax ignore the value with that action label and redo np.argmax
            print('reco dict host: ', reco_dict['host'])
            if type(reco_dict['host']) == list:
                reco_dict['host'] = reco_dict['host'][0]
            reco_dict['host'] = list(reco_dict['host'].split(" "))
            problem_constraints = policy_configurator.extract_problem_constraints(
                reco_dict['intent_type'], reco_dict['threat'], reco_dict)
            new_action_label = qos_check(problem_constraints, action_dict, action_label, reco_dict)
            reco_dict['action'] = new_action_label
            print('reco dict: ', reco_dict)
            for ind in df_policy.index:
                #print(df_policy['intent_type'][ind], df_policy['threat'][ind], df_policy['action'][ind])
                if df_policy['intent_type'][ind] == reco_dict['intent_type'] and \
                    df_policy['threat'][ind] == reco_dict['threat'] and \
                        df_policy['action'][ind] == reco_dict['action']:
                    reco_dict['priority'] = df_policy['priority'][ind]
            #reco_dict['priority'] =
            #IF MITIGATION, SEND STRAIGHT TO POLICY CONFIGURATOR 2
            #IF PREVENTION INTENT THEN APPLY WHAT-IF THINGS WITH A FIELD INDICATING IT'S COMING FROM
            # ML RECOMMENDER AFTER WHICH WHAT-IF CAN CALL POLICY CONFIGURATOR
            #reco_dict['host'] = list(reco_dict['host'].split(" "))
            policy_configurator.policy_configurator_fun_2(workflow_url, stored_intents_url, elasticsearch_url,
                                                      reco_dict)
            #store_recommended(reco_dict)

        #store current state, goal state, action, host, duration, priority in a reco store
        #for each command sent to the policy configurator a priority value must be traced from
        #the policy store and given to it
    '''end = time.time()
    time_taken = '%.6f' % (end - start)
    current_usage, peak_usage = tracemalloc.get_traced_memory()
    # print(f"{current_usage = }, {peak_usage = }")
    data_dict['duration'] = time_taken
    data_dict['memory_usage'] = current_usage
    columns = ['method', 'duration', 'memory_usage']
    file_name = data_dict['method'] + '.csv'
    if os.path.exists(file_name) == True:
        with open(file_name, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writerow(data_dict)
    elif os.path.exists(file_name) == False:
        with open(file_name, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerow(data_dict)
    # print(current_usage)
    # print(time_taken)
    # stopping the tracemalloc library
    tracemalloc.stop()'''

#once duration elapses and no repetition intent is received, then the rewarding function is called
def rewarding(reward_dict):
    #reward dict will have next_state_label, current_state_label, goal_state_label, action
    #next_state, goal_state, current_state, action
    #next state is the result, ie the current state after the action was implemented in the network
    #current state was the previous state before action was implemented
    # Simulate the environment (move to the next state)
    # For simplicity, move to the next state
    #next_state = (current_state + 1) % n_states
    #print('rewarding started: ', reward_dict)
    next_state_label = reward_dict['next_state_label']
    current_state_label = reward_dict['current_state_label']
    goal_state_label = reward_dict['goal_state_label']
    action_label = reward_dict['action']
    # Define a simple reward function (1 if the goal state is reached, 0 otherwise)
    reward = 0.5 if next_state_label == goal_state_label else -0.5
    current_state_index = retrieve_state_index(current_state_label)
    next_state_index = retrieve_state_index(next_state_label)
    action_index = retrieve_action_index(action_label)
    Q_table = retrieve_q_table()
    # Update Q-value using the Q-learning update rule
    #Q_table[current_state_index, action_index] += learning_rate * \
    #    (reward + discount_factor *
    #     np.max(Q_table[next_state_index]) - Q_table[current_state_index, action_index])
    Q_table[current_state_index][action_index] += learning_rate * \
            (reward + discount_factor * np.max(Q_table[next_state_index]) -
             Q_table[current_state_index][action_index])
    Q_table_df = pd.DataFrame(Q_table)
    # save the dataframe as a csv file
    Q_table_df.to_csv(config.q_table_directory, index=False)
    #current_state = next_state  # Move to the next state
    # After training, the Q-table represents the learned Q-values
    #print("Learned Q-table:")
    #print(retrieve_q_table())
