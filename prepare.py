import string
import chardet

num_of_questions = 2194
q_folder = 'QDATA'
tf_idf_folder = 'TF-IDF'
vocab = {}
documents = []
accepted = list(string.ascii_lowercase)
accepted.append('-')
accepted.append('(')
accepted.append(')')

def find_encoding(file):
    r_file = open(file, 'rb').read()
    res = chardet.detect(r_file)
    charenc = res['encoding']
    return charenc

def openfile(filename):
    with open(filename,'r',encoding=find_encoding(filename),errors="ignore") as f:
        lines = f.readlines()
    return lines

#Process title and problem statement text separately
#Title contains index number which is irrelevant so we strip after skipping the 1st word(which is the index) of the string 
#Problem Statement has been stripped normally from the 0th index
def process(text,ch):
    if ch == 0:
        terms = [term.lower() for term in text.strip().split()[1:]]
    else:
        terms = [term.lower() for term in text.strip().split()[0:]]
    return terms

#Process problem statement text(extract only the main statement and trim the sample test cases and constraints)
def process_ps(lines):
    txt = ""
    for line in lines:
        if 'Example 1' in line:
            break
        txt += line
    return txt

#process document lines to exclude everything apart from elements of accepted characters('a-z','-','(',')')
def process_vocab(lines,case):
    for line in lines:
        elem = process(line,case)
        documents.append(elem)
        elem = set(elem)
        for el in elem:
            valid = True
            for chars in el:
                if chars not in accepted:
                    valid = False
                    break
            if valid is False:
                continue
            if el not in vocab:
                vocab[el] = 1
            else:
                vocab[el] += 1

process_vocab(openfile(str(q_folder) + '/index.txt'),0)
lines = []
for ind in range (1,num_of_questions+1):
    lines.append(process_ps(openfile(str(q_folder) + '/' + str(ind) + '/' + str(ind) + '.txt')))

process_vocab(lines,1)

# print(len(vocab))
# print(len(documents))

#Sort vocab in decreasing order of frequency of terms
vocab = dict(sorted(vocab.items(), key = lambda item: item[1], reverse=True))

#Save vocab in text file
with open(str(tf_idf_folder) + '/vocab.txt','w',encoding=find_encoding(str(tf_idf_folder) + '/vocab.txt'),errors="ignore") as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

#Save idf-values in text file
with open(str(tf_idf_folder) + '/idf-values.txt','w',encoding=find_encoding(str(tf_idf_folder) + '/idf-values.txt'),errors="ignore") as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

#Save documents in text file
with open(str(tf_idf_folder) + '/documents.txt','w',encoding=find_encoding(str(tf_idf_folder) + '/documents.txt'),errors="ignore") as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))

#Calculating inverted index to store list of documents any vocab term is present in
inverted_index = {}
for index,doc in enumerate(documents):
    for token in doc:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

#Save inverted index in text file
with open(str(tf_idf_folder) + '/inverted-index.txt','w',encoding=find_encoding(str(tf_idf_folder) + '/inverted-index.txt'),errors="ignore") as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))