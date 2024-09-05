# cleantext: https://pypi.org/project/cleantext/
# string: https://docs.python.org/3/library/string.html
import cleantext, string
# rdflib.URIRef: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.URIRef
# rdflib.BNode: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.BNode
# rdflib.Literal: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.Literal
# rdflib.Graph: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph
# rdflib.Namespace: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.Namespace
from rdflib import URIRef, BNode, Literal, Graph, Namespace
# concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html
import concurrent.futures
# time: https://docs.python.org/3/library/time.html#module-time
# tqdm: https://tqdm.github.io/
import time, tqdm
# multiprocessing.Pool: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
from multiprocessing import Pool

"""
Crawls a pod.

param: address, the address of the pod to crawl.
param: CSSa, the CSSaccess object that allows access to the pod.
return: filedict, a dictionary of the files in that pod 
"""
def crawl(address, CSSa):
    # initialize an empty dictionary of files
    filedict= dict()
    # get the data from the pod at that address
    data = CSSa.get_file(address)
    # parse the graph of that pod
    g=Graph().parse(data=data,publicID=address)
    # query to get every file contained in that graph
    q='''
    prefix ldp: <http://www.w3.org/ns/ldp#>
    
    SELECT ?f WHERE{
        ?a ldp:contains ?f.
    }
    '''
    # For every result returned by the query
    for r in g.query(q):
        # get a string representation of that file
        f=str(r["f"])
        # if this is a directory
        if f[-1]=='/':
            # crawl this directory
            d=crawl(f,CSSa)
            filedict|=d
        # if it's a file, and it's not one of our operational files
        elif ('.' in f.rsplit('/')[-1]) and (not f.endswith('ttl')) and (not f.endswith('.ndx')) and (not f.endswith('.file')):
            # get the file as a dictionary representation
            filedict[f]=CSSa.get_file(f)
        else:
            # do nothing
            pass

    # return the file dictionary
    return filedict

"""
Crawls a container at a given address and returns a list of file tuples

param: address, the address of a container
param: podaddress, the address of a pod
param: CSSa, the CSSaccess object providing the client credentials
return: filetuples, a list of file tuples containing [relative path, text of the file, WebID list]
"""
def aclcrawlwebidnew(address,podaddress, CSSa):
    #print('inside aclcrawlwebidnew')
    #print('address = ' + address)
    #print('podaddress = ' + podaddress)
    #print('CSSa = ' + str(CSSa))
    # initialize an empty list to hold the file tuples
    filetuples= []
    # get the container at the given address
    #print('about to call CSSaccess.get_file')
    #print('address = ' + address)
    data = CSSa.get_file(address)
    #print('data = ' + data)
    # parse the response
    g=Graph().parse(data=data,publicID=address)
    #print('g = ' + str(g))
    # construct a SPARQL query to get all the resources in the returned container
    q='''
    prefix ldp: <http://www.w3.org/ns/ldp#>
    
    SELECT ?f WHERE{
        ?a ldp:contains ?f.
    }
    '''
    # for every result (resource in this container)
    for r in g.query(q):
        # get a string representation of the path
        f=str(r["f"])
        #print('f = ' + f)
        # if this is a directory
        if f[-1]=='/':
            # crawl the directory
            #print('about to recursively call aclcrawlwebidnew')
            #print('f = ' + f)
            #print('podaddress = ' + podaddress)
            #print('CSSa = ' + str(CSSa))
            d=aclcrawlwebidnew(f,podaddress,CSSa)
            #print('d = ' + str(d))
            # add the file tuples from this directory to the list
            filetuples=filetuples+d
        # if this is a file and it's not one of ESPRESSO's utility files
        elif ('.' in f.rsplit('/')[-1]) and (not f.endswith('ttl')) and (not f.endswith('.ndx')) and (not f.endswith('.file')) and (not f.endswith('.sum')) and (not f.endswith('.webid')):
            # get the text of the file
            #print('about to call CSSaccess.get_file')
            #print('f = ' + f)
            text=CSSa.get_file(f)
            # display the text of the file
            #print(text)
            # get the list of WebIDs that have access to this file
            #print('about to call getwebidlistlist')
            #print('f = ' + f)
            #print('CSSa = ' + str(CSSa))
            webidlist=getwebidlistlist(f,CSSa)
            #print('webidlist = ')
            #print(webidlist)
            # get the relative path
            ftrunc=f[len(podaddress):]
            #print('ftrunc = ' + ftrunc)
            # append [relative path, text of the file, WebID list] to the file tuples
            filetuples.append((ftrunc,text,webidlist))
        else: # if it's not a container, and not a file we need to deal with, do nothing
            pass
    
    # return the list of file tuples containing [pod address, text of the file, WebID list]
    #print('filetuples = ')
    #print(filetuples)
    return filetuples

