import codecs
import numpy as np
def get_word_vec():
	file_name = '../data/all_sen.ec.vec'
	f = codecs.open(file_name, 'r', 'utf-8')
	data = f.readline().split(' ')
	nWords = int(data[0])
	nDimension = int(data[1])
	word_vec = dict()
	for i in range(nWords):
		line = f.readline().split(' ')
		word = line[0]
		vec = np.zeros(100)
		for j in range(nDimension):
			vec[j] = float(line[j + 1])
		word_vec[word] = vec
	f.close()
	return word_vec
def get_pos_label_vec():
	file_name = '../data/trn.ec_case'
	pos_id = 1
	num_pos = 39
	label_id = 0
	pos_vec = dict()
	label_index = dict()
	f = codecs.open(file_name, 'r', 'utf-8')
	while True:
		arc_label = f.readline()
		if not arc_label:
			break
		if arc_label not in label_index:
			label_index[arc_label] = label_id
			label_id += 1
		line = f.readline().split(' ')
		for i in range(0, 4):
			if line[i * 2 + 1] not in pos_vec:
				tmp_array = np.zeros(num_pos)
				tmp_array[pos_id] = 1
				pos_vec[line[i * 2 + 1]] = tmp_array;
				pos_id += 1
	print pos_id, label_id
	print label_index
	return pos_vec, label_index
#pos_vec, label_index = get_pos_label_vec()