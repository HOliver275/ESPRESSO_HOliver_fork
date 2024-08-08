# an ESPRESSO experiment script
import flexexperiment
# https://github.com/RDFLib/rdflib
from rdflib import URIRef

def deployexperiment(experiment):
"""
Step 2.

(1) ESPRESSO PODS CHECKED IF CREATED 

(2) PODS CREATED 

(2) aclmetaindex() CREATE METAINDEXES 

(3) indexpub() INDEXES OPENED 

(4) metaindexpub() METAINDEXES OPENED 

param: experiment, a flexexperiment.ESPRESSOexperiment
"""
    
    # calls: flexexperiment.ESPRESSOexperiment.ESPRESSOcreate()
    experiment.ESPRESSOcreate()
    print('ESPRESSO checked')
    
    # calls: flexexperiment.ESPRESSOexperiment.podcreate()
    experiment.podcreate()
    print('Pods created')
    
    # calls: flexexperiment.ESPRESSOexperiment.inserttriples()
    experiment.inserttriples()
    print('Triples inserted')
    
    # calls: flexexperiment.ESPRESSOexperiment.aclmetaindex()
    experiment.aclmetaindex()
    print('metaindexes created')
    
    # calls: flexexperiment.ESPRESSOexperiment.indexpub()
    experiment.indexpub()
    print('indexes opened')
    
    # calls: flexexperiment.ESPRESSOexperiment.metaindexpub()
    experiment.metaindexpub()
    print('metaindexes opened')

def uploadexperiment(experiment):
"""
Step 3. 

Upload Files to the pods from the image 

Upload ACLs to the pods from the image

param: experiment, a flexexperiment.ESPRESSOexperiment  
"""

    # calls: flexexperiment.ESPRESSOexperiment.uploadfiles()
    experiment.uploadfiles()
    print('Pods populated')
    
    # calls: flexexperiment.ESPRESSOexperiment.uploadacls()
    experiment.uploadacls()
    print('Acls populated')
    
def indexexperiment(experiment):
"""
Step 4.

Indexes the experiment.

param: experiment, a flexexperiment.ESPRESSOexperiment 
"""
    
    # calls: flexexperiment.ESPRESSOexperiment.aclindexwebidnewthreaded()
    experiment.aclindexwebidnewthreaded()
    print('pods indexed')
    
    # calls: flexexperiment.ESPRESSOexperiment.indexfixerwebidnew()
    experiment.indexfixerwebidnew()
    print('indices checked')

# Serverlists
serverlist1=[]
serverlist2=[]
# source directories for data
sourcedir1=''
sourcedir2=''
sourcedir3=''

# Name of the ESPRESSO pod. ESPRESSO is default.
espressopodname='ESPRESSO'
# Email to register the ESPRESSO pod. espresso@example.com is default.
espressoemail='espresso@example.com'
# Name for the pods in the experiment the pods will be called podname0, podmane1, etc.
#podname
    
# Email to register the pod. the emails will be podname0@example.org,
# podname1@example.org, etc.
podemail='@example.org'
# Folder where the pod indexes will go
podindexdir='espressoindex/'
# Same password for all the logins
password='12345'
# percs of sp.agents
percs=[100,50,25,10]
# percent of openfiles
openperc=10
# number of agents
numofwebids=50
# on average how many webids can read a given file
mean=10
# relative deviation of the percentage of webids that can read a given file, can be left 0
disp=0
    #how many files on average a webid can read
    #initializing the experiment


