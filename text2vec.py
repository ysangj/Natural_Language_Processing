import stop_list
import sys
import numpy as np
import re, string
import math

stoplist = stop_list.closed_class_stop_words

def remove(wordlist, stoplist):
    stoplist = stop_list.closed_class_stop_words

    returner = []
    for word in wordlist:
        if word in stoplist:
            continue
        if word == ",":
            continue
        returner.append(word)
    return returner

def find_match(query, article):
    return list(set(query) & set(article))

def get_tf(word, query):
    tf = 0
    for cw in query:
        if (word == cw):
            tf = tf + 1
    return tf

# Get IDF for each word in vector
def get_idf(word, matrix):
    N =len(matrix) #=365
    ni = 0
    for query in matrix:
        if (word in query):
            ni = ni + 1

    return np.log(N/ni)

def idf_hash(queries):
    hash = {}
    for query in queries:
        for word in query:
            idf = get_idf(word, queries)
            hash[word] = idf
    return hash

def create_hashes_list(articles, idf_hash):
    dictlist = []
    for article in articles:

        dict ={}
        for word in article:
           
            dict[word] = get_tf(word, article) * idf_hash[word]
        dictlist.append(dict)
    return dictlist

def score(queries, idf_hash):

    qs=[]

    for query in queries:
        q = []

        for word in query:
            q.append(get_tf(word, query) * idf_hash[word])   
        qs.append(q)

    return qs

def create_article_vector(query, match, match_words,article_hash):
    match_ = match[:]
    for entry in match_words:
        match_[query.index(entry)] = article_hash[entry]
    return match_

def vector_length(vector):
    total_entry = 0
    for entry in vector:
        total_entry = total_entry + entry

    return math.sqrt(total_entry)

def dot_product(query, article):
    returner = 0;
    for i in range(len(query)):
        returner = returner + (query[i] * article[i])

    return returner

def cosine_similarity(query, article):
    if(  (vector_length(article) == 0.0 )):
        return 0

    return dot_product(query,article)/(   vector_length(query) * vector_length(article)  )

################################################## create question matrix ##################################
question_matrix = []
text = open(sys.argv[1], "r") # read question list to create question matrix
for line in text:
    question_matrix.append(remove(re.sub('[%s]' % re.escape(string.punctuation), '', line).split(),stoplist))
text.close()

#now we have (non-integerized) question matrix

###############################now, integerize question matrix  #################
integerized_question_matrix = score(question_matrix, idf_hash(question_matrix))##
#################################################################################



################################### now process fantasy scripts ################################################

count = 0
fant = []
sen = ""
fantasy_scripts = open(sys.argv[2], "r")
for line in fantasy_scripts:
    if(line[0] == "*" ):
        count = count+1
        fant.append(sen)
        sen = ""
        continue
    else:
        sen = sen + line

fantasy_matrix = []
for script in fant:

    fantasy_matrix.append(remove(re.sub('[%s]' % re.escape(string.punctuation), '', script).split(),stoplist))


#now, we have a fantasy matrix( non-integerized ) which are, question_matrix and fantasy_matrix
fantasy_hash_list = create_hashes_list(fantasy_matrix, idf_hash(fantasy_matrix))

fantasy_vectors=[] 
for question_vector in question_matrix:
    vector = []
    for i in range(len(fantasy_matrix)):
        match = [0]*len(question_vector)
        match_words = find_match(question_vector, fantasy_matrix[i])
        if(len(match_words)==0):
            match = match
        else:
            match = create_article_vector(question_vector, match, match_words,fantasy_hash_list [i])
        vector.append(match)
    fantasy_vectors.append(vector)


question_fantasy = []
for i in range(len(question_matrix)):
    for j in range(  len(fantasy_vectors[i])  ):
        question_fantasy.append(cosine_similarity(integerized_question_matrix[i], fantasy_vectors[i][j]))


print(421*71)

#####################################################process action################################################################

count = 0
act = []
sen = ""
action_scripts = open(sys.argv[3], "r")
for line in action_scripts:
    if(line[0] == "*" ):
        count = count+1
        act.append(sen)
        sen = ""
        continue
    else:
        sen = sen + line

action_matrix = []
for script in act:

    action_matrix.append(remove(re.sub('[%s]' % re.escape(string.punctuation), '', script).split(),stoplist))


#now, we have a fantasy matrix( non-integerized ) which are, question_matrix and fantasy_matrix
action_hash_list = create_hashes_list(action_matrix, idf_hash(action_matrix))



action_vectors=[] 
for question_vector in question_matrix:
    vector = []
    for i in range(len(action_matrix)):
        match = [0]*len(question_vector)
        match_words = find_match(question_vector, action_matrix[i])
        if(len(match_words)==0):
            match = match
        else:
            match = create_article_vector(question_vector, match, match_words,action_hash_list [i])
        vector.append(match)
    action_vectors.append(vector)


question_action = []
for i in range(len(question_matrix)):
    for j in range(  len(action_vectors[i])  ):
        question_action.append(cosine_similarity(integerized_question_matrix[i], action_vectors[i][j]))


print(question_action)





