# an ESPRESSO experiment script
import flexexperiment
# https://github.com/RDFLib/rdflib
from rdflib import URIRef
from math import floor

"""
Step 2. Actual deployment of the experiment.

This is the actual work of creating everything:
    - creating ESPRESSO pods if not created 
    - creating the pods on the servers  
    - creating the metaindexes  
    - opening the indexes  
    - opening the metaindexes  
    
(1) ESPRESSO PODS CHECKED IF CREATED 
(2) PODS CREATED 
(2) aclmetaindex() CREATE METAINDEXES 
(3) indexpub() INDEXES OPENED 
(4) metaindexpub() METAINDEXES OPENED 
    
param: experiment, a flexexperiment.ESPRESSOexperiment
"""
def deployexperiment(experiment):
    # Create the ESPRESSO pods, if they haven't already been created.
    experiment.ESPRESSOcreate()
    # display progress message
    print('ESPRESSO checked')
    
    # Create the normal pods, unless they're already there in which case, wipe the contents
    experiment.podcreate()
    print('Pods created')
    
    # Insert the triples into the pods.
    experiment.inserttriples()
    # display progress message
    print('Triples inserted')
    
    # Create the server-level metaindexes.
    experiment.aclmetaindex()
    # display progress message
    print('metaindexes created')
    
    # Make all the pod indexes open access.
    experiment.indexpub()
    # display progress message
    print('indexes opened')
    
    # Make the metaindexes open access.
    # HO 06/09/2024 - MR documented this as opening access, but they're only accessible to the experiment
    experiment.metaindexpub()
    # display progress message
    print('metaindexes made accessible to the experiment')

"""
Step 3. 

Upload Files to the pods from the image 
Upload ACLs to the pods from the image
param: experiment, a flexexperiment.ESPRESSOexperiment  
"""
def uploadexperiment(experiment):
    # upload the files to populate the pods
    experiment.uploadfiles()
    # display progress message
    print('Pods populated')
    
    # upload the ACL files
    experiment.uploadacls()
    # display progress message
    print('Acls populated')
    
"""
Step 4. We can do this if the experiment is not too big, otherwise we have to call zip(experiment,zipdir,SSHuser,SSHPassword) 

Indexes the experiment.
param: experiment, a flexexperiment.ESPRESSOexperiment 
"""
def indexexperiment(experiment):
    
    ########################
    # Option A step 1, for smaller experiments: index the pods on the fly 
    experiment.aclindexwebidnewthreaded()
    print('pods indexed')
    
    # Option A step 2, for smaller experiments: check the indexes 
    # note: we're not doing this for the metaindex even for small experiments
    experiment.indexfixerwebidnew()
    print('indexes checked')
    ########################
    
    ########################
    # Option B: if the experiment is too big, do the zipping and unzipping method: 
    # This will store the indexes in zips locally  
    # And distribute them to the corresponding servers using ssh.
    
    # Option B, step 1, zip the indexes and store locally 
    #experiment.storelocalindexzipdirs('zipdir')
    """experiment.serverlevel_storelocalindexzipdirs('zipdir')
    
    # Option B, step 2: distribute zips(using SSH username and password) 
    experiment.distributezips('zipdir',SSHUser,SSHPassword,targetdir='/srv/espresso/')"""
    ########################
# Server labels
servlab1 = 'Serverlabel1'
servlab2 = 'Serverlabel2'
servlab3 = 'Serverlabel3'
# file labels
filelab1 = 'Filelabel1'
filelab2 = 'Filelabel2'
filelab3 = 'Filelabel3'
# pod labels
podlab1 = 'pod1'
podlab2 = 'pod2'
podlab3 = 'pod3'
# server lists
serverlist1=['http://localhost:3000/']
serverlist2=['http://localhost:3001/']
serverlist3=['http://localhost:3002/']
# source directories for data
sourcedir1='../DatasetSplitter/sourcedir1/'
sourcedir2='../DatasetSplitter/sourcedir2/'
sourcedir3='../DatasetSplitter/sourcedir3/'
numfiles = 10

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
#numofwebids=50
# TODO this is always hard-coded to 20 at the last minute
# set a differently named variable
numwebids=8
# number of pods
numpods=10
# on average how many webids can read a given file
mean=10
# relative deviation of the percentage of webids that can read a given file, can be left 0
disp=0
    #how many files on average a webid can read
    #initializing the experiment

