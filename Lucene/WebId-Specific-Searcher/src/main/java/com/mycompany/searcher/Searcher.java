package com.mycompany.searcher;

import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.store.*;
import org.apache.lucene.index.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.*;
import org.apache.lucene.document.Document;
import org.apache.lucene.queryparser.classic.QueryParser;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.*;
import org.apache.lucene.util.BytesRef;

public class Searcher {
    private static Map<String, Double> backgroundModel = null;

    public static void main(String[] args) throws Exception {
        int minArgs = 3;
        if (args.length < minArgs) {
            System.err.println("Usage: java com.mycompany.searcher.Searcher <query> [k] <UUID>");
            System.exit(1);
        }

        String queryStr = args[0].toLowerCase();
        String model = "LM";
        int topK = 10;
        int initialRetrieve = 50; // Reduce to 5K for performance

        String layer = "document";

        if (args.length >= 2) {
            try {
                topK = Integer.parseInt(args[1]);
                if (topK <= 0) {
                    System.err.println("The value of k must be a positive integer.");
                    System.exit(1);
                }
            } catch (NumberFormatException e) {
                System.err.println("Invalid value for k. It must be an integer.");
                System.exit(1);
            }
        }

        String strUUID = "";

        if (args.length >= 3) {
            try {
                strUUID = args[2];
                if (strUUID.length() == 0) {
                    System.err.println("You must provide a UUID.");
                    System.exit(1);
                }
            } catch (NullPointerException e) {
                System.err.println("Invalid value for UUID.");
                System.exit(1);
            }
        }

        // HO 27/07/2025 BEGIN ********
        /*
        RAMDirectory ramDirectory = new RAMDirectory();
        // HO 26/07/2025 BEGIN ********
        //InputStream zipStream = System.in;
        // HO 26/07/2025 END ********
        String testSinkPath = "Dataswyfttestsink/";
        String networkZipIndexFilePath = testSinkPath.concat("metaindex/");
        String UUIDSpecificNetworkIndexPath = networkZipIndexFilePath.concat(strUUID).concat("/");
        String networkZipIndexFileSuffix = "-servers.zip";
        String UUIDSpecificNetworkZipIndexFileName = strUUID.concat(networkZipIndexFileSuffix);
        String fullPathToUUIDSpecificNetworkIndex = UUIDSpecificNetworkIndexPath.concat(UUIDSpecificNetworkZipIndexFileName);
        // HO 26/07/2025 BEGIN ********
        //InputStream zipStream = new FileInputStream("6561a0f3-ed1b-4378-bf46-c4ed190ad213-servers.zip");
        InputStream zipStream = new FileInputStream(fullPathToUUIDSpecificNetworkIndex);
        // HO 26/07/2025 END *****************


        try (ZipInputStream zis = new ZipInputStream(zipStream)) {
            ZipEntry entry;
            // HO 26/07/2025 BEGIN ********
            //while ((entry = zis.getNextEntry()) != null) {
            while (true) {
                if ((entry = zis.getNextEntry()) == null) break;
                // HO 26/07/2025 END ********
                String entryName = entry.getName();
                if (entryName.contains("segments") || entryName.endsWith(".index") || entryName.endsWith(".doc") ||
                        entryName.endsWith(".cfe") || entryName.endsWith(".si") || entryName.endsWith(".cfs") || entryName.endsWith("write.lock")) {
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    byte[] buffer = new byte[65536];
                    int len;
                    while ((len = zis.read(buffer)) != -1) {
                        baos.write(buffer, 0, len);
                    }
                    try (IndexOutput output = ramDirectory.createOutput(entryName, IOContext.DEFAULT)) {
                        output.writeBytes(baos.toByteArray(), baos.size());
                    }
                }
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        IndexReader reader = DirectoryReader.open(ramDirectory);
        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser("content", new StandardAnalyzer());
        Query query = parser.parse(queryStr);
        TopDocs results = searcher.search(query, initialRetrieve);

        if (backgroundModel == null && "LM".equals(model)) {
            backgroundModel = computeBackgroundModel(reader);
        }

        // Calculate the average document length for the entire index
        List<Map<String, Object>> documents = new ArrayList<>();

        // Precompute query terms once
        String[] queryTerms = queryStr.split("\\s+");

        for (ScoreDoc scoreDoc : results.scoreDocs) {
            int docID = scoreDoc.doc;
            Document doc = searcher.doc(docID);
            String content = doc.get("content");

            Map<String, Object> docData = new HashMap<>();
            docData.put("Id", doc.get("Id"));
            if( ("document".equals(layer)))
            docData.put("content", doc.get("content"));
            docData.put("BM25Score", scoreDoc.score);
            // Compute LM score directly without storing term frequencies
            if ("LM".equals(model))
                docData.put("LanguageModelingScore", (content != null) ? computeLMScore(content, queryTerms) : Double.NEGATIVE_INFINITY);
            
            // Compute document length and add to the result
            int docLength = (content != null) ? content.split("\\s+").length : 0;
            if( ("document".equals(layer)))
            docData.put("DocLength", docLength);

            if (("document".equals(layer)))
            {
            // Add TermFrequencies for each query term
            Map<String, Integer> termFrequencies = new HashMap<>();
            if (content != null) {
                String[] words = content.toLowerCase().split("\\s+");
                for (String term : queryTerms) {
                    int termCount = 0;
                    for (String word : words) {
                        if (word.equals(term.toLowerCase())) {
                            termCount++;
                        }
                    }
                    termFrequencies.put(term, termCount);
                }
            }
            docData.put("TermFrequencies", termFrequencies);

           
            }
             documents.add(docData);
        }

        // Sort only if needed
        if (model.equals("LM")) {
            documents.sort((d1, d2) -> Double.compare(
                (double) d2.get("LanguageModelingScore"),
                (double) d1.get("LanguageModelingScore")
            ));
        }

        // Create final JSON response with top K results
        Map<String, Object> jsonResponse = new HashMap<>();
        jsonResponse.put("totalHits", results.totalHits.value);
        jsonResponse.put("documents", documents.subList(0, Math.min(topK, documents.size())));
        //jsonResponse.put("avgDocLength", avgDocLength); // Include the average document length


        String networkLevelSearchResultsPath = "searchresults/networklevel/";
        String networkLevelSearchResultsSuffix = "-networklevel-searchresults.json";
        String UUIDSpecificNetworkLevelResults = networkLevelSearchResultsPath.concat(strUUID.concat(networkLevelSearchResultsSuffix));
        // HO 26/07/2025 BEGIN ********
        //System.out.println(new ObjectMapper().writeValueAsString(jsonResponse));
        new ObjectMapper().writeValue(new File(UUIDSpecificNetworkLevelResults), jsonResponse);
        // HO 26/07/2025 END ********

        reader.close();
        ramDirectory.close();
        */

        String openAccessUUID = "public";
        String testSinkPath = "Dataswyfttestsink/";
        String networkZipIndexFilePath = testSinkPath.concat("metaindex/");

        // network level search
        String networkZipIndexFileSuffix = "-servers.zip";
        String networkLevelSearchResultsPath = "searchresults/networklevel/";
        String networkLevelSearchResultsSuffix = "-networklevel-searchresults.json";

        // UUID-specific network level search
        String UUIDSpecificNetworkIndexPath = networkZipIndexFilePath.concat(strUUID).concat("/");
        String UUIDSpecificNetworkZipIndexFileName = strUUID.concat(networkZipIndexFileSuffix);
        String fullPathToUUIDSpecificNetworkIndex = UUIDSpecificNetworkIndexPath.concat(UUIDSpecificNetworkZipIndexFileName);
        String UUIDSpecificNetworkLevelResults = networkLevelSearchResultsPath.concat(strUUID.concat(networkLevelSearchResultsSuffix));

        // open-access network level search
        String openAccessNetworkIndexPath = networkZipIndexFilePath.concat(openAccessUUID).concat("/");
        String openAccessNetworkZipIndexFileName = openAccessUUID.concat(networkZipIndexFileSuffix);
        String fullPathToOpenAccessNetworkIndex = openAccessNetworkIndexPath.concat(openAccessNetworkZipIndexFileName);
        String openAccessNetworkLevelResults = networkLevelSearchResultsPath.concat(openAccessUUID.concat(networkLevelSearchResultsSuffix));

        // do a UUID-specific network-level search followed by an open-access network-level search
        conductSearch(strUUID, queryStr, initialRetrieve, model, layer, topK, fullPathToUUIDSpecificNetworkIndex, UUIDSpecificNetworkLevelResults);
        conductSearch(openAccessUUID, queryStr, initialRetrieve, model, layer, topK, fullPathToOpenAccessNetworkIndex, openAccessNetworkLevelResults);
        // HO 27/07/2025 END ********
    }

