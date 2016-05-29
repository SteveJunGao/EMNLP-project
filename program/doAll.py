#from neural_networks import My_NN_Model
from keras.models import Sequential
from keras.models import Sequential  
from keras.callbacks import ProgbarLogger, TensorBoard
from keras.layers.core import Dense, Dropout, Activation
from keras.regularizers import l2, activity_l2 
from keras.models import model_from_json 
from keras.optimizers import SGD
from transition import Transition
from getDependencyTree import *
from read_file import *
from get_vec import *
from read_case import *
def transfer_target(target):
	n_targets = len(target)
	n_types = 47
	array = []
	for i in range(n_targets):
		t = []
		for j in range(n_types):
			t.append(0)
		t[target[i]] = 1
		array.append(t)
	return np.array(array)

#get the training and dev data
trn_file = '../data/trn.ec_case'
test_file = '../data/dev.ec_case'
trn_input, trn_target, trn_num = read_case(trn_file)
test_input, test_target, test_num = read_case(test_file)
trn_target = transfer_target(trn_target)
test_target = transfer_target(test_target)
#define the model
nWords = 4
dWords = 100
dpos = 39
model = Sequential()
#because I get a low accuracy at training time ,so I add a new layer 
model.add(Dense(200, input_dim = 4 * 139, init = 'uniform')) 
#model.add(Activation('tanh'))  
#model.add(Dense(200, W_regularizer=l2(1e-8), init = 'uniform')) 
model.add(Activation('relu'))  
model.add(Dense(47, init = 'uniform')) 
model.add(Activation('softmax')) 

#train the model
#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) # 
model.compile(loss='categorical_crossentropy', optimizer = 'adagrad', metrics = ['accuracy']) # 
print 'training start'
print trn_target.shape
for i in range(7):
	print 'training set:'
	model.fit(trn_input, trn_target, batch_size=32, nb_epoch=2, shuffle=True, verbose=1, sample_weight = None)  
	print 'test set'  
	score = model.evaluate(test_input, test_target, verbose=1)
	print score
	print model.metrics_names
#save the model
json_string = model.to_json()
open('NN3Layers_ada.json', 'w').write(json_string)
model.save_weights('NN3Layers_ada_weights.h5')

# elsewhere...
#model = model_from_json(open('my_model_architecture.json').read())
#model.load_weights('my_model_weights.h5')

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

