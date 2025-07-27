package com.mycompany.searcher;

import org.apache.lucene.store.*;
import org.apache.lucene.index.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.*;
import org.apache.lucene.document.Document;
import org.apache.lucene.util.IOUtils;
import org.apache.lucene.queryparser.classic.QueryParser;

import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Searcher {

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Usage: java com.mycompany.searcher.Searcher <query> [k]");
            System.exit(1);
        }

        String queryStr = args[0];
        int topK = Integer.MAX_VALUE; // Default to all results
        
        if (args.length >= 2  && args[2] != null && !args[2].trim().isEmpty()) {
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
        
        
        RAMDirectory ramDirectory = new RAMDirectory();
        InputStream zipStream = System.in;

        // Unzip the content from the stream into the RAMDirectory
        try (ZipInputStream zis = new ZipInputStream(zipStream)) {
            ZipEntry entry;
            while ((entry = zis.getNextEntry()) != null) {
                String entryName = entry.getName();
                
                if (entryName.contains("segments") || entryName.endsWith(".index") || entryName.endsWith(".doc") ||
                    entryName.endsWith(".cfe") || entryName.endsWith(".si") || entryName.endsWith(".cfs") || entryName.endsWith("write.lock")) {
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    byte[] buffer = new byte[1024];
                    int len;
                    while ((len = zis.read(buffer)) != -1) {
                        baos.write(buffer, 0, len);
                    }
                    try (ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray())) {
                        try (IndexOutput output = ramDirectory.createOutput(entryName, IOContext.DEFAULT)) {
                            output.writeBytes(baos.toByteArray(), baos.size());
                        }
                    }
                }
            }
        }

        // Proceed with Lucene search using the RAMDirectory
        IndexReader reader = DirectoryReader.open(ramDirectory);
        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser("content", new StandardAnalyzer());
        
        
        
        Query query = parser.parse(queryStr);
        TopDocs results = searcher.search(query, topK);

        // Prepare JSON result
        Map<String, Object> jsonResponse = new HashMap<>();
        jsonResponse.put("totalHits", results.totalHits.value);

        List<Map<String, String>> documents = new ArrayList<>();
        for (ScoreDoc scoreDoc : results.scoreDocs) {
            Document doc = searcher.doc(scoreDoc.doc);
            Map<String, String> docData = new HashMap<>();
            docData.put("Id", doc.get("Id"));
            docData.put("Score", Float.toString(scoreDoc.score));
            documents.add(docData);
        }
        jsonResponse.put("documents", documents);

        // Output JSON
        System.out.println(new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(jsonResponse));

        // Clean up
        reader.close();
        ramDirectory.close();
    }
}