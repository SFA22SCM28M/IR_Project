# Import groupby for grouping elements
from itertools import groupby
# Import NLTK for natural language processing
import nltk
# Download the 'words' corpus from NLTK
nltk.download('words')
# Import the 'words' corpus from NLTK
from nltk.corpus import words
# Import numpy for numerical operations
import numpy as np
# Import defaultdict for creating dictionaries with default values
from collections import defaultdict
# Import pickle for object serialization
import pickle
# Load a list of correct English words
correct_words = words.words()

# Function to load the inverted index from a pickle file
def load_index(pickle_file):
    # Open the pickle file in read binary mode
    with open(pickle_file, 'rb') as f:
        # Load the dictionary from the pickle file
        dict = pickle.load(f)
    return dict

# Function to load the corpus from a text file
def load_corpus_file(corpus_file):
    # Open the corpus file in read mode
    with open(corpus_file, 'r') as f:
        # Read all lines from the file
        lines = f.readlines()
    return lines

# Function to load URLs from a text file    
def load_urls(url_file):
    # Open the URL file in read mode
    with open(url_file, 'r') as f:
        # Read all lines from the file
        lines = f.readlines()
    return lines

# Function to get the vocabulary (terms) from the inverted index
def get_vocab(index):
    return [term for term in index.keys()]

# Function for spelling correction using the NLTK words corpus
def spelling_correction(query):
    # Initialize an empty string to store corrected query
    corrected_query = ''
    # Split the query into words and iterate through each word
    for word in query.split():
        # Calculate edit distance between word and correct words
        temp = [(nltk.edit_distance(word, w),w) for w in correct_words if w[0]==word[0]]
        # Append the corrected word to the corrected query
        corrected_query += sorted(temp, key = lambda val:val[0])[0][1] + ' '
    # Return the corrected query
    return corrected_query

# Function to modify the query terms based on the vocabulary (terms) in the index
def modify_query(query, vocab):
    # Split the query into terms
    query_terms = query.split() 
    # Initialize an empty string to store modified query
    modified_query = ''
    # Iterate through each term in the query
    for term in query_terms:
        match = vocab[0]
        # Calculate edit distance between term and first vocab term
        min_dst = nltk.edit_distance(term, match)
        # Iterate through remaining vocab terms
        for i in range(1, len(vocab)):
            # Calculate edit distance between term and vocab term
            dst = nltk.edit_distance(term, vocab[i])
            if  dst < min_dst:
                min_dst = dst
                match = vocab[i]
        # Append the matched term to the modified query
        modified_query += match + ' '
    
    return modified_query

