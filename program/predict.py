from keras.models import Sequential
from keras.models import Sequential  
from keras.callbacks import ProgbarLogger, TensorBoard
from keras.layers.core import Dense, Dropout, Activation 
from keras.models import model_from_json 
from keras.optimizers import SGD
from transition import Transition
from getDependencyTree import *
from read_file import *
from get_vec import *
from read_case import *

model = model_from_json(open('NN3Layers_ada.json').read())
model.load_weights('NN3Layers_ada_weights.h5')
model.compile(loss='categorical_crossentropy', optimizer = 'adagrad', metrics = ['accuracy'])
#test on the dev file:
#del trn_input, trn_target, test_input, test_target

dev_file_name = '../data/dev.ec'
dev_result_name = '../data/dev_result.ec'
sentences = getTree(dev_file_name)
word_vec = get_word_vec()
pos_vec, label_index = get_pos_label_vec()
f_result = codecs.open(dev_result_name, 'w', 'utf-8')

for i in range(0, len(sentences)):
	sentence = sentences[i]
	words = sentence['words']
	poses = sentence['poses']
	indexs = sentence['indexs']
	arc_labels = sentence['arc_labels']
	for i in range(len(indexs)):
		indexs[i] = -2
		arc_labels[i] = 'None\n'
	trans = Transition(sentence)
	while not trans.finish():
		arc_index = 0	# everytime we should find an arc index
		# get test_vec
		input_array = []
		if len(trans.stack) == 0:
			trans.shift()
			continue
		'''
		if len(trans.stack) == 0:
			wrd_v = word_vec['unk']
			pos_v = pos_vec['unk']
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
			wrd_v = word_vec['unk']
			pos_v = pos_vec['unk']
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
		else:
		'''
		if len(trans.stack) == 1:
			if trans.stack[0] == -1:
				wrd_v = word_vec['ROOT']
				pos_v = pos_vec['ROOT']
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			else:
				wrd_v = word_vec[words[trans.stack[-1]]]
				pos_v = pos_vec[poses[trans.stack[-1]]]
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			wrd_v = word_vec['unk']
			pos_v = pos_vec['unk']
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
		else:
			wrd_v = word_vec[words[trans.stack[-1]]]
			pos_v = pos_vec[poses[trans.stack[-1]]]
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
			if trans.stack[-2] == -1:
				wrd_v = word_vec['ROOT']
				pos_v = pos_vec['ROOT']
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			else:
				wrd_v = word_vec[words[trans.stack[-2]]]
				pos_v = pos_vec[poses[trans.stack[-2]]]
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
		'''
		if len(trans.buffer) == 0:
			wrd_v = word_vec['unk']
			pos_v = pos_vec['unk']
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
			wrd_v = word_vec['unk']
			pos_v = pos_vec['unk']
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
		else:
		'''
		if len(trans.buffer) == 1:
			if trans.buffer[0] == -1:
				wrd_v = word_vec['ROOT']
				pos_v = pos_vec['ROOT']
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			else:
				wrd_v = word_vec[words[trans.buffer[0]]]
				pos_v = pos_vec[poses[trans.buffer[0]]]
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			wrd_v = word_vec['unk']
			pos_v = pos_vec['unk']
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
		else:
			if trans.buffer[0] == -1:
				wrd_v = word_vec['ROOT']
				pos_v = pos_vec['ROOT']
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			else:
				wrd_v = word_vec[words[trans.buffer[0]]]
				pos_v = pos_vec[poses[trans.buffer[0]]]
				together = np.hstack((wrd_v, pos_v))
				input_array = np.hstack((input_array, together))
			wrd_v = word_vec[words[trans.buffer[1]]]
			pos_v = pos_vec[poses[trans.buffer[1]]]
			together = np.hstack((wrd_v, pos_v))
			input_array = np.hstack((input_array, together))
		input_vec = np.array(input_array).reshape(1, 4 * 139)
		#print input_vec.shape
		arc_label = model.predict(input_vec)
		#print arc_label
		arc_label = np.argmax(arc_label)
		if arc_label == 0:
			trans.shift()
			continue
		for k in label_index:
			if label_index[k] == arc_label:
				arc_label = k
				break
		arc_label = arc_label.split('_')
		if arc_label[0] == 'L':
			trans.left_arc(arc_label[1])
		else: trans.right_arc(arc_label[1])
	for arc_label in trans.arc:
		indexs[arc_label[1]] = arc_label[0]
		arc_labels[arc_label[1]] = arc_label[2]
	for i in range(len(words)):
		f_result.write(words[i] + '\t' + poses[i] + '\t' + str(indexs[i]) + '\t' + arc_labels[i])
	f_result.write('\n')

f_result.close()	

'''
for epoch in range(100):
	for i in range(trn_num):
		print i
		model.train(trn_input[i], trn_target[i])
	cnt = 0
	for i in range(test_num):
		output = model.predict(test_input[i])
		if output == target:
			cnt += 1
	print 'epoch = ' + str(epoch) + ', test correctness:'
	print '===>   ',
	print float(cnt) / test_num
'''

