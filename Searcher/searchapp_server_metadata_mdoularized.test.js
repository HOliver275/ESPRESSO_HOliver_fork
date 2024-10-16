
const AxiosMockAdapter = require('axios-mock-adapter');
const supertest = require('supertest');
const {
    fetchFile,
    getWebIdData,
    getKeywordFileData,
    readAllSources,
    integrateResults,
    handleQuery,
    readSourcesWithSrvrMetadata,
    app,
    axiosInstance
} = require('./searchapp_server_metadata_mdoularized'); // Importing the required funct
// Create an Axios mock adapter for the axios instance used in fetchFile
const mock = new AxiosMockAdapter(axiosInstance);
const request = require('supertest');

describe('fetchFile', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should return file data when a valid URL is provided', async () => {
        const url = 'http://example.com/file.txt';
        const mockData = 'line1\r\nline2\r\nline3'; // Mock data

        // Mocking the GET request for a valid URL
        mock.onGet(url).reply(200, mockData);

        const result = await fetchFile(url);
        console.log(`Test result: ${result}`); // Log the result for debugging
        expect(result).toEqual(['line1', 'line2', 'line3']); // Assert the result
    });

    test('should return null when an invalid URL is provided', async () => {
        const url = 'http://example.com/invalid-url';

        // Mocking the GET request for an invalid URL (404 Not Found)
        mock.onGet(url).reply(404);

        const result = await fetchFile(url);
        expect(result).toBeNull(); // Assert that the result is null
    });

    test('should handle errors correctly', async () => {
        const url = 'http://example.com/error-url';

        // Mocking the GET request to simulate an error (500 Internal Server Error)
        mock.onGet(url).reply(500);

        const result = await fetchFile(url);
        expect(result).toBeNull(); // Assert that the result is null
    });
});

describe('getWebIdData', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should return pod URLs and user handle when valid data is fetched', async () => {
        const baseUrl = 'https://example.com/';
        const webIdQuery = 'user1'; // Sample WebID query
        const serverIndexUrl = 'http://example.com/'; // Base server index URL
        const userWebIdUrl = `${serverIndexUrl}${webIdQuery}.webid`;

        // Mock data for the .webid file
        const mockWebIdData = 'user1,Handle1\r\npod1,/pod1/\r\npod2,/pod2/'; // Mock WebID data

        // Mocking the GET request for the user webId URL
        mock.onGet(userWebIdUrl).reply(200, mockWebIdData);

        const { podUrls, userHandle } = await getWebIdData(baseUrl, webIdQuery, serverIndexUrl);

        console.log({ podUrls, userHandle }); // Log output for debugging

        // Expected results
        const expectedPodUrls = {
            pod1: 'https://example.com//pod1/espressoindex/',
            pod2: 'https://example.com//pod2/espressoindex/',
        };

        expect(podUrls).toEqual(expectedPodUrls); // Assert pod URLs
        expect(userHandle).toEqual('Handle1'); // Assert user handle
    });
});

describe('getKeywordFileData', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should return file data for a valid keyword', async () => {
        const serverIndexUrl = 'http://example.com/';
        const keyword = 'testKeyword';
        const keywordFileUrl = `${serverIndexUrl}${keyword.split('').join('/')}.ndx`; // Constructed URL

        const mockData = 'keywordData1\r\nkeywordData2\r\nkeywordData3'; // Mock data

        // Mocking the GET request for the keyword file URL
        mock.onGet(keywordFileUrl).reply(200, mockData);

        const result = await getKeywordFileData(serverIndexUrl, keyword);
        console.log(`Test result: ${result}`); // Log the result for debugging
        expect(result).toEqual(['keywordData1', 'keywordData2', 'keywordData3']); // Assert the result
    });

    test('should return null for an invalid keyword', async () => {
        const serverIndexUrl = 'http://example.com/';
        const keyword = 'invalidKeyword';
        const keywordFileUrl = `${serverIndexUrl}${keyword.split('').join('/')}.ndx`; // Constructed URL

        // Mocking the GET request for an invalid keyword file URL (404 Not Found)
        mock.onGet(keywordFileUrl).reply(404);

        const result = await getKeywordFileData(serverIndexUrl, keyword);
        expect(result).toBeNull(); // Assert that the result is null
    });

    test('should handle errors for keyword file fetch', async () => {
        const serverIndexUrl = 'http://example.com/';
        const keyword = 'errorKeyword';
        const keywordFileUrl = `${serverIndexUrl}${keyword.split('').join('/')}.ndx`; // Constructed URL

        // Mocking the GET request to simulate an error (500 Internal Server Error)
        mock.onGet(keywordFileUrl).reply(500);

        const result = await getKeywordFileData(serverIndexUrl, keyword);
        expect(result).toBeNull(); // Assert that the result is null
    });
});

