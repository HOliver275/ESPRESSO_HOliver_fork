This module accepts query (bag of terms), with relevant statistics, in relation to a resource (e.g. server, pod, or file), and gives you ranking scores based on TF.IDF , BM25 and Language Modelling. Example ussage is
const queryTerms = [
    {
        term: "apple",
        termFrequency: 4000000,
        collectionFrequency: 500,
        documentFrequency: 100,
        documentFrequencyBM25: 80  // For BM25-specific df
    },
    {
        term: "banana",
        termFrequency: 3000,
        collectionFrequency: 300,
        documentFrequency: 50,
        documentFrequencyBM25: 40  // For BM25-specific df
    }
];

// Define document and collection statistics
const documentLength = 100;                    // Length of the document
const totalTermsInCollection = 100000;         // Total terms in the collection
const totalDocuments = 5000;                   // Total number of documents in the collection
const collectionSize = 5000;                   // Collection size (BM25)
const avgDocumentLength = 120;                 // Average document length (BM25)
const mu = 2000;                               // Dirichlet smoothing parameter for Query Likelihood
const k1 = 1.5;                                // BM25 k1 parameter
const b = 0.75;                                // BM25 b parameter

// Calculate the final scores for the query terms
const scores = calculateQueryScores({
    queryTerms,
    documentLength,
    totalTermsInCollection,
    totalDocuments,
    collectionSize,
    avgDocumentLength,
    mu,
    k1,
    b
});

console.log("Final BM25 Score:", scores.bm25Score);
console.log("Final Query Likelihood Score:", scores.queryLikelihoodScore);
console.log("Final TF-IDF Score:", scores.tfidfScore);
