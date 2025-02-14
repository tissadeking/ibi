from elasticsearch import Elasticsearch
import whatif_loop
import warnings
import config
import get_intents_script
import time
import requests
import ml_recommender

warnings.filterwarnings('ignore')


elasticsearch_url = config.elasticsearch_url
es = Elasticsearch(elasticsearch_url)
whatif_send_url = config.whatif_send_url
stored_intents_url = config.stored_intents_url

def run_whatif_loop_fun():
    whatif_loop.whatif_loop_fun(es, whatif_send_url)

def run_duration_check_loop():
    duration_check_2()

#check when duration of intent has elapsed
def duration_check_2():
    while True:
        intent_index = es.exists(index="stored_intents", id=1)
        if intent_index == True:
            resp1 = es.search(index="stored_intents", size=100, query={"match_all": {}})
            id_arr = []
            source_arr = []
            for hit in resp1['hits']['hits']:
                id_arr.append(hit["_id"])
                source_arr.append(hit["_source"])
            for source, id in zip(source_arr, id_arr):
                duration = 0
                if source['duration'] != '':
                    duration = int(source['duration'])
                time_elapsed = source['actual_time'] + duration
                #time_elapsed = source['actual_time'] + int(source['duration'])
                n = 0
                if time_elapsed <= time.time():
                    if n == 0:
                        # alert ML recommender
                        reco_dict = source
                        reco_dict['status'] = 'success'
                        print('success')
                        ml_recommender.call_recommender(reco_dict)
                        print('n: ', n)

                        # delete intent
                        url_to_delete = stored_intents_url + "/" + str(source['intent_id'])
                        requests.delete(url_to_delete)
                        n += 1
                time.sleep(0.5)
        time.sleep(0.5)

#check when duration for intent has elapsed
def duration_check():
    #time.sleep(2)
    while True:
        intent_index = es.exists(index="stored_intents", id=1)
        if intent_index == True:
            stored_intents_arr = get_intents_script.get_intent_fun(stored_intents_url)
            if len(stored_intents_arr) > 0:
                for i in range(len(stored_intents_arr)):
                    duration = 0
                    if stored_intents_arr[i]['duration'] != '':
                        duration = int(stored_intents_arr[i]['duration'])

                    time_elapsed = stored_intents_arr[i]['actual_time'] + duration
                    n = 0
                    if time_elapsed <= time.time():
                        if n == 0:
                            #alert ML recommender
                            reco_dict = stored_intents_arr[i]
                            reco_dict['status'] = 'success'
                            ml_recommender.call_recommender(reco_dict)
                            n += 1
                        #delete intent
                        url_to_delete = stored_intents_url + "/" + str(stored_intents_arr[i]['intent_id'])
                        requests.delete(url_to_delete)
                    time.sleep(0.5)
        time.sleep(0.5)