from getDependencyTree import *
from read_file import *
from transition import Transition
import codecs
#pos of unk is unk, pos of root is root

#if we only need do the arc shift, arc_label is the shift;
def legal_right_arc(index_j, indexs, tmp_buffer):
	for i in range(0, len(tmp_buffer)):
		if indexs[tmp_buffer[i]] == index_j:
			return False
	return True

def save_case(f_case, words, poses, label, tmp_buffer, stack):
	f_case.write(label)
	# top 2 words at stack
	if len(stack) == 1:
		f_case.write('unk ')# words
		f_case.write('unk ')
		if stack[0] == -1:
			f_case.write('ROOT ')
			f_case.write('ROOT ')
		else:
			f_case.write(words[stack[0]] + ' ')
			f_case.write(poses[stack[0]] + ' ')
	else:
		f_case.write(words[stack[-1]] + ' ')
		f_case.write(poses[stack[-1]] + ' ')
		f_case.write(words[stack[-2]] + ' ')
		f_case.write(poses[stack[-2]] + ' ')
	# top 2 words at buffer:
	if len(tmp_buffer) == 1:
		f_case.write('unk ')# words
		f_case.write('unk ')
		if tmp_buffer[0] == -1:
			f_case.write('ROOT ')
			f_case.write('ROOT ')
		else:
			f_case.write(words[tmp_buffer[0]] + ' ')
			f_case.write(poses[tmp_buffer[0]] + ' ')
	else:
		f_case.write(words[tmp_buffer[0]] + ' ')
		f_case.write(poses[tmp_buffer[0]] + ' ')
		f_case.write(words[tmp_buffer[1]] + ' ')
		f_case.write(poses[tmp_buffer[1]] + ' ')

	f_case.write('\n')

def get_data(file_name):
	wrd_voc, wrd_list, pos_voc, pos_list, depen_voc, depen_list = read_data(file_name)
	sentences = getTree(file_name)

	#skip the empty catagories
	# input data:
	#		top 2 words at buffer & stack; leftmost and rightmost child of the top 2 words at stack
	#		wordIndex ===> wordVec, posIndex ==>posVec, arc_labels ==> arcLabels
	cnt_case = 1
	trn_case_name = file_name + '_case'
	#trn_label_name = '../data/trn_label'
	f_case = codecs.open(trn_case_name, 'w', 'utf-8')
	#f_label = codecs.open(trn_label_name, 'w', 'utf-8')


	for i in range(0, len(sentences)):
		sentence = sentences[i]
		words = sentence['words']
		poses = sentence['poses']
		indexs = sentence['indexs']
		arc_labels = sentence['arc_labels']
		trans = Transition(sentence)
		while not trans.finish():
			index_i = trans.stack[-1]
			index_j = trans.buffer[0]
			#print index_i
			if index_i == -1:
				if indexs[index_j] == index_i:
					if legal_right_arc(index_j, indexs, trans.buffer):
						save_case(f_case, words, poses, 'R_' + arc_labels[index_j], trans.buffer, trans.stack)
						trans.right_arc(arc_labels[index_j])
						#if len(trans.stack) != 0: print len(trans.stack)
						if len(trans.buffer) != 1: print len(trans.buffer)
						break# finish parsing
				else:
					save_case(f_case, words, poses, 'SHIFT\n', trans.buffer, trans.stack) 
					trans.shift()
					continue
			# we must confirm there are no any arc belong to the buffer header
			if indexs[index_j] == index_i:
				if legal_right_arc(index_j, indexs, trans.buffer):
					save_case(f_case, words, poses, 'R_' + arc_labels[index_j], trans.buffer, trans.stack)
					trans.right_arc(arc_labels[index_j])
				else:
					save_case(f_case, words, poses, 'SHIFT\n', trans.buffer, trans.stack) 
					trans.shift()
				continue
			# all the left arc is OK~
			if indexs[index_i] == index_j:
				save_case(f_case, words, poses, 'L_' + arc_labels[index_i], trans.buffer, trans.stack)
				trans.left_arc(arc_labels[index_i])
				continue
			save_case(f_case, words, poses, 'SHIFT\n', trans.buffer, trans.stack) 
			trans.shift()

	f_case.close()

get_data('../data/trn.ec')
get_data('../data/dev.ec')