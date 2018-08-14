import nltk
import sys
from nltk.corpus import wordnet as wn

cutoff=2
lexical_chains = [] #empty list to hold all the chains
dictionary = {} #empty dictionart to hold the count of each word encountered

filename = sys.argv[-5]
thre1 = float(sys.argv[-4]) #threshold values for judging Chain Similarity
thre2 = float(sys.argv[-3])
thre3 = float(sys.argv[-2])
thre4 = float(sys.argv[-1])
print(filename)
File = open(filename)
lines = (File.read()).lower()


is_noun = lambda x: True if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS') else False
nouns = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(lines)) if is_noun(pos)]  #extract all nouns

# print('Computing count of each Word\n')
for word in nouns:
	if (word in dictionary.keys()):
		dictionary[word]+=1
	else:
		dictionary[word]=1

for word in dictionary.keys():
	if(dictionary[word] < cutoff):
		del dictionary[word]

class Chain(): 
	def __init__(self, words, senses, count, dfreq ):
		self.words = set(words)
		self.senses = set(senses)
		self.count = count
		self.dfreq = dfreq

	def addWord(self, word):
		self.words.add(word)

	def addSense(self, sense):
		self.senses.add(sense)

for word in dictionary.keys():
	lexical_chains.append(Chain([word], wn.synsets(word),dictionary[word],0))

print('Chains Before Merging\n')
for chain in lexical_chains:
	print chain.senses
print('\n')

def merge(chain1,chain2,cutoff1):
	
	if(chain1==chain2):
		return chain1

	chain3=Chain({},[],chain1.count+chain2.count,0)
	for word1 in chain1.words:
		chain3.addWord(word1)
	for word2 in chain2.words:
		chain3.addWord(word2)
	for sense1 in chain1.senses:
		for sense2 in chain2.senses:
			if(sense1.path_similarity(sense2)>=cutoff1 or sense2.path_similarity(sense1)>=cutoff1):
				chain3.addSense(sense1)
				chain3.addSense(sense2)
	return chain3           


def scan_chains(lexical_chains,cutoff1,cutoff2):
	flag=0
	
	for chain1 in lexical_chains:
		for chain2 in lexical_chains:
			
			count=0
			if(chain1==chain2):
				continue
			for sense1 in chain1.senses:
				for sense2 in chain2.senses:
					if (sense1.path_similarity(sense2)>=cutoff1 or sense2.path_similarity(sense1)>=cutoff1):
						count+=1

			# print count
			if(count>=cutoff2):
				flag=1
				chain3=merge(chain1,chain2,cutoff1)
				lexical_chains.remove(chain1)
				lexical_chains.remove(chain2)
				lexical_chains.append(chain3)
				return flag
	return flag

# print(9)
print('Merging Chains')
flag=1
while(1):
	if(flag==0):
		break
	flag=scan_chains(lexical_chains,thre1,thre2)

flag=1
while(1):
	if(flag==0):
		break
	flag=scan_chains(lexical_chains,thre3,thre4)

print('Chains after Merging')
for chain in lexical_chains:
	print chain.senses
print('\n')

# For computing Document Frequency of each chain
print('Computing Document Frequency of each chain')
def dfreq(arr):
	f = open('DocumentList.txt','r')
	f1 = f.readlines()
	cnt1 = 0
	for line in f1:
		file1 = open(line.partition('\n')[0],'r')
		file1txt = (file1.read()).lower()
		is_noun = lambda x: True if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS') else False
		brr = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(file1txt)) if is_noun(pos)]  #extract all nouns
		for wrd in arr:
			if (wrd in brr):
				cnt1 = cnt1 + 1
				break
	return cnt1	
print('\n')	

for chain in lexical_chains:
	# print chain.words
	chain.dfreq = dfreq(chain.words)
	# print chain.dfreq


print('Saving the Lexical Chains as a Pickle file')
w = []
sen = []
cnt = []
df  = []
for chin in lexical_chains:
	w.append(chin.words)
	ftr = []
	for ss in chin.senses:
		# saving the synsets as there offset ids and their POS tag
		ftr.append( str(ss.offset()).zfill(8) +'-' + ss.pos() ) 
	sen.append(set(ftr))
	cnt.append(chin.count)
	df.append(chin.dfreq)

import cPickle as pickle
# pkl = open(filename.partition('/')[2] + '_dl.pckl','wb')
pkl = open('Chains/' + filename.partition('/')[2] + '_dl.pckl','wb')
# pkl = open(filename + '_dl.pckl','wb')
pickle.dump(dictionary,pkl)
pickle.dump(w,pkl)
pickle.dump(sen,pkl,-1)
pickle.dump(cnt,pkl)
pickle.dump(df,pkl)
pkl.close()