    // HO 27/07/2025 BEGIN *************
    private static void conductSearch(String strUUID, String queryStr, int initialRetrieve, String model, String layer, int topK, String fullIndexPath, String resultsPath) {
        if(strUUID == null || strUUID.length() == 0) {
            throw new NullPointerException("Invalid UUID.");
            //System.exit(1);
        }
        if(queryStr == null || queryStr.length() == 0) {
            throw new NullPointerException("Invalid query string.");
            //System.exit(1);
        }
        if(initialRetrieve <= 0) {
            initialRetrieve = 50;
        }
        if(model == null || model.length() == 0) {
            model = "LM";
        }
        if(layer == null || layer.length() == 0) {
            layer = "document";
        }
        if(topK <= 0) {
            topK = 10;
        }
        if(fullIndexPath == null || fullIndexPath.length() == 0) {
            System.err.println("Invalid index path.");
            System.exit(1);
        }
        if(resultsPath == null || resultsPath.length() == 0) {
            System.err.println("Invalid path to results output file.");
            System.exit(1);
        }

        RAMDirectory ramDirectory = new RAMDirectory();
        // HO 26/07/2025 BEGIN ********
        //InputStream zipStream = System.in;
        // HO 26/07/2025 END ********

        // HO 26/07/2025 BEGIN ********
        //InputStream zipStream = new FileInputStream("6561a0f3-ed1b-4378-bf46-c4ed190ad213-servers.zip");
        // HO 26/07/2025 END *****************

        try {
            InputStream zipStream = new FileInputStream(fullIndexPath);
            ZipInputStream zis = new ZipInputStream(zipStream);
            ZipEntry entry;
            // HO 26/07/2025 BEGIN ********
            //while ((entry = zis.getNextEntry()) != null) {
            while (true) {
                if ((entry = zis.getNextEntry()) == null) break;
                // HO 26/07/2025 END ********
                String entryName = entry.getName();
                if (entryName.contains("segments") || entryName.endsWith(".index") || entryName.endsWith(".doc") ||
                        entryName.endsWith(".cfe") || entryName.endsWith(".si") || entryName.endsWith(".cfs") || entryName.endsWith("write.lock")) {
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    byte[] buffer = new byte[65536];
                    int len;
                    while ((len = zis.read(buffer)) != -1) {
                        baos.write(buffer, 0, len);
                    }
                    try (IndexOutput output = ramDirectory.createOutput(entryName, IOContext.DEFAULT)) {
                        output.writeBytes(baos.toByteArray(), baos.size());
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.err.print("file ");
            System.err.print(fullIndexPath);
            System.err.println(" not found.");
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Error reading next zip entry.");
            System.exit(1);
        }


        IndexReader reader = null;
        try {
            reader = DirectoryReader.open(ramDirectory);
        } catch (IOException e) {
            System.err.println("Error opening index.");
            System.exit(1);
        }

        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser("content", new StandardAnalyzer());
        Query query = null;
        try {
            query = parser.parse(queryStr);
        } catch (ParseException e) {
            System.err.println("Error parsing query.");
            System.exit(1);
        }

        TopDocs results = null;
        try {
            results = searcher.search(query, initialRetrieve);
        } catch (IOException e) {
            System.err.println("Error searching for query.");
            System.exit(1);
        }

        if (backgroundModel == null && "LM".equals(model)) {
            try {
                backgroundModel = computeBackgroundModel(reader);
            }  catch (IOException e) {
                System.err.println("Error reading background model.");
                System.exit(1);
            }
        }

        // Calculate the average document length for the entire index
        List<Map<String, Object>> documents = new ArrayList<>();

        // Precompute query terms once
        String[] queryTerms = queryStr.split("\\s+");

        for (ScoreDoc scoreDoc : results.scoreDocs) {
            int docID = scoreDoc.doc;

            Document doc = new Document();
            try {
                searcher.doc(docID);
            } catch (IOException e) {
                System.err.println("Error searching for query.");
                System.exit(1);
            }

            String content = doc.get("content");

            Map<String, Object> docData = new HashMap<>();
            docData.put("Id", doc.get("Id"));
            if( ("document".equals(layer)))
                docData.put("content", doc.get("content"));
            docData.put("BM25Score", scoreDoc.score);
            // Compute LM score directly without storing term frequencies
            if ("LM".equals(model))
                docData.put("LanguageModelingScore", (content != null) ? computeLMScore(content, queryTerms) : Double.NEGATIVE_INFINITY);

            // Compute document length and add to the result
            int docLength = (content != null) ? content.split("\\s+").length : 0;
            if( ("document".equals(layer)))
                docData.put("DocLength", docLength);

            if (("document".equals(layer)))
            {
                // Add TermFrequencies for each query term
                Map<String, Integer> termFrequencies = new HashMap<>();
                if (content != null) {
                    String[] words = content.toLowerCase().split("\\s+");
                    for (String term : queryTerms) {
                        int termCount = 0;
                        for (String word : words) {
                            if (word.equals(term.toLowerCase())) {
                                termCount++;
                            }
                        }
                        termFrequencies.put(term, termCount);
                    }
                }
                docData.put("TermFrequencies", termFrequencies);


            }
            documents.add(docData);
        }

        // Sort only if needed
        if (model.equals("LM")) {
            documents.sort((d1, d2) -> Double.compare(
                    (double) d2.get("LanguageModelingScore"),
                    (double) d1.get("LanguageModelingScore")
            ));
        }

        // Create final JSON response with top K results
        Map<String, Object> jsonResponse = new HashMap<>();
        jsonResponse.put("totalHits", results.totalHits.value);
        jsonResponse.put("documents", documents.subList(0, Math.min(topK, documents.size())));
        //jsonResponse.put("avgDocLength", avgDocLength); // Include the average document length

        // HO 26/07/2025 BEGIN ********
        //System.out.println(new ObjectMapper().writeValueAsString(jsonResponse));
        try {
            new ObjectMapper().writeValue(new File(resultsPath), jsonResponse);
            // HO 26/07/2025 END ********
        } catch (IOException e) {
            System.err.println("Error writing network level search results.");
        }

        try {
            reader.close();
        } catch (IOException e) {
            System.err.println("Error closing index reader.");
        }

        ramDirectory.close();
    }
    // HO 27/07/2025 END ***************

    private static double computeLMScore(String content, String[] queryTerms) {
        double lmScore = 0.0;
        double lambda_d = 0.2;
        String[] words = content.toLowerCase().split("\\s+");
        int docLength = words.length;

        // Directly compute term frequencies on the fly
        Map<String, Integer> termFrequencies = new HashMap<>();
        for (String word : words) {
            termFrequencies.merge(word, 1, Integer::sum);
        }

        for (String term : queryTerms) {
            int tf_d = termFrequencies.getOrDefault(term, 0);
            double alpha_c = backgroundModel.getOrDefault(term, 1e-10);
            double p_lm = (1 - lambda_d) * ((double) tf_d / docLength) + lambda_d * alpha_c;
            if (p_lm > 0) {
                lmScore += Math.log(p_lm);
            }
        }
        return lmScore;
    }


    private static Map<String, Double> computeBackgroundModel(IndexReader reader) throws IOException {
        Map<String, Integer> documentFrequencies = new HashMap<>();
        int sumDf = 0;

        // Iterate over all terms in the index once
        TermsEnum termsEnum;
        for (LeafReaderContext leaf : reader.getContext().leaves()) {
            Terms terms = leaf.reader().terms("content");
            if (terms != null) {
                termsEnum = terms.iterator();
                BytesRef term;
                while ((term = termsEnum.next()) != null) {
                    String termText = term.utf8ToString();
                    int df = termsEnum.docFreq(); // Get document frequency once
                    documentFrequencies.put(termText, df);
                    sumDf += df;
                }
            }
        }

        // Normalize probabilities
        Map<String, Double> backgroundModel = new HashMap<>();
        for (Map.Entry<String, Integer> entry : documentFrequencies.entrySet()) {
            backgroundModel.put(entry.getKey(), (double) entry.getValue() / sumDf);
        }
        return backgroundModel;
    }

}
