# an ESPRESSO experiment script
import flexexperiment
# https://github.com/RDFLib/rdflib
from rdflib import URIRef
# HO 17/08/2024 BEGIN ***********
from math import floor
# HO 17/08/2024 END *************

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
    #print('about to call flexexperiment.ESPRESSOcreate')
    # Create the ESPRESSO pods, if they haven't already been created.
    experiment.ESPRESSOcreate()
    # display progress message
    #print('ESPRESSO checked')
    #print('-------------------')
    
    # Create the normal pods, unless they're already there in which case, wipe the contents
    #print('about to call flexexperiment.podcreate')
    experiment.podcreate()
    #print('Pods created')
    #print('-------------------')
    
    # Insert the triples into the pods.
    #print('about to call flexexperiment.inserttriples')
    experiment.inserttriples()
    # display progress message
    #print('Triples inserted')
    #print('-------------------')
    
    # Create the server-level metaindexes.
    experiment.aclmetaindex()
    # display progress message
    #print('metaindexes created')
    #print('-------------------')
    
    # Make all the pod indexes open access.
    experiment.indexpub()
    # display progress message
    #print('indexes opened')
    #print('-------------------')
    
    # Make the metaindexes open access.
    experiment.metaindexpub()
    # display progress message
    #print('metaindexes opened')
    #print('-------------------') 

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
    #print('Pods populated')
    #print('-----------------')
    
    # upload the ACL files
    experiment.uploadacls()
    # display progress message
    #print('Acls populated')
    #print('-----------------')
    
"""
Step 4. We can do this if the experiment is not too big, otherwise we have to call zip(experiment,zipdir,SSHuser,SSHPassword) 

Indexes the experiment.
param: experiment, a flexexperiment.ESPRESSOexperiment 
"""
def indexexperiment(experiment):
    #print('inside indexexperiment')
    
    ########################
    # Option A step 1, for smaller experiments: index the pods on the fly 
    experiment.aclindexwebidnewthreaded()
    #print('pods indexed')
    
    # Option A step 2, for smaller experiments: check the indexes 
    """experiment.indexfixerwebidnew()
    #print('indexes checked')
    ########################
    
    ########################
    # Option B: if the experiment is too big, do the zipping and unzipping method: 
    # This will store the indexes in zips locally  
    # And distribute them to the corresponding servers using ssh.
    
    # Option B, step 1, zip the indexes and store locally 
    experiment.storelocalindexzipdirs('zipdir')""" 
    
    # Option B, step 2: distribute zips(using SSH username and password) 
    #experiment.distributezips('zipdir',SSHUser,SSHPassword,targetdir='/srv/espresso/')
    ########################
# Serverlists
# HO 16/08/2024 BEGIN *********
servlab1 = 'Serverlabel1'
servlab2 = 'Serverlabel2'
servlab3 = 'Serverlabel3'
filelab1 = 'Filelabel1'
filelab2 = 'Filelabel2'
filelab3 = 'Filelabel3'

podlab1 = 'pod1'
#podlab1 = 'compod'
podlab2 = 'pod2'
#podlab2 = 'goodpod'
podlab3 = 'pod3'
# serverlist1=[]
serverlist1=['http://localhost:3000/']
#serverlist2=[]
serverlist2=['http://localhost:3001/']
serverlist3=['http://localhost:3002/']
# source directories for data
#sourcedir1=''
#sourcedir2=''
#sourcedir3=''
sourcedir1='../DatasetSplitter/sourcedir1/'
sourcedir2='../DatasetSplitter/sourcedir2/'
sourcedir3='../DatasetSplitter/sourcedir3/'
numfiles = 10
# HO 16/08/2024 END ***********

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
    #print('Entered expeerimenttemplate.createexperiment')
    # Initializing the experiment
    #print('About to initialize the experiment')

    experiment=flexexperiment.ESPRESSOexperiment(espressopodname=espressopodname, espressoemail=espressoemail, podname=podname,podemail=podemail, podindexdir=podindexdir, password=password)

    #print('Constructed ESPRESSOexperiment.')
    #print('--------------------------------')

    # Server list loading

    # HO 16/08/2024 BEGIN *************
    # experiment.loadserverlist(serverlist1,'Serverlabel1')
    experiment.loadserverlist(serverlist1, servlab1)
    # HO 16/08/2024 END *************

    # HO 16/08/2024 BEGIN **************
    #experiment.loadserverlist(serverlist2,'Serverlabel2')
    experiment.loadserverlist(serverlist2, servlab2)
    # HO 16/08/2024 END **************
    
    # HO 20/08/2024 BEGIN **************
    experiment.loadserverlist(serverlist3, servlab3)
    # HO 20/08/2024 END **************

    # user message
    #print('serverlist loaded')
    #print('---------------------------')
    
    # Creating connected pod pairs 
    #print('Creating connected pod pairs')

    
