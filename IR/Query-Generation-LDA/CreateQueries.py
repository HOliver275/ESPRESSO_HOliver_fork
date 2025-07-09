import itertools
import nltk
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
import paramiko
import os
import logging

# Ensure you have the NLTK stopwords downloaded
nltk.download('punkt')  # Tokenizer
nltk.download('stopwords')  # Stopwords

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to download files from the server
def download_files_from_server(hostname, username, password, remote_path, local_path, max_files=100):
    try:
        logging.info("Connecting to the server to download files...")
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        # Create an SFTP session
        sftp = ssh.open_sftp()
        sftp.chdir(remote_path)

        # List of files to download, limited to max_files
        files = sftp.listdir()[:max_files]  # Only get the top 100 files

        # Download each file
        for file in files:
            if file.endswith('.txt'):  # Filter for text files
                local_file_path = os.path.join(local_path, file)
                logging.info(f"Downloading file: {file}")
                sftp.get(os.path.join(remote_path, file), local_file_path)

        # Close SFTP session and SSH connection
        sftp.close()
        ssh.close()
        logging.info("File download completed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Function to preprocess the text
def preprocess_documents(documents):
    stop_words = set(stopwords.words('english'))
    processed_docs = []
    for doc in documents:
        tokens = word_tokenize(doc.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        processed_docs.append(filtered_tokens)
    logging.info("Documents preprocessed.")
    return processed_docs

# Function to generate queries focusing on rare key terms in topics
def generate_queries(documents, num_topics=5, num_queries=10, frequency_min=2, frequency_max=20):
    # Preprocess documents
    processed_docs = preprocess_documents(documents)

    if not processed_docs:
        logging.warning("No valid documents found after preprocessing.")
        return [], [], [], []

    # Create a dictionary and corpus for LDA
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # Train the LDA model
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    logging.info("LDA model trained.")

    # Get topics and their frequencies
    topics = lda_model.show_topics(num_topics=num_topics, formatted=False)

    # Calculate document frequency for each word
    word_freq = {}
    for doc in corpus:
        for word_id, count in doc:
            word = dictionary[word_id]
            word_freq[word] = word_freq.get(word, 0) + count  # Count occurrences across documents

    # Prepare topics with their key rare terms
    topic_info = []
    for topic in topics:
        # Filter to keep only rare terms based on frequency threshold
        rare_terms = [word[0] for word in topic[1] if frequency_min < word_freq[word[0]] < frequency_max]
        topic_info.append((topic[0], rare_terms))

    # Generate queries from topics focusing on rare terms
    short_queries = []
    medium_queries = []
    long_queries = []

    # Helper function to generate queries
    def generate_query_combinations(words, r):
        return [" ".join(combo) for combo in itertools.combinations(words, r)]

    # Generate queries from rare terms in topics
    for topic in topic_info:
        words = topic[1]
        if words:  # Only proceed if there are rare terms
            short_queries.extend(words)  # Single terms
            if len(words) > 1:
                short_queries.extend(generate_query_combinations(words, 2))  # Combinations of 2
            if len(words) > 2:
                medium_queries.extend(generate_query_combinations(words, 3))  # Combinations of 3
            if len(words) > 3:
                long_queries.extend(generate_query_combinations(words, 4))  # Combinations of 4

    # Randomly select a subset of queries if needed
    short_queries = random.sample(short_queries, min(num_queries, len(short_queries))) if short_queries else []
    medium_queries = random.sample(medium_queries, min(num_queries, len(medium_queries))) if medium_queries else []
    long_queries = random.sample(long_queries, min(num_queries, len(long_queries))) if long_queries else []

    logging.info("Queries generated with a focus on rare key terms.")
    return short_queries, medium_queries, long_queries, topic_info

# Function to find the best matching topic for a given query
def best_matching_topic(query, topics):
    max_score = 0
    best_topic = None
    for topic_id, words in topics:
        score = sum(1 for word in words if word in query)
        if score > max_score:
            max_score = score
            best_topic = (topic_id, words)
    return best_topic

# Example usage
if __name__ == "__main__":
    # Server details
    hostname = 'srv03768.soton.ac.uk'
    username = 'XXXX'
    password = 'XXXX'  # Replace with your actual password
    remote_path = '/srv/health_datasets/synthea/synthea/output/text'
    local_path = './downloaded_files/'  # Local directory to save downloaded files

    # Create local directory if it doesn't exist
    os.makedirs(local_path, exist_ok=True)

    # Download the top 100 files from the server
    download_files_from_server(hostname, username, password, remote_path, local_path, max_files=100)

    # Read downloaded text files
    documents = []
    for filename in os.listdir(local_path):
        if filename.endswith('.txt'):
            with open(os.path.join(local_path, filename), 'r') as file:
                content = file.read().strip()
                if content:  # Only add non-empty documents
                    documents.append(content)

    # Limit documents to 10,000
    documents = documents[:10000]

    # Generate queries based on the documents focusing on rare key terms
    short, medium, long, topics = generate_queries(documents, num_topics=100, frequency_min=2, frequency_max=20)

    # Combine all queries for topic mapping
    all_queries = short + medium + long
    query_topic_mapping = {}

    # Now find the best matching topic for each query
    for query in all_queries:
        best_topic = best_matching_topic(query, topics)
        if best_topic:
            query_topic_mapping[query] = best_topic

    # Print queries with their best matching topics
    logging.info("\nQueries with Best Matching Topics:")
    for query, (topic_id, words) in query_topic_mapping.items():
        logging.info(f"Query: '{query}' -> Best Matching Topic: {topic_id} ({', '.join(words)})")

    # Print generated queries
    logging.info("\nShort Queries:")
    for q in short:
        logging.info(q)

    logging.info("\nMedium Queries:")
    for q in medium:
        logging.info(q)

    logging.info("\nLong Queries:")
    for q in long:
        logging.info(q)