""" Step 0. 

Creates an image (graph) that represents the relationship among everything (Servers, pods, files in those pods, and access control specs on those files). 

In this function we decide on everything, number of servers, number of files,  distribution of pods across servers, distribution of files across pods, number of WebIDs, and distribution of access given to those WebIDs.

By the end of this function: 
The experiment is logically saved in a .ttl file, but not yet deployed. 
The .ttl file is ready to be deployed in action. 
This ttl image knows everything:
    - what are the Solid servers  
    - what are the pods' information on the Solid servers 
    - files to be distributed on those Pods. 
    - Agents and Special Agents  
    - ACL information to files for the Agents/WebIDs. 

param: podname, example value: 'ardfhealth'
return: experiment, an object of type flexexperiment.ESPRESSOexperiment
"""
def createexperiment(podname):
    # Initializing the experiment

    experiment=flexexperiment.ESPRESSOexperiment(espressopodname=espressopodname, espressoemail=espressoemail, espressoindexdir=espressoindexdir, podname=podname,podemail=podemail, podindexdir=podindexdir, password=password)

    print("Constructed experiment")
    
    # Server list loading
    experiment.loadserverlist(serverlist1, servlab1)

    experiment.loadserverlist(serverlist2, servlab2)

    experiment.loadserverlist(serverlist3, servlab3)

    # user message
    print('serverlist loaded')
    
    # Creating connected pod pairs 
    experiment.createlogicalpairedpods(numberofpods=numpods,serverdisp=0,serverlabel1=servlab1,serverlabel2=servlab2,podlabel1=podlab1,podlabel2=podlab2,conpred=URIRef('http://espresso.org/haspersonalWebID'))
    print('logical paired pods created ')
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab3,podlabel=podlab3)
    print('logical pods created ')

    experiment.loaddirtopool(sourcedir1, filelab1)

    experiment.loaddirtopool(sourcedir2, filelab2)

    experiment.loaddirtopool(sourcedir3, filelab3)
    print('loaded source dirs to pool')
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab1,podlabel=podlab1,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab2,podlabel=podlab2,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab3,podlabel=podlab3,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    
    # the purpose of this appears to be distributing batches of files, it has no discernibly different effect if you run it straight after logicaldistfilestopodsfrompool
    #TODO will probably need to use this when deploying to the VMs
#experiment.distributebundles(numberofbundles=10,bundlesource=sourcedir3,filetype='text/turtle',filelabel=filelab3,subdir='file',podlabel=podlab3,predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),hashliststring='')
    #print('Back from flexexperiment.distributebundles')

    print('files distributed')
    
    # agent nodes
    experiment.initanodelist(numberofwebids=numwebids)
    
    print('agent nodes initialized')
    
    #print('about to call initsanodelist')
    experiment.initsanodelist(percs)
    
    print('special agent nodes initialized')

    experiment.imagineaclnormal(openperc=100,mean=(floor(numwebids/2)), disp=0,filelabel=filelab1)

    experiment.imagineaclnormal(openperc=50,mean=(floor(numwebids/2)), disp=0,filelabel=filelab2)

    experiment.imagineaclnormal(openperc=10,mean=floor(numwebids/2), disp=0,filelabel=filelab3)
    
    print('Normal ACLs distributed')

    experiment.imagineaclspecial(filelab1)

    experiment.imagineaclspecial(filelab2)

    experiment.imagineaclspecial(filelab3)
    
    print('Special agent ACLs distributed')
    
    # saves the experiment as a .ttl file named after the podname plus 'exp'
    experiment.saveexp(podname+'exp.ttl')

    # user progress message
    print('experiment saved') 
    print('===================')
    # return the flexexperiment.ESPRESSOexperiment object
    return experiment

# Pod name template and experiment name
# example podname value: 'ardfhealth'
podname='ardfhealth'

# name for the metaindex file.
# example espressoindexfile value: 'ardfhealthmetaindex.csv'
espressoindexfile=podname+'metaindex.csv'
# name for the metaindex directory.
# example espressoindexdir value: 'ardfhealthmetaindex/'
espressoindexdir=podname+'metaindex/'

# create and save the logical view of the experiment
# example podname value: 'ardfhealth'
experiment=createexperiment(podname)

# Loading the experiment. Step 1.
experiment=flexexperiment.loadexp(podname+'exp.ttl')
# display progress message
print('Experiment loaded')
print('===================')

# Creating the experiment infrastructure - pods, metaindexes, triples
# and making the indexes and metaindexes open access
deployexperiment(experiment)
print('Experiment deployed')
print('===================')


# Uploading of the files and corresponding acls
uploadexperiment(experiment)
print('Experiment uploaded')
print('===================')

#Indexing of the experiment
indexexperiment(experiment)
"""print('Experiment indexed')
print('===================')"""