def crawllist(address, CSSa):
    filelist= []
    data = CSSa.get_file(address)
    #print(data)
    g=Graph().parse(data=data,publicID=address)
    #q1='''
    #prefix ldp: <http://www.w3.org/ns/ldp#>
    
    #SELECT ?s ?p ?o WHERE{
    #   ?s ?p ?o .
    #}
    #'''
    #for r in g.query(q1):
    #    print(r)
    q='''
    prefix ldp: <http://www.w3.org/ns/ldp#>
    
    SELECT ?f WHERE{
        ?a ldp:contains ?f.
    }
    '''
    for r in g.query(q):
        #print(r["f"])
        f=str(r["f"])
        if f[-1]=='/':
            d=crawllist(f,CSSa)
            filelist+=d
        else:
            filelist.append(f)
      
    return filelist

"""
Check the indexes.

param: address, the index address
param: CSSa, the CSSaccess object that gets us the client credentials
return: a list of files at the given index address
"""
def indexchecker(address, CSSa):
    # construct an empty list to hold the files
    files= []
    # get the file(s) at the given index address
    data = CSSa.get_file(address)
    # parse the graph
    g=Graph().parse(data=data,publicID=address)
    
    # define a query q that gets every file at this address
    q='''
    prefix ldp: <http://www.w3.org/ns/ldp#>
    
    SELECT ?f WHERE{
        ?a ldp:contains ?f.
    }
    '''
    # for every query result (file)
    for r in g.query(q):
        # get a string representation
        f=str(r["f"])
        # split the string and append each bit to the list of files
        files.append(f.rsplit('/')[-1])

    # return the list of files
    return files


def getwebidlist(address,CSSA):
    acladdress=address+'.acl'
    acldata=CSSA.get_file(acladdress)
    #print(acldata)
    g=Graph().parse(data=acldata,publicID=acladdress)
    ACL=Namespace('http://www.w3.org/ns/auth/acl')
    #for s,p,o in g:
        #print(s,p,o)
    webidlist=[]
    q='''prefix acl: <http://www.w3.org/ns/auth/acl#>

    SELECT ?a ?f WHERE{
        ?a a acl:Authorization.
        ?a acl:mode acl:Read.
        ?a acl:agent ?f.
    }
    '''
    q1='''prefix acl: <http://www.w3.org/ns/auth/acl#>
    SELECT (COUNT(?a) as ?n) WHERE{
        ?a a acl:Authorization.
        ?a acl:mode acl:Read.
        ?a acl:agentClass foaf:Agent.
    } 
    '''
    #for i in g.subjects('acl:mode','acl.Read'):
        #print(i)
        #for webid in g.object(i,ACL.agent):
            #webidlist.append(str(webid))

    for r in g.query(q1):
        if int(r['n'])>0:
            webidlist.append('*')
    for r in g.query(q):
        #print(r["f"])
        f=str(r["f"])
        webidlist.append(f)
    webidstring=','.join(webidlist)
    return webidstring