def createexperiment(podname):
""" Step 0. 

Creates an image (graph) that represents the relationship among everything (Servers, pods, files in those pods, and access control specs on those files). 

In this function we decide on everything, number of servers, number of files,  distribution of pods across servers, distribution of files across pods, number of WebIDs, and distribution of access given to those WebIDs.

param: podname (the current pod name: 'podname' + sequential number) 
return: experiment, an object of type flexexperiment.ESPRESSOexperiment
"""

    # Initializing the experiment
    # calls: flexexperiment.ESPRESSOexperiment
    # passes in: espressopodname default: 'ESPRESSO'
    # passes in: espressoemail default: 'espresso@example.com'
    # passes in: podname ('podname' + current sequential number)
    # passes in: podemail (podname + '@example.org')
    # passes in: podindexdir ('espressoindex/')
    # passes in: password (hardcoded '12345')
    # gets back: experiment, a flexexperiment.ESPRESSOexperiment
    experiment=flexexperiment.ESPRESSOexperiment(espressopodname=espressopodname, espressoemail=espressoemail, podname=podname,podemail=podemail, podindexdir=podindexdir, password=password)

    # Server list loading
    # calls: flexexperiment.ESPRESSOexperiment.loadserverlist
    # passes in: serverlist1 
    # passes in: 'Serverlabel1' [what?]
    experiment.loadserverlist(serverlist1,'Serverlabel1')
    # calls: flexexperiment.ESPRESSOexperiment.loadserverlist
    # passes in: serverlist2 
    # passes in: 'Serverlabel2' [what?]
    experiment.loadserverlist(serverlist2,'Serverlabel2')
    # user feedback
    print('serverlist loaded')

    # Creating connected pod pairs if needed
    # calls: flexexperiment.ESPRESSOexperiment.createlogicalpairedpods
    # passes in: numberofpods=10 
    # passes in: serverdisp=0 [what?]
    # passes in: serverlabel1='server1' [why?] [pairs pods in two different servers]
    # passes in: serverlabel2='server2' [why?] [pairs pods in two different servers]
    # passes in: podlabel1='pod1'
    # passes in: podlabel2='pod2'
    # passes in: conpred=URIRef('http://espresso.org/haspersonalWebID') - creates an IRI 
    #                or URI 
    # https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.term.URIRef
    #                with base http://espresso.org/haspersonalWebID
    experiment.createlogicalpairedpods(numberofpods=10,serverdisp=0,serverlabel1='server1',serverlabel2='server2',podlabel1='pod1',podlabel2='pod2',conpred=URIRef('http://espresso.org/haspersonalWebID'))

    # loading files into the file pool
    # calls: flexexperiment.ESPRESSOexperiment.loaddirtopool
    # passes in: sourcedir1 (source directory for data)
    # passes in: 'Filelabel1' [what?]
    experiment.loaddirtopool(sourcedir1,'Filelabel1')
    # calls: flexexperiment.ESPRESSOexperiment.loaddirtopool
    # passes in: sourcedir2 (source directory for data)
    # passes in: 'Filelabel2' [what?]
    experiment.loaddirtopool(sourcedir2,'Filelabel2')
    # distributing the files from the file pools into the pods
    # calls: flexexperiment.ESPRESSOexperiment.logicaldistfilestopodsfrompool
    # passes in: numberoffiles=100
    # passes in: filedisp=0 [what?]
    # passes in: filetype=0 [what?]
    # passes in: filelabel='Filelabel1' which is the same as loaddirtopool with sourcedir1
    # passes in: podlabel='pod1' which is the same as the first of two logical paired pods
    # passes in: subdir='file' [what?]
    # passes in: predicatetopod=URIRef, a URI/IRI with base 
    #                http://example.org/SOLIDindex/HasFile
    # passes in: replacebool=False [what?]
    experiment.logicaldistfilestopodsfrompool(numberoffiles=100,filedisp=0,filetype=0,filelabel='Filelabel1',podlabel='pod1',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    
    # calls: flexexperiment.ESPRESSOexperiment.logicaldistfilestopodsfrompool
    # passes in: numberoffiles=100
    # passes in: filedisp=0 [what?]
    # passes in: filetype=0 [what?]
    # passes in: filelabel='Filelabel2' which is the same as loaddirtopool with sourcedir2
    # passes in: podlabel='pod2' which is the same as the second of two logical paired pods
    # passes in: subdir='file' [what?]
    # passes in: predicatetopod=URIRef, a URI/IRI with base 
    #                http://example.org/SOLIDindex/HasFile
    # passes in: replacebool=False [what?]
    experiment.logicaldistfilestopodsfrompool(numberoffiles=100,filedisp=0,filetype=0,filelabel='Filelabel2',podlabel='pod2',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    
    # distributing the file bundles if needed
    # calls: flexexperiment.ESPRESSOexperiment.distributebundles
    # passes in: numberofbundles=10 [what?]
    # passes in: bundlesource=sourcedir3 (source directory for data)
    # passes in: filetype='text/turtle'
    # passes in: filelabel='FileLabel3' [so a third one?]
    # passes in: subdir='file' [same as before]
    # passes in: podlabel='pod' [really, why?]
    # passes in: predicatetopod=URIRef, a URI/IRI with base 
    #                http://example.org/SOLIDindex/HasFile
    # passes in: hashliststring='' [what?]
    experiment.distributebundles(numberofbundles=10,bundlesource=sourcedir3,filetype='text/turtle',filelabel='Filelabel3',subdir='file',podlabel='pod',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),hashliststring='')
    
    # user feedback
    print('files loaded')
    
    # acl creation
    # calls: flexexperiment.ESPRESSOexperiment.imagineaclnormal
    # passes in: openperc=100 [what?]
    # passes in: numofwebids=20 [what?]
    # passes in: mean=10 [what?]
    # passes in: disp=0 [what?]
    # passes in: 'Filelabel1' [same as loaddirtopool with sourcedir1]
    experiment.imagineaclnormal(openperc=100,numofwebids=20,mean=10, disp=0,filelabel='Filelabel1')
    # calls: flexexperiment.ESPRESSOexperiment.imagineaclnormal
    # passes in: openperc=50 [what?]
    # passes in: numofwebids=20 [what?]
    # passes in: mean=10 [what?]
    # passes in: disp=0 [what?]
    # passes in: 'Filelabel2' [same as loaddirtopool with sourcedir2]
    experiment.imagineaclnormal(openperc=50,numofwebids=20,mean=10, disp=0,filelabel='Filelabel2')
    # calls: flexexperiment.ESPRESSOexperiment.imagineaclnormal
    # passes in: openperc=10 [what?]
    # passes in: numofwebids=20 [what?]
    # passes in: mean=10 [what?]
    # passes in: disp=0 [what?]
    # passes in: 'Filelabel3' [same as distributebundles with sourcedir3]
    experiment.imagineaclnormal(openperc=10,numofwebids=20,mean=10, disp=0,filelabel='Filelabel3')
    # calls: flexexperiment.ESPRESSOexperiment.imagineaclspecial
    # passes in: percs [what?]
    # passes in: 'Filelabel1' [same as loaddirtopool with sourcedir1]
    experiment.imagineaclspecial(percs,'Filelabel1')
    # calls: flexexperiment.ESPRESSOexperiment.imagineaclspecial
    # passes in: percs [what?]
    # passes in: 'Filelabel2' [same as loaddirtopool with sourcedir2]
    experiment.imagineaclspecial(percs,'Filelabel2')
    # calls: flexexperiment.ESPRESSOexperiment.imagineaclspecial
    # passes in: percs [what?]
    # passes in: 'Filelabel3' [same as distributebundles with sourcedir3]
    experiment.imagineaclspecial(percs,'Filelabel3')
    
    # user feedback
    print('files acl imagined')
    
    # saves the experiment as a .ttl file named after the podname plus 'exp'
    # calls: flexexperiment.ESPRESSOexperiment.saveexp
    # passes in: podname plus 'exp.ttl'
    experiment.saveexp(podname+'exp.ttl')

    # user feedback
    print('experiment saved')
    
    # return the flexexperiment.ESPRESSOexperiment object
    return experiment

# Pod name template and experiment name
podname='ardfhealth'

#name for the metaindex file.
espressoindexfile=podname+'metaindex.csv'

#creating the logical view and saving it
experiment=createexperiment(podname)

# Loading the experiment
experiment=flexexperiment.loadexp(podname+'exp.ttl')
print('Experiment loaded')

# Creating the experiment infrastructure - pods, metaindices, triples
deployexperiment(experiment)

#Uploading of the files and corresponding acls
uploadexperiment(experiment)

#Indexing of the experiment
indexexperiment(experiment)