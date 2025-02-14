import requests
import time
import get_intents_script

#function to resolve conflict in policies
def conflict_fun(ind, policy_dict, workflow_url, stored_intents_url, elasticsearch_url):
    #if intent is a qos intent
    if policy_dict['intent_type'] == 'qos_ntp' or policy_dict['intent_type'] == 'qos_dns' \
            or policy_dict['intent_type'] == 'qos_pfcp':

        intent_host_arr = policy_dict['host']
        stored_qos_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
        conflict_res = False
        if stored_qos_intents_arr[ind]['host'] in intent_host_arr and \
                stored_qos_intents_arr[ind]['name'] == policy_dict['name'] and \
                stored_qos_intents_arr[ind]['intent_type'] == policy_dict['intent_type']:
            for i in range(len(intent_host_arr)):
                if stored_qos_intents_arr[ind]['host'] == intent_host_arr[i] and \
                        stored_qos_intents_arr[ind]['name'] == policy_dict['name'] and \
                        stored_qos_intents_arr[ind]['intent_type'] == policy_dict['intent_type']:
                    url_to_delete = stored_intents_url + "/" + str(stored_qos_intents_arr[ind]['qos_intent_id'])
                    requests.delete(url_to_delete)
                    conflict_res = True
                    print('a qos conflict resolved for host: ', stored_qos_intents_arr[ind]['host'])
                    print('')
                time.sleep(1)

            if conflict_res == True:
                stored_qos_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
                # repeat the process for the next intent in the intent store
                if (ind < len(stored_qos_intents_arr)):
                    print('starting new qos conflict resolution')
                    conflict_fun(ind, policy_dict, workflow_url, stored_intents_url,
                                 elasticsearch_url)
                else:
                    print('qos conflicts resolved')
            else:
                ind = ind + 1
                stored_qos_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
                # repeat the process for the next intent in the intent store
                if (ind < len(stored_qos_intents_arr)):
                    print('starting new qos conflict resolution')
                    conflict_fun(ind, policy_dict, workflow_url, stored_intents_url,
                                 elasticsearch_url)
                else:
                    print('qos conflicts resolved')

        # if an existing intent doesn't conflict with new intent then move to the next intent in the intent store
        else:
            ind = ind + 1
            stored_qos_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
            # repeat the process for the next intent in the intent store
            if (ind < len(stored_qos_intents_arr)):
                print('starting new qos conflict resolution')
                conflict_fun(ind, policy_dict, workflow_url, stored_intents_url,
                             elasticsearch_url)
            else:
                print('ok')


    #now, if the intent is a security intent
    else:
        # intent_host_arr is the array containing the host(s) for which the intent(s) apply
        intent_host_arr = policy_dict['host']
        stored_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
        conflict_res = False
        if stored_intents_arr[ind]['host'] in intent_host_arr and \
                stored_intents_arr[ind]['threat'] == policy_dict['threat'] and \
                int(policy_dict['priority']) < int(stored_intents_arr[ind]['priority']):
            for i in range(len(intent_host_arr)):
                if stored_intents_arr[ind]['host'] == intent_host_arr[i] and \
                        stored_intents_arr[ind]['threat'] == policy_dict['threat'] and \
                        int(policy_dict['priority']) < int(stored_intents_arr[ind]['priority']):
                    url_to_delete = stored_intents_url + "/" + str(stored_intents_arr[ind]['intent_id'])
                    requests.delete(url_to_delete)
                    conflict_res = True
                    print('a conflict resolved for host: ', stored_intents_arr[ind]['host'])
                    print('')
                time.sleep(1)

            if conflict_res == True:
                stored_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
                #repeat the process for the next intent in the intent store
                if (ind < len(stored_intents_arr)):
                    print('starting new conflict resolution')
                    conflict_fun(ind, policy_dict, workflow_url, stored_intents_url,
                                 elasticsearch_url)
                else:
                    print('conflicts resolved')
            else:
                ind = ind + 1
                stored_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
                # repeat the process for the next intent in the intent store
                if (ind < len(stored_intents_arr)):
                    print('starting new conflict resolution')
                    conflict_fun(ind, policy_dict, workflow_url, stored_intents_url,
                                 elasticsearch_url)
                else:
                    print('conflicts resolved')

        #if an existing intent doesn't conflict with new intent then move to the next intent in the intent store
        else:
            ind = ind + 1
            stored_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
            # repeat the process for the next intent in the intent store
            if (ind < len(stored_intents_arr)):
                print('starting new conflict resolution')
                conflict_fun(ind, policy_dict, workflow_url, stored_intents_url,
                             elasticsearch_url)
            else:
                print('ok')