describe('readAllSources', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should return sources when valid URL is provided', async () => {
        const baseUrl = 'http://example.com/';
        const metaIndexName = 'testMetaIndex.ndx';
        const mockData = 'pod1\r\npod2\r\npod3'; // Mock data

        // Mocking the GET request for the meta index
        mock.onGet(`${baseUrl}ESPRESSO/${metaIndexName}`).reply(200, mockData);

        const result = await readAllSources(baseUrl, metaIndexName);
        console.log(`Test result: ${result}`); // Log the result for debugging
        expect(result).toEqual(['pod1', 'pod2', 'pod3']); // Assert expected sources
    });

    test('should return empty array when an error occurs', async () => {
        const baseUrl = 'http://example.com/';
        const metaIndexName = 'testMetaIndex.ndx';

        // Mocking the GET request for the meta index to simulate an error (404 Not Found)
        mock.onGet(`${baseUrl}ESPRESSO/${metaIndexName}`).reply(404);

        const result = await readAllSources(baseUrl, metaIndexName);
        console.log(`Test result when error occurs: ${result}`); // Log the result for debugging
        expect(result).toEqual([]); // Expecting an empty array when error occurs
    });
});


describe('readAllSources', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should return selected pods for a valid URL', async () => {
        // Arrange
        const baseUrl = 'http://example.com/';
        const metaIndexName = 'validMetaIndex';
        const responseData = 'pod1,pod1_url\r\npod2,pod2_url\r\n';

        mock.onGet(`${baseUrl}ESPRESSO/${metaIndexName}`).reply(200, responseData);

        // Act
        const result = await readAllSources(baseUrl, metaIndexName);

        // Assert
        expect(result).toEqual(['pod1,pod1_url', 'pod2,pod2_url']);
    });

    test('should return an empty array for an invalid URL', async () => {
        // Arrange
        const baseUrl = 'http://invalid-url.com/';
        const metaIndexName = 'invalidMetaIndex';

        mock.onGet(`${baseUrl}ESPRESSO/${metaIndexName}`).reply(404); // Simulate a 404 error

        // Act
        const result = await readAllSources(baseUrl, metaIndexName);

        // Assert
        expect(result).toEqual([]);
    });

    test('should return an empty array when no input parameters are provided', async () => {
        // Act
        const result = await readAllSources(undefined, undefined);

        // Assert
        expect(result).toEqual([]);
    });
});
describe('integrateResults', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should integrate results from valid sources', async () => {
        // Arrange
        const sources = ['http://example.com/espressoindex/source1/', 'http://example.com/espressoindex/source2/'];
        const webIdQuery = 'testWebIdQuery';
        const searchWord = 'testKeyword';

        const webIdResponse1 = 'fileId1,fileName1\r\nfileId2,fileName2\r\n';
        const webIdResponse2 = 'fileId3,fileName3\r\nfileId4,fileName4\r\n';
        const ndxResponse1 = 'fileId1,5\r\nfileId2,10\r\n';
        const ndxResponse2 = 'fileId3,15\r\nfileId4,20\r\n';

        // Mock responses for the sources
        mock.onGet(`${sources[0]}${searchWord.split('').join('/')}.ndx`).reply(200, ndxResponse1);
        mock.onGet(`${sources[0]}${webIdQuery}.webid`).reply(200, webIdResponse1);
        mock.onGet(`${sources[1]}${searchWord.split('').join('/')}.ndx`).reply(200, ndxResponse2);
        mock.onGet(`${sources[1]}${webIdQuery}.webid`).reply(200, webIdResponse2);

        // Act
        const result = await integrateResults(sources, webIdQuery, searchWord);

        // Assert
        expect(result).toEqual([
            { address: 'http://example.com/source1/fileName1', frequency: '5' },
            { address: 'http://example.com/source1/fileName2', frequency: '10' },
            { address: 'http://example.com/source2/fileName3', frequency: '15' },
            { address: 'http://example.com/source2/fileName4', frequency: '20' }
        ]);
    });

    test('should handle invalid URLs', async () => {
        // Arrange
        const sources = ['http://invalid.url/'];
        const webIdQuery = 'testWebIdQuery';
        const searchWord = 'testKeyword';

        // Mock response for the invalid URL
        mock.onGet(`${sources[0]}${searchWord.split('').join('/')}.ndx`).reply(404);
        mock.onGet(`${sources[0]}${webIdQuery}.webid`).reply(404);

        // Act
        const result = await integrateResults(sources, webIdQuery, searchWord);

        // Assert
        expect(result).toEqual([]); // Expecting no results on error
    });

    test('should return empty array when no input is provided', async () => {
        // Act
        const result = await integrateResults([], 'testWebIdQuery', 'testKeyword');

        // Assert
        expect(result).toEqual([]); // Expecting empty results
    });

    test('should handle request errors gracefully', async () => {
        // Arrange
        const sources = ['http://example.com/espressoindex/source1/'];
        const webIdQuery = 'testWebIdQuery';
        const searchWord = 'testKeyword';

        // Mock responses with one failing request
        mock.onGet(`${sources[0]}${searchWord.split('').join('/')}.ndx`).reply(200, 'fileId1,5\r\n');
        mock.onGet(`${sources[0]}${webIdQuery}.webid`).reply(500); // Simulate server error

        // Act
        const result = await integrateResults(sources, webIdQuery, searchWord);

        // Assert
        expect(result).toEqual([]); // Expecting no results due to the error
    });
});
describe('handleQuery Vulnerability Tests', () => {
    afterEach(() => {
        mock.reset(); // Reset the mock after each test
    });

    test('should handle SQL injection attempts gracefully', async () => {
        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: "'; DROP TABLE users; --,user1" // SQL Injection attempt
            }
        };
        const res = {
            json: jest.fn(), // Mock json response
            send: jest.fn() // Mock send response
        };

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.json).toHaveBeenCalled(); // Check that a response was sent
        expect(res.send).not.toHaveBeenCalledWith(expect.stringContaining("DROP TABLE")); // Ensure sensitive data is not leaked
    });

    test('should handle XSS attempts gracefully', async () => {
        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: '<script>alert("xss")</script>,user1' // XSS attack
            }
        };
        const res = {
            json: jest.fn(),
            send: jest.fn()
        };

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.json).toHaveBeenCalled(); // Check that a response was sent
        expect(res.send).not.toHaveBeenCalledWith(expect.stringContaining("<script>")); // Ensure sensitive data is not leaked
    });

    test('should return an error response for malformed input', async () => {
        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: '' // Malformed input
            }
        };
        const res = {
            json: jest.fn(),
            send: jest.fn()
        };

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.send).toHaveBeenCalledWith("invalid keyword"); // Ensure proper error response
    });

    test('should not expose sensitive error details in case of internal errors', async () => {
        // Simulating an internal error
        jest.spyOn(global.console, 'log'); // Mock console.log to avoid cluttering test output

        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: 'validKeyword,user1'
            }
        };
        const res = {
            json: jest.fn(),
            send: jest.fn()
        };

        // Mock the integrateResults function to throw an error
        jest.spyOn(require('./Searcher'), 'integrateResults').mockImplementationOnce(() => {
            throw new Error("Internal server error");
        });

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.send).toHaveBeenCalledWith(expect.stringContaining("An error occurred")); // Ensure the error message is generic
        expect(console.log).toHaveBeenCalledWith(expect.stringContaining("Internal server error")); // Log the actual error for debugging, without exposing it to the client
    });

    test('should handle XSS attempts gracefully', async () => {
        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: '<script>alert("xss")</script>,user1' // XSS attack
            }
        };
        const res = {
            json: jest.fn(),
            send: jest.fn()
        };

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.json).toHaveBeenCalled(); // Check that a response was sent
        expect(res.send).not.toHaveBeenCalledWith(expect.stringContaining("<script>")); // Ensure sensitive data is not leaked
    });

    test('should return an error response for malformed input', async () => {
        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: '' // Malformed input
            }
        };
        const res = {
            json: jest.fn(),
            send: jest.fn()
        };

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.send).toHaveBeenCalledWith("invalid keyword"); // Ensure proper error response
    });

    test('should not expose sensitive error details in case of internal errors', async () => {
        // Simulating an internal error
        jest.spyOn(global.console, 'log'); // Mock console.log to avoid cluttering test output

        const urlArgument = 'valid-url';
        const metaIndexName = 'testMetaIndex';
        const req = {
            query: {
                keyword: 'validKeyword,user1'
            }
        };
        const res = {
            json: jest.fn(),
            send: jest.fn()
        };

        // Mock the integrateResults function to throw an error
        jest.spyOn(require('./Searcher'), 'integrateResults').mockImplementationOnce(() => {
            throw new Error("Internal server error");
        });

        await handleQuery(req, res, urlArgument, metaIndexName);

        expect(res.send).toHaveBeenCalledWith(expect.stringContaining("An error occurred")); // Ensure the error message is generic
        expect(console.log).toHaveBeenCalledWith(expect.stringContaining("Internal server error")); // Log the actual error for debugging, without exposing it to the client
    });
});

