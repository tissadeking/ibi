# Intent-Based Networking Interface

The IBI is a software prototype developed within the scope of a project. The main goal of the module is to match intents that 
represent the desired state of the system or network and apply policies to 
achieve those states or, in other words, to fulfill the intents. Currently, the 
IBI can receive intents encoded as JSON files through a RESTful API or put in natural language through a 
graphical user interface (GUI). It receives security intents that could be 
mitigation or prevention intents regarding threats affecting the network. Within 
the IBI, the intents are processed and matched with the policies that are sent 
to another module within the project. This other module needs to be up and running for the IBI to function.
The IBI also has an ML Recommender based on Reinforcement Learning that recommends policies based on their previous performances.
The network topology and other important details are contained in the config.yml file.


## Installation

- Download the application code:
    ```
    git clone https://github.com/tissadeking/ibi.git
    ```
- Change the current directory to ibi.
    ```
    cd ibi

- Build and run the software as Docker container:
    ```
    sudo docker build -t ibi .
    sudo docker run --network host ibi
    ```
## Accessing the service
- The API is available at http://172.21.0.1, on port 7777.
- The ElasticSearch Instance is exposted at port 9200, also at http://172.21.0.1.
- The IP at which the software and ElasticSearch run can be changed in the config.yml file.
- The entire API endpoints to access stored intents, etc are contained in the config.yml file.