# HO 16/08/2024 BEGIN *********
    #experiment.createlogicalpairedpods(numberofpods=10,serverdisp=0,serverlabel1='server1',serverlabel2='server2',podlabel1='pod1',podlabel2='pod2',conpred=URIRef('http://espresso.org/haspersonalWebID'))
    experiment.createlogicalpairedpods(numberofpods=numpods,serverdisp=0,serverlabel1=servlab1,serverlabel2=servlab2,podlabel1=podlab1,podlabel2=podlab2,conpred=URIRef('http://espresso.org/haspersonalWebID'))
    #print('logical paired pods created ')
    #print('---------------------------')
    # HO 20/08/2024 BEGIN **************
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab3,podlabel=podlab3)
    #print('logical pods created ')
    #print('---------------------------')
    # HO 20/08/2024 END **************
    #experiment.createlogicalpods(9,0,servlab1,podlab1)
    #experiment.createlogicalpods(1,0,servlab1,podlab2)

    #experiment.createlogicalpods(9,0,servlab2,podlab1)
    #experiment.createlogicalpods(1,0,servlab2,podlab2)
    
# HO 16/08/2024 END ********* 
    # loading files into the file pool
    # HO 16/08/2024 BEGIN ********* 
    # experiment.loaddirtopool(sourcedir1,'Filelabel1')
    #print('About to load dirs to pools')
    experiment.loaddirtopool(sourcedir1, filelab1)
    # HO 16/08/2024 END ********* 

    # HO 16/08/2024 BEGIN *********
    #experiment.loaddirtopool(sourcedir2,'Filelabel2')
    experiment.loaddirtopool(sourcedir2, filelab2)
    # HO 16/08/2024 END *********
    #print('---------------------------')
    # HO 20/08/2024 BEGIN **************
    experiment.loaddirtopool(sourcedir3, filelab3)
    #print('---------------------------')
    # HO 20/08/2024 END **************
    
    #print('About to call flexexperiment.logicaldistfilestopodsfrompool')
    # HO 16/08/2024 BEGIN ************
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=100,filedisp=0,filetype=0,filelabel='Filelabel1',podlabel='pod1',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab1,podlabel=podlab1,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    #print('Back from logicaldistfilestopodsfrompool ' + filelab1)
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles-1,filedisp=0,filetype=0,filelabel=filelab1,podlabel=podlab1,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles-9,filedisp=0,filetype=0,filelabel=filelab1,podlabel=podlab2,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    #print('---------------------------')
    # HO 16/08/2024 END ************
    
    #HO 16/08/2024 BEGIN ************
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=100,filedisp=0,filetype=0,filelabel='Filelabel2',podlabel='pod2',subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab2,podlabel=podlab2,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab3,podlabel=podlab3,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles-1,filedisp=0,filetype=0,filelabel=filelab2,podlabel=podlab1,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles-9,filedisp=0,filetype=0,filelabel=filelab2,podlabel=podlab2,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    #experiment.logicaldistfilestopodsfrompool(numberoffiles=10,filedisp=0,filetype=0,filelabel=filelab3,podlabel=podlab3,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
#HO 16/08/2024 END ************
    experiment.distributebundles(numberofbundles=10,bundlesource=sourcedir3,filetype='text/turtle',filelabel=filelab3,subdir='file',podlabel=podlab3,predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),hashliststring='')
    # HO 16/08/2024 END *********
    #print('Back from flexexperiment.distributebundles')
    #print('---------------------------')
    # user progress message
    #print('files loaded')
    
    # acl creation
    # HO 16/08/2024 BEGIN **********
    #print('about to call initanodelist')
    #experiment.initanodelist(numberofwebids=20)
    experiment.initanodelist(numberofwebids=numwebids)
    #print('back from initanodelist')
    #print('---------------------------')
    
    #print('about to call initsanodelist')
    experiment.initsanodelist(percs)
    #print('back from initsanodelist ')
    #print('---------------------------')
    #experiment.imagineaclnormal(openperc=100,numofwebids=20,mean=10, disp=0,filelabel='Filelabel1')
    #print('About to call flexexperiment.imagineaclnormal')
    #experiment.imagineaclnormal(openperc=100,numofwebids=20,mean=10, disp=0,filelabel=filelab1)
    experiment.imagineaclnormal(openperc=100,mean=(floor(numwebids/2)), disp=0,filelabel=filelab1)
    #print('Back from flexexperiment.imagineaclnormal')
    #print('---------------------------')
    # HO 16/08/2024 END **********

    # HO 16/08/2024 BEGIN **********
    #experiment.imagineaclnormal(openperc=50,numofwebids=20,mean=10, disp=0,filelabel='Filelabel2')
    #print('About to call flexexperiment.imagineaclnormal')
    experiment.imagineaclnormal(openperc=50,mean=(floor(numwebids/2)), disp=0,filelabel=filelab2)
    #print('Back from flexexperiment.imagineaclnormal')
    #print('---------------------------')
    # HO 16/08/2024 END **********

    # HO 16/08/2024 BEGIN *************
    #experiment.imagineaclnormal(openperc=10,numofwebids=20,mean=10, disp=0,filelabel='Filelabel3')
    #print('About to call flexexperiment.imagineaclnormal')
    experiment.imagineaclnormal(openperc=10,mean=floor(numwebids/2), disp=0,filelabel=filelab3)
    #print('Back from flexexperiment.imagineaclnormal')
    # HO 16/08/2024 END *************

    # HO 16/08/2024 BEGIN *********
    #experiment.imagineaclspecial(percs,'Filelabel1')
    #print('About to call flexexperiment.imagineaclspecial')
    #experiment.imagineaclspecial(percs,filelab1)
    experiment.imagineaclspecial(filelab1)
    #print('Back from flexexperiment.imagineaclspecial')
    #print('---------------------------')
    # HO 16/08/2024 END *********

    # HO 16/08/2024 BEGIN *******
    # experiment.imagineaclspecial(percs,'Filelabel2')
    #print('About to call flexexperiment.imagineaclspecial')
    #experiment.imagineaclspecial(percs, filelab2)
    experiment.imagineaclspecial(filelab2)
    #print('Back from flexexperiment.imagineaclspecial')
    #print('---------------------------')
    # HO 16/08/2024 END *********

    # HO 16/08/2024 BEGIN ***********
    #experiment.imagineaclspecial(percs,'Filelabel3')
    ##print('About to call flexexperiment.imagineaclspecial')
    #experiment.imagineaclspecial(percs, filelab3)
    experiment.imagineaclspecial(filelab3)
    #print('Back from flexexperiment.imagineaclspecial')
    # HO 16/08/2024 ENDs ***********
    
    # user progress message
    #print('files acl imagined')
    
    # saves the experiment as a .ttl file named after the podname plus 'exp'
    #print('About to call flexexperiment.saveexp')
    experiment.saveexp(podname+'exp.ttl')

    # user progress message
    #print('experiment saved') 
    #print('===================')
    # return the flexexperiment.ESPRESSOexperiment object
    return experiment

