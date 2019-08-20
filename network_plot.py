import networkx as nx
import matplotlib.pyplot as plt
import queue
import tweet_fnts as tf
import random
import time
import json

def graph_network(arr,usNam, G):
    
    G.add_node(usNam)
    
    for i in arr:
        G.add_node(i)
        G.add_edge(usNam,i)

    return G
    # nx.draw(G, with_labels = True)
    # plt.show()


# reads user information pre accumilated from the users.json file
# used only after information is gathered from user_data_accum.py
def graph_extended_network(arr,usNam, api):
    colors = []
    G = nx.Graph()
    
    users = []
    with open('users.json', 'r') as f:
        users = [json.loads(line) for line in f]
        
    # for i in users:
    #     q.put(i)
    
    colors.append(['red'] * len(users))

    # for i in arr:
    #    colors.append([random_color()] * len(tf.get_followers(i,api)))
        
      
    # while(not q.empty()):
    #     G.add_node(usNam)
    #     G = graph_network(tf.get_followers(usNam,api) ,usNam)
    #     usNam = q.get()
    #     for i in tf.get_followers(usNam,api):
    #         q.put(i)
    
    
    for i in users:
        G = graph_network(i['Following'],i['name'] , G)

    #Change distance between nodes
    pos=nx.spring_layout(G,k=2)

    plt.figure(figsize=(50,20),dpi=100)

    nx.draw(G, with_labels = True, pos=pos)

    plt.savefig("userNetworks/" + usNam + "_network.png")
    plt.savefig("userNetworks/" + usNam + "_network.pdf")

    plt.show()
 


def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

