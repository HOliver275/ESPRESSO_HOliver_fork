# ESPRESSO modules
import FileDistributor, FileUploader
# ESPRESSO module
# HO 15/08/2024 BEGIN **************
# from Indexer import PodIndexer
import sys
sys.path.append('../../Indexer')
import PodIndexer
sys.path.append('../../')
import config
from ServerIndexer import ServerIndex
# ESPRESSO modules for accessing Community Solid Server using DPOP 
# from Automation.CSSAccess import CSSaccess,dpop_utils
sys.path.append('../CSSAccess')
import CSSaccess,dpop_utils
# HO 15/08/2024 END ****************
import cleantext, string
# os: https://docs.python.org/3/library/os.html
# random: https://docs.python.org/3/library/random.html
# requests: https://requests.readthedocs.io/en/latest/
# numpy: https://numpy.readthedocs.io/en/latest/
import os, random, requests, numpy
# rdflib.URIRef: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.URIRef
# rdflib.BNode: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.BNode
# rdflib.Literal: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.Literal
# rdflib.Graph: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph
# rdflib.Namespace: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.Namespace
from rdflib import URIRef, BNode, Literal, Graph, Namespace
# math: https://docs.python.org/3/library/math.html#module-math
from math import floor
# threading: https://docs.python.org/3/library/threading.html#module-threading
import threading
# time: https://docs.python.org/3/library/time.html#module-time
# tqdm: https://tqdm.github.io/
# getpass: https://docs.python.org/3/library/getpass.html#module-getpass
import time, tqdm, getpass
# zipfile: https://docs.python.org/3/library/zipfile.html#module-zipfile
from zipfile import ZipFile
# concurrent.futures: https://python.readthedocs.io/en/latest/library/concurrent.futures.html#module-concurrent.futures
import concurrent.futures
# paramiko: https://readthedocs.org/projects/paramiko-docs/
import paramiko
# paramiko.client.SSHClient: https://docs.paramiko.org/en/latest/api/client.html
from paramiko import SSHClient
# scp: https://pypi.org/project/scp/
from scp import SCPClient
# sys: https://docs.python.org/3/library/sys.html#module-sys
from sys import argv

# Hard-coded list of servers. Replace the below with your own.
"""serverlistglobal=['https://srv03812.soton.ac.uk:3000/',
                    'https://srv03813.soton.ac.uk:3000/',
                    'https://srv03814.soton.ac.uk:3000/',
                    'https://srv03815.soton.ac.uk:3000/',
                    'https://srv03816.soton.ac.uk:3000/',
                    'https://srv03911.soton.ac.uk:3000/',
                    'https://srv03912.soton.ac.uk:3000/',
                    'https://srv03913.soton.ac.uk:3000/',
                    'https://srv03914.soton.ac.uk:3000/',
                    'https://srv03915.soton.ac.uk:3000/',
                    'https://srv03916.soton.ac.uk:3000/',
                    'https://srv03917.soton.ac.uk:3000/',
                    'https://srv03918.soton.ac.uk:3000/',
                    'https://srv03919.soton.ac.uk:3000/',
                    'https://srv03920.soton.ac.uk:3000/',
                    'https://srv03921.soton.ac.uk:3000/',
                    'https://srv03922.soton.ac.uk:3000/',
                    'https://srv03923.soton.ac.uk:3000/',
                    'https://srv03924.soton.ac.uk:3000/',
                    'https://srv03925.soton.ac.uk:3000/',
                    'https://srv03926.soton.ac.uk:3000/',
                    'https://srv03927.soton.ac.uk:3000/',
                    'https://srv03928.soton.ac.uk:3000/',
                    'https://srv03929.soton.ac.uk:3000/',
                    'https://srv03930.soton.ac.uk:3000/',
                    'https://srv03931.soton.ac.uk:3000/',
                    'https://srv03932.soton.ac.uk:3000/',
                    'https://srv03933.soton.ac.uk:3000/',
                    'https://srv03934.soton.ac.uk:3000/',
                    'https://srv03935.soton.ac.uk:3000/',
                    'https://srv03936.soton.ac.uk:3000/',
                    'https://srv03937.soton.ac.uk:3000/',
                    'https://srv03938.soton.ac.uk:3000/',
                    'https://srv03939.soton.ac.uk:3000/',
                    'https://srv03940.soton.ac.uk:3000/',
                    'https://srv03941.soton.ac.uk:3000/',
                    'https://srv03942.soton.ac.uk:3000/',
                    'https://srv03943.soton.ac.uk:3000/',
                    'https://srv03944.soton.ac.uk:3000/',
                    'https://srv03945.soton.ac.uk:3000/',
                    'https://srv03946.soton.ac.uk:3000/',
                    'https://srv03947.soton.ac.uk:3000/',
                    'https://srv03948.soton.ac.uk:3000/',
                    'https://srv03949.soton.ac.uk:3000/',
                    'https://srv03950.soton.ac.uk:3000/',
                    'https://srv03951.soton.ac.uk:3000/',
                    'https://srv03952.soton.ac.uk:3000/',
                    'https://srv03953.soton.ac.uk:3000/',
                    'https://srv03954.soton.ac.uk:3000/',
                    'https://srv03955.soton.ac.uk:3000/'
                    ]"""

serverlistglobal = ['https://srv04031.soton.ac.uk:3000/']

# HO 14/08/2024 appears not to be in use
def returnaclopen(fileaddress,webidlist):
    webidstring='<'+'>,<'.join(webidlist)+'>'
    acltext='''@prefix : <'''+fileaddress+'''.acl#>.
@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <profile/card#>.

:ControlReadWrite a acl:Authorization;
    acl:accessTo <'''+fileaddress+'''>;
    acl:agent c:me;
    acl:mode acl:Control, acl:Read, acl:Write.
:Read a acl:Authorization;
    acl:accessTo <'''+fileaddress+'''>;
    acl:mode acl:Read;
    acl:agentClass foaf:Agent;
    acl:agent '''+webidstring+'''.
'''
    return acltext

# HO 14/08/2024 appears not to be in use
def returnacldefault(fileaddress,webidlist):
    webidstring='<'+'>,<'.join(webidlist)+'>'
    acltext='''@prefix : <'''+fileaddress+'''.acl#>.
@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <profile/card#>.

<#ControlReadWrite> a acl:Authorization;
    acl:accessTo <'''+fileaddress+'''>;
    acl:agent c:me;
    acl:mode acl:Control, acl:Read, acl:Write.
<#Read> a acl:Authorization;
    acl:accessTo <'''+fileaddress+'''>;
    acl:mode acl:Read;
    acl:agent '''+webidstring+'''.
'''
    return acltext

# query to construct a default open ACL
acldefopen='''@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <profile/card#>.

<#owner> a acl:Authorization;
acl:agent c:me;
acl:mode acl:Control, acl:Read, acl:Write;
acl:accessTo <./>;
acl:default <./>.

<#public> a acl:Authorization;
acl:mode  acl:Control, acl:Read, acl:Write;
acl:accessTo <./>;
acl:default <./>;
acl:agentClass foaf:Agent.'''

