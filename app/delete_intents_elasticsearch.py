import time
from elasticsearch import Elasticsearch, exceptions

#function for deleting intents on elasticsearch
def delete_intents_elasticsearch_fun(elasticsearch_url, id_to_delete, index):
    es = Elasticsearch(elasticsearch_url)
    #try:
    #    es.delete(index=index,  id=id_to_delete)
    #except exceptions.NotFoundError:
    #    pass
    intent_index = es.exists(index=index, id=id_to_delete)
    if intent_index == True:
        es.delete(index=index, id=id_to_delete)
    time.sleep(1)
    resp = es.search(index=index, size=100, query={"match_all": {}})
    id_arr = []
    source_arr = []
    for hit in resp['hits']['hits']:
        source_arr.append(hit["_source"])
        id_arr.append(hit["_id"])
    new_source_arr = []
    id_change = 0
    for source, id in zip(source_arr, id_arr):
        new_doc = source
        if index != 'awaiting_intents':
            new_doc['id'] = id_change + 1
        id_change += 1
        new_source_arr.append(new_doc)
        es.update(index=index, id=id, doc=new_doc)
    time.sleep(1)
    resp = es.search(index=index, size=100, query={"match_all": {}})

    for hit in resp['hits']['hits']:
        es.delete(index=index, id=hit["_id"])

    for i in range(len(new_source_arr)):
        es.index(index=index, id=str(i+1), document=new_source_arr[i])


#function for deleting qos intents on elasticsearch
def delete_intents_elasticsearch_fun_qos(elasticsearch_url, id_to_delete, index):
    es = Elasticsearch(elasticsearch_url)
    es.delete(index=index, id=id_to_delete)
    time.sleep(1)
    resp = es.search(index=index, size=100, query={"match_all": {}})
    id_arr = []
    source_arr = []
    for hit in resp['hits']['hits']:
        source_arr.append(hit["_source"])
        id_arr.append(hit["_id"])
    new_source_arr = []
    id_change = 0
    for source, id in zip(source_arr, id_arr):
        new_doc = source
        if index != 'awaiting_intents':
            new_doc['id'] = id_change + 1
        id_change += 1
        new_source_arr.append(new_doc)
        es.update(index=index, id=id, doc=new_doc)
    time.sleep(1)
    resp = es.search(index=index, size=100, query={"match_all": {}})

    for hit in resp['hits']['hits']:
        es.delete(index=index, id=hit["_id"])

    for i in range(len(new_source_arr)):
        es.index(index=index, id=str(i+1), document=new_source_arr[i])