"""
Add to the WebID list list

param: address, the address of a file
param: CSSA, the CSSaccess object that provides the client credentials
return: a deduplicated list of WebIDs that have access to the file at the given address
"""
def getwebidlistlist(address,CSSA):
    #print('inside getwebidlistlist')
    #print('address = ' + address)
    #print('CSSA = ' + str(CSSa))
    # find the .acl file at the given address
    acladdress=address+'.acl'
    # get the .acl file
    #print('acladdress = ' + acladdress)
    acldata=CSSA.get_file(acladdress)
    #print('acldata = ' + str(acldata))
    # parse the .acl file
    g=Graph().parse(data=acldata,publicID=acladdress)
    #print('g = ' + str(g))
    # the ACL namespace
    ACL=Namespace('http://www.w3.org/ns/auth/acl')
    # create an empty list to hold the WebIDs
    webidlist=[]
    # define a query q to get all the WebIDs of the agents that have Read access
    q='''prefix acl: <http://www.w3.org/ns/auth/acl#>

    SELECT ?a ?f WHERE{
        ?a a acl:Authorization.
        ?a acl:mode acl:Read.
        ?a acl:agent ?f.
    }
    '''

    # define a query q1 to find the ones with open access
    q1='''prefix acl: <http://www.w3.org/ns/auth/acl#>
    SELECT (COUNT(?a) as ?n) WHERE{
        ?a a acl:Authorization.
        ?a acl:mode acl:Read.
        ?a acl:agentClass foaf:Agent.
    } 
    '''

    # for every positive result of query q1 (where open access is granted)
    # append an asterisk to the WebID list.
    # It looks like the asterisk indicates open access.
    for r in g.query(q1):
        if int(r['n'])>0:
            #print(int(r['n']))
            webidlist.append('*')
            #print('webidlist = ')
            #print(webidlist)
    # for every agent that has Read access, 
    for r in g.query(q):
        # get the WebID and add it to the WebID list
        f=str(r["f"])
        #print('f = ' + f)
        webidlist.append(f)
        #print('webidlist = ')
        #print(webidlist)
    # return the deduplicated list of WebIDs that have access to this file
    #print('deduplicated webidlist = ')
    #print(list(set(webidlist)))
    return list(set(webidlist))



class Appearance:
    """
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """
    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency
        
    def __repr__(self):
        """
        String representation of the Appearance object
        """
        return str(self.__dict__)

"""
Cleans a text for NLP processing.

param: text, the text of a file
return: res, the cleansed text as a list of individual words
"""
def myclean(text):
    #print('inside myclean')
    res=cleantext.clean_words(text,
    clean_all= False, # Execute all cleaning operations
    extra_spaces=True ,  # Remove extra white spaces 
    stemming=False , # Stem the words
    stopwords=True ,# Remove stop words
    lowercase=True ,# Convert to lowercase
    numbers=True ,# Remove all digits 
    punct=True ,# Remove all punctuations
    stp_lang='english'  # Language for stop words
    )
    #print('res = ')
    #print(res)
    # return the cleaned text
    return res

