import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;


import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.apache.lucene.document.IntPoint;
import org.apache.lucene.document.NumericDocValuesField;
import org.apache.lucene.document.StoredField;
import org.apache.lucene.document.TextField;

import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;




/**
 *
 * @author thanassis
 */
public class Indexer {

    public static void main(String[] args) throws IOException {
         if (args.length < 3) {
            System.out.println("Usage: java -jar Indexer.jar <files_location> <access_control_data> <destination>");
            return;
         }

        String filesLocation = args[0];
        String accessControlData = args[1];
        String destination = args[2];

        Type mapType = new TypeToken<HashMap<String, List<String>>>(){}.getType();
        Map<String, List<String>> accessControlMap = new Gson().fromJson(accessControlData, mapType);



        indexFiles(filesLocation,accessControlMap,destination);


    }
    private static void indexFiles(String filesLocation, Map<String, List<String>> accessControlMap, String destination) throws IOException
    {
        Directory index = FSDirectory.open(Paths.get(destination));
        StandardAnalyzer analyzer = new StandardAnalyzer();
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        IndexWriter writer = new IndexWriter(index, config);

        File[] files = new File(filesLocation).listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {

                    Document doc = new Document();
                    String content = readFile(file);
                    int docLength = content.split("\\s+").length;

                    doc.add(new TextField("content", content, Field.Store.YES));
                    doc.add(new NumericDocValuesField("length", docLength));
                    doc.add(new StoredField("length", docLength));

                    Set<String> uniqueTerms = new HashSet<>();
                    for (String term : content.split("\\s+")) {
                        uniqueTerms.add(term);
                    }
                    int uniqueDocLength = uniqueTerms.size();

                    doc.add(new NumericDocValuesField("uniqueLength", uniqueDocLength));
                    doc.add(new StoredField("uniqueLength", uniqueDocLength));

                    List<String> webIds = accessControlMap.get(file.getName());

                    if (webIds != null) {
                        for (String webId : webIds) {
                            doc.add(new TextField("authorizedWebIds", webId, Field.Store.YES));
                        }
                    }

                    writer.addDocument(doc);
                }
            }
        }

        writer.close();
        System.out.println("Indexing completed!");
    }

    private static void indexFiles(String filesLocation, String podPath, Map<String, List<String>> accessControlMap, String destination) throws IOException
    {
        Directory index = FSDirectory.open(Paths.get(destination));
        StandardAnalyzer analyzer = new StandardAnalyzer();
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        IndexWriter writer = new IndexWriter(index, config);

        File[] files = new File(filesLocation).listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {

                    Document doc = new Document();
                    String content = readFile(file);
                    int docLength = content.split("\\s+").length;

                    doc.add(new TextField("content", content, Field.Store.YES));
                    doc.add(new NumericDocValuesField("length", docLength));
                    doc.add(new StoredField("length", docLength));

                    Set<String> uniqueTerms = new HashSet<>();
                    for (String term : content.split("\\s+")) {
                        uniqueTerms.add(term);
                    }
                    int uniqueDocLength = uniqueTerms.size();

                    doc.add(new NumericDocValuesField("uniqueLength", uniqueDocLength));
                    doc.add(new StoredField("uniqueLength", uniqueDocLength));

                    List<String> webIds = accessControlMap.get(file.getName());

                    if (webIds != null) {
                        for (String webId : webIds) {
                            doc.add(new TextField("authorizedWebIds", webId, Field.Store.YES));
                        }
                    }

                    if (podPath != null) {
                        doc.add(new TextField("podPath", podPath, Field.Store.YES));
                    }

                    writer.addDocument(doc);
                }
            }
        }

        writer.close();
        System.out.println("Indexing completed!");
    }
 private static String readFile(File file) {
        StringBuilder content = new StringBuilder();
        try (FileReader fr = new FileReader(file)) {
            int i;
            while ((i = fr.read()) != -1) {
                content.append((char) i);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content.toString();

}

}

