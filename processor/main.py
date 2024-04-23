# Import functions from query_processor.py and inverted_index.py
from query_processor import *
from indexer.inverted_index import *
# Import necessary modules from Flask
from flask import Flask, render_template, redirect, url_for, request
import sys
# Add the parent directory to sys.path to access modules from a different directory
sys.path.append('../')

# Initialize Flask app
app = Flask(__name__)
 
# Define the main route for the homepage 
@app.route("/")
def main():
    # Render the HTML template for the homepage
    return render_template('index.html')

# Define the route for handling search requests
@app.route("/search",methods =['POST','GET'])
def search():
    # If the request method is POST (form submission), get the search input from the form
    if request.method == 'POST':
        input = request.form['search']
        # Redirect to the 'result' route with the search input
        return redirect(url_for('result',search = input))
    # If the request method is GET (query parameter), get the search input from the query parameter
    else:
      input = request.args.get('search')
      # Redirect to the 'result' route with the search input
      return redirect(url_for('result',search = input))

# Define the route for displaying search results
@app.route("/result/<search>")
def result(search):
    # Load the inverted index, corpus, and URLs
    index = load_index('../indexer/cs_courses.pickle')
    corpus, urls = load_corpus_file('../indexer/corpus.txt'), load_urls('../indexer/urls.txt')
    # Initialize a variable to store search results
    results = ''
    # Set the maximum number of search results to display
    K = 10

    # search = spelling_correction(search)[:-1]
    # Modify the search query and convert it to a vector
    query = modify_query(search, get_vocab(index))[:-1]
    vector = query_to_vector(query, index, len(corpus))
    # Calculate cosine similarity between query vector and documents in the index
    matches = cos_similarity(vector, index, corpus)
    # Print the query and top matching documents (for debugging)
    print(query)
    print(matches[:K])
    
    # Generate the list of search results (URLs)
    for i in range(K):
        results += urls[matches[i][0]] + '\n'
    
    # Render the HTML template for displaying search results
    return render_template('results.html', **locals())

  

if __name__ == '__main__':
    app.run()