class LdpIndex:
    """
    Inverted Index class.
    
    index: a Dictionary.
    f: the sequential number for each file
    """
    def __init__(self):
        self.index = dict()
        self.f=0
        
    def __repr__(self):
        """
        String representation of the index
        """
        return self.index
        
    
    def index_id_text(self, id, text):
        """
        Process a given document, save it to the DB and update the index.
        """
        
        terms=myclean(text)
        #print(terms)
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if len(term)<50:
                termword=term+'.ndx'
                term_frequency = appearances_dict[termword] if termword in appearances_dict else 0
                appearances_dict[termword] =  term_frequency + 1
            
        fileword='f'+str(self.f)
        self.f=self.f+1
        filename=fileword+'.file'
        self.index[filename]=id
        self.index['index.sum']=str(self.f)
        #print(fileword,id)
        for (key, freq) in appearances_dict.items():
            if key not in self.index.keys():
                self.index[key]=''           
            self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'                      

        return id

    def index_id_text_acl(self, id, text, webidliststring):
        """
        Process a given document, save it to the DB and update the index.
         """
        
        terms=myclean(text)
            #print(terms)
        appearances_dict = dict()
            # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if len(term)<50:
                termword=term+'.ndx'
                term_frequency = appearances_dict[termword] if termword in appearances_dict else 0
                appearances_dict[termword] =  term_frequency + 1
            
        fileword='f'+str(self.f)
        self.f=self.f+1
        filename=fileword+'.file'
        self.index[filename]=id+','+ webidliststring
        self.index['index.sum']=str(self.f)
        #print(fileword,id)
        for (key, freq) in appearances_dict.items():
            if key not in self.index.keys():
                self.index[key]=''           
            self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'                      

        return id
    
    def indexwebid(self, id, text, webidlist):
        terms=myclean(text)
            #print(terms)
        appearances_dict = dict()
            # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if len(term)<50:
                termword=term+'.ndx'
                term_frequency = appearances_dict[termword] if termword in appearances_dict else 0
                appearances_dict[termword] =  term_frequency + 1
            
        fileword='f'+str(self.f)
        self.f=self.f+1
        filename=fileword+'.file'
        self.index[filename]=id
        for webid in webidlist:
            if webid=="*":
                webidword='openaccess.webid'
            else:
                webidword=webid.translate(str.maketrans('', '', string.punctuation))+'.webid'
            if webidword not in self.index.keys():
                self.index[webidword]=''
            self.index[webidword]=self.index[webidword]+fileword+'\r\n'
        self.index['index.sum']=str(self.f)
        #print(fileword,id)
        for (key, freq) in appearances_dict.items():
            if key not in self.index.keys():
                self.index[key]=''           
            self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'                      

        return id

    def indexwebidnew(self, id, text, webidlist):
        terms=myclean(text)
            #print(terms)
        appearances_dict = dict()
            # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            if len(term)<50:
                termword=term+'.ndx'
                term_frequency = appearances_dict[termword] if termword in appearances_dict else 0
                appearances_dict[termword] =  term_frequency + 1
        
        # create a short file ID consisting of the letter f plus a sequential number
        fileword='f'+str(self.f)
        # increment the sequential number
        self.f=self.f+1
        
        # go through the WebID list
        for webid in webidlist:
            if webid=="*":
                webidword='openaccess.webid'
            else:
                webidword=webid.translate(str.maketrans('', '', string.punctuation))+'.webid'
            if webidword not in self.index.keys():
                self.index[webidword]=''
            self.index[webidword]=self.index[webidword]+fileword+','+id+'\r\n'
        self.index['index.sum']=str(self.f)
        #print(fileword,id)
        for (key, freq) in appearances_dict.items():
            if key not in self.index.keys():
                self.index[key]=''           
            self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'                      

        return id

    """
    Updates the inverted index with the index file path structure, file ID, text of file, and the list
    of WebIDs that have access to the file.
    This function indexes one file at a time.
    
    param: self
    param: id, the filename
    param: text, text of the file
    param: webidlist, list of WebIDs that have access to the file
    return: id, unchanged from the id that was passed in
    """
    def indexwebidnewdirs(self, id, text, webidlist):
        print('inside indexwebidnewdirs')
        # if the file is empty, return the filename
        if len(text)==0:
            #print('returning id = ' + ids)
            return id
        # cleans the text for NLP processing
        #print('about to call myclean')
        terms=myclean(text)
        # Dictionary with each term and the frequency it appears in the text.
        appearances_dict = dict()
        # if a word is less than 50 characters long [TODO why this restriction?]
        # c/r/e/a/t/e.ndx so we can create a f/i/l/e.ndx in a trie-like structure
        # and keep a running total of the number of times it appears in this file
        for term in terms:
            if len(term)<50:
                termword='/'.join(term)+'.ndx'
                term_frequency = appearances_dict[termword] if termword in appearances_dict else 0
                appearances_dict[termword] =  term_frequency + 1
        # HO 21/08/2024 BOOKMARK
        # say that we have a pod-level running total,
        # well then we want a pod-level running total.
        # say we also  
        # prepend 'f' and just a sequential number
        fileword='f'+str(self.f)
        # increment the sequential number
        self.f=self.f+1
        #print('fileword = ' + fileword)
        # the asterisk means open access
        for webid in webidlist:
            if webid=="*":
                webidword='openaccess.webid'
            else: # remove the punctuation from the WebID so it doesn't gum up the works
                webidword=webid.translate(str.maketrans('', '', string.punctuation))+'.webid'
            # if this WebID isn't already an index key, add it
            if webidword not in self.index.keys():
                self.index[webidword]=''
            # concatenate the sequentially numbered file ID plus the file ID that got
            # passed in [TODO is this adding a local sequentially numbered ID to another that was passed in?]
            # plus a newline, and assign it to this WebID
            self.index[webidword]=self.index[webidword]+fileword+','+id+'\r\n'
            #print('next index item = ')
            #print(self.index[webidword])
        
        # updating the index dictionary entry 'index.sum'
        # with a running total of the number of files
        self.index['index.sum']=str(self.f)
        # now go through the word counts
        for (key, freq) in appearances_dict.items():
            # if this word isn't already being counted, add it
            if key not in self.index.keys():
                self.index[key]=''
            # append the sequentially numbered file ID, a comma, the appearance count, and a newline           
            self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'                     

        # return the filename
        #print('id = ' + id)
        return id

