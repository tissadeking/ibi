import yaml
from elasticsearch import Elasticsearch

files_directory = '/code/app/'
yml_file = files_directory + 'config.yml'
with open(yml_file) as f:
    parameters = yaml.safe_load(f)
host = parameters['ip']
port = parameters['port']
elastic_host = parameters['elasticsearch_ip']
elastic_port = parameters['elasticsearch_port']
elasticsearch_url = "http://" + elastic_host + ":" + elastic_port
es = Elasticsearch(elasticsearch_url)

whatif_receive_url = "http://" + host + ":" + port + parameters['to_receive_whatif']
whatif_send_url = parameters['san_api_url']
workflow_url = parameters['rtr_api_url']
intents_url = parameters['intents_url']
alerts_url = parameters['alerts_url']
stored_intents_url = parameters['stored_intents_url']
qos_intents_url = parameters['qos_intents_url']
stored_qos_intents_url = parameters['stored_qos_intents_url']
rtr_username = parameters['rtr_username']
rtr_password = parameters['rtr_password']
rtr_email = parameters['rtr_email']
to_connect_to_rtr = parameters['to_connect_to_rtr']

groq_api_key = parameters['groq_api_key']

templates_directory = files_directory + parameters['templates_directory']
static_directory = files_directory + parameters['static_directory']
policy_store_directory = files_directory + parameters['policy_store_file']
q_table_directory = files_directory + parameters['q_table_file']
q_labels_directory = files_directory + parameters['q_labels_file']

ddos_ntp = parameters['ddos_ntp']
ddos_dns = parameters['ddos_dns']
ddos_pfcp = parameters['ddos_pfcp']

rate_req = parameters['req/s']
qos_requirements = parameters['qos_requirements']

hosts = parameters['hosts']
links = parameters['links']

