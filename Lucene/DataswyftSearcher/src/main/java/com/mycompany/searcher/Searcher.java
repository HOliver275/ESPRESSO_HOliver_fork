package com.mycompany.searcher;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.store.*;
import org.apache.lucene.index.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.*;
import org.apache.lucene.document.Document;
import org.apache.lucene.queryparser.classic.QueryParser;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.*;
import org.apache.lucene.util.BytesRef;

/**
 * @author Mohammad Bahrani for the ESPRESSO Project 2025
 * @author Helen Oliver for the ESPRESSO Project 2025
 * Conducts a UUID-specific search of the ESPRESSO-indexed HATs.
 */

public class Searcher {
    private static Map<String, Double> backgroundModel = null;
    private static String espressoAccessToken = "";
    private static String espressoUserId = "";
    private static final String ESPRESSO_USERNAME = "espressohubofallthing";
    private static final String ESPRESSO_PASSWORD = "E6pr4661yourself_hTa";
    private static final String ESPRESSO_URL = "https://espressohubofallthing.hubofallthings.net/";
    // DEV
    //private static final String ESPRESSO_USERNAME = "espressohubofallthfjs";
    //private static final String ESPRESSO_PASSWORD = "blorf";
    //private static final String ESPRESSO_URL = "https://espressohubofallthfjs.hubat.net/";
    private static final String AUTHTOKEN_PATH = "users/access_token";
    private static final String ESPRESSO_IDX_FILE_PREFIX = "espresso_metaindex";
    private static final String ESPRESSO_PUBLIC_IDX_FILENAME_STEM = "public";
    private static final String ESPRESSO_IDX_FILE_TYPE = ".zip";
    private static final String NETWORK_LEVEL_IDX_FILE_SUFFIX = "-servers";
    private static final String DATASWYFT_FILE_PATH = "api/v2.6/files/";
    private static final String DATASWYFT_FILE_CONTENT_PATH = "api/v2.6/files/content/";
    private static final String DATASWYFT_FILE_METADATA_PATH = "api/v2.6/files/file/";
    private static final String ESPRESSO_METAINDEX_ENDPOINT = "api/v2.6/data/espresso/metaindex";
    private static final String POD_LEVEL_IDX_FILE_SUFFIX = "";
    private static final String SERVER_LEVEL_IDX_FILE_SUFFIX = "-pods";
    private static final String POD_LEVEL_RESULTS_SUFFIX = "-podlevel-searchresults.json";
    private static final String SERVER_LEVEL_RESULTS_SUFFIX = "-serverlevel-searchresults.json";
    private static final String EXHAUSTIVE_SEARCH_RESULTS_FOLDER = "exhaustive_search_results/";
    private static final String SEARCH_RESULTS_PATH = "searchresults/";
    private static final String NETWORK_SEARCH_RESULTS_PATH = "networksearchresults/";
    private static final String SERVER_SEARCH_RESULTS_PATH = "serversearchresults/";
    private static final String NETWORK_SEARCH_RESULTS_FILE_SUFFIX = "-networklevel-searchresults.json";
    private static final String SERVER_SEARCH_RESULTS_FILE_SUFFIX = "-serverlevel-searchresults.json";
    private static final String[] HAT_DOMAINS = new String[]{".hubofallthings.net/", ".hubat.net/"};
    private static final String TEST_SINK_PATH = "Dataswyfttestsink/";
    private static final String TEST_OUTPUT_METAINDEX_PATH = "metaindex/";

    private static String searchPartyUsername = "";
    private static String searchPartyPassword = "";
    private static String searchPartyUrl = "";
    private static String searchPartyAccessToken = "";
    private static String searchPartyUserId = "";
    private static String searchPartyDomain = "";

    private static ArrayList<String> allEspressoServers = null;
    private static HashMap<String, String> espressoServerCreds = null;
    private static ArrayList<String> allRegisteredHATs = null;


    public static void setEspressoAccessToken(String strAccessToken) {
        espressoAccessToken = strAccessToken;
    }

