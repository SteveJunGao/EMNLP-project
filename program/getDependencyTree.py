import numpy as np
import codecs

def getTree(file_name):
	fileNm = file_name
	f = codecs.open(fileNm, 'r', 'utf-8')
	sentences = []
	words = []
	indexs = []
	poses = []
	arc_labels = []
	while(True):
		line = f.readline()
		if not line:
			break
		if line == '\n':
			structure = getStructure(words, poses, indexs, arc_labels)
			words = []
			indexs = []
			poses = []
			arc_labels = []
			sentences.append(structure)
			continue
		line_ele = line.split('\t')
		words.append(line_ele[0])
		poses.append(line_ele[1])
		indexs.append(int(line_ele[2]))
		arc_labels.append(line_ele[3])
	f.close()
	return sentences

def getStructure(words, poses, indexs, arc_labels):
	structure = dict()
	structure['words'] = words
	structure['poses'] = poses
	structure['indexs'] = indexs
	structure['arc_labels'] = arc_labels
	return structure

#sentences = getTree()

