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

/**
 * @author Mohammad Bahrani for the ESPRESSO Project 2025
 * @author Helen Oliver for the ESPRESSO Project 2025
 */

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

        searchByLevels(strUUID, queryStr, initialRetrieve, model, layer, topK);
        // search for public results too
        searchByLevels("public", queryStr, initialRetrieve, model, layer, topK);
    }

    /**
     * Searches the local file system offline, simulating a search first at network level,
     * then server level, then pod level.
     *
     * @param strUUID The UUID of the search party.
     * @param queryStr The query string
     * @param initialRetrieve
     * @param model The model
     * @param layer The layer to search
     * @param topK
     */
    private static void searchByLevels(String strUUID, String queryStr, int initialRetrieve, String model, String layer, int topK) {
        // Parent folder where index files are kept
        String testSinkPath = "Dataswyfttestsink/";
        // Index folder for network index
        String networkZipIndexFilePath = testSinkPath.concat("metaindex/");
        // Path to UUID-specific network-level index
        String UUIDSpecificNetworkIndexPath = networkZipIndexFilePath.concat(strUUID).concat("/");
        // Suffix denoting a network-level index file
        String networkZipIndexFileSuffix = "-servers.zip";
        // Full name of UUID-specific network index file
        String networkZipIndexFileName = strUUID.concat(networkZipIndexFileSuffix);
        // Full path to UUID-specific network index file
        String fullPathToUUIDSpecificNetworkIndex = UUIDSpecificNetworkIndexPath.concat(networkZipIndexFileName);
        // Output path for network-level search results
        String networkLevelSearchResultsPath = "searchresults/networklevel/";
        // Create the output file if it doesn't already exist
        File netresdir = new File(networkLevelSearchResultsPath);
        if (!netresdir.exists()) {
            netresdir.mkdirs();
        }
        // Suffix denoting network-level search results file
        String networkLevelSearchResultsSuffix = "-networklevel-searchresults.json";
        // Path to UUID-specific network level results output
        String UUIDSpecificNetworkLevelResults = networkLevelSearchResultsPath.concat(strUUID.concat(networkLevelSearchResultsSuffix));

        // do a network-level search
        List<String> foundServers = conductSearch(fullPathToUUIDSpecificNetworkIndex, queryStr, initialRetrieve, model, layer, topK, strUUID, UUIDSpecificNetworkLevelResults);

        // Now we've pinpointed the servers and pods containing results
        HashMap<String, List<String>> podsInServers = new HashMap<>();
        // no point looking if there were no results
        // otherwise look only in the servers where we know there are results
        if ((foundServers != null) && (foundServers.size() > 0)) {
            // do a server-level search
            int numServers = foundServers.size();
            for (int i = 0; i < numServers; i++) {
                // Path to folder where server-level index files are kept
                String serverZipIndexFilePath = testSinkPath.concat(foundServers.get(i).concat("metaindex/"));
                // Path to UUID-specific server-level index
                String UUIDSpecificServerIndexPath = serverZipIndexFilePath.concat(strUUID).concat("/");
                // Suffix denoting a server-level index file
                String serverZipIndexFileSuffix = "-pods.zip";
                // Full name of UUID-specific server-level index file
                String serverZipIndexFileName = strUUID.concat(serverZipIndexFileSuffix);
                // Full path to UUID-specific server-level index file
                String fullPathToUUIDSpecificServerIndex = UUIDSpecificServerIndexPath.concat(serverZipIndexFileName);
                // Output folder of server-level search results
                String serverLevelSearchResultsPath = "searchresults/serverlevel/".concat(foundServers.get(i));
                // Create the output folders if they don't already exist
                File servresdir = new File(serverLevelSearchResultsPath);
                if (!servresdir.exists()) {
                    servresdir.mkdirs();
                }
                // Suffix denoting server-level search results file
                String serverLevelSearchResultsSuffix = "-serverlevel-searchresults.json";
                // Full path to UUID-specific server-level search results
                String UUIDSpecificServerLevelResults = serverLevelSearchResultsPath.concat(strUUID.concat(serverLevelSearchResultsSuffix));
                // List of pods containing search results
                List<String> foundPods = conductSearch(fullPathToUUIDSpecificServerIndex, queryStr, initialRetrieve, model, layer, topK, strUUID, UUIDSpecificServerLevelResults);
                if((foundPods != null) && (foundPods.size() > 0)) {
                    podsInServers.put(foundServers.get(i), foundPods);
                }
            }
        }
        // search the pods now
        for (Map.Entry<String, List<String>> entry : podsInServers.entrySet()) {
            if(entry.getValue().size() != 0) {
                // Path to pod-level index files
                String serverPath = testSinkPath.concat(entry.getKey());
                // List of pods that contain results
                List<String> podsOnServer = entry.getValue();
                for(String pod : podsOnServer) {
                    // Path to pod index folder
                    String podIndexPath = serverPath.concat(pod.concat("/metaindex/"));
                    // Path to UUID-specific pod index file
                    String UUIDSpecificPodIndexPath = podIndexPath.concat(strUUID).concat(".zip");
                    // Path to UUID-specific pod-level results output folder
                    String podLevelUUIDSpecificResultsPath = "searchresults/podlevel/".concat(strUUID).concat("/");
                    // Full path to UUID-specific pod-level results output
                    String podLevelSearchResultsPath = podLevelUUIDSpecificResultsPath.concat(entry.getKey()).concat(pod);
                    // if the output folders don't exist, create them.
                    File podresdir = new File(podLevelSearchResultsPath);
                    if (!podresdir.exists()) {
                        podresdir.mkdirs();
                    }
                    // Suffix denoting a pod-level search results file
                    String podLevelSearchResultsSuffix = "-podlevel-searchresults.json";
                    // Full path of UUID-specific pod-level search results file
                    String UUIDSpecificPodLevelResults = podLevelSearchResultsPath.concat("/").concat(strUUID.concat(podLevelSearchResultsSuffix));

                    // Now search the pods for the actual files containing results
                    List<String> foundFiles = conductSearch(UUIDSpecificPodIndexPath, queryStr, initialRetrieve, model, layer, topK, strUUID, UUIDSpecificPodLevelResults);
                    // Output links to search results listed in a text file
                    String simpleResultsFile = podLevelUUIDSpecificResultsPath.concat("results.txt");
                    try (BufferedWriter writer = new BufferedWriter(new FileWriter(simpleResultsFile, true))) {
                        for (String file : foundFiles) {
                            // URL format in a HAT's file API: https://blorf.hubofallthings.net/api/v2.6/files/
                            String fileToGet = "https://".concat(pod).concat("/api/v2.6/files/").concat(file);

                            writer.write(fileToGet);
                            writer.newLine();
                        }
                        // close the simple results file
                        writer.close();
                    } catch (IOException ex) {
                            ex.printStackTrace();
                    }
                }
            }
        }
    }

    /**
     * Actually do the search. This is an offline search of the local file system.
     * @param fullPathToIndex Full path to the index file on which to do the query
     * @param queryStr The query string
     * @param initialRetrieve
     * @param model
     * @param layer
     * @param topK
     * @param strUUID UUID of the search party
     * @param resultsPath Path to search results output file
     * @return A List of Strings representing the locations (servers, pods, files) where results were found
     */
    private static List<String> conductSearch(String fullPathToIndex, String queryStr, int initialRetrieve, String model, String layer, int topK, String strUUID, String resultsPath) {
        RAMDirectory ramDirectory = new RAMDirectory();
        InputStream zipStream = null;

        File f = new File(fullPathToIndex);
        // if there isn't an index file for this user, there won't be any query results
        if(!f.exists() || f.isDirectory()) {
            //System.out.println("No results for query " + queryStr + " for UUID " + strUUID);
            return null;
        }
        try {
           zipStream = new FileInputStream(fullPathToIndex);
        } catch(FileNotFoundException e) {
            e.printStackTrace();
        }

        try (ZipInputStream zis = new ZipInputStream(zipStream)) {
            ZipEntry entry;

            while (true) {
                if ((entry = zis.getNextEntry()) == null) break;

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

        // list the locations where results are found
        List<String> scopeIds = new ArrayList<String>();

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
            // add the current Id to the list of places to look
            scopeIds.add(doc.get("Id"));
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
        // don't return any results if the keyword isn't found
        if (results.totalHits.value <= 0) {
            closeOpenSearchStreams(reader, ramDirectory);
            return null;
        }

        Map<String, Object> jsonResponse = new HashMap<>();
        jsonResponse.put("totalHits", results.totalHits.value);
        jsonResponse.put("documents", documents.subList(0, Math.min(topK, documents.size())));
        //jsonResponse.put("avgDocLength", avgDocLength); // Include the average document length

        try {
            new ObjectMapper().writeValue(new File(resultsPath), jsonResponse);
        } catch (IOException e) {
            e.printStackTrace();
        }

        closeOpenSearchStreams(reader, ramDirectory);
        // return list of places to look
        return scopeIds;
    }

    /**
     * Closes the streams we opened to do the search
     * @param reader The IndexReader we opened earlier
     * @param ramDirectory The RAMDirectory we opened earlier
     */
    private static void closeOpenSearchStreams(IndexReader reader, RAMDirectory ramDirectory) {
        if (reader != null) {
            try {
                reader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (ramDirectory != null) {
            ramDirectory.close();
        }
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