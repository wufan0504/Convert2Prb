# This script generates approximately the probe file necessary for running Klusta. For more accurate results, please check the connectivity graph
# and make modifications according to specific probe design

# Fan Wu 03/23/2021

import json
import numpy as np

fname = 'int64-1dbc.json'
with open(fname) as f:
    data = json.load(f)

all_channels = data['channel']
total_nb_channels = len(all_channels)

channel_groups = {}
# Can find out how many groups there are by counting the frequency of occurance of data['y'][0], because 
# if there are multiple groups, the next group's first channel's y-coordinate will be the same as the first group's first channel's y-coordinate
# DBC probes also do not have any design where there are more than one site with the same y-coordinate from the same group, except for int64-12
if fname == 'int64-12dbc.json':
    num_groups = 1
else:
    num_groups = data['y'].count(data['y'][0])

for i in range(num_groups):
    sub_channels = []
    graph = []
    geometry = {}
    col_tracker = []
    for j in range(int(total_nb_channels/num_groups)):
        index = int(j + i*total_nb_channels/num_groups)
        sub_channels.append(all_channels[index])
        geometry[all_channels[index]] = (data['x'][index], data['y'][index])
        if data['x'][index] not in col_tracker:
            col_tracker.append(data['x'][index])
    # check to see if there is more than one column of sites
    if len(col_tracker) > 1: 
        for k in range(len(sub_channels)-1):
            if k == len(sub_channels)-2:
                graph.append((sub_channels[k], sub_channels[k+1]))
            else:
                graph.append((sub_channels[k], sub_channels[k+1]))
                graph.append((sub_channels[k], sub_channels[k+2]))
    else:
        for k in range(len(sub_channels)-1):
            graph.append((sub_channels[k], sub_channels[k+1]))

    channel_groups[i] = {'channels' : sub_channels, 'graph' : graph, 'geometry' : geometry}

probe_file = {'total_nb_channels' : total_nb_channels, 'channel_groups' : channel_groups}

with open('int64-1dbc.prb', 'w') as json_file:
    json.dump(probe_file, json_file, indent = 4)