"""
The main class defining an experiment and its attributes.

"""
class ESPRESSOexperiment:
    """
    Constructor for an ESPRESSOexperiment.
        
    param: self
    param: espressopodname, the name of the server-level ESPRESSO pod, default: 'ESPRESSO'
    param: espressoemail, the email of the server-level ESPRESSO pod, default: 'espresso@example.com'
    param: espressoindexdir, the current server-level metaindex directory, default: 'metaindex/'
    param: podname, the current base podname, default: 'pod' (currently set to 'ardfhealth')
    param: podemail, the current pod email, default: '@example.org'
    param: podindexdir, the current pod index directory, default: 'espressoindex/'
    param: password, default '12345'
    """
    def __init__(self, 
        espressopodname='ESPRESSO',
        espressoemail='espresso@example.com',
        espressoindexdir='metaindex/',
        podname='pod',
        podemail='@example.org',
        podindexdir='espressoindex/',
        password='12345'):

        # server names are sequentially numbered per experiment, from a zero base
        self.servernum=0
        # filepool is an empty dictionary
        self.filepool=dict()
        # the 'red' server-level ESPRESSO pod name
        # default value: 'ESPRESSO', example value: 'ESPRESSO'
        self.espressopodname=espressopodname
        # email of the 'red' server-level ESPRESSO pod, set to 'espresso@example.com' 
        # default value: 'espresso@example.com', example value: 'espresso@example.com'
        self.espressoemail=espressoemail
        # the server-level metaindex
        self.espressoindexdir=espressoindexdir
        # original version of the server-level MetaIndex that is stored in the 
        # 'red' server-level ESPRESSO pod; contains only a list of pod indexes on this server
        # example value: 'ardfhealthmetaindex.csv'
        self.espressoindexfile=podname+'metaindex.csv'
        # general base name for the pods in these experiments,
        # default value: 'pod', example value: 'ardfhealth'
        self.podname=podname
        # directory where the pod index is stored
        # default value: 'espressoindex/', example value: 'espressoindex/'
        self.podindexdir=podindexdir
        # domain base for a pod's account email for this experiment
        # default value: '@example.org', example value: '@example.org' 
        self.podemail=podemail
        # account password for a pod in this experiment
        # default value: '12345', example value: '12345'
        self.password=password
        # sequential pod number, starting from a zero base
        # HO 03/09/2024: does not appear to be in use
        # initial value: 0
        self.podnum=0
        # sequential file number, starting from a zero base, 
        # seemingly counting files through the whole experiment
        # initial value: 0
        self.filenum=0
        # forbidden: does not seem to be used 
        # looks like it's related to this issue:
        # https://forum.solidproject.org/t/automatic-setup-of-solid-css/6846
        self.forbidden=["setup"]
        # template for replacement text
        # example value: 'espressosrv/podname/'
        self.replacetemplate='espressosrv/podname/'
        # instantiate experiment namespace
        # example value: 'http://example.org/SOLIDindex/'
        self.namespace=Namespace("http://example.org/SOLIDindex/")
        # instantiate image graph
        # example value: [a rdfg:Graph;rdflib:storage [a rdflib:Store;rdfs:label 'Memory']].
        self.image=Graph()
        #print('self.image= '+str(self.image))
        
    def __repr__(self):
        """
        Return image of the experiment in turtle format. 
        """
        return self.image.serialize(format='turtle')
    
    # HO 14/08/2024 appears not to be in use
    def loaddir(self,datasource,label='file',filetype='text/plain'):
        #n=len(self.filelist)
        pbar=tqdm.tqdm(total=len(os.listdir(datasource)),desc='files loaded:')
        for filename in os.listdir(datasource):
            filepath = os.path.join(datasource, filename)
            # checking if it is a file
            if os.path.isfile(filepath) and not filename.startswith('.'):
                fword='F'+label+str(self.filenum)
                #n=n+1
                self.filenum=self.filenum+1
                fnode=BNode(fword)
                self.image.add((fnode,self.namespace.Type,self.namespace.File))
                self.image.add((fnode,self.namespace.LocalAddress,Literal(filepath)))
                self.image.add((fnode,self.namespace.Filename,Literal(filename)))  
                self.image.add((fnode,self.namespace.Filetype,Literal(filetype)))
                self.image.add((fnode,self.namespace.Label,Literal(label)))
                
                #self.filelist.append(fnode)
                pbar.update(1)
        pbar.close()
                
    """
    Loads the source data directory to the pool.
    
    experiment.loaddirtopool(sourcedir,’file’) would (if you're doing it that way) load the restricted-access files
    experiment.loaddirtopool(sourcedir,'goodfile') would (if you're doing it that way) load the open-access files
    
    param: self
    param: datasource, the source directory for the data. Example: '../DatasetSplitter/sourcedir1/'
    param: label, the label applied to the relevant files, default: 'file', example: 'Filelabel1' 
    """
    def loaddirtopool(self,datasource,label='file'):
        # if the label is a key, get the relevant filelist
        if label in self.filepool.keys():
            thisfilelist=self.filepool[label]
        else: # if the label is not a key, initialize an empty list
            thisfilelist=[]

        # get a list of every item in the source directory
        for filename in os.listdir(datasource):
            # get the full path of each item
            filepath = os.path.join(datasource, filename)
            # checking if it is a file, if so, add it to the file list
            if os.path.isfile(filepath) and not filename.startswith('.'):
                    thisfilelist.append((filepath,filename))
        # update the file list in the pool
        self.filepool[label]=thisfilelist
        #print('self = ' + str(self))
                
    """
    Loads the servers for the experiment.
    
    serverlist=serverlistglobal[0:1] means only on the first server in the serverlist. 
    
    serverlistglobal[10*i:10*(i+1)] , means the first 10 servers if i=0 
    
    param: self
    param: serverlist, the list of servers. example: ['http://localhost:3000/']
    param: label, the label applied to the relevant servers. default: 'server', example: 'Serverlabel1'
    """
    def loadserverlist(self,serverlist,label='server'):
        # for every server in the list
        for s in serverlist:
            # construct a short name by prepending 'S' to the label and appending a counter
            sword='S'+label+str(self.servernum)
            # advance the counter
            self.servernum=self.servernum+1
            # create a blank server node
            snode=BNode(sword)
            # create a short ESPRESSO server handle by prepending 'E' to the short server name
            eword='E'+sword
            # create a blank ESPRESSO server node
            enode=BNode(eword)
            # add the server to the image
            self.image.add((snode,self.namespace.Type,self.namespace.Server))
            # add the short server handle to the image
            self.image.add((snode,self.namespace.Sword,Literal(sword)))
            # save the current server in the list
            IDP=s
            # add the current listed server as the address of this server node
            self.image.add((snode,self.namespace.Address,Literal(IDP)))
            # add the server label
            self.image.add((snode,self.namespace.Label,Literal(label)))
            # create endpoint
            register_endpoint=IDP+'idp/register/'
            # add endpoint to the image
            self.image.add((snode,self.namespace.RegisterEndpoint,Literal(register_endpoint)))
            # add the ESPRESSO pod to the image
            self.image.add((snode,self.namespace.ContainsEspressoPod,enode))
            # construct the name of the ESPRESSO pod at the endpoint address
            esppod=IDP+self.espressopodname+'/'
            # add the ESPRESSO pod to the image
            self.image.add((enode,self.namespace.Type,self.namespace.EspressoPod))
            # add the ESPRESSO pod address to the image
            self.image.add((enode,self.namespace.Address,Literal(esppod)))
            # add the ESPRESSO pod name to the image
            self.image.add((enode,self.namespace.Name,Literal(self.espressopodname)))
            # construct the MetaIndex address within the ESPRESSO pod
            # HO 04/09/2024 BEGIN **************
            # Note that as of now the MetaindexAddress points to a directory, not a .csv file
            # in conformity to IndexDir
            # and the metaindex.csv file is still written to the ESPRESSO pod, but whereas
            # it used to be in the root, it's now in this folder, along with all the other
            # metaindex files
            #metaindexaddress=esppod+self.espressoindexfile
            metaindexaddress=esppod+self.espressoindexdir
            # add the MetaIndex address to the image
            self.image.add((enode,self.namespace.MetaindexAddress,Literal(metaindexaddress)))
            # to point to the metaindex.csv file we add another attribute, MetaindexFile
            metaindexfile=metaindexaddress+self.espressoindexfile
            self.image.add((enode,self.namespace.MetaindexFile,Literal(metaindexfile)))
            # HO 04/09/2024 END **************
        #print('self: ' + str(self))
        
    """
    Initializes a pod node
    
    param: self
    param: pword, the sequentially numbered name given to the pod node, example value: Ppod20
    param: podname
    param: podlabel, default 'pod'  
    
    return: the initialized pod node  
    """
    def initpnode(self,pword,podname,podlabel='pod'):
        # create a blank node named after pword
        pnode=BNode(pword)
        # add [pod node, Name, podname] to the image
        self.image.add((pnode,self.namespace.Name,Literal(podname)))
        # add [pod node, Type, Pod] to the image
        self.image.add((pnode,self.namespace.Type,self.namespace.Pod))
        # add [pod node, Label, podlabel] to the image
        self.image.add((pnode,self.namespace.Label,Literal(podlabel)))
        # create an email address for this podname
        podemail=podname+self.podemail
        # add [pod node, Email, podemail] to the image
        self.image.add((pnode,self.namespace.Email,Literal(podemail)))
        # return the initialized pod node
        return pnode
    
    """
    Initialize a file node.
    
    param: self
    param: fword, short sequentially-numbered filename
    param: filename, the filename
    param: filepath, the file path
    param: filetype, the filetype
    param: filelabel, the short file label, default: 'pod'
    
    return: an initialized file node
    """
    def initfnode(self,fword,filename,filepath,filetype,filelabel='pod'):
        # Create a blank file node
        fnode=BNode(fword)
        # add [file node, Type, File] to the graph
        self.image.add((fnode,self.namespace.Type,self.namespace.File))
        # add [file node, LocalAddress, filepath] to the graph
        self.image.add((fnode,self.namespace.LocalAddress,Literal(filepath)))
        # add [file node, Filename, filename] to the graph
        self.image.add((fnode,self.namespace.Filename,Literal(filename))) 
        # add [file node, Filetype, filetype] to the graph 
        self.image.add((fnode,self.namespace.Filetype,Literal(filetype)))
        # add [file node, Label, file label] to the graph
        self.image.add((fnode,self.namespace.Label,Literal(filelabel)))
        # return the blank file node
        return fnode
        
    """
    Assign a pod to a server
    
    param: self
    param: snode, a server node, example value: SServerlabel21
    param: pnode, a pod node, example value: Ppod20
    """
    def assignpod(self,snode,pnode):
        # get the string representation of the server node's address
        IDP=str(self.image.value(snode,self.namespace.Address))
        # add pod to server
        self.image.add((snode,self.namespace.Contains,pnode))
        # get the name of the pod node
        podname=str(self.image.value(pnode,self.namespace.Name))
        # construct the pod address from the server node's address plus the podname
        podaddress=IDP+podname+'/'
        # add [pod node, Address, podaddress] to the graph
        self.image.add((pnode,self.namespace.Address,Literal(podaddress)))
        # construct the pod index address
        podindexaddress=podaddress+self.podindexdir
        # add [pod node, Index Address, pod index address] to the graph
        self.image.add((pnode,self.namespace.IndexAddress,Literal(podindexaddress)))
        # construct a WebID for this pod address
        webid=podaddress+'profile/card#me'
        # add [pod node, WebID, webid] to the graph
        self.image.add((pnode,self.namespace.WebID,Literal(webid)))
        #print('output: self = ' + str(self))
        
    """
    Creates the logical pods.
    
    Two types of pods, closed ('compod') and open ('goodpod') (if you're doing it that way): 
        - experiment.createlogicalpods(8500*10,0.01,podlabel='compod') 
        - experiment.createlogicalpods(850*10,0.05,podlabel='goodpod') 
    
    param: self
    param: numberofpods
    param: serverdisp
    param: serverlabel, default: 'server', the label applied to the relevant servers
    param: podlabel, default: 'pod'
    param: zipf, default: 0, assuming this weights the word rank in a zipf distribution
    """
    def createlogicalpods(self,numberofpods,serverdisp,serverlabel='server',podlabel='pod',zipf=0):
        # Load all the server nodes with the relevant label into a list
        thisserverlist=[snode for snode in self.image.subjects(self.namespace.Type,self.namespace.Server) if str(self.image.value(snode,self.namespace.Label))==serverlabel]
        # Initialize an empty list to hold the pod nodes
        pnodelist=[]
        # For each pod
        for i in range(numberofpods):
            # Prepend 'P' to the podlabel, and append a sequential number
            # (the sequential number starts from 0, it is not bookmarked)
            pword='P'+podlabel+str(i)
            # Construct a podname with the same sequential number appended
            podname=self.podname+podlabel+str(i)
            # Initialize a pod node with the podword, podname, and podlabel
            pnode=self.initpnode(pword,podname,podlabel)
            # Add the pod node to the list
            pnodelist.append(pnode)

        # If we are doing a zipf distribution
        if zipf>0: # do the zipf distribution with this pod node list, this server list, and the zipf
            poddist=FileDistributor.distribute(pnodelist,len(thisserverlist), zipf)
        else: # if we are not doing a zipf distribution, do a normal distribution
            poddist=FileDistributor.normaldistribute(pnodelist,len(thisserverlist), serverdisp)
        
        # for each server in the server list
        for s in range(len(thisserverlist)):
            # get the current server node
            snode=thisserverlist[s]
            # get the server node's address
            IDP=str(self.image.value(snode,self.namespace.Address))
            # for each pod in the server's current pod distribution
            for p in range(len(poddist[s])):
                # get the current pod
                pnode=poddist[s][p]
                # get the pod's name
                podname=str(self.image.value(pnode,self.namespace.Name))
                # assign this pod to this server
                self.assignpod(snode,pnode)
                # initialize an empty triplestring
                triplestring=''
                # add the empty triplestring to the pod node
                self.image.add((pnode,self.namespace.TripleString,Literal(triplestring)))
        #print('self = ' + str(self))
        
    """
    Creates logical pairs of pods. You can safely create pod pairs and then not do anything with the fact that they're paired.
    
    param: self
    param: numberofpods, example: 10
    param: serverdisp, standard deviation, example: 0
    param: serverlabel1, the label of the first server in the pair, default: 'server1', example: 'Serverlabel1'
    param: serverlabel2, the label of the second server in the pair, default 'server2', example: 'Serverlabel2'
    param: podlabel1, the label of the first pod in the pair, default 'pod1', example: 'pod1'
    param: podlabel2, the label of the second pod in the pair, default 'pod2', example: 'pod2'
    param: conpred, a URI/IRI base, default: 'http://espresso.org/haspersonalWebID', example: 'http://espresso.org/haspersonalWebID'
    """                    
    def createlogicalpairedpods(self,numberofpods,serverdisp,serverlabel1='server1',serverlabel2='server2',podlabel1='pod1',podlabel2='pod2',conpred=URIRef('http://espresso.org/haspersonalWebID')):
        # Type, Server, serverlabel1
        thisserverlist1=[snode for snode in self.image.subjects(self.namespace.Type,self.namespace.Server) if str(self.image.value(snode,self.namespace.Label))==serverlabel1]
        # Type, Server, serverlabel2
        thisserverlist2=[snode for snode in self.image.subjects(self.namespace.Type,self.namespace.Server) if str(self.image.value(snode,self.namespace.Label))==serverlabel2]
        
        # list of paired pod nodes
        ppnodelist=[]
        # for an initial range of 10 pods, initialize a blank node for each one
        for i in range(numberofpods):
            # initially 'Ppod10 .. Ppod19'
            pword1='P'+podlabel1+str(i)
            # initially 'ardfhealthpod10' .. 'ardfhealthpod19'
            podname1=self.podname+podlabel1+str(i)
            # initialize a blank node for the first pod
            pnode1=self.initpnode(pword=pword1,podname=podname1,podlabel=podlabel1)
            # initially 'Ppod20 .. Ppod29'
            pword2='P'+podlabel2+str(i)
            # initially 'ardfhealthpod20' .. 'ardfhealthpod29'
            podname2=self.podname+podlabel2+str(i)
            # initialize a blank node for the second pod
            pnode2=self.initpnode(pword=pword2,podname=podname2,podlabel=podlabel2)
            # add the two blank pod nodes to the paired pod nodes list
            ppnodelist.append((pnode1,pnode2))
        # distribute the list of paired nodes over as many places as there are in thisserverlist2
        poddist2=FileDistributor.normaldistribute(ppnodelist,len(thisserverlist2), serverdisp)
        
        # and for every server in thisserverlist2
        for s in range(len(thisserverlist2)):
            # get the current node
            snode=thisserverlist2[s]
            # get a string representation of the node
            sword=str(snode)
            # string value of server node address
            IDP=str(self.image.value(snode,self.namespace.Address))
            # For the distribution of pods on this server
            for p in range(len(poddist2[s])):
                # find the node at element 1
                pnode=poddist2[s][p][1]
                # get the name of the pod
                podname=str(self.image.value(pnode,self.namespace.Name))
                # assign the current pod node to this server node
                self.assignpod(snode,pnode)
                # create an empty string to hold the triple
                triplestring=''
                # add [pod node, TripleString, empty string] to the graph
                self.image.add((pnode,self.namespace.TripleString,Literal(triplestring)))

        # distribute the list of paired nodes over as many places as there are in thisserverlist1
        poddist1=FileDistributor.normaldistribute(ppnodelist,len(thisserverlist1), serverdisp)
        
        # stepping through the servers in thisserverlist1
        for s in range(len(thisserverlist1)):
            # get the current server node
            snode=thisserverlist1[s]
            # get the string representation of the current server node
            sword=str(snode)
            # get the string representation of the current server node's address
            IDP=str(self.image.value(snode,self.namespace.Address))
            # now for every pod that is distributed to this server
            for p in range(len(poddist1[s])):
                # find the first node in the pair
                pnode=poddist1[s][p][0]
                # find the other node in the pair
                otherpnode=poddist1[s][p][1]
                # assign the current pod node to this server node
                self.assignpod(snode,pnode)
                # get the webid of this pod node
                webid=str(self.image.value(pnode,self.namespace.WebID))
                # get the webid of the other pod node in the pair
                otherwebid=str(self.image.value(otherpnode,self.namespace.WebID))
                # about that triplestring: [web ID, URI, other web ID]
                triplestring='<'+webid+'> <'+str(conpred)+'> <'+otherwebid+'>'
                # add [pod node, TripleString, triplestring] to the graph
                self.image.add((pnode,self.namespace.TripleString,Literal(triplestring)))
        #print('self = ' + str(self))       
    
    """
    Logically distribute files to pods from pool, if we know the number of files we want to distribute.
    
    param: self
    param: number of files, example: 10
    param: filedisp, example: 0
    param: filetype, example: 0
    param: filelabel, default: 'file', example: 'Filelabel1'
    param: podlabel, default: 'pod', example: 'pod1'
    param: subdir, default: 'file', example: 'file'
    param: predicatetopod, default: 'http://example.org/SOLIDindex/HasFile', example: 'http://example.org/SOLIDindex/HasFile'
    param: replacebool, default: False, example: False. If true, there will be some text to be replaced.
    param: zipf, default: 0, example: 0. Weights the word rank in a zipf distribution    
    """
    def logicaldistfilestopodsfrompool(self,numberoffiles,filedisp,filetype,filelabel='file',podlabel='pod',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False,zipf=0):
        # filepool dictionary and in the default case the key would be 'file'
        # save the list of whatever goes by this file label
        afiletuplelist=self.filepool[filelabel]
        # slice out however many files from this file tuple list
        thisfiletuplelist=afiletuplelist[:numberoffiles]
        # save back the original list of whatever went by this file label
        self.filepool[filelabel]=afiletuplelist[numberoffiles:]
        
        # a progress bar for the requisite number of files
        pbar=tqdm.tqdm(total=len(thisfiletuplelist),desc='files loaded:')
        # a file list
        thisfilelist=[]
        # now every filepath and filename gets a sequentially numbered short
        # filename that goes Ffilelabel0, .. Ffilelabeln
        for filepath,filename in thisfiletuplelist:
            # construct the short filename
            fword='F'+filelabel+str(self.filenum)
            # increment the file number suffix
            self.filenum=self.filenum+1
            # initialize a file node
            # passes: the short filename, the filename, the filepath, the filetype, the file label
            fnode=self.initfnode(fword,filename,filepath,filetype,filelabel)
            # append the current file node to the file list
            thisfilelist.append(fnode)
            # move the progress bar along
            pbar.update(1)
        # close the progress bar
        pbar.close()
        
        # create pod list from all the pod nodes with the given podlabel
        thispodlist=[pnode for pnode in self.image.subjects(self.namespace.Label,Literal(podlabel))]
        # distribute the files around the list of pods
        # zipf seems to represent the frequency rank, as its name implies - if it's set, 
        # use it to distribute the files
        # TODO we know we want to place 1 file in each pod for the Aug-Sep 2024 experiments
        # so all we have to do is specify a number of files equal to the number of pods
        # each time and normaldistribute will handle it
        if zipf>0:
            filedist=FileDistributor.distribute(thisfilelist,len(thispodlist),zipf)
        else: # if zipf is not set, distribute them normally 
            filedist=FileDistributor.normaldistribute(thisfilelist,len(thispodlist),filedisp)
        # we now have a list of lists of files,
        # and each list of list represents a place to distribute the respective list of files
        for p in range(len(filedist)):
            # and we get the next pod node in the list
            pnode=thispodlist[p]
            # we get its address
            podaddress=str(self.image.value(pnode,self.namespace.Address))
            # we get its WebID
            webid=str(self.image.value(pnode,self.namespace.WebID))
            # and for each file node in the current list of files
            for fnode in filedist[p]:
                # we add the file node to the pod node
                self.image.add((pnode,self.namespace.Contains,fnode))
                # get the name of the file
                filename=str(self.image.value(fnode,self.namespace.Filename))
                # use it to construct the full address of the file
                fileaddress=podaddress+subdir+'/'+filename
                # add the address of the file to the file node
                self.image.add((fnode,self.namespace.Address,Literal(fileaddress)))
                # set replacement text
                self.image.add((fnode,self.namespace.ReplaceText,Literal(podaddress)))
                # if there's a predicate we can add into the string representation of the triple, do so
                # and we get [webid, predicatetopod, fileaddress]
                if len(str(predicatetopod))>0:
                    triplestring='<'+webid+'> <'+str(predicatetopod)+'> <'+fileaddress+'>'
                else: # if there isn't a predicate, the triple string is empty
                    triplestring=''
                # at this point we are adding [file node, TripleString, triplestring] to the graph
                # which is either [file node, TripleString, [webid, predicatetopod, fileaddress]]
                # or [file node, TripleString, '']
                self.image.add((fnode,self.namespace.TripleString,Literal(str(triplestring))))
                # and if the replace-text flag is true, set the pod address to be 
                # the replace-text for this file node
                if replacebool:
                    self.image.add((fnode,self.namespace.ReplaceText,Literal(podaddress)))
        #print('self = ' + str(self))

    """
    Logically assigns Pareto distribution of files to pods from the file pool.
    
        - experiment.paretofilestopodsfrompool('text/plain','file','compod','medhist','',False,1) (compod=restricted access, if you're doing it this way)
        - experiment.paretofilestopodsfrompool('text/plain','goodfile','goodpod','medhist','',False,1) (goodpod=open access, if you're doing it this way)
    
    param: self
    param: filetype
    param: filelabel, default: 'file', the label applied to the relevant files
    param: podlabel, default: 'pod', the label applied to the relevant pods
    param: subdir, default: 'file', the target subdirectory
    param: predicatetopod, default: 'http://example.org/SOLIDindex/HasFile', the base URI
    param: replacebool, default: False; if True designates that text is to be replaced
    param: alpha, default: 1, the shape parameter for the Pareto distribution
    """
    def paretofilestopodsfrompool(self,filetype,filelabel='file',podlabel='pod',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False,alpha=1):
        # get the list of relevant file tuples from the file pool
        thisfiletuplelist=self.filepool[filelabel]
        
        # get the list of relevant pods 
        thispodlist=[pnode for pnode in self.image.subjects(self.namespace.Label,Literal(podlabel))]
        # get a list of Pareto-sampled lists of files, one list of files per place
        filedist=FileDistributor.paretopluck(thisfiletuplelist,len(thispodlist),alpha)
        # initialize the progress bar
        pbar=tqdm.tqdm(total=len(filedist),desc='files loaded to pods:')
        # for each place
        for p in range(len(filedist)):
            # get the current pod node
            pnode=thispodlist[p]
            # get the address of the current pod node
            podaddress=str(self.image.value(pnode,self.namespace.Address))
            # get the WebID of the current pod node
            webid=str(self.image.value(pnode,self.namespace.WebID))
            # for each file tuple in the current list of files to be distributed
            # to this pod
            for ftuple in filedist[p]:
                # construct the short filename
                # prepend an 'F' to the file label and append a sequential number
                # (that picks up where the last number left off)
                fword='F'+filelabel+str(self.filenum)
                # increment the sequential file number
                self.filenum=self.filenum+1
                # initializes the file node
                # passes: the short filename
                # the second element of the file tuple (the filename)
                # the first element of the file tuple (the filepath)
                # the file type
                # the file label
                fnode=self.initfnode(fword,ftuple[1],ftuple[0],filetype,filelabel)
                # assign this file node to this pod node in the graph
                self.image.add((pnode,self.namespace.Contains,fnode))
                # get the current filename
                filename=str(self.image.value(fnode,self.namespace.Filename))
                # construct the address for this filename at this pod
                fileaddress=podaddress+subdir+'/'+filename
                # add the file address to the graph
                self.image.add((fnode,self.namespace.Address,Literal(fileaddress)))
                # if there is text to be replaced
                if replacebool:
                    # mark the pod address as text to be replaced
                    self.image.add((fnode,self.namespace.ReplaceText,Literal(podaddress)))
                # if there is a predicate to pod string
                if len(str(predicatetopod))>0:
                    # use it to construct a triple string of [webid, predicatetopod, fileaddress]
                    triplestring='<'+webid+'> <'+str(predicatetopod)+'> <'+fileaddress+'>'
                else: # if there isn't a predicate to pod string, the triple string is empty
                    triplestring=''
                # either way, add the triple string to the graph
                self.image.add((fnode,self.namespace.TripleString,Literal(str(triplestring))))
                # if there is text to be replaced
                if replacebool: # mark the pod address as replace text
                    self.image.add((fnode,self.namespace.ReplaceText,Literal(podaddress)))
            # advance the progress bar
            pbar.update(1)
        # close the progress bar
        pbar.close()

    # HO 14/08/2024 appears not to be in use
    def logicaldistfilestopods(self,numberoffiles,filedisp,filelabel='file',podlabel='pod',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False):
        thisfilelist=[fnode for fnode in self.image.subjects(self.namespace.Type,self.namespace.File) if str(self.image.value(fnode,self.namespace.Label))==filelabel]
        thisfilelisttr=thisfilelist[:numberoffiles]
        thispodlist=[pnode for pnode in self.image.subjects(self.namespace.Label,Literal(podlabel))]
        filedist=FileDistributor.normaldistribute(thisfilelisttr,len(thispodlist),filedisp)
        for p in range(len(filedist)):
            pnode=thispodlist[p]
            podaddress=str(self.image.value(pnode,self.namespace.Address))
            webid=str(self.image.value(pnode,self.namespace.WebID))
            for fnode in filedist[p]:
                self.image.add((pnode,self.namespace.Contains,fnode))
                filename=str(self.image.value(fnode,self.namespace.Filename))
                fileaddress=podaddress+subdir+'/'+filename
                self.image.add((fnode,self.namespace.Address,Literal(fileaddress)))
                self.image.add((fnode,self.namespace.ReplaceText,Literal(podaddress)))
                triplestring='<'+webid+'> <'+str(predicatetopod)+'> <'+fileaddress+'>'
                self.image.add((fnode,self.namespace.TripleString,Literal(str(triplestring))))
                if replacebool:
                    replstring=podaddress
                else:
                    replstring=''
                self.image.add((fnode,self.namespace.ReplaceText,Literal(replstring)))

    """
    Distributes bundles of files.
    
    param: self
    param: numberofbundles, the number of bundles, example: 10
    param: bundlesource, the source directory of these bundles, example: '../DatasetSplitter/sourcedir2/'
    param: filetype, the filetype, example: 'text/turtle'
    param: filelabel, default: 'file', example: 'Filelabel2'
    param: subdir, default: 'file', example: 'file'
    param: podlabel, default: 'pod', example: 'pod2'
    param: predicatetopod, default: 'http://example.org/SOLIDindex/HasFile', example: 'http://example.org/SOLIDindex/HasFile'
    param: hashliststring, default: '', example: ''
    """
    def distributebundles(self,numberofbundles,bundlesource,filetype,filelabel='file',subdir='file',podlabel='pod',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),hashliststring=''):
        # get the list of all the pod nodes in this graph with the relevant label
        thispodlist=[pnode for pnode in self.image.subjects(self.namespace.Label,Literal(podlabel))]
        # set up a progress bar
        pbar=tqdm.tqdm(total=numberofbundles,desc='files loaded:')
        # set a counter for the number of bundles
        i=numberofbundles
        # now list all the items in the bundle source directory
        for bundle in os.listdir(bundlesource):
            # count down through the bundles
            i=i-1
            if i<0:
                break
            
            # get the current pod node
            pnode=thispodlist[i]
            # get the address of the current pod node
            podaddress=str(self.image.value(pnode,self.namespace.Address))
            # get the WebID of the current pod node
            webid=str(self.image.value(pnode,self.namespace.WebID))
            
            # get the full path of the current bundle in the source directory
            bundlepath=os.path.join(bundlesource, bundle)
            # if the current path is a directory
            if os.path.isdir(bundlepath):
                # get all the items in the current path
                for filename in os.listdir(bundlepath):
                    # and get the full path of the current item
                    filepath = os.path.join(bundlepath, filename)
                    # checking if it is a file
                    if os.path.isfile(filepath) and not filename.startswith('.'):
                        # if so, prepend 'F' and append the sequential file number
                        fword='F'+str(self.filenum)
                        # increment the sequential file number
                        self.filenum=self.filenum+1
                        # create a blank file node
                        fnode=BNode(fword)
                        # add [file node, type, File] to the graph
                        self.image.add((fnode,self.namespace.Type,self.namespace.File))
                        
                        # add the filepath as the file node's local address
                        self.image.add((fnode,self.namespace.LocalAddress,Literal(filepath)))
                        # add the filename as the file node's file name
                        self.image.add((fnode,self.namespace.Filename,Literal(filename)))  
                        # add the filetype as the file node's file type
                        self.image.add((fnode,self.namespace.Filetype,Literal(filetype)))
                        # add the file label as the file node's file label
                        self.image.add((fnode,self.namespace.Label,Literal(filelabel)))
                        
                        # add the file node to the current pod node
                        self.image.add((pnode,self.namespace.Contains,fnode))
                        # set the full address of the file in the pod
                        fileaddress=podaddress+subdir+'/'+filename
                        # add the file address to the file node
                        self.image.add((fnode,self.namespace.Address,Literal(fileaddress)))
                        # set the pod address as the ReplaceText
                        self.image.add((fnode,self.namespace.ReplaceText,Literal(podaddress)))
                        # if no hashliststring is set, make the triple string [webid, predicatetopod, fileaddress]
                        if len(hashliststring)==0:
                            triplestring='<'+webid+'> <'+str(predicatetopod)+'> <'+fileaddress+'>'
                        else: # if there is a hashliststring, parse it as the object of the triplestring
                            triplestring='<'+webid+'> <'+str(predicatetopod)+'>'
                            for h in hashliststring.rsplit(','):
                                triplestring=triplestring+' <'+fileaddress + '#' + h +'>,'
                            triplestring=triplestring[:-1]+'.'
                        # add the triple string to the file node
                        self.image.add((fnode,self.namespace.TripleString,Literal(str(triplestring))))
            # update the progress bar
            pbar.update(1)
        # close the progress bar
        pbar.close()
        #print('self = ' + str(self))

    """
    Initialize agents (WebID) list. 

    _:A0 ns1:Type ns1:Agent ; 

    ns1:WebID "mailto:agent0@example.org" . 
    
    param: self
    param: numberofwebids
    return: anodelist, the list of agent nodes
    """
    def initanodelist(self,numberofwebids):
        # initialize an empty list of agents
        anodelist=[]

        # for each WebID
        for i in range(numberofwebids):
            # construct a sequentially-numbered agent name
            # by concatenating 'A' and the sequential number
            # (This is zero-based inside this function and
            # does not pick up from where a class-level counter
            # left off)
            aword='A'+str(i)
            # construct a blank node with the sequentially-numbered agent name
            anode=BNode(aword)
            # construct a webid in the form of a sequentially-numbered email address
            email = 'agent'+str(i)+'@example.org'
            # add the web ID to the agent node
            self.image.add((anode,self.namespace.Email,Literal(email)))
            webid='http://example.org/agent'+str(i)+'/profile/card#me'
            self.image.add((anode,self.namespace.WebID,Literal(webid)))
            # mark the node as being of type Agent
            self.image.add((anode,self.namespace.Type,self.namespace.Agent))
            # append the agent node to the list
            anodelist.append(anode)
            
        # return the list of agent nodes
        return anodelist

    """
    Imagine (Assign) ACL on Files for the WebIDs.
    
    This is done on the files and good files for the normal WebIDs and only on good/open files for the Special WebIDs 
    - experiment.imagineaclnormal(0,mean, disp,'file') 
    - experiment.imagineaclnormal(0,mean, disp,'goodfile') 
    - experiment.imagineaclspecial('goodfile') 
    
    param: self
    param: openperc, the percentage of files that are open-access. example: 50
    param: mean, the mean of the distribution. example: 4
    param: disp, the standard deviation of the distribution. example: 0
    param: filelabel, default='file', example: 'Filelabel2'
    """
    def imagineaclnormal(self,openperc,mean, disp,filelabel='file'):
        # Make a list of Agent nodes
        anodelist=list(self.image.subjects(self.namespace.Type,self.namespace.Agent))
        # Show the user the length of the list
        print ('anode list has',len(anodelist))

        # make a list of all the file nodes for the input filelabel
        thisfilelist=[fnode for fnode in self.image.subjects(self.namespace.Type,self.namespace.File) if str(self.image.value(fnode,self.namespace.Label))==filelabel]
        # get an integer representing the number of files for the requisite percentage
        openn=floor(len(thisfilelist)*(openperc/100))
        # and select the open files at random from the list of file nodes
        thisopenfilelist=random.sample(thisfilelist, openn)
        # and for every file in the list of open files
        for fnode in thisopenfilelist:
            # add them to the filenode as the OpenFile type
            self.image.add((fnode,self.namespace.Type,self.namespace.OpenFile))

        # initialize the progress bar
        pbar=tqdm.tqdm(total=len(thisfilelist),desc='acls:')
        # if there aren't any Agent nodes, return (TODO we could have done this off the bat)
        if len(anodelist)==0:
            return
        # go through every file node in the list 
        for fnode in thisfilelist:
            # if the standard deviation is set to 0, just use the mean
            if disp==0:
                n=mean
            else: # if the standard deviation is not set to 0,
                # draw random sample from a normal distribution 
                n=floor(numpy.random.normal(mean,disp*mean))
                # the lowest value n can have is 1
                if n<=1:
                    n=1
                # the highest value n can have is the number of nodes
                if n>len(anodelist):
                    n=len(anodelist)
            # make a list out of a random sample of Agent nodes
            accanodelist=random.sample(anodelist, n)
            # now go through the randomly sampled list of Agent nodes
            for anode in accanodelist:
                # and mark the file node as accessible by those Agent nodes
                self.image.add((fnode,self.namespace.AccessibleBy,anode))
            # update the progress bar
            pbar.update(1)
        # close the progress bar
        pbar.close()
        #print('self: ' + str(self))
        
    """
    Initialize Special Agents (WebID) as a list, each with a percentage of access to the files.
    
    webid='mailto:sagent'+str(i)+'@example.org' 
    _:SA3 ns1:Power "10" ; 
    ns1:Type ns1:SAgent ; 
    ns1:WebID "mailto:sagent3@example.org" . 

    _:SA2 ns1:Power "25" ; 
    ns1:Type ns1:SAgent ; 
    ns1:WebID "mailto:sagent2@example.org" . 

    _:SA1 ns1:Power "50" ; 
    ns1:Type ns1:SAgent ; 
    ns1:WebID "mailto:sagent1@example.org" . 

    _:SA0 ns1:Power "100" ; 
    ns1:Type ns1:SAgent ; 
    ns1:WebID "mailto:sagent0@example.org" . 
    
    param: self
    param: percs, percentages of special agents
    return: sanodelist, a list of special agent nodes
    """
    def initsanodelist(self,percs):
        # initialize an empty list of special agent nodes
        sanodelist=[]
        # for each different percentage of special agents
        for i in range(len(percs)):
            # construct a label with the prefix 'SA' and a sequential number
            # (the sequential number is 0-based inside this function,
            # it does not pick up from where a class-level variable left off)
            saword='SA'+str(i)
            # create a blank node for this special agent
            sanode=BNode(saword)
            webid = 'http://example.org/sagent' + str(i) + '/profile/card#me'
            # add the WebID to this special agent node
            self.image.add((sanode,self.namespace.WebID,Literal(webid)))
            email = 'sagent' + str(i) + '@example.org'
            self.image.add((sanode,self.namespace.Email,Literal(email)))
            # add the current percentage to this special agent node as a Power
            self.image.add((sanode,self.namespace.Power,Literal(str(percs[i]))))
            # mark this node as a Special Agent type node
            self.image.add((sanode,self.namespace.Type,self.namespace.SAgent))
            # and add the current node to the list of special agent nodes
            sanodelist.append(sanode)
        # return the list of special agent nodes
        return sanodelist
        
    """
    A distribution of special agent ACLs.
    
    param: self
    param: filelabel, default: 'file', example: 'Filelabel1'   
    """    
    def imagineaclspecial(self,filelabel='file'):
        # list of special agent nodes
        sanodelist=list(self.image.subjects(self.namespace.Type,self.namespace.SAgent))

        # list of file nodes that match the relevant label
        thisfilelist=[fnode for fnode in self.image.subjects(self.namespace.Type,self.namespace.File) if str(self.image.value(fnode,self.namespace.Label))==filelabel]
        # display the number of file nodes
        print(len(thisfilelist))
        # for each special agent node
        for sanode in sanodelist:
            # get the int value of the node's power, divide it by 100, multiply it by the 
            # length of the file list
            n=floor(len(thisfilelist)*(int(self.image.value(sanode,self.namespace.Power))/100))
            # and get a random sample of that number of files from the file list
            chfilelist=random.sample(thisfilelist, n)
            # display the number of files for this special agent node
            print('sanode',n)
            # initialize the progress bar
            pbar=tqdm.tqdm(total=n,desc='special acl:')
            # for each file node in the random sample list
            for fnode in chfilelist:
                # add an ACL file saying it's accessible to this node
                self.image.add((fnode,self.namespace.AccessibleBy,sanode))
                # advance the progress bar
                pbar.update(1)
            # close the progress bar
            pbar.close()
        #print('self: ' + str(self))

    """
    Saves the experiment as a graph.
    
    param: self
    param: filename of the file containing the graph representation of the whole experimental structure
        example: 'ardfhealthexp.ttl'
    """
    def saveexp(self,filename):
        with open(filename, 'w') as f:
            f.write(repr(self))
            f.close()
            
    """
    After the .ttl image of the experiment is created, load the experiment from this Image 
    to know the information required for the actual deployment, and to upload the files. 
    
    param: self
    param: filename, the .ttl file containing the image of the experiment
    """
    def loadexp(self,filename):
        # instantiate a Graph
        g=Graph()
        # parse the .ttl file into the Graph
        g.parse(filename)
        # now the Graph is the experiment's image
        self.image=g
        # initialize the server counter to 0
        self.servernum=0
        # initialize the file counter to 0
        self.filenum=0
        # for every server node in the image
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # increment the server's counter
            self.servernum=self.servernum+1
        # for every file node in the image
        for fnode in self.image.subjects(self.namespace.Type,self.namespace.File):
            # increment the file's counter
            self.filenum=self.filenum+1
       #print('self = ' + str(self))

    """
    Creates the ESPRESSO pods, if they haven't already been created.
    
    param: self
    """                    
    def ESPRESSOcreate(self):
        # Display total number of servers
        print(self.servernum, 'servers total')
        # for each server in the image
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # check if the ESPRESSO pod has been created
            enode=self.image.value(snode,self.namespace.ContainsEspressoPod)
            # get the address of the ESPRESSO pod
            esppodaddress=self.image.value(enode,self.namespace.Address)
            # get the response text without using DPOP to access the ESPRESSO pod address
            # HO 25/09/2024 BEGIN ******************
            #try:
            res =CSSaccess.get_file(esppodaddress)
            #except:
                #print("ESPRESSOcreate: Couldn't get file at " + esppodaddress + ", trying again.")
                #res =CSSaccess.get_file(esppodaddress)
            # HO 25/09/2024 END ******************
            # if it didn't work, there isn't an ESPRESSO pod, so we have to create one
            if not res.ok:
                # display user message
                print('Creating the ESPRESSO pod')
                # register endpoint
                register_endpoint = str(self.image.value(snode,self.namespace.RegisterEndpoint))
                # do a POST request to create the ESPRESSO pod
                res = requests.post(
                    register_endpoint,
                    json={
                    "createWebId": "on",
                    "webId": "",
                    "register": "on",
                    "createPod": "on",
                    "podName": self.espressopodname,
                    "email": self.espressoemail,
                    "password": self.password,
                    "confirmPassword": self.password,
                    },
                    timeout=5000,
                )
                if not res.ok:
                    raise Exception(f"Could not create account: {res.status_code} {res.text}")

                # construct a CSSaccess object with the identity provider, 
                # the ESPRESSO email, and the password
                CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
                # HO 25/09/2024 BEGIN ******************
                #try:
                # now try again to access the ESPRESSO pod and display the response text
                print(CSSA.get_file(esppodaddress))
                #except:
                    #print("ESPRESSOcreate: Couldn't get file at " + esppodaddress + ", trying again.")
                    #print(CSSA.get_file(esppodaddress))
                # HO 25/09/2024 BEGIN ******************
                 
            else: # if it did work, display user message
                print('ESPRESSO pod is present at '+IDP+self.espressopodname+'/')
        #print('self = ' + str(self))

    """
    Creates the pods on the servers.
    
    If a pod is already there, delete all the files in it.
    If a pod isn't already there, create it.
    
    param: self
    """
    def podcreate(self):
        # For each server node
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # for every pod on this server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod address
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                # get the pod name
                podname=str(self.image.value(pnode,self.namespace.Name))
                # get the pod email
                email=str(self.image.value(pnode,self.namespace.Email))
                # get the WebID
                webid=str(self.image.value(pnode,self.namespace.WebID))
                # get the triple string
                triplestring=str(self.image.value(pnode,self.namespace.TripleString))
                # access the pod and display the response text
                # HO 25/09/2024 BEGIN *****************
                #try: 
                res=CSSaccess.get_file(podaddress)
                #except:
                    #print("podcreate: Couldn't get file at " + podaddress + ", trying again.")
                    #res=CSSaccess.get_file(podaddress)
                # HO 25/09/2024 END *****************
                
                # if it worked
                if res.ok:
                    # then say the pod is already there and we're going to 
                    # wipe it and start again.
                    print('Pod '+podname+ ' at '+IDP +' exists. Deleting.')
                    # delete all the files in this pod
                    self.cleanuppod(snode, pnode)
                else: # if it didn't work the pod isn't already there and we create it
                    print('Creating '+podname+ ' at '+IDP,CSSaccess.podcreate(IDP,podname,email,self.password))
        #print('self = ' + 'self')

                     
    # HO 14/08/2024 appears not to be in use
    def threadedpodcreate(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                IDP=str(self.image.value(snode,self.namespace.Address))
                podlist=[str(self.image.value(pnode,self.namespace.Name)) for pnode in self.image.objects(snode,self.namespace.Contains)]
                executor.submit(seriespodcreate,IDP,podlist,self.podemail,self.password)
                
    """
    Deletes a pod.
    
    param: self
    param: snode, the server node where the pod is located
    param: pnode, the pod to remove
    """
    def cleanuppod(self,snode,pnode):
        # get the identity provider
        IDP=str(self.image.value(snode,self.namespace.Address))
        # get the name of the pod to remove
        podname=str(self.image.value(pnode,self.namespace.Name))
        # user message
        print('cleaning up pod '+podname+' at '+ IDP)
        # get the pod email
        email=str(self.image.value(pnode,self.namespace.Email))
        # create a CSSaccess object with this identity provider, email and password
        CSSA=CSSaccess.CSSaccess(IDP, email, self.password)
        # HO 25/09/2024 BEGIN *******************
        try: 
            # get the auth string containing the ID and secret
            a=CSSA.create_authstring()
            # get the auth token from the client credentials
            t=CSSA.create_authtoken()
        except:
            print("Couldn't create auth token, trying again: ")
            CSSA=CSSaccess.CSSaccess(IDP, email, self.password)
            # get the auth string containing the ID and secret
            a=CSSA.create_authstring()
            # get the auth token from the client credentials
            t=CSSA.create_authtoken()
        # HO 25/09/2024 END *******************
        # get the pod address
        podaddress=str(self.image.value(pnode,self.namespace.Address))
        # crawl that pod and get back a dictionary of its files
        d=PodIndexer.crawl(podaddress, CSSA)
        # the keys of the dictionary are the files
        files=d.keys()
        # set up the progress bar
        pbar=tqdm.tqdm(total=len(files))
        # for every target URL
        for targetUrl in files:
            # delete the file
            # HO 25/09/2024 BEGIN *******************
            #try: 
            res=CSSA.delete_file(targetUrl)
            #except: 
                #print("Couldn't delete file at " + targetUrl + ", trying again: ")
                #res=CSSA.delete_file(targetUrl)
            # HO 25/09/2024 END *******************
            # display the response text
            print(res.text)
            # if the deletion attempt didn't work
            if not res.ok:
                # HO 25/09/2024 BEGIN *******************
                # get the auth token from the client credentials
                try: 
                    CSSA.create_authtoken()
                except:
                    print("Couldn't create auth token, trying again: ")
                    CSSA.create_authtoken()
                # HO 25/09/2024 BEGIN *******************
            # update the progress bar
            pbar.update(1)
        # close the progress bar
        pbar.close()
            
    """
    Upload the files to the pods.
    
    param: self
    """
    def uploadfiles(self):
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # for each pod on the server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod address
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                # get the pod name
                podname=str(self.image.value(pnode,self.namespace.Name))
                # get the username
                USERNAME=str(self.image.value(pnode,self.namespace.Email))
                # get the password
                PASSWORD=self.password
                # initialize an empty list to hold the file tuples
                filetuplelist=[]
                # for every file in the pod
                for fnode in self.image.objects(pnode,self.namespace.Contains):
                    # find the ReplaceText
                    substring=str(self.image.value(fnode,self.namespace.ReplaceText))
                    # find the file URL
                    targetUrl=str(self.image.value(fnode,self.namespace.Address))
                    # find the filetype
                    filetype=str(self.image.value(fnode,self.namespace.Filetype))
                    # the file itself
                    f=str(self.image.value(fnode,self.namespace.LocalAddress))
                    # add [local file address, file URL, filetype, ReplaceText] to the file tuple list
                    filetuplelist.append((f,targetUrl,filetype,substring))
                # create a CSSaccess object and get the client credentials
                CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                # HO 23/09/2024 BEGIN ****************
                try:
                    a=CSSA.create_authstring()
                    t=CSSA.create_authtoken()
                except:
                    print("Couldn't create authtoken to upload files, trying again: ")
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    a=CSSA.create_authstring()
                    t=CSSA.create_authtoken()
                # HO 23/09/2024 END ****************
                
                # display progress message
                print('populating',podaddress)
                # upload the file list, replacing any designated replacement text,
                # and display a progress bar while doing so
                FileUploader.uploadllistreplacewithbar(filetuplelist,self.replacetemplate,podaddress,CSSA)
        #print('self = ' + str(self))

    """
    Upload the .acl files
    
    param: self
    """
    def uploadacls(self):
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # for each pod on the server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod address
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                # get the pod name
                podname=str(self.image.value(pnode,self.namespace.Name))
                # get the username
                USERNAME=str(self.image.value(pnode,self.namespace.Email))
                # get the password
                PASSWORD=self.password
                # construct the client credentials
                CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                # HO 24/09/2024 BEGIN **************
                try:
                    a=CSSA.create_authstring()
                    t=CSSA.create_authtoken()
                except:
                    print("Couldn't create authtoken. Trying again: ")
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    a=CSSA.create_authstring()
                    t=CSSA.create_authtoken()
                # HO 24/09/2024 END **************
                # get the WebID
                webid=str(self.image.value(pnode,self.namespace.WebID))
                # display progress message
                # for each file in the pod
                for fnode in self.image.objects(pnode,self.namespace.Contains):
                    # get the URL
                    targetUrl=str(self.image.value(fnode,self.namespace.Address))
                    
                    # initialize a list to hold the WebIDs
                    webidlist=[]
                    # for every agent that can access this file
                    for anode in self.image.objects(fnode,self.namespace.AccessibleBy):
                        # get the agent's WebID
                        webid=str(self.image.value(anode,self.namespace.WebID))
                        # and add the WebID to the list
                        webidlist.append(webid)
                    
                    # check if this is an open-access file
                    openbool= fnode in self.image.subjects(self.namespace.Type,self.namespace.OpenFile)
                    # update the .acl file to grant Read access to the given list of WebIDs
                    # (and make c:me the owner)
                    # HO 25/09/2024 BEGIN **************
                    #try:
                    res=CSSA.makeurlaccessiblelist(targetUrl,podaddress,webid,webidlist,openbool)
                    #except:
                        #print("Couldn't make webidlist accessible at " + targeturl + ", trying again: ")
                        #res=CSSA.makeurlaccessiblelist(targetUrl,podaddress,webid,webidlist,openbool)
                    # HO 25/09/2024 END **************
                    # display the server response
                    print(res,end=' ')
                    print('\n')
       #print('self = ' + str(self))

    """
    Inserts the triples into the pods.
    
    param: self
    """
    def inserttriples(self):
        # for every server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # for each pod on the server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod address
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                # get the pod name
                podname=str(self.image.value(pnode,self.namespace.Name))
                # get the pod account username (the email)
                USERNAME=str(self.image.value(pnode,self.namespace.Email))
                # get the pod password
                PASSWORD=self.password
                CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                # HO 23/09/2024 BEGIN *********************
                try:
                    # get the pod auth string containing the ID and secret
                    a=CSSA.create_authstring()
                    # get the pod auth token from the client credentials
                    t=CSSA.create_authtoken()
                except KeyError: 
                    print("Couldn't create auth token, trying again: ")
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    # get the pod auth string containing the ID and secret
                    a=CSSA.create_authstring()
                    # get the pod auth token from the client credentials
                    t=CSSA.create_authtoken()
                # HO 23/09/2024 END *********************
                
                # get the pod WebID
                webid=str(self.image.value(pnode,self.namespace.WebID))
                # user progress message
                print('inserting triples ',podaddress)
                # get the triple string to insert
                triplestring=self.image.value(pnode,self.namespace.TripleString)
                # if there is a triple string
                if len(triplestring)>0:
                    # HO 23/09/2024 BEGIN *********************
                    # insert the triple string
                    try:
                        res=CSSA.inserttriplestring(webid[:-3],triplestring)
                    except:
                        print("Couldn't insert triple string, trying again: ")
                        res=CSSA.inserttriplestring(webid[:-3],triplestring)
                    # HO 23/09/2024 END *********************
                    # display the WebID and the result text
                    print(webid,res.text)
                
                # for every file in the pod
                for fnode in self.image.objects(pnode,self.namespace.Contains):   
                    # get the triple string
                    triplestring=self.image.value(fnode,self.namespace.TripleString)
                    # if there is a triple string
                    if len(triplestring)>0:
                        # HO 23/09/2024 BEGIN *********************
                        # insert the triple string
                        try: 
                            res=CSSA.inserttriplestring(webid[:-3],triplestring)
                        except:
                            print("Couldn't insert triple string, trying again: ")
                            res=CSSA.inserttriplestring(webid[:-3],triplestring)
                        # HO 23/09/2024 END *********************
                        # display the WebID and the result text
                        print(webid,res.text)
        #print('self = ' + str(self))

    # HO 14/08/2024 appears not to be in use
    def uploadpnodewithbar(self,pnode,IDP):
        podaddress=str(self.image.value(pnode,self.namespace.Address))
        
        USERNAME=str(self.image.value(pnode,self.namespace.Email))
        PASSWORD=self.password
        CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
        CSSA.create_authstring()
        CSSA.create_authtoken()
        pnodefilelist=[]
        for fnode in self.image.objects(pnode,self.namespace.Contains):
            pnodefilelist.append(fnode)
        n=len(pnodefilelist)
        print('populating',podaddress)
        pbar = tqdm.tqdm(total=n)
        for fnode in pnodefilelist:
            targetUrl=str(self.image.value(fnode,self.namespace.Address))
            filetype=str(self.image.value(fnode,self.namespace.Filetype))
            
            f=str(self.image.value(fnode,self.namespace.LocalAddress))
            file = open(f, "r")
            filetext=file.read()
            file.close()
            res=CSSA.put_url(targetUrl, filetext, filetype)
            if not res.ok:
                print(res)
                continue
            pbar.update(1)
        pbar.close()

    # HO 14/08/2024 appears not to be in use
    def uploadwithbarsthreaded(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                IDP=str(self.image.value(snode,self.namespace.Address))
                for pnode in self.image.objects(snode,self.namespace.Contains):
                    podaddress=str(self.image.value(pnode,self.namespace.Address))
                    USERNAME=str(self.image.value(pnode,self.namespace.Email))
                    PASSWORD=self.password
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                    filetuplelist=[]
                    for fnode in self.image.objects(pnode,self.namespace.Contains):
                        targetUrl=str(self.image.value(fnode,self.namespace.Address))
                        filetype=str(self.image.value(fnode,self.namespace.Filetype))
                        f=str(self.image.value(fnode,self.namespace.LocalAddress))
                        filetuplelist.append((f,targetUrl,filetype))
                    executor.submit(FileUploader.uploadllistwithbar, filetuplelist,podaddress,CSSA)

    # appears not to be in use
    def storeexplocal(self,dir):
        os.makedirs(dir,exist_ok=True)
        i=0
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            serword='S'+str(i)
            i=i+1
            serdir=dir+'/'+serword
            os.makedirs(serdir,exist_ok=True)
            for pnode in self.image.objects(snode,self.namespace.Contains):
                podname=str(self.image.value(pnode,self.namespace.Name))
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                poddir=serdir+'/'+podname
                os.makedirs(poddir,exist_ok=True)
                pnodefilelist=[]
                filetuples=[]
                print('populating',poddir)
                for fnode in self.image.objects(pnode,self.namespace.Contains):
                    targetUrl=str(self.image.value(fnode,self.namespace.Address))
                    filetype=str(self.image.value(fnode,self.namespace.Filetype))
                    filename=str(self.image.value(fnode,self.namespace.Filename))
                    f=str(self.image.value(fnode,self.namespace.LocalAddress))
                    file = open(f, "r")
                    filetext=file.read()
                    file.close()
                    floc=poddir+'/'+filename
                    file = open (floc,'w')
                    file.write(filetext)
                    file.close
                    webidlist=[]
                    for anode in self.image.objects(fnode,self.namespace.AccessibleBy):
                        webid=str(self.image.value(anode,self.namespace.WebID))
                        webidlist.append(webid)
                    webidstring='<'+'>,<'.join(webidlist)+'>'
                    #if fnode in self.openfilelist:
                    if fnode in self.image.subjects(self.namespace.Type,self.namespace.OpenFile):
                        acltext=returnaclopen(targetUrl,webidlist)
                    else:
                        acltext=returnacldefault(targetUrl,webidlist)
                    flocacl=poddir+'/'+filename+'.acl'
                    file = open (flocacl,'w')
                    file.write(acltext)
                    file.close
                    ftrunc=targetUrl[len(podaddress):]
                    filetuples.append((ftrunc,filetext,webidlist))
                index=PodIndexer.aclindextupleswebidnewdirs(filetuples)
                indexdir=poddir+'/'+self.podindexdir
                os.makedirs(indexdir,exist_ok=True)
                n=len(index.keys())
                pbar = tqdm.tqdm(total=n,desc=indexdir)
                for (name,body) in index.items():
                    targetf=indexdir+'/'+name
        #print(targetUrl,end=' ')
                    file = open (targetf,'w')
                    file.write(body)
                    file.close
                    pbar.update(1)
                pbar.close()

    # HO 14/08/2024 appears not to be in use
    def storeindexlocal(self,dir):
        i=0
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                IDP=str(self.image.value(snode,self.namespace.Address))
                serword='S'+str(i)
                i=i+1
                for pnode in self.image.objects(snode,self.namespace.Contains):
                    podaddress=str(self.image.value(pnode,self.namespace.Address))
                    podname=str(self.image.value(pnode,self.namespace.Name))
                    USERNAME=str(self.image.value(pnode,self.namespace.Email))
                    PASSWORD=self.password
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                    d=PodIndexer.aclcrawlwebidnew(podaddress,podaddress, CSSA)
                    indexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                    index=PodIndexer.aclindextupleswebidnewdirs(d) 
                    filename=dir+'/'+serword+podname+'.locind'
                    with open(filename, 'w') as f:
                        f.write(str(index))
                        f.close()
                    print('Local index',filename,'stored')

    # HO 14/08/2024 appears not to be in use
    def uploadindexlocal(self,dir):
        i=0
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                IDP=str(self.image.value(snode,self.namespace.Address))
                serword='S'+str(i)
                i=i+1
                for pnode in self.image.objects(snode,self.namespace.Contains):
                    podaddress=str(self.image.value(pnode,self.namespace.Address))
                    podname=str(self.image.value(pnode,self.namespace.Name))
                    USERNAME=str(self.image.value(pnode,self.namespace.Email))
                    PASSWORD=self.password
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                    indexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                    filename=dir+'/'+serword+podname+'.locind'
                    f = open(filename, "r")
                    indexstr=f.read()
                    f.close()
                    index=eval(indexstr)
                    print('starting uploading',filename)
                    executor.submit(PodIndexer.uploadaclindexwithbar, index, indexaddress, CSSA)

    """
    Recursively indexes the containers in each pod in each server, on-the-fly. Suitable for smaller experiments.
    
    param: self
    """
    def aclindexwebidnewthreaded(self):
        # execute these calls asynchronously
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
        # submit tasks
            # for each server
            for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                # get the identity provider
                IDP=str(self.image.value(snode,self.namespace.Address))
                # initialize a string to write the metaindex data
                testservindex=ServerIndex()
            
                # for each pod on this server
                for pnode in self.image.objects(snode,self.namespace.Contains):
                    # get the pod details
                    podaddress=str(self.image.value(pnode,self.namespace.Address))
                    podname=str(self.image.value(pnode,self.namespace.Name))
                    # here we need to create a podword for this pod relative to the server
                    podpath=podname+'/'+self.podindexdir
                    testservindex.addpod(podpath)
                    USERNAME=str(self.image.value(pnode,self.namespace.Email))
                    PASSWORD=self.password
                    # construct the client credentials
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    # HO 25/09/2024 BEGIN ************
                    try:
                        CSSA.create_authstring()
                        CSSA.create_authtoken()
                    except: 
                        print("Couldn't create auth token, trying again: ")
                        CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                        CSSA.create_authstring()
                        CSSA.create_authtoken()
                    # HO 25/09/2024 END ************
                    # gets a list of file tuples containing [relative path, text of the file, WebID list]
                    d=PodIndexer.aclcrawlwebidnew(podaddress,podaddress, CSSA)
                    # get the address of this pod index
                    indexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                    # sequentially number the webids that have access to resources on this server
                    for (id,text,webidlist) in d:     
                        testservindex.addwebids(podpath, webidlist)    

                    # get the inverted index for this file
                    podlevel_index=dict()
                    servtuples=PodIndexer.serverlevel_aclindextupleswebidnewdirs(d, podpath, testservindex)
                    # the first item is the pod level index, and the second item is the
                    # dictionary to be unwound into a server-level index
                    if (servtuples is not None):
                        # get the running total file count from each pod and add them up into the server-level total
                        runningsum=0
                        if (len(servtuples) >= 1):
                            podlevel_index = servtuples[0]
                            if config.INDEX_FILECOUNT_FILENAME in podlevel_index.keys():
                                runningsum = podlevel_index[config.INDEX_FILECOUNT_FILENAME]
                        if (len(servtuples) >= 2):
                            testservindex = servtuples[1]
                            testservindex.indexsum=testservindex.indexsum+int(runningsum)

                    # submit the task with the inverted podlevel_index for this file
                    print('indexaddress = ' + indexaddress)
                    print('CSSA = ' + str(CSSA))
                    executor.submit(PodIndexer.uploadaclindexwithbar, podlevel_index, indexaddress, CSSA)

                # unwind the server-level metaindex
                testservindex.buildservermetaindex_simple()

                # find the ESPRESSO pod to write to
                enode=self.image.value(snode,self.namespace.ContainsEspressoPod)
                metaindexaddress=str(self.image.value(enode,self.namespace.MetaindexAddress))
                # construct the client credentials
                CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
                # HO 25/09/2024 BEGIN ************
                try:
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                except:
                    print("Couldn't create auth token, trying again: ")
                    CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                # HO 25/09/2024 END ************
                # and write that server-level index
                executor.submit(PodIndexer.uploadaclindexwithbar, testservindex.index, metaindexaddress, CSSA)

        # quick-and-dirty tests for files known to be at the given hard-coded addresses
        CSSA=CSSaccess.CSSaccess('https://srv04031.soton.ac.uk:3000', self.espressoemail, self.password)
        try: 
            CSSA.create_authstring()
            CSSA.create_authtoken()
        except:
            print("Couldn't get auth token, trying again: ")
            CSSA=CSSaccess.CSSaccess('https://srv04031.soton.ac.uk:3000', self.espressoemail, self.password)
            CSSA.create_authstring()
            CSSA.create_authtoken()
            
        try: 
            res = CSSA.get_file('https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/httpexampleorgagent4profilecardme.webid')
        except:
            print("Couldn't get file at https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/httpexampleorgagent4profilecardme.webid, trying again") 
            res = CSSA.get_file('https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/httpexampleorgagent4profilecardme.webid')
        
        print('Contents of https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/httpexampleorgagent4profilecardme.webid: ' + res)
        print('---------------')
        try: 
            res = CSSA.get_file('https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/e/f/f/e/c/t.ndx')
        except: 
            print("Couldn't get file at https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/e/f/f/e/c/t.ndx, trying again: ")
            res = CSSA.get_file('https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/e/f/f/e/c/t.ndx')
        
        print('Contents of https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/e/f/f/e/c/t.ndx: ' + res)
        print('---------------')
        try:
            res = CSSA.get_file('https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/index.sum')
        except:
            print("Couldn't get file at https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/index.sum, trying again: ")
            res = CSSA.get_file('https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/index.sum')
        
        print('Contents of https://srv04031.soton.ac.uk:3000/ESPRESSO/ardfhealthmetaindex/index.sum: ' + res)
        print('===============')

    """
    Create and/or update the ACL metaindexes in the server-level ESPRESSO pods.
    
    param: self
    """ 
    def aclmetaindex(self): 
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            print('IDP=' + IDP)
            # initialize an output string for the metaindex data
            metaindexpodlist=''
            
            # for each pod on the server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod index address
                indexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                # append a newline to the pod index address to prepare it for writing to a file
                addstring=indexaddress+'\r\n'
                # append the current pod index address to the output string
                metaindexpodlist+=addstring    
                
            # instantiate a new CSSaccess object for the server-level ESPRESSO pod
            CSSAe=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
            # HO 23/09/2024 BEGIN **************
            # get the auth string containing the ID and secret for the server-level ESPRESSO pod
            try: 
                CSSAe.create_authstring()
                # get the auth token for the server-level ESPRESSO pod from the client credentials
                CSSAe.create_authtoken()
            except:
                print("Couldn't create auth token. Trying again: ")
                # instantiate a new CSSaccess object for the server-level ESPRESSO pod
                CSSAe=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
                CSSAe.create_authstring()
                # get the auth token for the server-level ESPRESSO pod from the client credentials
                CSSAe.create_authtoken()
            # HO 23/09/2024 END **************
            # PUT the new metaindex data out to the server-level ESPRESSO pod metaindex,
            # and display the identity provider and the server response to the PUT request
            enode=self.image.value(snode,self.namespace.ContainsEspressoPod)
            targurl = str(self.image.value(enode,self.namespace.MetaindexFile))
            # HO 23/09/2024 BEGIN **************
            try:
                print(IDP,CSSAe.put_url(targurl, metaindexpodlist, 'text/csv'))
            except:
                print("Couldn't put to " + targurl + ", trying again: ")
                print(IDP,CSSAe.put_url(targurl, metaindexpodlist, 'text/csv'))
            # HO 23/09/2024 END **************
        #print('self = ' + str(self))

    """
    Suitable for smaller experiments.
    
    param: self
    """
    def indexfixerwebidnew(self):
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # HO 17/09/2024 BEGIN ******
            testservindex=ServerIndex()
            # HO 17/09/2024 END ********
            # for each pod on the server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod details
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                podname=str(self.image.value(pnode,self.namespace.Name))
                USERNAME=str(self.image.value(pnode,self.namespace.Email))
                PASSWORD=self.password
                # display progress message
                print("checking index of "+IDP+podname)
                # HO 17/09/2024 BEGIN ************
                # here we need to create a podword for this pod relative to the server
                podpath=podname+'/'+self.podindexdir
                testservindex.addpod(podpath)
                # HO 17/09/2024 END **************
                # construct the client credentials
                CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                # HO 25/09/2024 BEGIN ******
                try:
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                except:
                    print("Couldn't create auth token, trying again: ") 
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                # HO 25/09/2024 END ******
                # get the index address
                indexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                # get the list of files at the given index address
                # HO 17/09/2024 BEGIN *****************
                n=PodIndexer.crawllist(indexaddress, CSSA)
                # HO 17/09/2024 END *****************

                print('currently in index of ' +IDP+podname +':' +str(len(n)))
                # crawl the container at the pod address and get back a list of file tuples
                d=PodIndexer.aclcrawlwebidnew(podaddress, podaddress,CSSA)
                # HO 17/09/2024 BEGIN **********
                for (id,text,webidlist) in d:
                    # Sequentially number the WebIDs            
                    testservindex.addwebids(podpath, webidlist) 
                
                # construct an LdpIndex from the list of file tuples
                podlevel_index=dict()
                servtuples=PodIndexer.serverlevel_aclindextupleswebidnewdirs(d, podpath, testservindex)
                if (servtuples is not None):
                    runningsum=0
                    if (len(servtuples) >= 1):
                        podlevel_index = servtuples[0]
                            
                        if config.INDEX_FILECOUNT_FILENAME in podlevel_index.keys():
                            runningsum = podlevel_index[config.INDEX_FILECOUNT_FILENAME]
                    if (len(servtuples) >= 2):
                        testservindex = servtuples[1]
                        testservindex.indexsum=testservindex.indexsum+int(runningsum)
                
                print('should be in index of ' +IDP+podname +':' +str(len(podlevel_index.keys())))
                
                n=PodIndexer.crawllist(indexaddress, CSSA)
                # files from the list of files we got from the indexaddress, remove them one by one
                compareindexes(podaddress, self.podindexdir, n, podlevel_index)

                # populate the files
                PodIndexer.uploadaclindexwithbar(podlevel_index, indexaddress, CSSA)
                # HO 17/09/2024 END **************
            #HO 17/09/2024 BEGIN ****************
            testservindex.buildservermetaindex_simple()
            # find the ESPRESSO pod to write to
            enode=self.image.value(snode,self.namespace.ContainsEspressoPod)
            metaindexaddress=str(self.image.value(enode,self.namespace.MetaindexAddress))
            esppodname=self.image.value(enode,self.namespace.Name)
            # construct the client credentials
            CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
            # HO 25/09/2024 BEGIN ***********
            try: 
                CSSA.create_authstring()
                CSSA.create_authtoken()
            except:
                print("Couldn't create auth token, trying again: ")
                CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
                CSSA.create_authstring()
                CSSA.create_authtoken()
            # HO 25/09/2024 BEGIN ***********
            # get the list of files at the given metaindex address
            n=PodIndexer.crawllist(metaindexaddress, CSSA)
            print('currently in index of ' +IDP+esppodname +':' +str(len(n)))
            print('should be in index of ' +IDP+esppodname +':' +str(len(testservindex.index.keys())))
            # files from the list of files we got from the metaindexaddress, remove them one by one
            compareindexes('', metaindexaddress, n, testservindex.index)
                    
            PodIndexer.uploadaclindexwithbar(testservindex.index, metaindexaddress, CSSA)
            #HO 17/09/2024 END ******************

    # HO 14/08/2024 appears not to be in use
    def indexfixerthreaded(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                IDP=str(self.image.value(snode,self.namespace.Address))
                metaindexdata=''
                for pnode in self.image.objects(snode,self.namespace.Contains):
                    podaddress=str(self.image.value(pnode,self.namespace.Address))
                    podname=str(self.image.value(pnode,self.namespace.Name))
                    USERNAME=str(self.image.value(pnode,self.namespace.Email))
                    PASSWORD=self.password
                    #addstring=indexaddress+'\r\n'
                    #metaindexdata+=addstring
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    CSSA.create_authstring()
                    CSSA.create_authtoken()
                    indexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                    n=PodIndexer.indexchecker(indexaddress, CSSA)
                    print('currently in index of' +IDP+podname +':' +str(len(n)))
                    d=PodIndexer.aclcrawl(podaddress, CSSA)
                    
                    #index=rdfindex.podlistindexer(d,namespace,podaddress,reprformat)
                    index=PodIndexer.aclindextuples(d)
                    print('should be in index of' +IDP+podname +':' +str(len(index.keys())))
                    for f in n:
                        index.pop(f)
                    #for f in self.forbidden:
                        #index.pop(f+'.ndx','no key')
                    print("Difference?"+str(len(index.keys())))
                    #brewmaster.uploadaclindex(index, indexaddress, CSSA)
                    executor.submit(PodIndexer.uploadaclindex, index, indexaddress, CSSA)

    """
    Creates an .acl file that makes each pod's index file open access.
    
    param: self   
    """
    def indexpub(self):
        # for every server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # display progress message
            print('opening indexes for '+ IDP)
            # for every pod on the server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # get the pod index address
                podindexaddress=str(self.image.value(pnode,self.namespace.IndexAddress))
                # get the pod account username (email)
                USERNAME=str(self.image.value(pnode,self.namespace.Email))
                # get the pod account password
                PASSWORD=self.password
                # create a CSSaccess object with the identity provider, username and password
                CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                
                # HO 22/09/2024 BEGIN ************
                try: 
                    # get the auth string containing the pod ID and secret
                    CSSA.create_authstring()
                    # get the pod auth token from the client credentials
                    CSSA.create_authtoken()
                except:
                    # try one more time
                    # create a CSSaccess object with the identity provider, username and password
                    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
                    # get the auth string containing the pod ID and secret
                    CSSA.create_authstring()
                    # get the pod auth token from the client credentials
                    CSSA.create_authtoken()
                # HO 22/09/2024 END ************
                
                # construct the target URL for an .acl file for the pod index address
                targetUrl=podindexaddress+'.acl'
                # construct the authorization headers for a turtle file
                headers={ 'content-type': 'text/turtle', 'authorization':'DPoP '+CSSA.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", CSSA.dpopKey)}
                # do a PUT request with the acldefopen query
                # which makes c.me (the experiment) the owner of the .acl file
                # and makes the .acl file open access 
                # HO 22/09/2024 BEGIN ************
                try:
                    #res= requests.put(targetUrl,headers=headers,data=acldefopen)
                    res= requests.put(targetUrl,headers=headers,data=acldefopen, timeout=5000)
                except:
                    print("Couldn't do a put to " + targetUrl + ", trying again: ")
                    res= requests.put(targetUrl,headers=headers,data=acldefopen,timeout=5000)
                # HO 22/09/2024 END ************
                # display the .acl file URL and the server response to the PUT request
                print(targetUrl,res)
        #print('self = ' + str(self))
        

    # HO 14/08/2024 appears not to be in use
    def indexpubthreaded(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            
            for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
                IDP=str(self.image.value(snode,self.namespace.Address))
                print('opening indexes for '+ IDP)
                addresstemplate='/'+self.podindexdir+'.acl'
                podlist=[str(self.image.value(pnode,self.namespace.Name)) for pnode in self.image.objects(snode,self.namespace.Contains)]
                executor.submit(seriespub,IDP,podlist,addresstemplate,self.podemail,self.password)
                    
    """
    Makes the ESPRESSO server-level metaindexes accessible to the experiment.
    
    param: self
    """
    def metaindexpub(self):
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            print('Making the metaindex for ' + snode + ' accessible to the experiment')
            # get the identity provider
            IDP=str(self.image.value(snode,self.namespace.Address))
            # display progress message
            print('Making the metaindex for '+IDP+' accessible to the experiment')
            # create a CSSaccess object for this identity provider, the ESPRESSO
            # pod email, and the ESPRESSO pod password
            CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
            #HO 23/09/2024 BEGIN ******************
            try:
                # get the auth string containing the ESPRESSO pod ID and secret
                a=CSSA.create_authstring()
                # get the ESPRESSO pod auth token from the client credentials
                t=CSSA.create_authtoken()
            except: 
                print("Couldn't create auth token. Trying again: ")
                CSSA=CSSaccess.CSSaccess(IDP, self.espressoemail, self.password)
                # get the auth string containing the ESPRESSO pod ID and secret
                a=CSSA.create_authstring()
                # get the ESPRESSO pod auth token from the client credentials
                t=CSSA.create_authtoken()
            # make the ESPRESSO index file accessible
            # we do need to make the whole metaindex folder accessible to the experiment
            # not just the metaindex file
            try:
                res=CSSA.makefileaccessible(self.espressopodname, self.espressoindexdir)
            except:
                print("Couldn't make " + self.espressoindexdir + " accessible, trying again: ")
                res=CSSA.makefileaccessible(self.espressopodname, self.espressoindexdir)
            #HO 23/09/2024 END ******************

            # display the server response
            print(res)
       #print('self = ' + str(self))

    # HO 14/08/2024 appears not to be in use
    def storelocalfileszip(self,dir):
        #os.makedirs(self.localimage,exist_ok=True)
        pbar=tqdm.tqdm(total=self.filenum)
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            serdir=dir+str(self.image.value(snode,self.namespace.Sword))
            os.makedirs(serdir,exist_ok=True)
            for pnode in self.image.objects(snode,self.namespace.Contains):
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                podzipfile=serdir +'/'+str(self.image.value(pnode,self.namespace.Name))+'.zip'
                podwebid=str(self.image.value(pnode,self.namespace.WebID))
                with ZipFile(podzipfile, 'w') as podzip:
                    for fnode in self.image.objects(pnode,self.namespace.Contains):
                        targetUrl=str(self.image.value(fnode,self.namespace.Address))
                        filetype=str(self.image.value(fnode,self.namespace.Filetype))
                        filename=str(self.image.value(fnode,self.namespace.Filename))
                        f=str(self.image.value(fnode,self.namespace.LocalAddress))
                        file = open(f, "r")
                        filetext=file.read()
                        file.close()
                        podzip.writestr(filename,filetext)
                        
                        webidlist=[]
                        for anode in self.image.objects(fnode,self.namespace.AccessibleBy):
                            webid=str(self.image.value(anode,self.namespace.WebID))
                            webidlist.append(webid)
                        #webidstring='<'+'>,<'.join(webidlist)+'>'
                        openbool = fnode in self.image.subjects(self.namespace.Type,self.namespace.OpenFile)
                        
                        acltext=CSSaccess.returnacllist(targetUrl,podaddress,webidlist,openbool)
                        flocacl=filename+'.acl'
                        podzip.writestr(flocacl,acltext)
                        pbar.update(1)
                        #ftrunc=targetUrl[len(podaddress):]
                        #filetuples.append((ftrunc,filetext,webidlist))
        pbar.close()

    # HO 14/08/2024 appears not to be in use
    def storelocalindexzip(self,dir):
        #os.makedirs(self.localimage,exist_ok=True)
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            serdir=dir+str(self.image.value(snode,self.namespace.Sword))
            os.makedirs(serdir,exist_ok=True)
            for pnode in self.image.objects(snode,self.namespace.Contains):
                podzipindexfile=serdir +'/'+str(self.image.value(pnode,self.namespace.Name))+'index.zip'
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                podwebid=str(self.image.value(pnode,self.namespace.WebID))
                filetuples=[]
                for fnode in self.image.objects(pnode,self.namespace.Contains):
                        targetUrl=str(self.image.value(fnode,self.namespace.Address))
                        filetype=str(self.image.value(fnode,self.namespace.Filetype))
                        filename=str(self.image.value(fnode,self.namespace.Filename))
                        f=str(self.image.value(fnode,self.namespace.LocalAddress))
                        file = open(f, "r")
                        filetext=file.read()
                        file.close()
                        webidlist=[]
                        for anode in self.image.objects(fnode,self.namespace.AccessibleBy):
                            webid=str(self.image.value(anode,self.namespace.WebID))
                            webidlist.append(webid)
                        #webidstring='<'+'>,<'.join(webidlist)+'>'
                        #openbool = fnode in self.openfilelist
                        if fnode in self.image.subjects(self.namespace.Type,self.namespace.OpenFile):
                            # HO 11/09/2024 BEGIN *********
                            #webidlist.append('*')
                            webidlist.append(OPENACCESS_SYMBOL)
                            # HO 11/09/2024 END ***********
                        ftrunc=targetUrl[len(podaddress):]
                        filetuples.append((ftrunc,filetext,webidlist))
                index=PodIndexer.aclindextupleswebidnew(filetuples)
                n=len(index.keys())
                pbar = tqdm.tqdm(total=n,desc=podzipindexfile)
                with ZipFile(podzipindexfile, 'w') as podindexzip:
                    for (name,body) in index.items():
                        
                        podindexzip.writestr(name,body)
                        info = podindexzip.getinfo(name)
                        info.external_attr = 0o777 << 16
                        pbar.update(1)
                pbar.close()

    # HO 14/08/2024 appears not to be in use
    def assignlocalimage(self,dir):
        i=0
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            sword='S'+str(i)
            i=i+1
            self.image.add((snode,self.namespace.LocalAddress,Literal(dir+self.podname+'/'+sword)))
            pass
    """
    Zip the indexes and store locally. For experiments that are too big to index on the fly.
    
    param: self
    param: zipdir, the directory
    """        
    def storelocalindexzipdirs(self,zipdir):
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # name the current zip directory after the current server
            serdir=zipdir+str(self.image.value(snode,self.namespace.Sword))
            # create directories recursively, no need to raise error if any already exist
            print('make directory ' + serdir)
            os.makedirs(serdir,mode=0o777,exist_ok=True)
            print('made directory ' + serdir)
            # for every pod in this server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # name the pod zip index file
                podzipindexfile=serdir +'/'+str(self.image.value(pnode,self.namespace.Name))+'index.zip'
                # get the pod address
                podaddress=str(self.image.value(pnode,self.namespace.Address))
                # create an empty list for the file tuples
                filetuples=[]
                # for each file in the pod
                for fnode in self.image.objects(pnode,self.namespace.Contains):
                    # get the file details
                    targetUrl=str(self.image.value(fnode,self.namespace.Address))
                    filetype=str(self.image.value(fnode,self.namespace.Filetype))
                    filename=str(self.image.value(fnode,self.namespace.Filename))
                    f=str(self.image.value(fnode,self.namespace.LocalAddress))
                    # open the file for reading
                    file = open(f, "r")
                    filetext=file.read()
                    file.close()
                    # create a list to hold the WebIDs that have access to this file
                    webidlist=[]
                    # and add each WebID to the list
                    for anode in self.image.objects(fnode,self.namespace.AccessibleBy):
                        webid=str(self.image.value(anode,self.namespace.WebID))
                        webidlist.append(webid)
                    # if a given file is open access, represent that in the list with an asterisk
                    if fnode in self.image.subjects(self.namespace.Type,self.namespace.OpenFile):
                        webidlist.append(config.OPENACCESS_SYMBOL)

                    # cut the pod address off the target URL
                    ftrunc=targetUrl[len(podaddress):]
                    # add the truncated pod address, file text, web ID list to the file tuples
                    filetuples.append((ftrunc,filetext,webidlist))
                # construct an inverted index from the file tuples
                print('constructing inverted index')
                index=PodIndexer.aclindextupleswebidnewdirs(filetuples)
                # work out how many .ndx files there are?
                n=len(index.keys())
                # set up a progress bar
                pbar = tqdm.tqdm(total=n,desc=podzipindexfile)
                
                # open the pod index zip file for writing
                podindexzip=ZipFile(podzipindexfile, 'w')
                # for each item in the index dictionary
                for (name,body) in index.items():
                    # write them to the zip file (name/key is archive name)
                    podindexzip.writestr(name,body)
                    # gets info about this item
                    info = podindexzip.getinfo(name)

                    # give full access to this file/item
                    info.external_attr = 0o777 << 16
                    # update the progress bar
                    pbar.update(1)
                # close the progress bar
                pbar.close()
                # close the pod index zip file
                podindexzip.close()
            
    """
    Zip the indexes and store locally. For experiments that are too big to index on the fly.
    
    param: self
    param: zipdir, the directory
    """        
    def serverlevel_storelocalindexzipdirs(self,zipdir):
        print('inside serverlevel_storelocalindexzipdirs')
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            # name the current zip directory after the current server
            serdir=zipdir+str(self.image.value(snode,self.namespace.Sword))
            testservindex=ServerIndex()

            # create directories recursively, no need to raise error if any already exist
            print('make directory ' + serdir)
            os.makedirs(serdir,mode=0o777,exist_ok=True)
            print('made directory ' + serdir)
            
            # name the server level zip metaindex file
            enode=self.image.value(snode,self.namespace.ContainsEspressoPod)
            serzipindexfile=serdir +'/' +self.podname+'metaindex.zip'
            
            # for every pod in this server
            for pnode in self.image.objects(snode,self.namespace.Contains):
                # name the pod zip index file
                podzipindexfile=serdir +'/'+str(self.image.value(pnode,self.namespace.Name))+'index.zip'
                # get the pod address
                podaddress=str(self.image.value(pnode,self.namespace.Address))

                # here we need to create a podword for this pod relative to the server
                podname=str(self.image.value(pnode,self.namespace.Name))
                podpath=podname+'/'+self.podindexdir
                testservindex.addpod(podpath)

                # create an empty list for the file tuples
                filetuples=[]
                # for each file in the pod
                for fnode in self.image.objects(pnode,self.namespace.Contains):
                    # get the file details
                    targetUrl=str(self.image.value(fnode,self.namespace.Address))
                    filetype=str(self.image.value(fnode,self.namespace.Filetype))
                    filename=str(self.image.value(fnode,self.namespace.Filename))
                    f=str(self.image.value(fnode,self.namespace.LocalAddress))
                    # open the file for reading
                    file = open(f, "r")
                    filetext=file.read()
                    file.close()
                    # create a list to hold the WebIDs that have access to this file
                    webidlist=[]
                    # and add each WebID to the list
                    for anode in self.image.objects(fnode,self.namespace.AccessibleBy):
                        webid=str(self.image.value(anode,self.namespace.WebID))
                        webidlist.append(webid)
                    # if a given file is open access, represent that in the list with an asterisk
                    if fnode in self.image.subjects(self.namespace.Type,self.namespace.OpenFile):
                        webidlist.append(config.OPENACCESS_SYMBOL)

                    # cut the pod address off the target URL
                    ftrunc=targetUrl[len(podaddress):]
                    # add the truncated pod address, file text, web ID list to the file tuples
                    filetuples.append((ftrunc,filetext,webidlist))

                    # Sequentially number the WebIDs            
                    testservindex.addwebids(podpath, webidlist) 
                # construct an inverted index from the file tuples
                print('constructing inverted index')
                podlevel_index=dict()
                servtuples=PodIndexer.serverlevel_aclindextupleswebidnewdirs(filetuples, podpath, testservindex)

                if (servtuples is not None):
                    runningsum=0
                    if (len(servtuples) >= 1):
                        podlevel_index = servtuples[0]
                        if config.INDEX_FILECOUNT_FILENAME in podlevel_index.keys():
                            runningsum = podlevel_index[config.INDEX_FILECOUNT_FILENAME]
                    if (len(servtuples) >= 2):
                        testservindex = servtuples[1]
                        testservindex.indexsum=testservindex.indexsum+int(runningsum)
                
                # work out how many .ndx files there are?
                n=len(podlevel_index.keys())
                print('About to write podlevel_index')

                # set up a progress bar
                pbar = tqdm.tqdm(total=n,desc=podzipindexfile)
                # open the pod index zip file for writing
                podindexzip=ZipFile(podzipindexfile, 'w')

                # for each item in the index dictionary
                for (name,body) in podlevel_index.items():

                    # write them to the zip file (name/key is archive name)
                    podindexzip.writestr(name,body)
                    # gets info about this item
                    info = podindexzip.getinfo(name)
                    # give full access to this file/item
                    info.external_attr = 0o777 << 16
                    # update the progress bar
                    pbar.update(1)
                # close the progress bar
                pbar.close()
                # close the pod index zip file
                podindexzip.close()

            # webid files first
            testservindex.buildservermetaindex_simple()

            n=len(testservindex.index.keys())
            print('About to write server level index:')
            # set up a progress bar
            pbar = tqdm.tqdm(total=n,desc=serzipindexfile)
            # open the server index zip file for writing
            serindexzip=ZipFile(serzipindexfile, 'w')
            # for each item in the index dictionary
            for (name,body) in testservindex.index.items():
                # write them to the zip file (name/key is archive name)
                serindexzip.writestr(name,body)
                # gets info about this item
                info = serindexzip.getinfo(name)
                #print('about to give full access')
                # give full access to this file/item
                info.external_attr = 0o777 << 16
                # update the progress bar
                pbar.update(1)
            # close the progress bar
            pbar.close()
            # close the server index zip file
            serindexzip.close()
            
    """
    Distribute the zip files around the servers using ssh
    
    param: self
    param: zipdir, the zip directory
    param: SSHUser
    param: SSHPassword
    param: targetdir, default: '/srf/espresso/'
    """
    def distributezips(self,zipdir,SSHUser,SSHPassword,targetdir='/srv/espresso/'):
        # counter
        i=0
        # for each server
        for snode in self.image.subjects(self.namespace.Type,self.namespace.Server):
            server=str(self.image.value(snode,self.namespace.Address)).rsplit('/')[-2].rsplit(':')[0]
            # display progress message
            print('Uploading',server)
            # instantiate the client
            client = SSHClient()
            # automatically add the hostname and new host key to the local HostKeys object
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # another SSH client, okay
            ssh = SSHClient()
            # load the host keys for the first client
            client.load_system_host_keys() 
            # connect to the first client   
            client.connect(server, port=22, username=SSHUser, password=SSHPassword)
            # secure copy protocol client
            scp = SCPClient(client.get_transport())
            # name the zip directory after the server
            sdir=zipdir+str(self.image.value(snode,self.namespace.Sword))+'/'
            # set up the progress bar
            pbar=tqdm.tqdm(total=len(os.listdir(sdir)))
            # for every item in the server directory, join the path segments to the filename
            for filename in os.listdir(sdir):
                filepath = os.path.join(sdir, filename)
                # checking if it is a file
                if os.path.isfile(filepath) and not filename.startswith('.'):
                    # then put the file in the target directory
                    scp.put(filepath,targetdir)
                # update the progress bar
                pbar.update(1)
            # close the progress bar
            pbar.close()
            
"""
Compares two indexes by their keys.

param: podaddress, the address of the pod where one index is located. Used to calculate the key offset from an absolute path.
param: indexaddress, the index address relative to the pod. Used to calculate the key offset from an absolute path.
param: comparefrom, the first of two indexes to compare. Assumes the keys have an absolute path that needs to be offset in order to make the comparison.
param: compareto, the second of two indexes to compare. 
"""
def compareindexes(podaddress, indexaddress, comparefrom, compareto):
    offset = len(podaddress+indexaddress)
        
    for f in comparefrom:
        splitf = str(f)
        splitf = splitf[offset:]

        if splitf in compareto.keys():
            print('splitf ' + splitf + ' is in compareto.keys!')
            compareto.pop(splitf)
                    
    print("Difference?"+str(len(compareto.keys())))

# possibly used by keywordfinder
def loadexp(filename):
        podname=filename[:-7]
        experiment=ESPRESSOexperiment(podname=podname)
        experiment.loadexp(filename)
        return experiment

# HO 14/08/2024 appears not to be in use
def seriespodcreate(IDP,podlist,podemail,password):
    pbar=tqdm.tqdm(total=len(podlist))
    for podname in podlist:
        email=podname+podemail
        CSSaccess.podcreate(IDP,podname,email,password)
        pbar.update(1)
    pbar.close(1)

# HO 14/08/2024 appears not to be in use
def seriespub(IDP,podlist,addresstemplate,podemail,password):
    pbar=tqdm.tqdm(total=len(podlist))
    for podname in podlist:
        USERNAME=podname+podemail
        CSSA=CSSaccess.CSSaccess(IDP, USERNAME, password)
        CSSA.create_authstring()
        CSSA.create_authtoken()
                
                
                    #print(acldef)
        targetUrl=IDP+podname+addresstemplate
                    #print(targetUrl)
        headers={ 'content-type': 'text/turtle', 'authorization':'DPoP '+CSSA.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", CSSA.dpopKey)}
        requests.put(targetUrl,headers=headers,data=acldefopen)
        pbar.update(1)
    pbar.close()
                #res=CSSAccess.get_file(indexaddress+'.acl')
                    #print(targetUrl,res)