# HO 28/08/2024 BEGIN **************        
    """
    Updates the inverted index with the index file path structure, file ID, text of file, and the list
    of WebIDs that have access to the file.
    This function indexes one file at a time.
    
    param: self
    param: id, the filename
    param: text, text of the file
    param: webidlist, list of WebIDs that have access to the file
    param: podaddress, the address of the pod we are indexing
    param: serverlevel_keyworddict, the server-level dictionary we are building up
    param: serverlevel_webidworddict, the dictionary of webidword handles
    param: serverlevel_poddict, the dictionary of pod handles
    return: serverlevel_keyworddict, the built-up server-level dictionary
    """
    def serverlevel_indexwebidnewdirs(self, id, text, webidlist, podaddress, serverlevel_keyworddict, serverlevel_webidworddict, serverlevel_poddict):
        print('inside serverlevel_indexwebidnewdirs')
        # if the file is empty, return the filename
        if len(text)==0:
            return id
            
        # create a short-form sequentially-numbered file handle
        # that will save space in the index instead of writing the
        # relative path every time
        fileword='f'+str(self.f)
        # increment the pod-level sequential file number
        self.f=self.f+1
        
        # the list of webidwords that can access the current file
        filelevel_webidwordlist=[]
        
        # TODO we've already translated these before adding them
        # to the server-level serverlevel_webidworddict, find a way to remove the redundancy
        # HO 02/09/2024 BOOKMARK 
        for webid in webidlist:
            # signify open access with an asterisk
            if webid=="*":
                webidword='openaccess.webid'
            else: # form the webidword by removing the punctuation from the WebID so it can become a filename
                webidword=webid.translate(str.maketrans('', '', string.punctuation))+'.webid'
            # if this webidword isn't already a key in the pod-level index, add it
            if webidword not in self.index.keys():
                self.index[webidword]=''
            # in the pod-level index,
            # the key is the .webid filename,
            #    the value is the short file handle, 
            #        followed by the relative path to the file,
            # which is to say: the key is the filename,
            #    the value is a line to be written to the file,
            # and so what this outputs is a .webid file 
            #    that contains a series of rows
            #    and each row is a file handle, a comma,
            #    then the relative path to the file it's mapped to,
            #    and then a CRLF
            # and the end result is that the .webid file 
            #    lists all the files this .webid has access to on this pod
            self.index[webidword]=self.index[webidword]+fileword+','+id+'\r\n'
            # save the list of webidwords having access to this file
            filelevel_webidwordlist.append(webidword)
            
        # cleans the text for NLP processing
        terms=myclean(text)
        # Dictionary with each term and the frequency it appears in the text.
        filelevel_appearances_dict = dict()
        # if a word is less than 50 characters long [TODO why this restriction?]
        # c/r/e/a/t/e.ndx so we can create a f/i/l/e.ndx in a trie-like structure
        # and keep a running total of the number of times it appears in this file
        for term in terms:
            if len(term)<50:
                termword='/'.join(term)+'.ndx'
                term_frequency = filelevel_appearances_dict[termword] if termword in filelevel_appearances_dict else 0
                filelevel_appearances_dict[termword] =  term_frequency + 1
                # At the same time as we are building the file-level keyword dictionary,
                # we are building the server-level keyword dictionary,
                # which has the following structure
                # {keyword : {webidword : {widword : {podaddress : {podword : keywordcount}}}}}
                webidworddict = serverlevel_keyworddict[termword] if termword in serverlevel_keyworddict else dict()
                # now add to the {keyword : {webidword : dictionary for every webidword
                # that has access to this file
                for f_webidword in filelevel_webidwordlist:
                    # {keyword : {webidword : {widword : 
                    widdict = webidworddict[f_webidword] if f_webidword in webidworddict else dict()
                    # get the short-form wid mapped to this webidword
                    wid = serverlevel_webidworddict[f_webidword]
                    # {keyword : {webidword : {widword : {podaddress : 
                    podaddressdict = widdict[wid] if wid in widdict else dict()
                    # {keyword : {webidword : {widword : {podaddress : {podword :
                    piddict = podaddressdict[podaddress] if podaddress in podaddressdict else dict()
                    # get the short-form pid mapped to this pod address
                    pid = serverlevel_poddict[podaddress]
                    # {keyword : {webidword : {widword : {podaddress : {podword : keywordcount
                    podlevel_term_frequency = piddict[pid] if pid in piddict else 0
                    # add another appearance to the pod-level count
                    # {podword : keywordcount}
                    piddict[pid] = podlevel_term_frequency + 1
                    # {podaddress : {podword : keywordcount}}
                    podaddressdict[podaddress] = piddict
                    # {widword : {podaddress : {podword : keywordcount}}}
                    widdict[wid] = podaddressdict
                    # {webidword : {widword : {podaddress : {podword : keywordcount}}}}
                    webidworddict[f_webidword] = widdict
                    #serverlevel_keyworddict[termword] = webdict
                # {keyword : {webidword : {widword : {podaddress : {podword : keywordcount}}}}}
                serverlevel_keyworddict[termword] = webidworddict
                #print('serverlevel_keyworddict[' + termword + '] = ')
                #print(serverlevel_keyworddict[termword])
        
        # updating the index dictionary entry 'index.sum'
        # with a running total of the number of files
        self.index['index.sum']=str(self.f)
        # now go through the word counts
        for (key, freq) in filelevel_appearances_dict.items():
            # if this word isn't already being counted, add it
            if key not in self.index.keys():
                self.index[key]=''
            # append the sequentially numbered file ID, a comma, the appearance count, and a newline           
            self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'                     

        # return the filename
        #print('id = ' + id)
        #return id
        return serverlevel_keyworddict
