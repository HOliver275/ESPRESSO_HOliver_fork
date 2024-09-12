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

import sys
sys.path.append('../../')
import config

"""
An index of terms at server level, effectively an aggregation of the server's pod indexes.

author: Helen Oliver for the ESPRESSO Project, 2024
"""
class ServerIndex:

    def __init__(self):
        # the server-level index to be written to the ESPRESSO pod metaindex
        self.index = dict()
        # count the pods on the server
        self.pod_counter=0
        # count the WebIDs that have access to any of the pods on the server
        self.webid_counter=0
        # server-level nested dictionary mapping of index keywords 
        self.keywords_dict = dict()
        # lookup of all the webidword:widword mappings on this server
        self.widword_lookup = dict()
        # lookup of all the podpath:pid mappings on this server
        self.podword_lookup = dict()
        # dictionary from which to create the .webid files to be added to the index
        self.webidwords_dict = dict()
        # running sum of all the files held on the server
        self.indexsum=0
        
    def __repr__(self):
        """
        String representation of the index
        """
        return self.index
        
    """
    Maps a sequentially numbered short pod handle to a pod address and adds it to the running total pods on this server.
    
    param: self
    param: podpath, the relative path to the pod index on the server 
    """
    def addpod(self, podpath):
        if podpath not in self.podword_lookup:
            podword = 'p' + str(self.pod_counter)
            # advance the pod counter
            self.pod_counter = self.pod_counter+1
            # map the podword to this podaddress
            self.podword_lookup[podpath] = podword
            
    """
    Maps a sequentially numbered short WebID handle to a WebID and adds it to the running total WebIDs on this server.
    
    param: self
    param: podpath, the relative path to the pod index on the server 
    param: webidlist, a list of webids to convert
    """
    def addwebids(self, podpath, webidlist):
        for webid in webidlist:
            if webid==config.OPENACCESS_SYMBOL:
                widword=config.OPENACCESS_WEBIDWORD
                webidword=config.OPENACCESS_FILENAME

                if webidword not in self.widword_lookup.keys():
                    # add this webidword:widword mapping to the lookup
                    self.widword_lookup[webidword]=widword
                    # add this widword : {podpath : podword} mapping to the dictionary
                    if webidword not in self.webidwords_dict.keys(): # it shouldn't be
                        piddict = {podpath : self.podword_lookup[podpath]}
                        widdict = {widword : piddict}
                        self.webidwords_dict[webidword] = widdict
            else: # remove the punctuation from the WebID so it doesn't gum up the works
                webidword=webid.translate(str.maketrans('', '', string.punctuation))+config.WEBID_FILEXTN
                            
            # if this webidword isn't already mapped to a widword, map it
            if webidword not in self.widword_lookup.keys():
                widword=config.WIDWORD_PREFIX + str(self.webid_counter)
                # advance the webid counter every time we add a new mapping
                self.webid_counter = self.webid_counter+1
                self.widword_lookup[webidword]=widword
                # add this widword : {podpath : podword} mapping to the dictionary
                if webidword not in self.webidwords_dict.keys(): # it shouldn't be
                    piddict = {podpath : self.podword_lookup[podpath]}
                    widdict = {widword : piddict}
                    self.webidwords_dict[webidword] = widdict
                            
            # if it's not in the dictionary by now something is wrong
            widword = self.widword_lookup[webidword] if webidword in self.widword_lookup else ''
            if (len(widword) > 0):
                widdict = self.webidwords_dict[webidword] if webidword in self.webidwords_dict else dict()
                poddict = widdict[widword] if widword in widdict else dict()
                # if this pod isn't already listed against this widword
                if podpath not in poddict.keys():
                    # add the podword mapping
                    poddict[podpath] = self.podword_lookup[podpath]
                    # update the podname mapping
                    widdict[widword] = poddict
                    # update the widword mapping
                    self.webidwords_dict[webidword] = widdict 

    """
    Takes the server-level dictionary and unwinds it into a server-level metaindex, with all the webids that can access a keyword listed in the one .ndx file

    """
    def buildservermetaindex_allwebidsinonefile(self):
        servidx = dict()
        # webid files first
        for (webidfile, widdict) in self.webidwords_dict.items():
            if webidfile not in servidx.keys():
                servidx[webidfile] = ''
            for(wid, poddict) in widdict.items():
                for(paddr, pid) in poddict.items():
                    if(wid==config.OPENACCESS_SYMBOL):
                        servidx[webidfile]=servidx[webidfile]+config.OPENACCESS_WEBIDWORD+','+pid+','+paddr+'\r\n'
                    else:
                        servidx[webidfile]=servidx[webidfile]+wid+','+pid+','+paddr+'\r\n'
                        
        # now the list of .ndx files
        for (key, wworddict) in self.keywords_dict.items():
            if key not in servidx.keys():
                servidx[key] = ''
        for (wwordkey, widdict) in wworddict.items():
            for(widkey, poddict) in widdict.items():
                if(widkey==config.OPENACCESS_SYMBOL):
                    widtowrite=config.OPENACCESS_WEBIDWORD
                else:
                    widtowrite=widkey
                        
                for(paddrkey, piddict) in poddict.items():
                    for(pidkey, freq) in piddict.items():
                        servidx[key]=servidx[key]+widtowrite+','+pidkey+','+str(freq)+'\r\n'
                            
        # and finally the index.sum
        servidx[config.INDEX_FILECOUNT_FILENAME]=str(self.indexsum)
        self.index=servidx
        print('self.index: ')
        print(self.index)
        
    # HO 11/09/2024 BEGIN **************************
    #def buildservermetaindex_webidlast(servwiddict, servkeydict, servidxsum):
    def buildservermetaindex_webidlast(self):
        servidx = dict()
        # set up the .webid files
        for (webidfile, widdict) in self.webidwords_dict.items():
            if webidfile not in servidx.keys():
                servidx[webidfile] = ''
            for(wid, poddict) in widdict.items():
                for(ppath, pid) in poddict.items():
                    if(wid==config.OPENACCESS_SYMBOL):
                        servidx[webidfile]=servidx[webidfile]+config.OPENACCESS_WEBIDWORD+','+pid+','+ppath+'\r\n'
                    else:
                        servidx[webidfile]=servidx[webidfile]+wid+','+pid+','+ppath+'\r\n'
    
        # set up the .ndx files with the wid inserted before the .ndx file suffix
        for (key, wworddict) in self.keywords_dict.items():
            for (wwordkey, widdict) in wworddict.items():
                for(widkey, poddict) in widdict.items():
                    startkey=key[:-(len(config.KEYWORD_INDEX_FILEXTN))]
                    if(widkey==config.OPENACCESS_SYMBOL):
                        servkey= startkey + '/' + config.OPENACCESS_WEBIDWORD + config.KEYWORD_INDEX_FILEXTN
                    else:
                        servkey= startkey + '/' + widkey + config.KEYWORD_INDEX_FILEXTN
                        
                    if servkey not in servidx.keys():
                        servidx[servkey]=''
                        
                    for(ppathkey, piddict) in poddict.items():
                        for(pidkey, freq) in piddict.items():
                            servidx[servkey]=servidx[servkey]+pidkey+','+str(freq)+'\r\n'
    
        # finally, write the index.sum file
        servidx[config.INDEX_FILECOUNT_FILENAME]=str(self.indexsum)
        # now set the server-level index's writable index to be the one we just created
        self.index = servidx

        