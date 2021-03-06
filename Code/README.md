Computing Document Similarity Using Lexical Chains

This code assumes that python2 is installed on the system with nltk and it's necessary libraries.
This code can process documents which are completely in unicode (UTF-8). Otherwise it may throw an error accordingly.

df_words.py computes the document frequency for each noun in the corpus. 
It assumes the the list of paths of documents is in the file DocumentList.txt 
df_words.py saves the doument frequencies in the form of a pickle file 'dfreq_nouns.pckl'

Preprocess.py processes the given document and saves it's Lexical Chains in the Folder Chains in the form of a pickle file.
It assumes the the list of paths of documents is in the file DocumentList.txt and the document frequencies for each word are saved in 'dfreq_nouns.pckl'. 

Preprocess.py takes 5 arguments:
1) Document file path (relative to itself)
2) threshold 1: path similarity threshold for Strong Relation (Default value 1)
3) threshold 2: Count threshold for Strong Relation (Default value 1)
4) threshold 3: path similarity threshold for Weak Relation (Default value 0.2)
5) threshold 4: Count threshold for Weak Relation (Default value 2)

One can run Preprocess.py by running in the Terminal:     python2 PreProcess.py file_path 1 1 0. 2

Thus, Preprocess.py saves the Lexical Chains of the given Document in the Chains Folder in the form of a pickle file.

similarity.py computes the similarity between 2 documents. It assumes that  the documents have been preprocessed 
and the pickle file containing their lexical chains. 

similarity.py takes 2 arguments:
1) File path for the pickle file of first document
2) File path for the pickle file of second document

One can run similarity.py by running in the Terminal:     python2 similarity.py file_path1 file_path2

This returns the Vector space model similarity and lexical Chain model similarity.

To sample test the the model we have kept some documents in the '/documents' folder and also added their paths to DocumentList.txt file.

Now, to sample test this code one needs to do the following steps:

1) Run df_words.py to compute document frequencies. : python2 df_words.py
2) Run Preprocess.py to compute and save the lexical chains for the documents for which the similarity is to be computed.
example: python2 PreProcess.py documents/moviestar 1 1 0. 2
3) Run similarity.py for similarity between the two documents:
example python2 similarity.py Chains/moviestar_dl.pckl Chains/skystar_dl.pckl