# HO 28/08/2024 END **************
        
def ldpindexdict(filedict):
    ldpindex=LdpIndex()
    for (id,text) in filedict.items():
        print('indexing '+id)
        ldpindex.index_id_text(id, text)
    return ldpindex.index

def aclindextuples(filetuples):
    ldpindex=LdpIndex()
    for (id,text,webidlist) in filetuples:
        print('indexing '+id)
        ldpindex.index_id_text_acl(id, text, webidlist)
    return ldpindex.index



def aclindextupleswebid(filetuples):
    ldpindex=LdpIndex()
    for (id,text,webidlist) in filetuples:
        print('indexing '+id)
        ldpindex.indexwebid(id, text, webidlist)
    return ldpindex.index

def aclindextupleswebidnew(filetuples):
    ldpindex=LdpIndex()
    pbar=tqdm.tqdm(len(filetuples))
    for (id,text,webidlist) in filetuples:
        #print('indexing '+id)
        ldpindex.indexwebidnew(id, text, webidlist)
        pbar.update(1)
    pbar.close()
    return ldpindex.index

"""
Takes a list of file tuples, constructs an LdpIndex from them, and returns the index

param: filetuples, a list of file tuples containing [relative path, text of file, WebIDs]
return: ldpindex.index, the index created over the file tuples
"""
def aclindextupleswebidnewdirs(filetuples):
    print('inside aclindextupleswebidnewdirs')
    #print('filetuples: ')
    #print(filetuples)
    #print('about to construct ldpindex')
    # construct an inverted index
    ldpindex=LdpIndex()
    # set up the progress bar
    pbar=tqdm.tqdm(total=len(filetuples))
    # for each file
    for (id,text,webidlist) in filetuples:
        # create the inverted index with .ndx files and word counts and
        # the 'index.sum'
        # the index is a member of the ldpindex object
        # the key is the t/r/i/e.ndx like string made o/u/t.ndx of the i/n/d/e/x/e/d.ndx k/e/y/w/o/r/d.ndx
        # the value is the sequentially (internal to the ldpindex) numbered file, 
        # a comma, the frequency of the word within that file, and a newline
        # HO 18/08/2024 BEGIN **************
        # I think the inclusion of this line must have been a typo
        #self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'
        # HO 18/08/2024 END **************
        # Update the inverted index with the index file path structure, file ID, text of file, and the list
        # of WebIDs that have access to the file.
        #print('id = ' + id)
        #print('text = ' + text)
        #print('webidlist = ')
        #print(webidlist)
        #print('about to call indexwebidnewdirs')
        ldpindex.indexwebidnewdirs(id, text, webidlist)
        # advance the progress bar
        pbar.update(1)
    # close the progress bar
    pbar.close()
    # return the index created over the file tuples
    #print('ldpindex.index = ')
    #print(ldpindex.index)
    return ldpindex.index
    
