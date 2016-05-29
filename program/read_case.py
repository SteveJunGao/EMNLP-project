from get_vec import *
import numpy as np
import codecs

def read_case(file_name):
	word_vec = get_word_vec()
	pos_vec, label_index = get_pos_label_vec()
	f = codecs.open(file_name, 'r', 'utf-8')
	target = []
	cnt_num = 0
	input_vec = []
	while True:
	#for i in range(10000):
		arc_label = f.readline()
		if not arc_label:
			break
		# get the target
		arc = label_index[arc_label]
		target.append(arc)
		# get the input
		input_array = np.zeros(0)
		words = f.readline().split(' ')
		for i in range(4):
			word = words[i * 2]
			pos = words[i * 2 + 1]
			word = word_vec[word]
			pos = pos_vec[pos]
			together = np.hstack((word, pos))
			input_array = np.hstack((input_array, together))
		input_vec.append(input_array)
		cnt_num += 1
	input_vec = np.array(input_vec)
	target = np.array(target)
	return input_vec, target, cnt_num


