import string
import chardet

num_of_questions_lc = 2194
num_of_questions_cf = 8636
cf_q_folder = 'CF_QDATA'
q_folder = 'QDATA'
tf_idf_folder = 'TF-IDF'
vocab = {}
vocab_cf = {}
documents = []
documents_cf = []
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

def process_cf_ps(lines):
    st = 0
    txt = ""
    for line in lines:
        if 'standard output' in line:
            st += 1
        if st == 1:
            st += 1
            continue
        if st == 2 and 'Input' not in line:
            txt += line
        if 'Input' in line:
            break
    print(txt)
    return txt

#process document lines to exclude everything apart from elements of accepted characters('a-z','-','(',')')
def process_vocab(lines,case,voc,docs):
    for line in lines:
        elem = process(line,case)
        docs.append(elem)
        elem = set(elem)
        for el in elem:
            valid = True
            for chars in el:
                if chars not in accepted:
                    valid = False
                    break
            if valid is False:
                continue
            if el not in voc:
                voc[el] = 1
            else:
                voc[el] += 1

process_vocab(openfile(str(q_folder) + '/index.txt'),0,vocab,documents)
lines = []
for ind in range (1,num_of_questions_lc+1):
    lines.append(process_ps(openfile(str(q_folder) + '/' + str(ind) + '/' + str(ind) + '.txt')))

process_vocab(lines,1,vocab,documents)
    
new_lines = []
for ind in range (1,num_of_questions_cf+1):
    new_lines.append(process_cf_ps(openfile(str(cf_q_folder) + '/' + str(ind) + '/' + str(ind) + '.txt')))
process_vocab(new_lines,1,vocab_cf,documents_cf)

print(len(vocab))
print(len(documents))
print(len(vocab_cf))
print(len(documents_cf))

# Sort vocab in decreasing order of frequency of terms
vocab = dict(sorted(vocab.items(), key = lambda item: item[1], reverse=True))
vocab_cf = dict(sorted(vocab_cf.items(), key = lambda item: item[1], reverse=True))

#Save vocab in text file
def save_vocab(file,voc):
    with open(str(tf_idf_folder) + str(file),'w',encoding=find_encoding(str(tf_idf_folder) + str(file)),errors="ignore") as f:
        for key in voc.keys():
            f.write("%s\n" % key)
save_vocab('/vocab.txt',vocab)
save_vocab('/vocab_cf.txt',vocab_cf)

#Save idf-values in text file
def save_idf_val(file,voc):
    with open(str(tf_idf_folder) + str(file),'w',encoding=find_encoding(str(tf_idf_folder) + str(file)),errors="ignore") as f:
        for key in voc.keys():
            f.write("%s\n" % voc[key])
save_idf_val('/idf-values.txt',vocab)
save_idf_val('/idf-values_cf.txt',vocab_cf)

#Save documents in text file
def save_doc(file,docs):
    with open(str(tf_idf_folder) + str(file),'w',encoding=find_encoding(str(tf_idf_folder) + str(file)),errors="ignore") as f:
        for document in docs:
            f.write("%s\n" % ' '.join(document))
save_doc('/documents.txt',documents)
save_doc('/documents_cf.txt',documents_cf)

#Calculating inverted index to store list of documents any vocab term is present in
inverted_index = {}
inverted_index_cf = {}
def create_inverted_index(docs, inv_ind):
    for index,doc in enumerate(docs):
        for token in doc:
            if token not in inv_ind:
                inv_ind[token] = [index]
            else:
                inv_ind[token].append(index)
create_inverted_index(documents,inverted_index)
create_inverted_index(documents_cf,inverted_index_cf)

#Save inverted index in text file
def save_inverted_index(file,inv_index):
    with open(str(tf_idf_folder) + str(file),'w',encoding=find_encoding(str(tf_idf_folder) + str(file)),errors="ignore") as f:
        for key in inv_index.keys():
            f.write("%s\n" % key)
            f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inv_index[key]]))
save_inverted_index('/inverted-index.txt',inverted_index)
save_inverted_index('/inverted-index_cf.txt',inverted_index_cf)