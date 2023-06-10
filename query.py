import math
import chardet

num_of_questions = 2194

def find_encoding(file):
    r_file = open(file, 'rb').read()
    res = chardet.detect(r_file)
    charenc = res['encoding']
    return charenc

def load_doc_links():
    links = []
    with open('QDATA/Qindex.txt','r',encoding=find_encoding('QDATA/Qindex.txt'),errors = "ignore") as f:
        links = f.readlines()
    return links

def load_vocab():
    vocab = {}
    with open('TF-IDF/vocab.txt','r',encoding=find_encoding('TF-IDF/vocab.txt'),errors = "ignore") as f:
        vocab_terms = f.readlines()
    with open('TF-IDF/idf-values.txt','r',encoding=find_encoding('TF-IDF/idf-values.txt'),errors = "ignore") as f:
        idf_vals = f.readlines()
    for (vocab_term,idf_val) in zip(vocab_terms,idf_vals):
        vocab[vocab_term.strip()] = int(idf_val.strip())
    return vocab

def load_documents():
    documents = []
    with open('TF-IDF/documents.txt','r',encoding=find_encoding('TF-IDF/documents.txt'),errors = "ignore") as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]
    return documents

def load_inverted_index():
    inv_ind = {}
    with open('TF-IDF/inverted-index.txt','r',encoding=find_encoding('TF-IDF/inverted-index.txt'),errors = "ignore") as f:
        inv_ind_terms = f.readlines()
    for row in range(0,len(inv_ind_terms),2):
        term = inv_ind_terms[row].strip()
        docs = inv_ind_terms[row+1].strip().split()
        inv_ind[term] = docs
    return inv_ind

vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()
links = load_doc_links()

#get question link(based on if it is a title or a problem statement)
def get_ques_link(doc_ind):
    if doc_ind <= num_of_questions:
        return doc_ind
    else:
        return doc_ind-num_of_questions

def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    return tf_values

def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])

def calculate_doc_order(query_terms):
    potential_docs = {}
    for term in query_terms:
        if term not in vocab_idf_values:
            continue
        tf_values = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        for document in tf_values:
            if document not in potential_docs:
                potential_docs[document] = tf_values[document]*idf_value 
            else:
                potential_docs[document] += tf_values[document]*idf_value

    if(len(potential_docs) == 0):
        print('No matching questions found. Please enter relevant keywords')

    for document in potential_docs:
        potential_docs[document] /= len(query_terms)

    potential_docs = dict(sorted(potential_docs.items(), key = lambda item: item[1], reverse = True))
    for doc_ind in potential_docs:
        print('Question-link: ', links[get_ques_link(int(doc_ind))], ' Score: ', potential_docs[doc_ind])
        # print('Document: ', documents[int(doc_ind)], ' Score: ', potential_docs[doc_ind])

query_string = input('Enter your query: ')
query_terms = [term.lower() for term in query_string.strip().split()]
calculate_doc_order(query_terms)
