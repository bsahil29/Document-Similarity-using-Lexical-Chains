import nltk
import sys
import math
from nltk.corpus import wordnet as wn

import pickle
f=open('dfreq_nouns.pckl','rb');  #loading Document frequency of each word
d_freq=pickle.load(f);
f.close()

lexical_chains  = []
lexical_chains1 = []

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

print('\n')
print('Loading Pickle file of each Document\n') 
# Loading the Pickle file for 1st Document
f1 = sys.argv[-2]
f = open(f1)
dictionary = pickle.load(f)
w = pickle.load(f)
sen = pickle.load(f)
sn = []
for zsx in sen:
	ftr = []
	for xdc in zsx:
		ftr.append(wn._synset_from_pos_and_offset(xdc.partition('-')[2], int(xdc.partition('-')[0])))
	ftr = set(ftr)
	sn.append(ftr)
cnt = pickle.load(f)
df = pickle.load(f)
for words,senses,count,dfreq in zip(w,sn,cnt,df):
	lexical_chains.append(Chain(words,senses,count,dfreq))

# Loading the Pickle file for 2nd Document
f2 = sys.argv[-1]
f = open(f2)
dictionary1 = pickle.load(f)
w = pickle.load(f)
sen = pickle.load(f)
sn = []
for zsx in sen:
	ftr = []
	for xdc in zsx:
		ftr.append(wn._synset_from_pos_and_offset(xdc.partition('-')[2], int(xdc.partition('-')[0])))
	ftr = set(ftr)
	sn.append(ftr)
cnt = pickle.load(f)
df = pickle.load(f)
for (words,senses,count,dfreq) in zip(w,sn,cnt,df):
	lexical_chains1.append(Chain(words,senses,count,dfreq))
	
# Denominator for Normalization for Vector Space model
denominator=0
for word in dictionary.keys():
    denominator+=(dictionary[word]*math.log(1+d_freq[word]))*(dictionary[word]*math.log(1+d_freq[word]))
denominator = math.sqrt(denominator)

# Updating the counts by Normalized Counts
for word in dictionary.keys():
    dictionary[word]=dictionary[word]*math.log(1+d_freq[word])/denominator

denominator1=0
for word in dictionary1.keys():
    denominator1+=(dictionary1[word]*math.log(1+d_freq[word]))*(dictionary1[word]*math.log(1+d_freq[word]))
denominator1 = math.sqrt(denominator1)

for word in dictionary1.keys():
    dictionary1[word]=dictionary1[word]*math.log(1+d_freq[word])/denominator1

# Computing Vector Space Similarity
vc_sim=0
for word in dictionary.keys():
    for word1 in dictionary1.keys():
        if(word == word1):
        	vc_sim = vc_sim +dictionary[word]*dictionary1[word]
           
# Computing Denominator for Normalization for Semantic Similarity
dn = 0
for chain in lexical_chains:
	if (len(chain.senses)!=0):
		dn+= (chain.count*math.log(1+chain.dfreq))*(chain.count*math.log(1+chain.dfreq))
dn = math.sqrt(dn)
for chain in lexical_chains:
	chain.count = chain.count*math.log(1+chain.dfreq)/dn

dn1 = 0
for chain1 in lexical_chains1:
	if (len(chain1.senses)!=0):
		dn1+= (chain1.count*math.log(1+chain1.dfreq))*(chain1.count*math.log(1+chain1.dfreq))
dn1 = math.sqrt(dn1)
for chain1 in lexical_chains1:
	chain1.count= chain1.count*math.log(1+chain1.dfreq)/dn1

# Computing Similarity for Semantic Similarity
sim_s=0
for chain in lexical_chains:
	for chain1 in lexical_chains1:
		flag = 0
		for sense in chain.senses:
				for sense1 in chain1.senses:
					if (sense == sense1):
						# print sense
						sim_s+= chain.count*chain1.count
						flag =1
					if(flag == 1):
						break
				if(flag == 1):
					break

print 'Vector Space Similarity = ' , vc_sim, 'Sematic Similarity = ', sim_s
