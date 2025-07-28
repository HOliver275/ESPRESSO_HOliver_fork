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

        // HO 26/07/2025 BEGIN ********
        //InputStream zipStream = System.in;
        String testSinkPath = "Dataswyfttestsink/";
        String networkZipIndexFilePath = testSinkPath.concat("metaindex/");
        String UUIDSpecificNetworkIndexPath = networkZipIndexFilePath.concat(strUUID).concat("/");
        String networkZipIndexFileSuffix = "-servers.zip";
        String networkZipIndexFileName = strUUID.concat(networkZipIndexFileSuffix);
        String fullPathToUUIDSpecificNetworkIndex = UUIDSpecificNetworkIndexPath.concat(networkZipIndexFileName);
        String networkLevelSearchResultsPath = "searchresults/networklevel/";
        String networkLevelSearchResultsSuffix = "-networklevel-searchresults.json";
        String UUIDSpecificNetworkLevelResults = networkLevelSearchResultsPath.concat(strUUID.concat(networkLevelSearchResultsSuffix));

        // do a network-level search
        conductSearch(fullPathToUUIDSpecificNetworkIndex, queryStr, initialRetrieve, model, layer, topK, strUUID, UUIDSpecificNetworkLevelResults);

        // do a server-level search of server1
        /*String serverZipIndexFilePath = testSinkPath.concat("server1_/metaindex/");
        String UUIDSpecificServerIndexPath = serverZipIndexFilePath.concat(strUUID).concat("/");
        String serverZipIndexFileSuffix = "-pods.zip";
        String serverZipIndexFileName = strUUID.concat(serverZipIndexFileSuffix);
        String fullPathToUUIDSpecificServerIndex = UUIDSpecificServerIndexPath.concat(serverZipIndexFileName);
        conductSearch(fullPathToUUIDSpecificServerIndex, queryStr, initialRetrieve, model, layer, topK, strUUID);*/
    }

    private static void conductSearch(String fullPathToNetworkIndex, String queryStr, int initialRetrieve, String model, String layer, int topK, String strUUID, String resultsPath) {
        RAMDirectory ramDirectory = new RAMDirectory();
        InputStream zipStream = null;
        try {
           zipStream = new FileInputStream(fullPathToNetworkIndex);
        } catch(FileNotFoundException e) {
            e.printStackTrace();
        }
        // HO 26/07/2025 END ********

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

        IndexReader reader = null;
        try {
            reader = DirectoryReader.open(ramDirectory);
        } catch(IOException e) {
            e.printStackTrace();
        }

        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser("content", new StandardAnalyzer());
        Query query = null;
        try {
            query = parser.parse(queryStr);
        } catch(ParseException e) {
            e.printStackTrace();
        }
        TopDocs results = null;
        try {
            results = searcher.search(query, initialRetrieve);
        } catch(IOException e) {
            e.printStackTrace();
        }

        if (backgroundModel == null && "LM".equals(model)) {
            try {
                backgroundModel = computeBackgroundModel(reader);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        // Calculate the average document length for the entire index
        List<Map<String, Object>> documents = new ArrayList<>();

        // Precompute query terms once
        String[] queryTerms = queryStr.split("\\s+");

        for (ScoreDoc scoreDoc : results.scoreDocs) {
            int docID = scoreDoc.doc;
            Document doc = null;
            try {
                doc = searcher.doc(docID);
            } catch (IOException e) {
                e.printStackTrace();
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
        } catch (IOException e) {
            e.printStackTrace();
        }
        // HO 26/07/2025 END ********

        try {
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        ramDirectory.close();
    }

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