import math
import chardet
from flask import Flask, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

num_of_questions = 2194
num_of_questions_cf = 8636

def find_encoding(file):
    r_file = open(file, 'rb').read()
    res = chardet.detect(r_file)
    charenc = res['encoding']
    return charenc

def load_doc_title(file):
    links = []
    with open(str(file),'r',encoding=find_encoding(str(file)),errors = "ignore") as f:
        links = f.readlines()
    return links

def load_doc_links(file):
    links = []
    with open(str(file),'r',encoding=find_encoding(str(file)),errors = "ignore") as f:
        links = f.readlines()
    return links

def load_vocab(file1, file2):
    vocab = {}
    with open(str(file1),'r',encoding=find_encoding(str(file1)),errors = "ignore") as f:
        vocab_terms = f.readlines()
    with open(str(file2),'r',encoding=find_encoding(str(file2)),errors = "ignore") as f:
        idf_vals = f.readlines()
    for (vocab_term,idf_val) in zip(vocab_terms,idf_vals):
        vocab[vocab_term.strip()] = int(idf_val.strip())
    return vocab

def load_documents(file):
    documents = []
    with open(str(file),'r',encoding=find_encoding(str(file)),errors = "ignore") as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]
    return documents

def load_inverted_index(file):
    inv_ind = {}
    with open(str(file),'r',encoding=find_encoding(str(file)),errors = "ignore") as f:
        inv_ind_terms = f.readlines()
    for row in range(0,len(inv_ind_terms),2):
        term = inv_ind_terms[row].strip()
        docs = inv_ind_terms[row+1].strip().split()
        inv_ind[term] = docs
    return inv_ind

lc_vocab_idf_values = load_vocab('./TF-IDF/vocab.txt','./TF-IDF/idf-values.txt')
cf_vocab_idf_values = load_vocab('./TF-IDF/vocab_cf.txt','./TF-IDF/idf-values_cf.txt')
lc_documents = load_documents('./TF-IDF/documents.txt')
cf_documents = load_documents('./TF-IDF/documents_cf.txt')
lc_inverted_index = load_inverted_index('./TF-IDF/inverted-index.txt')
cf_inverted_index = load_inverted_index('./TF-IDF/inverted-index_cf.txt')
lc_links = load_doc_links('./QDATA/Qindex.txt')
lc_title = load_doc_links('./QDATA/index.txt')
cf_links = load_doc_links('./CF_QDATA/Qindex.txt')
cf_title = load_doc_title('./CF_QDATA/index.txt')

# print(len(cf_documents))
# print(len(lc_documents))

#get lc question link(based on if it is a title or a problem statement)
def get_ques_link(doc_ind):
    if doc_ind <= num_of_questions:
        return doc_ind
    else:
        return doc_ind-num_of_questions

def get_tf_dictionary(term,inv_ind,docs):
    tf_values = {}
    if term in inv_ind:
        for document in inv_ind[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
    for document in tf_values:
        try:
            tf_values[document] /= len(docs[int(document)])
        except(ZeroDivisionError, ValueError, IndexError) as e:
            print(e)
            print("Error in doc: ", document)
    return tf_values

def get_idf_value(term,docs,idf):
    return math.log(len(docs)/idf[term])

def calculate_doc_order(query_terms,idf_vals,documents,inverted_index,cs):
    potential_docs = {}
    ans = []
    for term in query_terms:
        if term not in idf_vals:
            continue
        tf_values = get_tf_dictionary(term,inverted_index,documents)
        idf_value = get_idf_value(term,documents,idf_vals)
        for document in tf_values:
            if document not in potential_docs:
                potential_docs[document] = tf_values[document]*idf_value 
            else:
                potential_docs[document] += tf_values[document]*idf_value

    if(len(potential_docs) == 0):
        print('No matching questions found. Please enter relevant keywords')
    else:
        for document in potential_docs:
            potential_docs[document] /= len(query_terms)
        potential_docs = dict(sorted(potential_docs.items(), key = lambda item: item[1], reverse = True))
        if cs == 1:
            # print('\nTop-Results from CodeForces:')
            # for i,doc_ind in enumerate(potential_docs):
            #     if(i>=10):
            #         break
                # print('Question-title: ', cf_title[int(doc_ind)], 'Question-URL:' , cf_links[int(doc_ind)],' Score: ', potential_docs[doc_ind])
            # results = [(cf_links[int(doc_ind)]) for doc_ind in potential_docs]
            for doc_ind in potential_docs:
                ans.append({"Question Link": str(cf_links[int(doc_ind)]),"Question Title": str(cf_title[int(doc_ind)])})
        else:
            # print('\nTop-Results from Leetcode:')
            # for i,doc_ind in enumerate(potential_docs):
            #     if(i>=10):
            #         break
                # print('Question-link: ', lc_links[get_ques_link(int(doc_ind))], ' Score: ', potential_docs[doc_ind])
            # results = [(lc_links[get_ques_link(int(doc_ind))]) for doc_ind in potential_docs]
            for doc_ind in potential_docs:
                stri = ""
                for words in lc_documents[get_ques_link(int(doc_ind))]:
                    stri+=(words)
                    stri+=" "
                final_str = stri.capitalize()
                ans.append({"Question Link": str(lc_links[get_ques_link(int(doc_ind))])[:-2], "Question Title": final_str})
    return ans

# query_string = input('Enter your query: ')
# query_terms = [term.lower() for term in query_string.strip().split()]
# res = calculate_doc_order(query_terms,lc_vocab_idf_values,lc_documents,lc_inverted_index,0)
# print(res)
# calculate_doc_order(query_terms,cf_vocab_idf_values,cf_documents,cf_inverted_index,1)

# cf_results = [{"Question Link":"apple","Question Title":"a"}, {"Question Link":"banana","Question Title":"b"}, {"Question Link":"apple","Question Title":"c"}]
# lc_results = [{"Question Link":"abc"},{"Question Link":"xyz"},{"Question Link":"pqr"}]

app = Flask(__name__)

lc_results = []
cf_results = []

app.config['SECRET_KEY'] = 'your-secret-key'
class SearchForm(FlaskForm):
    search = StringField('Enter the search term')
    submit = SubmitField('Search')

@app.route("/", methods = ['GET', 'POST'])

def home():
    form = SearchForm()
    cf_results = []
    lc_results = []
    if form.validate_on_submit():
        query_string = form.search.data
        query_terms = [term.lower() for term in query_string.strip().split()]
        lc_results = (calculate_doc_order(query_terms,lc_vocab_idf_values,lc_documents,lc_inverted_index,0)[:20:])
        cf_results = (calculate_doc_order(query_terms,cf_vocab_idf_values,cf_documents,cf_inverted_index,1)[:20:])
        # cf_results = [{"Question Link":"apple","Question Title":"a"}, {"Question Link":"banana","Question Title":"b"}, {"Question Link":"apple","Question Title":"c"}]
        # lc_results = [{"Question Link":"abc"},{"Question Link":"xyz"},{"Question Link":"pqr"}]
    return render_template('index.html', form = form, lc_results = lc_results, cf_results = cf_results)

if __name__ == "__main__":
    app.run()