    public static String getEspressoAccessToken() {
        return espressoAccessToken;
    }

    public static void setEspressoUserId(String strUserId) {
        espressoUserId = strUserId;
    }

    public static String getEspressoUserId() {
        return espressoUserId;
    }

    public static void setSearchPartyUsername(String strSearchPartyUsername) {
        searchPartyUsername = strSearchPartyUsername;
    }

    public static String getSearchPartyUsername() {
        return searchPartyUsername;
    }

    public static void setSearchPartyPassword(String strSearchPartyPassword) {
        searchPartyPassword = strSearchPartyPassword;
    }

    public static String getSearchPartyPassword() {
        return searchPartyPassword;
    }

    public static void setSearchPartyUrl(String strSearchPartyUrl) {
        searchPartyUrl = strSearchPartyUrl;
    }

    public static String getSearchPartyUrl() {
        return searchPartyUrl;
    }

    public static void setSearchPartyAccessToken(String strSearchPartyAccessToken) {
        searchPartyAccessToken = strSearchPartyAccessToken;
    }

    public static String getSearchPartyAccessToken() {
        return searchPartyAccessToken;
    }

    public static void setSearchPartyUserId(String strSearchPartyUserId) {
        searchPartyUserId = strSearchPartyUserId;
    }

    public static String getSearchPartyUserId() {
        return searchPartyUserId;
    }

    public static void setSearchPartyDomain(String strSearchPartyDomain) {
        searchPartyDomain = strSearchPartyDomain;
    }

    public static String getSearchPartyDomain() {
        return searchPartyDomain;
    }

    public static void setAllEspressoServers(ArrayList<String> listEspressoServers) {
        allEspressoServers = listEspressoServers;
    }

    public static ArrayList<String> getAllEspressoServers() {
        return allEspressoServers;
    }

    public static void setEspressoServerCreds(HashMap<String, String> serverCreds) {
        espressoServerCreds = serverCreds;
    }

    public static HashMap<String, String> getEspressoServerCreds() {
        return espressoServerCreds;
    }

    public static void setAllRegisteredHATs(ArrayList<String> listRegisteredHATs) {
        allRegisteredHATs = listRegisteredHATs;
    }

    public static ArrayList<String> getAllRegisteredHATs() {
        return allRegisteredHATs;
    }

    public static void main(String[] args) throws Exception {
        int minArgs = 5;
        if (args.length < minArgs) {
            System.err.println("Usage: java com.mycompany.searcher.Searcher <query> [k] <username> <domain> <password>");
            System.exit(1);
        }

        // first argument is the query string
        String queryStr = args[0].toLowerCase();
        String model = "LM";
        int topK = 10;
        int initialRetrieve = 50; // Reduce to 5K for performance
        String layer = "document";

        // second argument is the top-K
        // validate the top-K
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

        // third argument is the search party user name, as in blorf.hubofallthings.net
        if (args.length >= 3) {
            if(!args[2].isEmpty()) {
                setSearchPartyUsername(args[2].toString().toLowerCase());
            }
        }

        // fourth argument is the domain, a finite list
        if (args.length >= 4) {
            for (int i=0; i< HAT_DOMAINS.length; i++) {
                String strInputDomain = args[3].toString().toLowerCase();
                if (HAT_DOMAINS[i].contains(strInputDomain))
                {
                    setSearchPartyDomain(HAT_DOMAINS[i]);
                    // rebuild the search party's HAT URL from the username and domain
                    setSearchPartyUrl("https://".concat(getSearchPartyUsername().concat(getSearchPartyDomain())));
                    break;
                }
            }
            if (getSearchPartyDomain().isEmpty()) {
                // use a default domain if there somehow isn't a value here by now
                setSearchPartyDomain(HAT_DOMAINS[0]);
            }
        }

        // fifth argument is the password
        if(args.length >= 5) {
            if (args[4].toString().isEmpty()) {
                System.err.println("You must enter a password.");
                System.exit(1);
            }

            setSearchPartyPassword(args[4].toString());
        }

        // authenticate the search party
        String strSearchPartyCreds = authenticateSearchParty();
        // get the search party's access token and userId out of there
        extractSearchPartyAccessDetails(strSearchPartyCreds);
        if (strSearchPartyCreds.isEmpty()) {
            System.err.println("Invalid search party credentials.");
            System.exit(1);
        }

        // the UUID will be the basis for the filenames we search for
        String strUUID = getSearchPartyUserId();

        // log in to ESPRESSO, as ESPRESSO
        String strCreds = logIntoEspresso();
        // get the ESPRESSO access token out of there
        extractEspressoAccessDetails(strCreds);
        if (!strCreds.isEmpty()) {
            // get a list of all ESPRESSO servers
            listAllEspressoServers();
            // map all the ESPRESSO server credentials so we don't have to login repeatedly
            mapEspressoServerCreds();

            // until file permissions are set up, do a direct pod search
            //exhaustiveSearch(strUUID, queryStr, initialRetrieve, model, layer, topK);
            //exhaustiveSearch("public", queryStr, initialRetrieve, model, layer, topK);
            // normally we would search from network level down, but we need to set the file permissions
            // so the indexing will be accurate
            searchByLevels(strUUID, queryStr, initialRetrieve, model, layer, topK);
            // search for public results too
            //searchByLevels("public", queryStr, initialRetrieve, model, layer, topK);
        }
    }

