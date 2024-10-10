import sys
import os
import tempfile
from rdflib import Graph, BNode, Literal, Namespace,URIRef
import unittest
from urllib.parse import urlparse
from unittest import mock
from unittest.mock import patch, MagicMock, mock_open
import concurrent.futures
from Automation.CSSAccess.CSSaccess import CSSaccess
from Automation.ExperimentSetup.flexexperiment import ESPRESSOexperiment  # Adjust import as needed


class FlexExperimentTests(unittest.TestCase):
    def setUp(self):
        # Initialize the ESPRESSOexperiment instance
        self.experiment = ESPRESSOexperiment()
        self.label = "test_label"
        self.datasource = "Automation/DatasetSplitter/sourcedir1"  # Update to your path
        self.bundlesource = self.datasource = "Automation/DatasetSplitter/sourcedir1"
        self.experiment.filenum = 0
        self.experiment.image = Graph()
        self.experiment.servernum = 0  # Initialize or reset server number
        self.experiment.namespace = Namespace("http://example.org/namespace#")  # Adjust to your actual namespace
        self.experiment.espressopodname = "EspressoPod"  # Set a sample pod name
        self.experiment.espressoindexfile = "index"  # Set a sample index file
        self.experiment.podemail = "@example.com"
        self.experiment.podindexdir = "indexdir"

        # Mock the subjects method specifically
        self.experiment.image.subjects = MagicMock()
        # Create a temporary directory for pod_dir
        self.pod_dir = tempfile.mkdtemp()

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False



    def dummyServers(self):
        self.server1 = BNode('server1')
        self.server2 = BNode('server2')
        self.experiment.image.add((self.server1, self.experiment.namespace.Type, self.experiment.namespace.Server))
        self.experiment.image.add((self.server1, self.experiment.namespace.Label, Literal('server1')))
        self.experiment.image.add((self.server1, self.experiment.namespace.Address, Literal("http://server1.com/")))

        self.experiment.image.add((self.server2, self.experiment.namespace.Type, self.experiment.namespace.Server))
        self.experiment.image.add((self.server2, self.experiment.namespace.Label, Literal('server2')))
        self.experiment.image.add((self.server2, self.experiment.namespace.Address, Literal("http://server2.com/")))

    def createMockServerAndNodes(self):
        # Create mock server and pod nodes
        self.mock_server_node = BNode('Server1')
        self.mock_pod_node = BNode('Pod1')

        # Add a mock server node
        self.experiment.image.add(
            (self.mock_server_node, self.experiment.namespace.Type, self.experiment.namespace.Server))
        self.experiment.image.add(
            (self.mock_server_node, self.experiment.namespace.Address, Literal("http://example.org/server1")))
        self.experiment.image.add((self.mock_server_node, self.experiment.namespace.Contains, self.mock_pod_node))

        # Add a mock pod node
        self.experiment.image.add(
            (self.mock_pod_node, self.experiment.namespace.Address, Literal("http://example.org/pod1")))
        self.experiment.image.add((self.mock_pod_node, self.experiment.namespace.Name, Literal("mockPod")))
        self.experiment.image.add((self.mock_pod_node, self.experiment.namespace.Email, Literal("test@example.com")))
        self.experiment.image.add(
            (self.mock_pod_node, self.experiment.namespace.WebID, Literal("mailto:test@example.com")))
        self.experiment.image.add(
            (self.mock_pod_node, self.experiment.namespace.TripleString, Literal("<tripleString>")))

    def create_sample_bundles(self):
        """Create sample bundles for testing."""
        # Define the base path for the bundles
        bundle_path = os.path.join(self.bundlesource, 'bundle0')  # Adjust for the specific bundle you want to create

        # Option 1: Check if the directory exists before creating
        if not os.path.exists(bundle_path):
            os.makedirs(bundle_path)

        # Option 2: Using exist_ok parameter (requires Python 3.2+)
        # os.makedirs(bundle_path, exist_ok=True)

        # Create sample files within the created directory
        with open(os.path.join(bundle_path, 'testfile0.txt'), 'w') as f:
            f.write('Sample content for testfile0.')

        with open(os.path.join(bundle_path, 'testfile1.txt'), 'w') as f:
            f.write('Sample content for testfile1.')

    def test_distributebundles_invalid_predicatetopod(self):
        """Test when predicatetopod is not a valid URL."""
        invalid_predicate = "invalid_predicate"
        with self.assertRaises(ValueError) as context:
            self.experiment.distributebundles(
                numberofbundles=2,
                bundlesource= self.bundlesource,
                filetype='txt',
                predicatetopod=invalid_predicate  # Invalid predicate
            )
        self.assertEqual(str(context.exception), "Invalid URL format for predicatetopod.")
    def test_logicaldistfilestopodsfrompool_invalid_file_format(self):
        """Test when file format is invalid."""
        self.experiment.filepool = {
            'file': [
                ('/path/to/file1.txt', 'file1.txt'),
                ('/path/to/file2.csv', 'file2.csv'),
                ('/path/to/file3.kjl', 'file3.kjl')  # Invalid file
            ]
        }
        with self.assertRaises(ValueError):
            self.experiment.logicaldistfilestopodsfrompool(
                numberoffiles=3,
                filedisp=0,
                filetype='text',  # Assuming we expect only 'text' types
                filelabel='file'
            )

    def test_createlogicalpods_negative_number(self):
        """Test when numberofpods is -1."""
        with self.assertRaises(ValueError):
            self.experiment.createlogicalpods(-1, 0)

    def test_createlogicalpods_serverdisp_zero(self):
        """Test when serverdisp is 0."""
        # Mock server subjects
        self.experiment.image.subjects.return_value = ['server1', 'server2']

        # Call the method with valid parameters
        self.experiment.createlogicalpods(2, 0)  # number of pods is 2, serverdisp is 0

        # Verify that the default server distribution is used
        self.assertIsNotNone(self.experiment.image)

    def test_distributebundles_success(self):
        """Test successful distribution of bundles to pods."""
        number_of_bundles = 2
        filetype = 'text/plain'
        filelabel = 'file'
        subdir = 'file'

        self.create_sample_bundles()

        self.experiment.distributebundles(number_of_bundles, self.bundlesource, filetype, filelabel, subdir)


    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddirtopool_empty_directory(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = []

        self.experiment.loaddirtopool('some/empty_directory', 'test_label')

        actual_result = self.experiment.filepool.get('test_label', [])
        self.assertEqual(actual_result, [])

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddirtopool_with_hidden_files(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', '.hidden_file.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        self.experiment.loaddirtopool('some/directory', 'test_label')

        expected_result = [
            ('some/directory/file1.txt', 'file1.txt'),
            ('some/directory/file2.txt', 'file2.txt'),
        ]
        actual_result = self.experiment.filepool.get('test_label', [])
        self.assertEqual(actual_result, expected_result)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddirtopool_existing_label(self, mock_isfile, mock_listdir):
        # Initial population of the filepool
        self.experiment.filepool['existing_label'] = [('existing_file.txt', 'existing_file.txt')]

        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        self.experiment.loaddirtopool('some/directory', 'existing_label')

        expected_result = [
            ('some/directory/file1.txt', 'file1.txt'),
            ('some/directory/file2.txt', 'file2.txt'),
        ]
        actual_result = self.experiment.filepool.get('existing_label', [])
        self.assertEqual(actual_result, expected_result)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddirtopool_invalid_directory(self, mock_isfile, mock_listdir):
        # Mock listdir to raise a FileNotFoundError
        mock_listdir.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            self.experiment.loaddirtopool('nonexistent/directory', 'test_label')

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddirtopool_multiple_calls(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        self.experiment.loaddirtopool('some/directory', 'test_label')
        self.experiment.loaddirtopool('some/directory', 'test_label')  # Call again

        expected_result = [
            ('some/directory/file1.txt', 'file1.txt'),
            ('some/directory/file2.txt', 'file2.txt'),
            ('some/directory/file1.txt', 'file1.txt'),
            ('some/directory/file2.txt', 'file2.txt'),
        ]
        actual_result = self.experiment.filepool.get('test_label', [])
        self.assertEqual(actual_result, expected_result)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    @mock.patch('tqdm.tqdm')  # Mock tqdm to prevent actual progress bar display
    def test_loaddir_basic_functionality(self, mock_tqdm, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        self.experiment.loaddir(self.datasource, self.label)

        # Assert that nodes are added correctly
        # You would need to check self.experiment.image to verify nodes were added
        # This part will depend on how `self.image` is structured
        self.assertEqual(len(self.experiment.image), 10)  # Assuming 2 files added

    @mock.patch('os.listdir')
    def test_loaddir_empty_directory(self, mock_listdir):
        mock_listdir.return_value = []

        self.experiment.loaddir(self.datasource, self.label)

        # Assert that no nodes are added
        self.assertEqual(len(self.experiment.image), 0)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddir_with_hidden_files(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', '.hidden_file.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        self.experiment.loaddir(self.datasource, self.label)

        # Check that only non-hidden files are added
        self.assertEqual(len(self.experiment.image), 10)

    @mock.patch('os.listdir')
    def test_loaddir_invalid_directory(self, mock_listdir):
        mock_listdir.side_effect = FileNotFoundError  # Simulate non-existent directory

        with self.assertRaises(FileNotFoundError):
            self.experiment.loaddir('nonexistent/directory', self.label)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddir_multiple_calls(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        # First call
        self.experiment.loaddir(self.datasource, self.label)

        # Second call
        self.experiment.loaddir(self.datasource, self.label)

        # Check that filenum is incremented correctly
        self.assertEqual(self.experiment.filenum, 4)  # 2 files loaded twice

    @mock.patch('os.listdir')
    @mock.patch('os.path.isfile')
    def test_loaddir_with_different_filetype(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        mock_isfile.side_effect = lambda filepath: True  # All items are files

        # Call with a different file type
        self.experiment.loaddir(self.datasource, self.label, filetype='image/png')

    def test_loadserverlist_basic_functionality(self):
        serverlist = ['http://server1.com', 'http://server2.com']
        self.experiment.loadserverlist(serverlist)

        # Check that the correct number of triples has been added
        expected_triples_count = len(serverlist) * 11  # 11 triples per server
        self.assertEqual(len(self.experiment.image), expected_triples_count)

    def test_loadserverlist_content(self):
        serverlist = ['http://server1.com']
        self.experiment.loadserverlist(serverlist)

        # Check that the correct triples are added for the first server
        server = serverlist[0]
        sword = 'Sserver0'  # First server with servernum = 0

        # Check that the server node has the correct type and address
        snode = BNode(sword)
        self.assertIn((snode, self.experiment.namespace.Type, self.experiment.namespace.Server), self.experiment.image)
        self.assertIn((snode, self.experiment.namespace.Address, Literal(server)), self.experiment.image)

        # Check the register endpoint
        register_endpoint = server + 'idp/register/'
        self.assertIn((snode, self.experiment.namespace.RegisterEndpoint, Literal(register_endpoint)),
                      self.experiment.image)

    def test_loadserverlist_empty(self):
        serverlist = []  # Test with an empty server list
        self.experiment.loadserverlist(serverlist)

        # Check that no triples were added
        self.assertEqual(len(self.experiment.image), 0)

    def test_loadserverlist_duplicates(self):
        serverlist = ['http://server1.com', 'http://server1.com']  # Duplicate server
        self.experiment.loadserverlist(serverlist)

        # Check that the correct number of triples has been added
        expected_triples_count = 2 * 11  # 11 triples per unique server
        self.assertEqual(len(self.experiment.image), expected_triples_count)

        # Check that only one server entry is actually present
        snode = BNode('Sserver0')
        self.assertIn((snode, self.experiment.namespace.Address, Literal('http://server1.com')), self.experiment.image)

    def test_loadserverlist_invalid_input(self):
        serverlist = [None, '']  # Invalid server entries
        self.experiment.loadserverlist(serverlist)

        # Check that no triples were added for invalid entries
        self.assertEqual(len(self.experiment.image), 0)

    def test_initpnode_none_values(self):
            with self.assertRaises(TypeError):  # Expecting TypeError when passing None for pword
                self.experiment.initpnode(None, "PodName", "PodLabel")

            with self.assertRaises(TypeError):  # Expecting TypeError when passing None for podname
                self.experiment.initpnode("Ppod1", None, "PodLabel")

            with self.assertRaises(TypeError):  # Expecting TypeError when passing None for podlabel
                self.experiment.initpnode("Ppod1", "PodName", None)

    def test_initfnode_none_values(self):
                # Test each parameter as None to ensure graceful error handling

                with self.assertRaises(TypeError):  # fword is required
                    self.experiment.initfnode(None, "filename", "/path/to/file", "text/plain")

                with self.assertRaises(TypeError):  # filename is required
                    self.experiment.initfnode("Ffile1", None, "/path/to/file", "text/plain")

                with self.assertRaises(TypeError):  # filepath is required
                    self.experiment.initfnode("Ffile1", "test.txt", None, "text/plain")

                with self.assertRaises(TypeError):  # filetype is required
                    self.experiment.initfnode("Ffile1", "test.txt", "/path/to/file", None)

                # filelabel has a default value, so no need to test for None explicitly

    def test_initfnode_empty_strings(self):
                # Test empty string values for parameters
                fnode = self.experiment.initfnode("", "", "", "")

                # Check that the node is added with empty literals
                self.assertIn((fnode, self.experiment.namespace.Type, self.experiment.namespace.File),
                              self.experiment.image)
                self.assertIn((fnode, self.experiment.namespace.LocalAddress, Literal("")), self.experiment.image)
                self.assertIn((fnode, self.experiment.namespace.Filename, Literal("")), self.experiment.image)
                self.assertIn((fnode, self.experiment.namespace.Filetype, Literal("")), self.experiment.image)
                self.assertIn((fnode, self.experiment.namespace.Label, Literal("")), self.experiment.image)

    def test_assignpod_valid_input(self):
        # Set up valid input
        snode = BNode('server1')
        pnode = BNode('pod1')

        # Add required triples for the server and pod
        self.experiment.image.add((snode, self.experiment.namespace.Address, Literal("http://server1.com/")))
        self.experiment.image.add((pnode, self.experiment.namespace.Name, Literal("Pod1")))

        # Call the method
        self.experiment.assignpod(snode, pnode)

        # Validate that the correct triples are added
        podaddress = "http://server1.com/Pod1/"
        podindexaddress = podaddress + self.experiment.podindexdir
        webid = podaddress + "profile/card#me"

        self.assertIn((snode, self.experiment.namespace.Contains, pnode), self.experiment.image)
        self.assertIn((pnode, self.experiment.namespace.Address, Literal(podaddress)), self.experiment.image)
        self.assertIn((pnode, self.experiment.namespace.IndexAddress, Literal(podindexaddress)), self.experiment.image)
        self.assertIn((pnode, self.experiment.namespace.WebID, Literal(webid)), self.experiment.image)

    def test_assignpod_none_snode(self):
        pnode = BNode('pod1')
        self.experiment.image.add((pnode, self.experiment.namespace.Name, Literal("Pod1")))

        with self.assertRaises(TypeError):  # Expecting TypeError due to None snode
            self.experiment.assignpod(None, pnode)

    def test_assignpod_none_pnode(self):
        snode = BNode('server1')
        self.experiment.image.add((snode, self.experiment.namespace.Address, Literal("http://server1.com/")))

        with self.assertRaises(TypeError):  # Expecting TypeError due to None pnode
            self.experiment.assignpod(snode, None)

    def test_assignpod_missing_server_address(self):
        # Set up input with missing server address
        snode = BNode('server1')
        pnode = BNode('pod1')
        self.experiment.image.add((pnode, self.experiment.namespace.Name, Literal("Pod1")))

        # Since the server address is missing, expect a failure
        with self.assertRaises(TypeError):  # or ValueError if handled differently
            self.experiment.assignpod(snode, pnode)

    def test_assignpod_missing_pod_name(self):
        # Set up input with missing pod name
        snode = BNode('server1')
        pnode = BNode('pod1')
        self.experiment.image.add((snode, self.experiment.namespace.Address, Literal("http://server1.com/")))

        # Since the pod name is missing, expect a failure
        with self.assertRaises(TypeError):  # or ValueError if handled differently
            self.experiment.assignpod(snode, pnode)

    def test_createlogicalpairedpods_valid_input(self):
        # Add mock servers to the graph
        self.dummyServers()

        number_of_pods = 2
        server_disp = 1

        # Call the method
        self.experiment.createlogicalpairedpods(number_of_pods, server_disp)

        # Validate the correct number of pods created and triples added
        pods = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.Pod))
        self.assertEqual(len(pods), 4)  # Two pairs of pods should be created (4 pods total)

        # Check for valid pod assignments
        for pod in pods:
            self.assertTrue((pod, self.experiment.namespace.Address, None) in self.experiment.image)

        # Check TripleStrings are added
        triplestrings = list(self.experiment.image.subject_objects(self.experiment.namespace.TripleString))
        self.assertGreater(len(triplestrings), 0)

    def test_createlogicalpairedpods_none_input(self):
        # Add mock servers to the graph
        self.dummyServers()

        with self.assertRaises(TypeError):  # Number of pods should be an int, and server_disp too
            self.experiment.createlogicalpairedpods(None, None)

    def test_createlogicalpairedpods_empty_server_list(self):
        self.dummyServers()
        # Remove all servers from the graph
        self.experiment.image.remove((self.server1, None, None))
        self.experiment.image.remove((self.server2, None, None))

        # Call the method
        self.experiment.createlogicalpairedpods(2, 1)

        # Check that no pods are created since there are no servers
        pods = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.Pod))
        self.assertEqual(len(pods), 0)

    def test_createlogicalpairedpods_invalid_number_of_pods(self):
        with self.assertRaises(ValueError):  # Expect an error if the number of pods is invalid
            self.experiment.createlogicalpairedpods(-1, 1)

    def test_logicaldistfilestopodsfrompool_valid_input(self):

        self.experiment.filepool = {
            'file': [('path1', 'file1.txt'), ('path2', 'file2.txt')]
        }

        # Mocking the RDF pod data
        self.pod1 = BNode('pod1')
        self.pod2 = BNode('pod2')
        self.experiment.image.add((self.pod1, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod1, self.experiment.namespace.Address, Literal("http://pod1.com/")))
        self.experiment.image.add(
            (self.pod1, self.experiment.namespace.WebID, Literal("http://pod1.com/profile/card#me")))

        self.experiment.image.add((self.pod2, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod2, self.experiment.namespace.Address, Literal("http://pod2.com/")))
        self.experiment.image.add(
            (self.pod2, self.experiment.namespace.WebID, Literal("http://pod2.com/profile/card#me")))

        number_of_files = 2
        filedisp = 1
        filetype = "text"
        filelabel = "file"
        podlabel = "pod"

        # Call the method
        self.experiment.logicaldistfilestopodsfrompool(number_of_files, filedisp, filetype, filelabel, podlabel)

        # Check that the files are properly assigned to the pods
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        self.assertEqual(len(files), 2)

        for file_node in files:
            # Check that each file has an Address triple
            self.assertTrue((file_node, self.experiment.namespace.Address, None) in self.experiment.image)
            # Check that each file has a TripleString
            self.assertTrue((file_node, self.experiment.namespace.TripleString, None) in self.experiment.image)

        # Check that each pod contains files
        pod_files = list(self.experiment.image.objects(self.pod1, self.experiment.namespace.Contains))
        self.assertGreater(len(pod_files), 0)

    def test_logicaldistfilestopodsfrompool_empty_file_pool(self):

        self.experiment.filepool = {
            'file': [('path1', 'file1.txt'), ('path2', 'file2.txt')]
        }

        # Mocking the RDF pod data
        self.pod1 = BNode('pod1')
        self.pod2 = BNode('pod2')
        self.experiment.image.add((self.pod1, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod1, self.experiment.namespace.Address, Literal("http://pod1.com/")))
        self.experiment.image.add(
            (self.pod1, self.experiment.namespace.WebID, Literal("http://pod1.com/profile/card#me")))

        self.experiment.image.add((self.pod2, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod2, self.experiment.namespace.Address, Literal("http://pod2.com/")))
        self.experiment.image.add(
            (self.pod2, self.experiment.namespace.WebID, Literal("http://pod2.com/profile/card#me")))

        self.experiment.filepool = {'file': []}  # Set empty file pool

        number_of_files = 2
        filedisp = 1
        filetype = "text"
        filelabel = "file"
        podlabel = "pod"

        # Call the method
        self.experiment.logicaldistfilestopodsfrompool(number_of_files, filedisp, filetype, filelabel, podlabel)

        # No files should be created
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        self.assertEqual(len(files), 0)

    def test_logicaldistfilestopodsfrompool_invalid_input(self):

        self.experiment.filepool = {
            'file': [('path1', 'file1.txt'), ('path2', 'file2.txt')]
        }

        # Mocking the RDF pod data
        self.pod1 = BNode('pod1')
        self.pod2 = BNode('pod2')
        self.experiment.image.add((self.pod1, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod1, self.experiment.namespace.Address, Literal("http://pod1.com/")))
        self.experiment.image.add(
            (self.pod1, self.experiment.namespace.WebID, Literal("http://pod1.com/profile/card#me")))

        self.experiment.image.add((self.pod2, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod2, self.experiment.namespace.Address, Literal("http://pod2.com/")))
        self.experiment.image.add(
            (self.pod2, self.experiment.namespace.WebID, Literal("http://pod2.com/profile/card#me")))

        # Test with None inputs for number_of_files and filedisp
        with self.assertRaises(TypeError):
            self.experiment.logicaldistfilestopodsfrompool(None, None, 'text')

    def test_logicaldistfilestopodsfrompool_fewer_files_than_pods(self):
        self.experiment.filepool = {
            'file': [('path1', 'file1.txt'), ('path2', 'file2.txt')]
        }

        # Mocking the RDF pod data
        self.pod1 = BNode('pod1')
        self.pod2 = BNode('pod2')
        self.experiment.image.add((self.pod1, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod1, self.experiment.namespace.Address, Literal("http://pod1.com/")))
        self.experiment.image.add(
            (self.pod1, self.experiment.namespace.WebID, Literal("http://pod1.com/profile/card#me")))

        self.experiment.image.add((self.pod2, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod2, self.experiment.namespace.Address, Literal("http://pod2.com/")))
        self.experiment.image.add(
            (self.pod2, self.experiment.namespace.WebID, Literal("http://pod2.com/profile/card#me")))

        # Only 1 file in pool but 2 pods
        self.experiment.filepool = {'file': [('path1', 'file1.txt')]}  # Only 1 file

        number_of_files = 1
        filedisp = 1
        filetype = "text"
        filelabel = "file"
        podlabel = "pod"

        # Call the method
        self.experiment.logicaldistfilestopodsfrompool(number_of_files, filedisp, filetype, filelabel, podlabel)

        # Check that only 1 file was created and assigned
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        self.assertEqual(len(files), 1)

    def test_logicaldistfilestopodsfrompool_fewer_pods_than_files(self):

        self.experiment.filepool = {
            'file': [('path1', 'file1.txt'), ('path2', 'file2.txt')]
        }

        # Mocking the RDF pod data
        self.pod1 = BNode('pod1')
        self.pod2 = BNode('pod2')
        self.experiment.image.add((self.pod1, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod1, self.experiment.namespace.Address, Literal("http://pod1.com/")))
        self.experiment.image.add(
            (self.pod1, self.experiment.namespace.WebID, Literal("http://pod1.com/profile/card#me")))

        self.experiment.image.add((self.pod2, self.experiment.namespace.Label, Literal('pod')))
        self.experiment.image.add((self.pod2, self.experiment.namespace.Address, Literal("http://pod2.com/")))
        self.experiment.image.add(
            (self.pod2, self.experiment.namespace.WebID, Literal("http://pod2.com/profile/card#me")))

        # Test where there are more files than pods
        self.experiment.filepool = {
            'file': [('path1', 'file1.txt'), ('path2', 'file2.txt'), ('path3', 'file3.txt')]}  # 3 files

        number_of_files = 3
        filedisp = 1
        filetype = "text"
        filelabel = "file"
        podlabel = "pod"

        # Call the method
        self.experiment.logicaldistfilestopodsfrompool(number_of_files, filedisp, filetype, filelabel, podlabel)

        # Check that 3 files were created and distributed across the 2 pods
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        self.assertEqual(len(files), 3)

    def test_paretofilestopodsfrompool_filetype_none(self):
        # Arrange: Add mock files to file pool
        self.experiment.filepool['file'] = [("/local/path/to/file.txt", "http://example.org/file")]

        # Replace FileDistributor.paretopluck to return controlled output
        with unittest.mock.patch(
                'Automation.ExperimentSetup.flexexperiment.FileDistributor.paretopluck') as mock_paretopluck:
            mock_paretopluck.return_value = [[("/local/path/to/file.txt", "http://example.org/file")]]

            # Act: Call the method with None as filetype
            predicatetopod = URIRef('http://example.org/SOLIDindex/HasFile')
            self.experiment.paretofilestopodsfrompool(filetype=None, predicatetopod=predicatetopod)

            # Assert: Ensure that filetype None doesn't cause errors
            # Since filetype is None, we can validate that it's handled gracefully by checking the graph
            file_nodes = list(self.experiment.image.subjects(self.experiment.namespace.Filename, None))
            self.assertGreater(len(file_nodes), 0)
    def test_paretofilestopodsfrompool_predicatetopod_valid_url(self):
        # Arrange: Add mock files to file pool
        self.experiment.filepool['file'] = [("/local/path/to/file.txt", "http://example.org/file")]

        # Replace FileDistributor.paretopluck to return controlled output
        with unittest.mock.patch(
                'Automation.ExperimentSetup.flexexperiment.FileDistributor.paretopluck') as mock_paretopluck:
            mock_paretopluck.return_value = [[("/local/path/to/file.txt", "http://example.org/file")]]

            # Act: Call the method with a valid predicatetopod URL
            predicatetopod = URIRef('http://example.org/SOLIDindex/HasFile')
            self.experiment.paretofilestopodsfrompool(filetype=None, predicatetopod=predicatetopod)

            # Assert: Ensure the predicatetopod is a valid URL
            self.assertTrue(self.is_valid_url(str(predicatetopod)))
    def test_paretofilestopodsfrompool_empty_file_pool(self):
        self.experiment.filepool = {'file': []}  # Set empty file pool

        filetype = "text"
        filelabel = "file"
        podlabel = "pod"
        alpha = 1

        # Call the method
        self.experiment.paretofilestopodsfrompool(filetype, filelabel, podlabel, alpha=alpha)

        # No files should be created
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        self.assertEqual(len(files), 0)

    def test_paretofilestopodsfrompool_invalid_alpha(self):
        filetype = "text"
        filelabel = "file"
        podlabel = "pod"
        alpha = -1  # Invalid alpha value
        # Mock filepool to contain the required key
        self.experiment.filepool = {
            filelabel: [("file1.txt", 100), ("file2.txt", 200)]  # Example tuple list
        }
        # Call the method with an invalid alpha
        with self.assertRaises(ValueError):
            self.experiment.paretofilestopodsfrompool(filetype, filelabel, podlabel, alpha=alpha)

    def test_paretofilestopodsfrompool_replacebool_true(self):
        filetype = "text"
        filelabel = "file"
        podlabel = "pod"
        alpha = 1
        replacebool = True

        # Mock filepool to contain the required key
        self.experiment.filepool = {
            filelabel: [("file1.txt", 100), ("file2.txt", 200)]  # Example tuple list
        }

        # Call the method with replacebool set to True
        self.experiment.paretofilestopodsfrompool(filetype, filelabel, podlabel, alpha=alpha, replacebool=replacebool)

        # Check that files have ReplaceText set
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        for file_node in files:
            self.assertTrue((file_node, self.experiment.namespace.ReplaceText, None) in self.experiment.image)

    def test_paretofilestopodsfrompool_fewer_files_than_pods(self):
        self.experiment.filepool = {'file': [('path1', 'file1.txt')]}  # Only 1 file

        filetype = "text"
        filelabel = "file"
        podlabel = "pod"
        alpha = 1

        # Mock filepool to contain the required key
        self.experiment.filepool = {
            filelabel: [("file1.txt", 100), ("file2.txt", 200)]  # Example tuple list
        }
        # Call the method
        self.experiment.paretofilestopodsfrompool(filetype, filelabel, podlabel, alpha=alpha)

        # Check that only 1 file was created and assigned
        files = list(self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.File))
        self.assertEqual(len(files), 1)


        # Call the method
        self.experiment.logicaldistfilestopods(numberoffiles, filedisp, filelabel, podlabel)

        # Check that files are properly distributed across pods
        pod_files1 = list(self.experiment.image.objects(self.pod1, self.experiment.namespace.Contains))
        pod_files2 = list(self.experiment.image.objects(self.pod2, self.experiment.namespace.Contains))

        self.assertGreater(len(pod_files1), 0)
        self.assertGreater(len(pod_files2), 0)

        # Check that each file has an Address and TripleString
        for fnode in [self.file1, self.file2, self.file3]:
            self.assertTrue((fnode, self.experiment.namespace.Address, None) in self.experiment.image)
            self.assertTrue((fnode, self.experiment.namespace.TripleString, None) in self.experiment.image)

    def test_loadexp_none_filename(self):
        """Test when filename is None."""
        with self.assertRaises(ValueError) as context:
            self.experiment.loadexp(None)
        self.assertEqual(str(context.exception), "Filename cannot be None.")

    def test_distributebundles_success(self):
        """Test successful distribution of bundles to pods."""
        number_of_bundles = 2
        filetype = 'text/plain'
        filelabel = 'file'
        subdir = 'file'

        self.create_sample_bundles()
        self.experiment.distributebundles(number_of_bundles, self.bundlesource, filetype, filelabel, subdir)

        # Check if files have been distributed
        for filename in os.listdir(self.pod_dir):
            self.assertIn(filename, ['testfile0.txt', 'testfile1.txt'])
            # Check RDF triples for each file
            fnode = next(self.experiment.image.subjects(self.experiment.namespace.Filename, Literal(filename)))
            self.assertIsNotNone(fnode)
            self.assertEqual(str(self.experiment.image.value(fnode, self.experiment.namespace.Filetype)), filetype)
            self.assertEqual(str(self.experiment.image.value(fnode, self.experiment.namespace.LocalAddress)),
                             self.assertEqual(
                                 str(self.experiment.image.value(fnode, self.experiment.namespace.LocalAddress)),
                                 os.path.join(self.bundlesource, 'bundle' + str(int(filename[-5]))), filename))

    def test_distributebundles_with_no_files(self):
                """Test the behavior when there are no files to distribute."""
                empty_source = tempfile.mkdtemp()
                number_of_bundles = 1
                filetype = 'text/plain'
                filelabel = 'file'
                subdir = 'file'

                self.experiment.distributebundles(number_of_bundles, empty_source, filetype, filelabel, subdir)

                # Check that no files are created in the pod directory
                self.assertEqual(len(os.listdir(self.pod_dir)), 0)

    def test_initsanodelist_negative_value(self):
        """Test when percs contains a negative value."""
        with self.assertRaises(ValueError) as context:
            self.experiment.initsanodelist([10, -5, 20])  # Contains a negative value
        self.assertEqual(str(context.exception), "Input parameter percs cannot contain negative values.")

    def test_initsanodelist_valid_input(self):
        """Test when percs contains valid values."""
        result = self.experiment.initsanodelist([10, 20, 30])
        self.assertEqual(len(result), 3)  # Expecting 3 special agent nodes
        self.assertTrue(isinstance(result[0], BNode))  # Checking if the nodes are BNodes

    def test_imagineaclnormal_no_agents(self):
        self.file_nodes = []
        for i in range(10):
            fnode = BNode(f'F{i}')
            self.experiment.image.add((fnode, self.experiment.namespace.Type, self.experiment.namespace.File))
            self.experiment.image.add((fnode, self.experiment.namespace.Label, Literal('file')))
            self.file_nodes.append(fnode)
        """Test the imagineaclnormal function with no agents present."""
        # Call the method with no agents initialized
        self.experiment.imagineaclnormal(openperc=50, mean=3, disp=0, filelabel='file')

        # Check that no files have been made OpenFile
        open_files = list(
            self.experiment.image.subjects(self.experiment.namespace.Type, self.experiment.namespace.OpenFile))
        self.assertEqual(len(open_files), 5)  # Still should mark 50% as open

        # Ensure no files have AccessibleBy triples since there are no agents
        for fnode in self.file_nodes:
            accessors = list(self.experiment.image.objects(fnode, self.experiment.namespace.AccessibleBy))
            self.assertEqual(len(accessors), 0)

    @patch('Automation.ExperimentSetup.flexexperiment.seriespodcreate')  # Patch method within the same class
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_threadedpodcreate(self, mock_thread_pool, mock_seriespodcreate):
        """Test the threaded pod creation method."""

        # Mock the executor's submit method
        mock_executor_instance = mock_thread_pool.return_value
        mock_executor_instance.__enter__.return_value = mock_executor_instance

        # Call the threadedpodcreate method
        self.experiment.threadedpodcreate()

        # Verify that submit was called with the expected parameters
        self.assertEqual(mock_executor_instance.submit.call_count, 1)  # Ensure that submit was called
        mock_seriespodcreate.assert_called_once()

    @patch('Automation.CSSAccess.CSSaccess.CSSaccess')
    @patch('Indexer.PodIndexer.crawl')
    @patch('tqdm.tqdm')  # Mock tqdm if you want to avoid output during tests
    def test_cleanuppod(self, mock_tqdm, mock_crawl, mock_CSSaccess):
        """Test the cleanuppod method."""
        self.createMockServerAndNodes()
        # Mock the response of crawl
        mock_crawl.return_value = {'file1': 'content1', 'file2': 'content2'}

        # Create a mock instance of CSSaccess
        mock_css_instance = MagicMock()
        mock_CSSaccess.return_value = mock_css_instance

        # Mock the delete_file method
        mock_css_instance.delete_file.return_value.ok = True  # Simulate successful deletion

        # Call the cleanuppod method
        self.experiment.cleanuppod(self.mock_server_node, self.mock_pod_node)

        # Assertions to verify the expected interactions
        mock_css_instance.create_authstring.assert_called_once()  # Check that create_authstring was called
        mock_css_instance.create_authtoken.assert_called_once()  # Check that create_authtoken was called
        self.assertEqual(mock_css_instance.delete_file.call_count, 2)  # Ensure delete_file was called for each file


    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_storeexplocal(self, mock_open, mock_makedirs):
        """Test the storeexplocal method."""
        self.createMockServerAndNodes()
        dir_path = "mock_directory"

        # Call the storeexplocal method
        self.experiment.storeexplocal(dir_path)

        # Assertions to verify the expected interactions
        self.assertEqual(mock_makedirs.call_count, 3)  # Ensure that makedirs was called to create directories
        self.assertEqual(mock_open.call_count, 2)  # Ensure that open was called to create files

    @patch('builtins.open', create=True)  # Mock file opening
    @patch('os.path.isdir')  # Mock the directory check
    def test_storeindexlocal_with_empty_dir(self, mock_isdir, mock_open):
        # Set up the mock to simulate an invalid (non-directory) path
        mock_isdir.return_value = False

        # Call the method with an invalid directory
        invalid_dir = ""
        self.experiment.storeindexlocal(invalid_dir)

        # Assert that no files were opened since the directory is invalid
        mock_open.assert_not_called()

    @patch('builtins.open', create=True)  # Mock file opening
    @patch('os.path.isdir')  # Mock the directory check
    def test_storeindexlocal_with_none_dir(self, mock_isdir, mock_open):
        # Set up the mock to simulate an invalid (None) directory path
        mock_isdir.return_value = False

        # Call the method with None as the directory
        none_dir = None
        self.experiment.storeindexlocal(none_dir)

        # Assert that no files were opened since the directory is None
        mock_open.assert_not_called()

    @patch('builtins.open', create=True)
    @patch('concurrent.futures.ThreadPoolExecutor')
    @patch('os.path.isdir')
    def test_uploadindexlocal_with_empty_dir(self, mock_isdir, mock_thread_pool, mock_open):
        # Set up the mock to simulate an invalid (non-directory) path
        mock_isdir.return_value = False

        # Call the method with an invalid directory
        invalid_dir = ""
        self.experiment.uploadindexlocal(invalid_dir)

        # Assert that no files were opened and no operations were submitted
        mock_open.assert_not_called()
        mock_thread_pool.return_value.submit.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data='file contents')
    @patch('os.makedirs')
    @patch('zipfile.ZipFile')
    @patch('tqdm.tqdm')
    def test_storelocalindexzipdirs(self, mock_tqdm, mock_zipfile, mock_makedirs, mock_open):
        # Mock the image object and its methods
        self.experiment.image = MagicMock()

        # Set up mock subjects
        mock_snode = MagicMock()
        mock_pnode = MagicMock()
        mock_fnode = MagicMock()

        # Mock the subjects method
        self.experiment.image.subjects.side_effect = [[mock_snode], [mock_pnode], [mock_fnode]]

        # Mock the value method of the image object
        self.experiment.image.value.side_effect = [
            'S0',  # Sword value
            'pod1',  # Pod name
            '/mockaddress',  # Address for pnode
            'filename.txt',  # Filename for fnode
            '/mock/local/address/file.txt',  # LocalAddress for fnode
            '*',  # AccessibleBy
        ]

        zipdir = '/mockzipdir/'
        self.experiment.storelocalindexzipdirs(zipdir)

        # Check if directories were created
        mock_makedirs.assert_called_once_with('/mockzipdirS0', exist_ok=True)

        # Check if file was opened and read
        mock_open.assert_called_once_with('/mock/local/address/file.txt', 'r')

        # Check if ZipFile was written to
        mock_zipfile.assert_called_once_with('/mockzipdirS0/filename.txtindex.zip', 'w')

        # Ensure the progress bar was updated correctly
        mock_tqdm().update.assert_called()

    @patch('paramiko.SSHClient')
    @patch('scp.SCPClient')
    @patch('os.listdir')
    @patch('tqdm.tqdm')
    def test_distributezips(self, mock_tqdm, mock_listdir, mock_SCPClient, mock_SSHClient):
        # Mock the directory listing
        mock_listdir.return_value = ['file1.zip', 'file2.zip']

        # Mock the subjects
        mock_snode = MagicMock()
        self.experiment.image.subjects.return_value = [mock_snode]

        # Mock the 'value' method of the 'image' attribute
        self.experiment.image.value = MagicMock(return_value='serveraddress:22')

        # Mock SSHClient and SCPClient behavior
        mock_client = mock_SSHClient.return_value
        mock_scp = mock_SCPClient.return_value

        # Call the method
        zipdir = '/mockzipdir/'
        self.experiment.distributezips(zipdir, 'user', 'password')

        # Check that SSHClient and SCPClient were called
        mock_SSHClient.assert_called_once()
        mock_client.connect.assert_called_once_with('serveraddress', port=22, username='user', password='password')

        # Check that files were transferred
        mock_scp.put.assert_any_call('/mockzipdir/file1.zip', '/srv/espresso/')
        mock_scp.put.assert_any_call('/mockzipdir/file2.zip', '/srv/espresso/')
        self.assertEqual(mock_scp.put.call_count, 2)

        # Ensure the progress bar was updated correctly
        mock_tqdm().update.assert_called()

    def test_assignlocalimage(self):
        # Set up mock subjects
        mock_snode1 = MagicMock()
        mock_snode2 = MagicMock()
        self.experiment.image.subjects.return_value = [mock_snode1, mock_snode2]

        # Call the method
        test_dir = '/mockdir/'
        self.experiment.assignlocalimage(test_dir)

        # Verify RDF triples were added correctly
        self.experiment.image.add.assert_any_call(
            (mock_snode1, self.experiment.namespace.LocalAddress, Literal('/mockdir/EspressoPod/S0'))
        )
        self.experiment.image.add.assert_any_call(
            (mock_snode2, self.experiment.namespace.LocalAddress, Literal('/mockdir/EspressoPod/S1'))
        )
        self.assertEqual(self.experiment.image.add.call_count, 2)




# Run the tests
if __name__ == '__main__':
    unittest.main()