"""
For indexing at server level
Takes a list of file tuples and a dictionary of podwords, 
constructs an LdpIndex and a dictionary from them,
and returns them together as a tuple

param: filetuples, a list of file tuples containing [relative path, text of file, WebIDs]
param: podaddress, the address of the pod we're currently indexing
param: serverlevel_keyworddict, a nested dictionary 
param: serverlevel_webidworddict, a dictionary of webidwords with mapped to their short-form handles sequentially numbered for a given server
param: serverlevel_poddict, a dictionary of pod addresses mapped to their short-form handles on a given server
return: servtuples, containing the ldpindex.index, and the serverlevel_keyworddict dictionary that is building up
    to create the server-level index (this is not the final data structure there will have to be more)
"""
def serverlevel_aclindextupleswebidnewdirs(filetuples, podaddress, serverlevel_keyworddict, serverlevel_webidworddict, serverlevel_poddict):
    print('inside serverlevel_aclindextupleswebidnewdirs')
    #print('filetuples: ')
    #print(filetuples)
    # construct the server tuples
    servtuples = []
    #print('about to construct ldpindex')
    # construct an inverted index
    ldpindex=LdpIndex()
    # test index for building up the server-level index
    testservindex=LdpIndex()
    # set up the progress bar
    pbar=tqdm.tqdm(total=len(filetuples))
    # for each file
    for (id,text,webidlist) in filetuples:
        # create the inverted index with .ndx files and word counts and
        # the 'index.sum'
        # the index is a member of the ldpindex object
        # the key is the t/r/i/e.ndx like string made o/u/t.ndx of the i/n/d/e/x/e/d.ndx k/e/y/w/o/r/d.ndx
        # the value is the sequentially (internal to the ldpindex) numbered file, 
        # a comma, the frequency of the word within that file, and a newline
        # HO 18/08/2024 BEGIN **************
        # I think the inclusion of this line must have been a typo
        #self.index[key]=self.index[key]+fileword+','+str(freq)+'\r\n'
        # HO 18/08/2024 END **************
        # Update the inverted index with the index file path structure, file ID, text of file, and the list
        # of WebIDs that have access to the file.
        #print('id = ' + id)
        #print('text = ' + text)
        #print('webidlist = ')
        #print(webidlist)
        #print('podaddress = ' + podaddress)
        #print('serverlevel_keyworddict')
        #print(serverlevel_keyworddict)
        #print('serverlevel_webidworddict')
        #print(serverlevel_webidworddict)
        #print('serverlevel_poddict')
        #print(serverlevel_poddict)
        #print('about to call indexwebidnewdirs')
        servindexdict = ldpindex.serverlevel_indexwebidnewdirs(id, text, webidlist, podaddress, serverlevel_keyworddict, serverlevel_webidworddict, serverlevel_poddict)
        # advance the progress bar
        pbar.update(1)
    # close the progress bar
    pbar.close()
    # return the index created over the file tuples
    #print('ldpindex.index = ')
    #print(ldpindex.index)
    # return a list with the index and the on-running server-level index
    servtuples.append(ldpindex.index)
    servtuples.append(servindexdict)
    #return ldpindex.index
    return servtuples
    