    // exhaustive pod search
    private static void exhaustiveSearch(String strUUID, String queryStr, int initialRetrieve, String model, String layer, int topK) {
        if (strUUID.isEmpty()) {
            return;
        }

        InputStream instr = null;

        // Get the list of registered HATs
        ArrayList<String> podsToSearch = getAllRegisteredHATs();
        if (podsToSearch == null || podsToSearch.isEmpty()) {
            // if the list is empty, initialize it
            listAllRegisteredHATs();
            podsToSearch = getAllRegisteredHATs();
            // if the list is still empty, there's nothing to search
            if (podsToSearch == null || podsToSearch.isEmpty()) {
                System.err.println("Failed to find any registered HATs.");
                System.exit(1);
            }
        }

        String podLevelUUIDSpecificResultsPath = SEARCH_RESULTS_PATH.concat(EXHAUSTIVE_SEARCH_RESULTS_FOLDER).concat(strUUID).concat("/");
        String podname = "";
        // Full path to UUID-specific pod-level results output
        String podLevelSearchResultsPath = "";
        String UUIDSpecificPodLevelResults = "";

        for (int i = 0; i < podsToSearch.size(); i++) {
            instr = fetchZipIndexFile(podsToSearch.get(i), strUUID, POD_LEVEL_IDX_FILE_SUFFIX, getSearchPartyAccessToken());
            if (instr != null) {
                // DEV output the search results to the local file structure
                // results of a direct pod search get their owm folder
                if (podsToSearch.get(i).startsWith("http")) {
                    int pos = podsToSearch.get(i).indexOf("://");
                    if (pos != -1) {
                        podname = podsToSearch.get(i).substring(pos + 3);
                        podLevelSearchResultsPath = podLevelUUIDSpecificResultsPath.concat(podname);
                        // if the output folders don't exist, create them.
                        File podresdir = new File(podLevelSearchResultsPath);
                        if (!podresdir.exists()) {
                            podresdir.mkdirs();
                        }
                        // Full path of UUID-specific pod-level search results file
                        UUIDSpecificPodLevelResults = podLevelSearchResultsPath.concat(strUUID.concat(POD_LEVEL_RESULTS_SUFFIX));
                        List<String> foundFiles = conductSearch(instr, queryStr, initialRetrieve, model, layer, topK, strUUID, UUIDSpecificPodLevelResults);
                        // Output links to search results listed in a text file
                        // which is what the results would look like to the search party
                        String simpleResultsFile = podLevelUUIDSpecificResultsPath.concat("results.txt");
                        try (BufferedWriter writer = new BufferedWriter(new FileWriter(simpleResultsFile, true))) {
                            if(foundFiles != null && !foundFiles.isEmpty()) {
                                for (String file : foundFiles) {
                                    // URL format in a HAT's file API: https://blorf.hubofallthings.net/api/v2.6/files/
                                    String fileToGet = (podsToSearch.get(i)).concat(DATASWYFT_FILE_PATH).concat(file);

                                    writer.write(fileToGet);
                                    writer.newLine();
                                }
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
    }

    private static void listAllEspressoServers() {
        String strEndpoint = ESPRESSO_URL.concat(ESPRESSO_METAINDEX_ENDPOINT);
        ArrayList<String> theServers = null;

        // get all the ESPRESSO server-level HATs registered at network level
        URL url = null;

        try {
            url = new URL(strEndpoint);
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }

        HttpURLConnection con = null;

        try {
            con = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        try {
            con.setRequestMethod("GET");
        } catch (ProtocolException e) {
            throw new RuntimeException(e);
        }

        // Use the search party's credentials to do the search
        String strAuthToken = getEspressoAccessToken();

        con.setRequestProperty("Content-Type", "application/json");
        con.setRequestProperty("x-auth-token", strAuthToken);

        int responseCode = 0;
        try {
            responseCode = con.getResponseCode();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("Response Code: " + responseCode);

        // I'm not OK, you're not OK
        if(responseCode != 200) {
            return;
        }

        String strResp = returnResponseAsString(con);

        // if we found the file, extract the HATs into an ArrayList

        if (strResp.isEmpty()) {
            return;
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode node = mapper.readTree(strResp);
            theServers = (ArrayList<String>) node.findValuesAsText("url");

            if(theServers == null || theServers.isEmpty()) {
                System.err.println("Failed to find any server-level ESPRESSO HATs.");
            }
            setAllEspressoServers(theServers);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private static void mapEspressoServerCreds() {
        String strUrl = "";

        // list of ESPRESSO servers
        ArrayList<String> theServers = getAllEspressoServers();
        // map of ESPRESSO servers and their credentials
        HashMap<String, String> serversAndCreds = new HashMap<String, String>();

        // go round all the ESPRESSO servers
        for(int i=0; i<theServers.size(); i++) {
            // get all the ESPRESSO server-level HATs registered at network level
            URL url = null;

            strUrl = theServers.get(i);
            // extract the username so we can use it to log in
            String strUsername = getUsernameFromURL(strUrl);

            if (!strUrl.endsWith("/")) {
                strUrl = strUrl.concat("/");
            }

            // log into the ESPRESSO server
            String strAuthResponse = logIntoEspressoServer(strUrl, strUsername);
            if (strAuthResponse.isEmpty()) {
                continue;
            }
            // save the ESPRESSO server creds while we're at it, as we'll need them again
            serversAndCreds.put(strUrl, strAuthResponse);
        }

        // save the server credentials to use again
        setEspressoServerCreds(serversAndCreds);
    }

    private static void listAllRegisteredHATs() {
        String strUrl = "";
        // list of registered HATs
        ArrayList<String> theHATs = new ArrayList<String>();
        // list of ESPRESSO servers
        ArrayList<String> theServers = getAllEspressoServers();

        // map of ESPRESSO servers and their credentials
        HashMap<String, String> serversAndCreds = getEspressoServerCreds();

        // go round all the ESPRESSO servers
        for (Map.Entry<String, String> entry : serversAndCreds.entrySet()) {
            // get all the ESPRESSO server-level HATs registered at network level
            URL url = null;

            strUrl = entry.getKey();
            String strCreds = entry.getValue();

            if (!strUrl.endsWith("/")) {
                strUrl = strUrl.concat("/");
            }

            // get the auth token for this ESPRESSO server
            String strAuthToken = extractAuthToken(strCreds);
            if (strAuthToken.isEmpty()) {
                return;
            }

            // now get the endpoint for the ESPRESSO metaindex
            String strEndpoint = strUrl.concat(ESPRESSO_METAINDEX_ENDPOINT);

            try {
                url = new URL(strEndpoint);
            } catch (MalformedURLException e) {
                throw new RuntimeException(e);
            }

            HttpURLConnection con = null;

            try {
                con = (HttpURLConnection) url.openConnection();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            try {
                con.setRequestMethod("GET");
            } catch (ProtocolException e) {
                throw new RuntimeException(e);
            }

            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("x-auth-token", strAuthToken);

            int responseCode = 0;
            try {
                responseCode = con.getResponseCode();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            System.out.println("Response Code: " + responseCode);

            // I'm not OK, you're not OK
            if(responseCode != 200) {
                return;
            }

            // get the response
            String strResp = returnResponseAsString(con);
            if (strResp.isEmpty()) {
                return;
            }

            try {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode node = mapper.readTree(strResp);
                // get all the HATs registered on tis server
                ArrayList<String> theseHATs = (ArrayList<String>) node.findValuesAsText("url");
                if(theseHATs == null || theseHATs.isEmpty()) {
                    System.err.println("Failed to find any ESPRESSO HATs on this server.");
                }
                // add the HATs on this server to the list
                theHATs.addAll(theseHATs);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
        }

        // save the list of registered HATs
        setAllRegisteredHATs(theHATs);
    }

    private static InputStream fetchZipIndexFile(String strHatUrl, String strUUID, String strLevelSuffix, String strAuth) {
        if (strHatUrl.isEmpty()) {
            System.err.println("No HAT URL provided.");
            System.exit(1);
        }

        if (!strHatUrl.endsWith("/")) {
            strHatUrl = strHatUrl.concat("/");
        }

        //String strSearchUrl = strHatUrl.concat(ESPRESSO_FILE_CONTENT_PATH).concat(ESPRESSO_IDX_FILE_PREFIX).concat(ESPRESSO_PUBLIC_IDX_FILENAME_STEM).concat(strLevelSuffix).concat(ESPRESSO_IDX_FILE_TYPE);
        // We must search by fileId, which we don't control. The File API strips the hyphens out so we have to do the same
        // in order to find our target file
        String cleansedUserId = strUUID.replaceAll("-","");
        String strFileIdName = ESPRESSO_IDX_FILE_PREFIX.concat(cleansedUserId);
        String cleansedLevelSuffix = strLevelSuffix.replaceAll("-","");
        String strSearchUrl = strHatUrl.concat(DATASWYFT_FILE_CONTENT_PATH).concat(strFileIdName).concat(cleansedLevelSuffix).concat(ESPRESSO_IDX_FILE_TYPE);

        // search for a public.zip index file
        URL url = null;

        try {
            url = new URL(strSearchUrl);
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }

        HttpURLConnection con = null;

        try {
            con = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        try {
            con.setRequestMethod("GET");
        } catch (ProtocolException e) {
            throw new RuntimeException(e);
        }

        // Use the search party's credentials to do the search
        //String strAuthToken = getSearchPartyAccessToken();
        //String strAuthToken = getEspressoAccessToken();
        String strAuthToken = strAuth;

        con.setRequestProperty("Content-Type", "application/json");
        con.setRequestProperty("x-auth-token", strAuthToken);

        int responseCode = 0;
        try {
            responseCode = con.getResponseCode();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("Response Code: " + responseCode);

        // I'm not OK, you're not OK
        if(responseCode != 200) {
            return null;
        }

        // if we found the file, return it to read as a zip stream
        try {
            return con.getInputStream();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    // there's no reason this has to have its own function, apart from readability
    // we get two sets of creds: the search party's, and espresso's
    private static void extractEspressoAccessDetails(String strAuthResponse) {
        String strAuth = "";
        String strUserId = "";

        if (strAuthResponse.isEmpty()) {
            return;
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode node = mapper.readTree(strAuthResponse);
            strAuth = node.get("accessToken").asText();
            if(strAuth == null || strAuth.isEmpty()) {
                System.err.println("Failed to get an access token from ESPRESSO.");
                System.exit(1);
            }
            setEspressoAccessToken(strAuth);
            strUserId = node.get("userId").asText();
            if(strUserId == null || strUserId.isEmpty()) {
                System.err.println("Failed to get a user ID from ESPRESSO.");
                System.exit(1);
            }
            setEspressoUserId(strUserId);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private static void extractSearchPartyAccessDetails(String strAuthResponse) {
        String strAuth = "";
        String strUserId = "";

        if (strAuthResponse.isEmpty()) {
            return;
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode node = mapper.readTree(strAuthResponse);
            strAuth = node.get("accessToken").asText();
            if(strAuth == null || strAuth.isEmpty()) {
                System.err.println("User authentication failed.");
                System.exit(1);
            }
            setSearchPartyAccessToken(strAuth);
            strUserId = node.get("userId").asText();
            if(strUserId == null || strUserId.isEmpty()) {
                System.err.println("Failed to get a user ID from ESPRESSO.");
                System.exit(1);
            }
            setSearchPartyUserId(strUserId);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    private static String extractAuthToken(String strAuthResponse) {
        String strAuth = "";

        if (strAuthResponse.isEmpty()) {
            return strAuth;
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode node = mapper.readTree(strAuthResponse);
            strAuth = node.get("accessToken").asText();
            if(strAuth == null || strAuth.isEmpty()) {
                System.err.println("User authentication failed.");
                System.exit(1);
            }
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }

        return strAuth;
    }

    private static String extractUserId(String strAuthResponse) {
        String strUserId = "";

        if (strAuthResponse.isEmpty()) {
            return strUserId;
        }

        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode node = mapper.readTree(strAuthResponse);
            strUserId = node.get("userId").asText();
            if(strUserId == null || strUserId.isEmpty()) {
                System.err.println("Could not extract userId.");
                System.exit(1);
            }
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        return strUserId;
    }

    // there's no reason this has to have its own function, apart from readability
    // we get two sets of creds: the search party's, and espresso's
    private static String logIntoEspresso() {
        String strRet = "";

        URL url = null;
        try {
            url = new URL(ESPRESSO_URL.concat(AUTHTOKEN_PATH));
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
        HttpURLConnection con = null;
        try {
            con = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        try {
            con.setRequestMethod("GET");
        } catch (ProtocolException e) {
            throw new RuntimeException(e);
        }

        con.setRequestProperty("Accept", "application/json");
        con.setRequestProperty("username", ESPRESSO_USERNAME);
        con.setRequestProperty("password", ESPRESSO_PASSWORD);

        int responseCode = 0;
        try {
            responseCode = con.getResponseCode();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("Response Code: " + responseCode);

        strRet = returnResponseAsString(con);
        return strRet;
    }

    private static String logIntoEspressoServer(String strUrl, String strUsername) {
        String strRet = "";

        if (strUrl.isEmpty()) {
            return strRet;
        }

        URL url = null;
        try {
            url = new URL(strUrl.concat(AUTHTOKEN_PATH));
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
        HttpURLConnection con = null;
        try {
            con = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        try {
            con.setRequestMethod("GET");
        } catch (ProtocolException e) {
            throw new RuntimeException(e);
        }

        con.setRequestProperty("Accept", "application/json");
        con.setRequestProperty("username", strUsername);
        con.setRequestProperty("password", ESPRESSO_PASSWORD);

        int responseCode = 0;
        try {
            responseCode = con.getResponseCode();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("Response Code: " + responseCode);

        strRet = returnResponseAsString(con);
        return strRet;
    }

    private static String getUsernameFromURL(String strUrl) {
        String strUsername = "";

        if (strUrl.isEmpty()) return strUsername;

        if (strUrl.startsWith("http")) {
            int pos = strUrl.indexOf("://");
            if (pos != -1) {
                strUsername = strUrl.substring(pos + 3);
                pos = strUsername.indexOf(".");
                if (pos != -1) {
                    strUsername = strUsername.substring(0, pos);
                }
            }
        }

        return strUsername;
    }

    private static String returnResponseAsString(HttpURLConnection con) {
        if (con == null) {
            System.err.println("No connection from which to return response as string.");
            return null;
        }

        BufferedReader in = null;
        try {
            in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        String inputLine;
        StringBuilder response = new StringBuilder();

        while (true) {
            try {
                if (!((inputLine = in.readLine()) != null)) break;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            response.append(inputLine);
        }
        try {
            in.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        String strRet = response.toString();
        System.out.println("Response: " + strRet);
        return strRet;
    }

    private static String authenticateSearchParty() {
        String strRet = "";

        URL url = null;
        try {
            url = new URL("https://".concat(getSearchPartyUsername()).concat(getSearchPartyDomain()).concat(AUTHTOKEN_PATH));
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
        HttpURLConnection con = null;
        try {
            con = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        try {
            con.setRequestMethod("GET");
        } catch (ProtocolException e) {
            throw new RuntimeException(e);
        }

        con.setRequestProperty("Accept", "application/json");
        con.setRequestProperty("username", getSearchPartyUsername());
        con.setRequestProperty("password", getSearchPartyPassword());

        int responseCode = 0;
        try {
            responseCode = con.getResponseCode();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.println("Response Code: " + responseCode);

        BufferedReader in = null;
        try {
            in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        String inputLine;
        StringBuilder response = new StringBuilder();

        while (true) {
            try {
                if (!((inputLine = in.readLine()) != null)) break;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            response.append(inputLine);
        }
        try {
            in.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        strRet = response.toString();
        System.out.println("Response: " + strRet);
        return strRet;
    }


    /**
     * Searches the local file system offline, simulating a search first at network level,
     * then server level, then pod level.
     * TODO adapt this from offline to online search
     *
     * @param strUUID The UUID of the search party.
     * @param queryStr The query string
     * @param initialRetrieve
     * @param model The model
     * @param layer The layer to search
     * @param topK
     */
    private static void searchByLevels(String strUUID, String queryStr, int initialRetrieve, String model, String layer, int topK) {
        // Index folder for network index
        String networkZipIndexFilePath = TEST_SINK_PATH.concat(TEST_OUTPUT_METAINDEX_PATH);
        // Path to UUID-specific network-level index
        String UUIDSpecificNetworkIndexPath = networkZipIndexFilePath.concat(strUUID).concat("/");
        // Full name of UUID-specific network index file
        String networkZipIndexFileName = strUUID.concat(NETWORK_LEVEL_IDX_FILE_SUFFIX);
        // hyphens will be stripped from the fileId
        networkZipIndexFileName = networkZipIndexFileName.replaceAll("-","");
        // Full path to UUID-specific network index file
        String fullPathToUUIDSpecificNetworkIndex = UUIDSpecificNetworkIndexPath.concat(networkZipIndexFileName);
        // Output path for network-level search results
        String networkLevelSearchResultsPath = SEARCH_RESULTS_PATH.concat(NETWORK_SEARCH_RESULTS_PATH);
        // Create the output path if it doesn't already exist
        File netresdir = new File(networkLevelSearchResultsPath);
        if (!netresdir.exists()) {
            netresdir.mkdirs();
        }
        // Path to UUID-specific network level results output
        String UUIDSpecificNetworkLevelResults = networkLevelSearchResultsPath.concat(strUUID.concat(NETWORK_SEARCH_RESULTS_FILE_SUFFIX));

        // do a network-level search
        if (strUUID.isEmpty()) {
            return;
        }

        InputStream instr = null;

        instr = fetchZipIndexFile(ESPRESSO_URL, strUUID, NETWORK_LEVEL_IDX_FILE_SUFFIX, getEspressoAccessToken());
            if (instr != null) {
                // DEV output the search results to the local file structure
                networkLevelSearchResultsPath = UUIDSpecificNetworkLevelResults;
                // if the output folders don't exist, create them.
                netresdir = new File(networkLevelSearchResultsPath);
                if (!netresdir.exists()) {
                    netresdir.mkdirs();
                }
                List<String> foundServers = conductSearch(instr, queryStr, initialRetrieve, model, layer, topK, strUUID, networkLevelSearchResultsPath);

                // look only in the servers where we know there are results
                if ((foundServers != null) && (foundServers.size() > 0)) {
                    // do a server-level search
                    int numServers = foundServers.size();
                    for (int i = 0; i < numServers; i++) {
                        String serverLevelUUIDSpecificResultsPath = SEARCH_RESULTS_PATH.concat(SERVER_SEARCH_RESULTS_PATH).concat(strUUID).concat("/");
                        String servername = "";
                        // Full path to UUID-specific server-level results output
                        String serverLevelSearchResultsPath = "";
                        String UUIDSpecificServerLevelResults = "";

                        //for (int i = 0; i < serversToSearch.size(); i++) {
                        String nextServer = foundServers.get(i);
                        String servCreds = getEspressoServerCreds().get(nextServer);
                        String servAuth = extractAuthToken(servCreds);

                        instr = fetchZipIndexFile(nextServer, strUUID, SERVER_LEVEL_IDX_FILE_SUFFIX, servAuth);
                        if (instr != null) {
                            // DEV output the search results to the local file structure
                            if (foundServers.get(i).startsWith("http")) {
                                int pos = foundServers.get(i).indexOf("://");
                                if (pos != -1) {
                                    servername = foundServers.get(i).substring(pos + 3);
                                    serverLevelSearchResultsPath = serverLevelUUIDSpecificResultsPath.concat(servername);
                                    // if the output folders don't exist, create them.
                                    File servresdir = new File(serverLevelSearchResultsPath);
                                    if (!servresdir.exists()) {
                                        servresdir.mkdirs();
                                    }
                                    // Full path of UUID-specific server-level search results file
                                    UUIDSpecificServerLevelResults = serverLevelSearchResultsPath.concat(strUUID.concat(SERVER_LEVEL_RESULTS_SUFFIX));
                                    /*List<String> foundFiles = conductSearch(instr, queryStr, initialRetrieve, model, layer, topK, strUUID, UUIDSpecificPodLevelResults);
                                    // Output links to search results listed in a text file
                                    // which is what the results would look like to the search party
                                    String simpleResultsFile = podLevelUUIDSpecificResultsPath.concat("results.txt");
                                    try (BufferedWriter writer = new BufferedWriter(new FileWriter(simpleResultsFile, true))) {
                                        if(foundFiles != null && !foundFiles.isEmpty()) {
                                            for (String file : foundFiles) {
                                                // URL format in a HAT's file API: https://blorf.hubofallthings.net/api/v2.6/files/
                                                String fileToGet = (podsToSearch.get(i)).concat(DATASWYFT_FILE_PATH).concat(file);

                                                writer.write(fileToGet);
                                                writer.newLine();
                                            }
                                        }
                                        // close the simple results file
                                        writer.close();
                                    } catch (IOException ex) {
                                        ex.printStackTrace();
                                    }*/
                                }
                            }
                        }
                        //}

                    }

                }
            }





        // Now we've pinpointed the servers and pods containing results
        /*HashMap<String, List<String>> podsInServers = new HashMap<>();
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

        //}
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
        }*/
    }

    /**
     * Actually do the search. This is an offline search of the local file system.
     * @param zipStream Input stream from the index file from which to create the zip stream
     * @param queryStr The query string
     * @param initialRetrieve
     * @param model
     * @param layer
     * @param topK
     * @param strUUID UUID of the search party
     * @param resultsPath Path to search results output file
     * @return A List of Strings representing the locations (servers, pods, files) where results were found
     */
    private static List<String> conductSearch(InputStream zipStream, String queryStr, int initialRetrieve, String model, String layer, int topK, String strUUID, String resultsPath) {
        if(zipStream == null) return null;

        RAMDirectory ramDirectory = new RAMDirectory();

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