# Pod name template and experiment name
# example podname value: 'ardfhealth'
podname='ardfhealth'
#print('BEGIN *************************************')
#print('Preparing for step 0')
#print('expeerimenttemplate.podname = ' + podname)

# name for the metaindex file.
# example espressoindexfile value: 'ardfhealthmetaindex.csv'
espressoindexfile=podname+'metaindex.csv'
#print('expeerimenttemplate.espressoindexfile = ' + espressoindexfile)

# creating the logical view and saving it
#print('expeerimenttemplate: about to create experiment')
#print('method: expeerimenttemplate.createexperiment')
#print('param: podname = ' + podname)
# example podname value: 'ardfhealth'
experiment=createexperiment(podname)
#print('created experiment, one step done')
#print('===================================')

# Loading the experiment. Step 1.
#print('expeerimenttemplate: about to call flexexperiment.loadexp for ' + podname+'exp.ttl')
experiment=flexexperiment.loadexp(podname+'exp.ttl')
# display progress message
#print('Experiment loaded')
#print('another step done')
#print('===================================')

# Creating the experiment infrastructure - pods, metaindexes, triples
# and making the indexes and metaindexes open access
#print('expeerimenttemplate: about to deploy experiment')
deployexperiment(experiment)
#print('Experiment deployed')
#print('another step done')
#print('===================================')

#Uploading of the files and corresponding acls
#print('expeerimenttemplate: about to upload experiment')
uploadexperiment(experiment)
#print('another step done')
#print('===================================')

#Indexing of the experiment
#print('expeerimenttemplate: about to index experiment')
indexexperiment(experiment) 
#print('===================================')