"""
Uploads the index, with ACL info, while displaying a progress bar.

We can do this if the experiment is not too big.

param: ldpindex, the LdpIndex for this file
param: indexdir, the index directory
param: CSSA, the CSSaccess object that provides the client credentials
"""
def uploadaclindexwithbar(ldpindex,indexdir,CSSA):
    # set up the progress bar
    n=len(ldpindex.keys())
    i=1
    pbar = tqdm.tqdm(total=n,desc=indexdir)
    
    # for each filename and file text in the index dictionary
    for (name,body) in ldpindex.items():
        # increment the count
        i=i+1
        # construct a target URL from the current filename
        targetUrl=indexdir+name
        # PUT the file text into that file
        res=CSSA.put_url(targetUrl,body,'text/csv')
        # if that didn't work
        if (not res.ok):
            # construct client credentials and try again
            CSSA.create_authtoken()
            res=CSSA.put_url(targetUrl,body,'text/csv')
            # then give up
            if (not res.ok):
                print('Cannot upload index')
                break
        # advance the progress bar
        pbar.update(1)
    # close the progress bar
    pbar.close()
    # display progress message
    print('index for',indexdir,'is uploaded',n,'files')

def uploadaclindex(ldpindex,indexdir,CSSA):
    n=len(ldpindex.keys())
    i=1
    for (name,body) in ldpindex.items():
        #print('putting '+str(i)+'/'+str(n),end=' ')
        i=i+1
        targetUrl=indexdir+name
        print(targetUrl,end=' ')
        #print('targetUrl = ' + targetUrl)
        #print('body = ' + body)
        res=CSSA.put_url(targetUrl,body,'text/csv')
        #print(res,end='\r')
        if (not res.ok):
            CSSA.create_authtoken()
            res=CSSA.put_url(targetUrl,body,'text/csv')
            if (not res.ok):
                print('Cannot upload index')
                break
    print('index for',indexdir,'is uploaded',n,'files')

def getacl(podpath, targetUrl, CSSA):
    line=targetUrl[len(podpath):]
    res=CSSA.get_file(podpath+line+'.acl')  
    while not res.ok:
        line= '/'.join(line.rsplit('/')[:-1])
        res=CSSA.get_file(podpath+line+'.acl') 
        if len(line)==0:
            break
    return res.text    




