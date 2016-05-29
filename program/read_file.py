# -*- coding: utf-8 -*-
"""
Created on Sat May 21 19:46:47 2016

@author: steve
"""

import numpy as np
import codecs

def read_data(file_name):
    wrd_voc = dict()
    pos_voc = dict()
    depen_voc = dict()
    wrd_list = []
    depen_list = []
#    wrd_list = []
    pos_list = []
    trn_set = file_name
    f = codecs.open(trn_set, 'r', 'utf-8')

    depen_id = 0
    wrd_id = 0
    pos_id = 0
    cnt_line = 0
    while True:
        entry = f.readline()
        if not entry:
            break
        if entry == '\n':
            cnt_line += 1
            continue
        entry = entry.split('\t')
        wrd = entry[0]
        pos = entry[1]
        depen = entry[3]
        if wrd in wrd_voc:
            wrd_voc[wrd][1] += 1
        else:
            wrd_voc[wrd] = [wrd_id, 1]
            wrd_id += 1
            wrd_list.append(wrd)
        if pos in pos_voc:
            pos_voc[pos][1] += 1
        else:
            pos_voc[pos] = [pos_id, 1]
            pos_id += 1
            pos_list.append(pos)
        if depen in depen_voc:
            depen_voc[depen][1] += 1
        else:
            depen_voc[depen] = [depen_id, 1]
            depen_id += 1
            depen_list.append(depen)
    print cnt_line
    f.close()
    return wrd_voc, wrd_list, pos_voc, pos_list, depen_voc, depen_list

#len(pos_voc) = 36
#len(depen_voc)) = 35
wrd_voc, wrd_list, pos_voc, pos_list, depen_voc, depen_list = read_data('../data/trn.ec')
print len(wrd_list)
            