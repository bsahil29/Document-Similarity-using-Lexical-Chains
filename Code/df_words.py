import os
import nltk
f = open('DocumentList.txt','r')
f1 = f.readlines()
dfreq = {}
print('\n')
for line in f1:
	print(line)
	file1 = open(line.partition('\n')[0] ,'r')
	file1txt = (file1.read()).lower()
	is_noun = lambda x: True if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS') else False
	nouns = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(file1txt)) if is_noun(pos)]  #extract all nouns
	dictionary = {}
	for word in nouns:
		if word in dictionary.keys():
			dictionary[word]+=1
		else:
			dictionary[word]=1

	for word in dictionary.keys():
		if (word in dfreq.keys()):
			dfreq[word] += 1
		else:
			dfreq[word] = 1


import pickle
pkl = open('dfreq_nouns.pckl', 'wb')
pickle.dump(dfreq,pkl)
pkl.close()
print('Document Frequencies saved as Pickle File')