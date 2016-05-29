from neural_networks import My_NN_Model
from keras.models import Sequential
from keras.models import Sequential  
from keras.callbacks import ProgbarLogger, TensorBoard
from keras.layers.core import Dense, Dropout, Activation  
from keras.optimizers import SGD
from transition import Transition
from get_vec import *
from read_case import *
#get the training and dev data

def precit(model, input_vec, target, n):
	arc_label = np.zeros(47)
	target_label = np.zeros(47)
	cnt = 0
	for i in range(n):
		output = model.predict(input_vec[i])
		arc_label[output] += 1
		target_label[target[i]] += 1
		if output == target[i]:
			#if output != 0:
			#print output
			cnt += 1
	n_sum = np.sum(arc_label)
	arc_label /= n_sum
	n_sum = np.sum(target_label)
	target_label /= n_sum
	print arc_label
	print target_label
	print '===>   ',
	print float(cnt) / n

trn_file = '../data/trn.ec_case'
test_file = '../data/dev.ec_case'
trn_input, trn_target, trn_num = read_case(trn_file)
print trn_target
test_input, test_target, test_num = read_case(test_file)
#define the model
nWords = 4
dWords = 100
dpos = 39
model = My_NN_Model()	
for epoch in range(100):
	for i in range(trn_num):
		if i % 10000 == 0:
			model.alpha *= 0.93
			print i
		model.train(trn_input[i], trn_target[i])
	cnt = 0
	#model.alpha *= 0.1
	print 'epoch = ' + str(epoch) + ', training correctness:'
	precit(model, trn_input, trn_target, trn_num)
	print 'epoch = ' + str(epoch) + ', test correctness:'
	precit(model, test_input, test_target, test_num)


