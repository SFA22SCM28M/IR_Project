# Importing the pickle module for object serialization
import pickle
# Importing the argparse module for command-line argument parsing
import argparse
# Importing TfidfVectorizer for text vectorization
from sklearn.feature_extraction.text import TfidfVectorizer
# Importing the math module for mathematical functions
import math
# Importing the json module for JSON file operations
import json

# Function to load corpus data from a JSON file
def load_corpus(json_file):
    # Open the JSON file
    f = open('../crawler/'+json_file)
    # Load JSON data into a Python object
    data = json.load(f)
    # Initialize a list to store corpus documents
    corpus = []
    # Initialize a list to store URLs
    urls = []
    # Iterate through each object in the JSON data
    for obj in data:
        # Concatenate course information into a document
        doc = obj['code'] + ' title: '+obj['title'] +' credits: ' + obj['credits'] + ' description: '+obj['description'] + ' prerequisites: ' 
        # Append prerequisites to the document
        for course in obj['prerequisites:']:
            doc += course +' '
        # Append the document to the corpus
        corpus.append(doc)
        # Append the URL to the URLs list
        urls.append(obj['link'])
    # Return the corpus and URLs
    return corpus, urls

# Function to create a TF-IDF index from the corpus
def tf_idf_index(corpus):
    # Initialize a TfidfVectorizer
    vectorizer = TfidfVectorizer()
    # Transform the corpus into TF-IDF vectors
    X = vectorizer.fit_transform(corpus).toarray()
    # Get feature names from the vectorizer
    feature_names = vectorizer.get_feature_names()
    # Initialize a dictionary to store the TF-IDF index
    tfidf_index = {}
    # Iterate through each feature in the TF-IDF matrix
    for i in range(len(feature_names)):
        tfidf_index[feature_names[i]] = []
        # Iterate through each document in the corpus
        for doc in range(len(corpus)):
            # If the TF-IDF score for the feature in the document is greater than 0, add it to the index
            if X[doc][i] > 0:
                tfidf_index[feature_names[i]].append((doc, X[doc][i]))
    # Return the TF-IDF index
    return tfidf_index

# Function to convert a query into a TF-IDF vector
def query_to_vector(query, inv_index, N):
    # Split the query into terms
    terms = query.split(" ")
    # Initialize a dictionary to store the query vector
    vector = {}
    # Iterate through each term in the query
    for term in terms:
        # If term not in index, set IDF to 0
        if term not in inv_index:
            vector[term] = 0
        else:
            # Get document frequency (DF) of the term
            df = len(inv_index[term])
            # Calculate IDF
            idf = math.log(N / df)
            # Assign IDF to the term in the query vector
            vector[term] = idf
    # Return the query vector
    return vector

# Function to calculate cosine similarity between query vector and documents in TF-IDF index
def cos_similarity(query_vector, tfidf_index, corpus):
    # Initialize a dictionary to store similarity scores
    scores = {}
    for i in range(len(corpus)):
        # Initialize scores for each document
        scores[i] = 0
    # Iterate through terms in query vector
    for term in query_vector:
        # Iterate through documents and their TF-IDF scores for the term
        for (doc, score) in tfidf_index[term]:
            # Update similarity score
            scores[doc] += score * query_vector[term]
    
    # Normalize scores by dividing by document length
    for doc in scores.keys():
        scores[doc] = scores[doc] / len(corpus[doc])

    # Sort scores in descending order
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Function to save corpus to a text file
def saved_corpus(corpus, output_file):
    with open(output_file, "w") as f:
        for c in corpus:
            f.write(c + "\n")
    f.close()
    print('saved urls to ', output_file)

# Function to save URLs to a text file
def saved_urls(urls, output_file):
    with open(output_file, "w") as f:
        for url in urls:
            f.write(url + "\n")
    f.close()
    print('saved urls to ', output_file)

# Function to save index to a pickle file
def to_pickle(index, output_file):
    with open(output_file, "wb") as file:
        pickle.dump(index, file)
    file.close()
    print('saved index to ', output_file)

# Main function to execute the program
def main(args):
    # Load corpus and URLs from JSON file
    corpus, urls = load_corpus(args.json_file)
    # Create TF-IDF index
    N = len(corpus)
    # Save TF-IDF index to pickle file
    index = tf_idf_index(corpus)
    print(index)
    to_pickle(index, args.output_file)
    saved_corpus(corpus, 'corpus.txt')
    saved_urls(urls, 'urls.txt')
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inverted index construction')

    # Example command
    parser.add_argument('--json_file', type=str, default='cs_courses.json')
    parser.add_argument('--output_file', type=str, default='cs_courses.pickle')
    main(parser.parse_args())