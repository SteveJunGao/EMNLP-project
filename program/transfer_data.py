# -*- coding: utf-8 -*-
"""
Created on Sat May 21 20:05:15 2016

@author: steve
"""

import numpy as np
import codecs

def transfer_data():
    
    origin_trn_set = '../data/trn.ec'
    new_trn_set = '../data/trn_withoutec.ec'
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
        if entry_tmp[0][0] == '*':
            continue
        f_new.write(entry)
    f.close()
    f_new.close()
transfer_data()