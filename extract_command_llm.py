#import dotenv
import json
from llama_index.llms.groq import Groq
import requests
import config
import os

#groq_api_key = os.getenv("GROQ_API_KEY")

# the various APIs to be connected to
intents_url = config.intents_url
stored_intents_url = config.stored_intents_url
qos_intents_url = config.qos_intents_url
stored_qos_intents_url = config.stored_qos_intents_url

#intent translation using LLM
def extract_command_fun(command):
    #dotenv.load_dotenv(dotenv.find_dotenv())
    #groq_api_key = "PUT YOUR OWN GROQ API KEY"
    groq_api_key = config.groq_api_key
    print("use your groq api key or request one from TUBS HORSE team")
    llama3 = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)

    examples = """Respond only with valid JSON. Do not write an introduction or summary.
    Here is an example input:
    Please, delete the intent with id TYS812B.
    Here is an example output:
    {"command": "delete_intent", "intent_id": "TYS812B"} 
    ###
    Here is an example input:
    I want to discontinue one qos intent running in the network. I think the id is 76SHBHHH.
    Here is an example output:
    {"command": "delete_intent", "qos_intent_id": "76SHBHHH", "qos": "qos"} 
    ###
    Here is an example input:
    Can you check and remove the security intent 6HSHJ0S?
    Here is an example output:
    {"command": "delete_intent", "intent_id": "6HSHJ0S"}  
    ###
    Here is an example input:
    Uninstall one QOS intent whose id 05FHSY73.
    Here is an example output:
    {"command": "delete_intent", "qos_intent_id": "05FHSY73", "qos": "qos"}  
    ###
    Here is an example input:
    Stop the quality-of-service intent whose id is POTE562.
    Here is an example output:
    {"command": "delete_intent", "qos_intent_id": "POTE562", "qos": "qos"}
    ###
    Here is an example input:
    A threat is happening on hosts dns-c1 and dns-c3. 
    The attack is ddos ntp, can you do something pls?
    Here is an example output:
    {"command": "add_intent", "intent_type": "mitigation", "threat": "ddos_ntp", 
    'host': ['dns-c1', 'dns-c3'], 'duration': ''}  
    ###
    Here is an example input:
    upf has just been attacked, and the attack is ddos_dns attack.
    Please, handle this for the next 3000 seconds to stop the attack.
    Here is an example output:
    {"command": "add_intent", "intent_type": "mitigation", "threat": "ddos_dns", 
    "host": ["upf"], "duration": "3000"} 
    ###
    Here is an example input:
    I want to install a security intent for mitigating network threats on five devices.
    The five devices are dns-c4, gnb, smf, dns-c2, and ceos1.
    The mitigation should last for 2 minutes. The threat is a dos signaling threat.
    Here is an example output:
    {"command": "add_intent", "intent_type": "mitigation", "threat": "dos_sig", 
    "host": ["dns-c4", "gnb", "smf", "dns-c2", "ceos1"], "duration": "120"}  
    ###
    Here is an example input:
    We just got an alert that a security threat is imminent, so we need to make sure it does not happen.
    The threat is api vulnerability. The concerned entities are dns-s and amf.
    Here is an example output:
    {"command": "add_intent", "intent_type": "prevention", "threat": "api_vul", 
    "host": ["dns-s", "amf"], "duration": ""}  
    ###
    Here is an example input:
    I suspect that a ddos pfcp network attack will happen soon at ceos2.
    Do something to avoid that. Don't exceed 3 minutes. 
    Here is an example output:
    {"command": "add_intent", "intent_type": "prevention", "threat": "ddos_pfcp", 
    "host": ["ceos2"], "duration": "180"}  
    ###
    Here is an example input:
    I want to deploy a dos signaling prevention security intent on these devices:
    upf, dns-s, and dns-c2.
    The action should last for 200 seconds.
    Here is an example output:
    {"command": "add_intent", "intent_type": "prevention", "threat": "dos_sig", 
    "host": ["upf", "dns-s", "dns-c2"], "duration": "200"}  
    ###
    Here is an example input:
    I want to deploy a ddos pfcp prevention security intent on these devices:
    upf, dns-s, and dns-c2.
    The action should last for 200 seconds.
    Here is an example output:
    {"command": "add_intent", "intent_type": "prevention", "threat": "ddos_pfcp", 
    "host": ["upf", "dns-s", "dns-c2"], "duration": "200"}  
    ###
    Here is an example input:
    I want to add some qos_pfcp intent for dns-c1 and dns-c2.
    The intent is that the reliability should remain above 0.99.
    Here is an example output:
    {"command": "add_qos_intent", "intent_type": "qos_pfcp", "name": "reliability", 
    "host": ["dns-c1", "dns-c2"], "value": "0.99", "unit": "1"}  
    ###
    Here is an example input:
    Please install a qos ntp intent for the device gnb.
    Make sure that the reliability is always more than 99.93%.
    Here is an example output:
    {"command": "add_qos_intent", "intent_type": "qos_ntp", "name": "reliability", 
    "host": ["gnb"], "value": "99.93", "unit": "%"}  
    ###
    Here is an example input:
    Can you ensure that the allocated bandwidth for every dns service on hosts amf, smf, and upf is never below 4000 kbps.
    Here is an example output:
    {"command": "add_qos_intent", "intent_type": "qos_dns", "name": "bandwidth", 
    "host": ["amf", "smf", "upf"], "value": "4000", "unit": "kbps"} 
    ###
    Here is an example input:
    All pfcp service communications to dns-s and ceos2 should be fast and happen within 2000 μs.
    Here is an example output:
    {"command": "add_qos_intent", "intent_type": "qos_pfcp", "name": "latency", 
    "host": ["dns-s", "ceos2"], "value": "2000", "unit": "μs"} 
    ###
    Here is an example input:
    The routers ceos2 and ceos1 are much needed now. 
    So the reliability of any ntp service to them must be over 0.979.
    Here is an example output:
    {"command": "add_qos_intent", "intent_type": "qos_ntp", "name": "reliability", 
    "host": ["ceos2", "ceos1"], "value": "0.979", "unit": "1"}  
    ###


    Here is the real input: """

    completing = """
    Now write the real output. Do not write an introduction or summary.
    Do not write any other thing aside the output in json:

    
    """
    #'{"category": ""}'
    all_text = examples + command + completing
    generation = llama3.complete(all_text)
    #print('generation:', generation)
    intent = json.loads(generation.text)
    # json_obj = json.loads(generation)
    # json_obj = generation.text
    #print('type intent: ', type(intent))
    print('intent: ', intent)
    if ((intent['command'] == 'delete_intent' and 'qos' in list(intent.keys())) or
        (intent['command'] == 'delete_qos_intent')):
        #to_delete = ''
        if 'qos_intent_id' in list(intent.keys()):
            to_delete = stored_qos_intents_url + '/' + intent['qos_intent_id']
            requests.delete(to_delete)
        elif 'intent_id' in list(intent.keys()):
            to_delete = stored_qos_intents_url + '/' + intent['intent_id']
            intent['qos_intent_id'] = intent['intent_id']
            requests.delete(to_delete)

        '''elif intent['command'] == 'delete_qos_intent' and 'qos' in list(intent.keys()):
            to_delete = stored_qos_intents_url + '/' + intent['qos_intent_id']
            requests.delete(to_delete)
            return intent'''
        intent['command'] = 'delete_intent'
        intent['qos'] = 'qos'
        return intent
    elif intent['command'] == 'delete_intent' and 'qos' not in list(intent.keys()):
        to_delete = stored_intents_url + '/' + intent['intent_id']
        requests.delete(to_delete)
        return intent
    elif intent['command'] == 'add_intent':
        if intent['duration'] == '':
            intent['duration'] = 3600
        else:
            intent['duration'] = int(intent['duration'])
        if intent['intent_type'] != 'mitigation' and intent['intent_type'] != 'prevention':
            error_output = 'invalid intent_type' + intent['intent_type']
            return error_output
        if (intent['threat'] != 'ddos_ntp' and intent['threat'] != 'ddos_dns' and intent['threat'] != 'ddos_pfcp'
                and intent['threat'] != 'dos_sig' and intent['threat'] != 'api_vul'):
            error_output = 'invalid threat' + intent['threat']
            return error_output
        requests.put(intents_url, json=intent)
        return intent
    elif intent['command'] == 'add_qos_intent':
        if (intent['intent_type'] != 'qos_ntp' and intent['intent_type'] != 'qos_dns'
            and intent['intent_type'] != 'qos_pfcp'):
            error_output = 'invalid service_type' + intent['intent_type']
            return error_output
        if (intent['name'] != 'reliability' and intent['name'] != 'bandwidth'
                and intent['name'] != 'latency'):
            error_output = 'invalid qos name' + intent['name']
            return error_output
        intent['unit'] = str(intent['unit'])
        intent['value'] = float(intent['value'])
        del intent['command']
        #print('intent before put: ', intent)
        requests.put(qos_intents_url, json=intent)
        intent['command'] = 'add_qos_intent'
        intent['service_type'] = intent['intent_type']
        del intent['intent_type']
        #print(intent)
        return intent
    # if json_obj['type'] == 'harmonise':
    #    data_harmonise_fun(json_obj['file'])
    # print('intent accepted')
    # print(type(json_obj))
    else:
        return 'invalid input'










