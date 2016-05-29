# -*- coding: utf-8 -*-
"""
Created on Sat May 21 20:05:15 2016

@author: steve
"""

import numpy as np
import codecs

def transfer_data(file_name):
    
    #origin_trn_set = '../data/trn.ec'
    #new_trn_set = '../data/trn_sentence.ec'
    origin_trn_set = file_name
    new_trn_set = file_name + '_sentences'
    f = codecs.open(origin_trn_set, 'r', 'utf-8')
    f_new = codecs.open(new_trn_set, 'w', 'utf-8')
    cnt_line = 0
    while True:
        entry = f.readline()
        if not entry:
            break
        if entry == '\n':
            f_new.write(entry)
            cnt_line += 1
            continue
        entry_tmp = entry.split('\t')
        f_new.write(entry_tmp[0] + ' ')
    f.close()
    f_new.close()
transfer_data('../data/trn.ec')
transfer_data('../data/dev.ec')
transfer_data('../data/tst.ec')