import codecs
f_ori = '../data/dev.ec'
f_new = '../data/dev_result.ec'
cnt_index = 0
cnt_label = 0
cnt_all = 0
cnt = 0
cnt_none = 0
f_ori = codecs.open(f_ori, 'r', 'utf-8')
f_new = codecs.open(f_new, 'r', 'utf-8')
while True:
	line1 = f_ori.readline()
	line2 = f_new.readline()
	if not line1:
		break
	if line1 == '\n':
		continue
	line1 = line1.split('\t')
	line2 = line2.split('\t')
	cnt += 1
	if line2[3] == 'None\n':
		cnt_none += 1
	if line1[2] == line2[2]:
		cnt_index += 1
	if line1[3] == line2[3]:
		cnt_label += 1
	if line1[3] == line2[3] and line1[2] == line2[2]:
		cnt_all += 1
print float(cnt_label) / cnt
print float(cnt_index) / cnt
print float(cnt_all) / cnt
print float(cnt_none) / cnt
