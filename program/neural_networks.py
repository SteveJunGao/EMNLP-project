# there are 35 different arc labels, thus |T| = 35 * 2 +1
# output size = 71
# hidden size = 100
# input size: d_words * n_words + d_pos * n_pos
# input words: 
#			leftmost/rightmost children of the top two words on the stack(not includes buffer)(4)
#					if no children inputs equals to 0
#			top 2 words on the stack and buffer(4)

# first version, don't use the pos embedding
import numpy as np 
import math
import random
import struct
import scipy

def cube(X):
	return X*X*X
def softmax(z):
    #max_z = np.max(z)
    #tmp_z = z - max_z
    z = np.exp(z)
    Z = np.sum(z)
    return z / Z
class My_NN_Model(object):

	def __init__(self):
		# define the parameters
		self.d_words = 100
		self.n_words = 4
		self.d_pos = 39
		self.n_pos = self.n_words
		self.n_input = self.d_words * self.n_words + self.d_pos * self.n_pos
		self.n_hidden = 200
		self.n_output = 47
		self.alpha = 0.000001
		#hidden weights
		self.W_hid = np.random.rand( self.n_hidden, self.n_input)
		self.W_hid -= 0.5
		#self.W_hid *= 0.1
		#hidden bias
		self.b_hid = np.random.rand( self.n_hidden, 1)#bias of hidden unit 
		self.b_hid -= 0.5
		#self.b_hid *= 0.1
		#output weights
		self.W_out = np.random.rand( self.n_output, self.n_hidden)
		self.W_out -= 0.5
		#self.W_out *= 0.1
		#output bias
		self.b_out = np.random.rand( self.n_output, 1)#bias of out unit
		self.b_out -= 0.5
		#self.b_out *= 0.1
		#layer values
		# I treat it as a colume vector
		print self.n_input
		print self.n_pos
		self.val_input = np.zeros([self.n_input, 1])
		self.val_hid = np.zeros([self.n_hidden, 1])
		self.cube_val_hid = np.zeros([self.n_hidden, 1])
		self.val_out = np.zeros([self.n_output, 1])
		self.softmax_val_out = np.zeros([self.n_output, 1])
	def forwardPropogation(self, input_vec):
		input_vec = input_vec.reshape(self.n_input, 1)
		self.val_input = input_vec
		#print self.val_input.shape
		self.val_hid = np.dot(self.W_hid, input_vec)
		#print self.val_hid.shape
		#print self.b_hid.shape
		self.val_hid += self.b_hid
		#print self.val_hid.shape
		self.cube_val_hid = cube(self.val_hid)
		#print np.size(self.cube_val_hid)
		self.val_out = np.dot(self.W_out, self.cube_val_hid) + self.b_out
		self.softmax_val_out = softmax(self.val_out)
	def backwordPropogation(self, target):
		# I use the MSE as the cost function
		# thus J = np.sum((softmax_val_out - target)^2)
		#calc the gradient 
		dJ_dval_out = self.softmax_val_out
		tmp_out = self.softmax_val_out
		tmp_out[target] -= 1
		dJ_dval_out[target] -= 1.0
		#print dJ_dval_out.shape
		#print len(self.cube_val_hid)
		#print self.n_hidden
		self.cube_val_hid = self.cube_val_hid.reshape(1, self.n_hidden)
		dJ_dW_out = np.dot(dJ_dval_out, self.cube_val_hid)
		dJ_dB_out = dJ_dval_out

		dJ_dval_out = dJ_dval_out.transpose()# transfer to a column vector
		dJ_dcube_val_hid = np.dot(dJ_dval_out, self.W_out)
		#print np.size(dJ_dcube_val_hid)

		dJ_dcube_val_hid = dJ_dcube_val_hid.transpose()
		dcube_val_dval_hid = 3 * self.val_hid * self.val_hid
		dJ_dval_hid = dJ_dcube_val_hid * dcube_val_dval_hid
		
		#print np.size(dJ_dval_hid)
		self.val_input = self.val_input.transpose()
		dJ_dW_hid = np.dot(dJ_dval_hid, self.val_input)
		dJ_dB_hid = dJ_dval_hid
		self.W_out -= self.alpha * dJ_dW_out
		self.W_hid -= self.alpha * dJ_dW_hid
		self.b_out -= self.alpha * dJ_dB_out
		self.b_hid -= self.alpha * dJ_dB_hid

	def train(self, input_vec, target):
		self.forwardPropogation(input_vec)
		self.backwordPropogation(target)
	def predict(self, input_vec):
		self.forwardPropogation(input_vec)
		target = np.argmax(self.softmax_val_out)
		return target
