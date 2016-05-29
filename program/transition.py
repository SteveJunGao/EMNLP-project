class Transition():
	def __init__(self, sentence):
		self.stack = [-1]
		self.buffer = list(range(0, len(sentence['words'])))
		self.arc = []# means head tail relation
		self.tokens = len(sentence['words'])
	def finish(self):
		if len(self.buffer) == 0:
			return True
		return False
	def left_arc(self, relation):
		index_i = self.stack.pop()
		index_j = self.buffer[0]
		self.arc.append((index_j, index_i, relation))
	def shift(self):
		index_i = self.buffer.pop(0)
		self.stack.append(index_i)
	def right_arc(self, relation):
		index_i = self.stack.pop()
		index_j = self.buffer[0]
		self.buffer[0] = index_i
		self.arc.append((index_i, index_j, relation))
