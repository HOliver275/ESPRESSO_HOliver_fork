# an ESPRESSO experiment script
import flexexperiment
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
    
    # Create the server-level metaindexes.
    experiment.aclmetaindex()
    # display progress message
    print('metaindexes created')
    
    # Make all the pod indexes open access.
    experiment.indexpub()
    # display progress message
    print('indexes opened')
    
    # Make the metaindexes accessible to the experiment
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
    # OPTION A: if you have 18 hours to waste
    """# upload the files to populate the pods
    experiment.uploadfiles()
    # display progress message
    print('Pods populated')
    
    # upload the ACL files
    experiment.uploadacls()
    # display progress message
    print('Acls populated')"""
    
    # OPTION B: for people who have things to do
    experiment.storelocalfileszip(zipdir)
    
"""
Step 4. We can do this if the experiment is not too big, otherwise we have to call zip(experiment,zipdir,SSHuser,SSHPassword) 

Indexes the experiment.
param: experiment, a flexexperiment.ESPRESSOexperiment 
"""
def indexexperiment(experiment):
    
    ########################
    # Option A step 1, for smaller experiments: index the pods on the fly 
    """experiment.aclindexwebidnewthreaded()
    print('pods indexed')
    
    # Option A step 2, for smaller experiments: check the indexes 
    # note: we're not doing this for the metaindex even for small experiments
    experiment.indexfixerwebidnew()
    print('indexes checked')"""
    ########################
    
    ########################
    # Option B: if the experiment is too big, do the zipping and unzipping method: 
    # This will store the indexes in zips locally  
    # And distribute them to the corresponding servers using ssh.
    
    # Option B, step 1, zip the indexes and store locally
    # HO 04/12/2024 BEGIN ************* 
    #experiment.serverlevel_storelocalindexzipdirs(zipdir)
    experiment.serverlevel_storelocalindexzipdirs(zipdir, overlaydir)
    # HO 04/12/2024 END ************* 
    
    # Option B, step 2: distribute zips(using SSH username and password) 
    """experiment.distributezips(zipdir,SSHUser,SSHPassword,targetdir='/srv/espresso/')"""
    ########################

# Server labels
servlab1 = 'Serverlabel1'
servlab2 = 'Serverlabel2'
servlab3 = 'Serverlabel3'
servlab4 = 'Serverlabel4'
servlab5 = 'Serverlabel5'
servlab6 = 'Serverlabel6'
servlab7 = 'Serverlabel7'
servlab8 = 'Serverlabel8'
servlab9 = 'Serverlabel9'
servlab10 = 'Serverlabel10'
servlab11 = 'Serverlabel11'
servlab12 = 'Serverlabel12'
servlab13 = 'Serverlabel13'
servlab14 = 'Serverlabel14'
servlab15 = 'Serverlabel15'
servlab16 = 'Serverlabel16'
servlab17 = 'Serverlabel17'
servlab18 = 'Serverlabel18'
servlab19 = 'Serverlabel19'
servlab20 = 'Serverlabel20'
servlab21 = 'Serverlabel21'
servlab22 = 'Serverlabel22'
servlab23 = 'Serverlabel23'
servlab24 = 'Serverlabel24'
servlab25 = 'Serverlabel25'
servlab26 = 'Serverlabel26'
servlab27 = 'Serverlabel27'
servlab28 = 'Serverlabel28'
servlab29 = 'Serverlabel29'
servlab30 = 'Serverlabel30'
servlab31 = 'Serverlabel31'
servlab32 = 'Serverlabel32'
servlab33 = 'Serverlabel33'
servlab34 = 'Serverlabel34'
servlab35 = 'Serverlabel35'
servlab36 = 'Serverlabel36'
servlab37 = 'Serverlabel37'
servlab38 = 'Serverlabel38'
servlab39 = 'Serverlabel39'
servlab40 = 'Serverlabel40'
servlab41 = 'Serverlabel41'
servlab42 = 'Serverlabel42'
servlab43 = 'Serverlabel43'
servlab44 = 'Serverlabel44'
servlab45 = 'Serverlabel45'
servlab46 = 'Serverlabel46'
servlab47 = 'Serverlabel47'
servlab48 = 'Serverlabel48'
servlab49 = 'Serverlabel49'
servlab50 = 'Serverlabel50'

# file labels
filelab1 = 'Filelabel1'
filelab2 = 'Filelabel2'
filelab3 = 'Filelabel3'
filelab4 = 'Filelabel4'
filelab5 = 'Filelabel5'
filelab6 = 'Filelabel6'
filelab7 = 'Filelabel7'
filelab8 = 'Filelabel8'
filelab9 = 'Filelabel9'
filelab10 = 'Filelabel10'
filelab11 = 'Filelabel11'
filelab12 = 'Filelabel12'
filelab13 = 'Filelabel13'
filelab14 = 'Filelabel14'
filelab15 = 'Filelabel15'
filelab16 = 'Filelabel16'
filelab17 = 'Filelabel17'
filelab18 = 'Filelabel18'
filelab19 = 'Filelabel19'
filelab20 = 'Filelabel20'
filelab21 = 'Filelabel21'
filelab22 = 'Filelabel22'
filelab23 = 'Filelabel23'
filelab24 = 'Filelabel24'
filelab25 = 'Filelabel25'
filelab26 = 'Filelabel26'
filelab27 = 'Filelabel27'
filelab28 = 'Filelabel28'
filelab29 = 'Filelabel29'
filelab30 = 'Filelabel30'
filelab31 = 'Filelabel31'
filelab32 = 'Filelabel32'
filelab33 = 'Filelabel33'
filelab34 = 'Filelabel34'
filelab35 = 'Filelabel35'
filelab36 = 'Filelabel36'
filelab37 = 'Filelabel37'
filelab38 = 'Filelabel38'
filelab39 = 'Filelabel39'
filelab40 = 'Filelabel40'
filelab41 = 'Filelabel41'
filelab42 = 'Filelabel42'
filelab43 = 'Filelabel43'
filelab44 = 'Filelabel44'
filelab45 = 'Filelabel45'
filelab46 = 'Filelabel46'
filelab47 = 'Filelabel47'
filelab48 = 'Filelabel48'
filelab49 = 'Filelabel49'
filelab50 = 'Filelabel50'

# pod labels
podlab1 = 'pod1'
podlab2 = 'pod2'
podlab3 = 'pod3'
podlab4 = 'pod4'
podlab5 = 'pod5'
podlab6 = 'pod6'
podlab7 = 'pod7'
podlab8 = 'pod8'
podlab9 = 'pod9'
podlab10 = 'pod10'
podlab11 = 'pod11'
podlab12 = 'pod12'
podlab13 = 'pod13'
podlab14 = 'pod14'
podlab15 = 'pod15'
podlab16 = 'pod16'
podlab17 = 'pod17'
podlab18 = 'pod18'
podlab19 = 'pod19'
podlab20 = 'pod20'
podlab21 = 'pod21'
podlab22 = 'pod22'
podlab23 = 'pod23'
podlab24 = 'pod24'
podlab25 = 'pod25'
podlab26 = 'pod26'
podlab27 = 'pod27'
podlab28 = 'pod28'
podlab29 = 'pod29'
podlab30 = 'pod30'
podlab31 = 'pod31'
podlab32 = 'pod32'
podlab33 = 'pod33'
podlab34 = 'pod34'
podlab35 = 'pod35'
podlab36 = 'pod36'
podlab37 = 'pod37'
podlab38 = 'pod38'
podlab39 = 'pod39'
podlab40 = 'pod40'
podlab41 = 'pod41'
podlab42 = 'pod42'
podlab43 = 'pod43'
podlab44 = 'pod44'
podlab45 = 'pod45'
podlab46 = 'pod46'
podlab47 = 'pod47'
podlab48 = 'pod48'
podlab49 = 'pod49'
podlab50 = 'pod50'

# server lists
serverlist1=['https://srv03812.soton.ac.uk:3000/']
serverlist2=['https://srv03813.soton.ac.uk:3000/']
serverlist3=['https://srv03814.soton.ac.uk:3000/']
serverlist4=['https://srv03815.soton.ac.uk:3000/']
serverlist5=['https://srv03816.soton.ac.uk:3000/']
serverlist6=['https://srv03911.soton.ac.uk:3000/']
serverlist7=['https://srv03912.soton.ac.uk:3000/']
serverlist8=['https://srv03913.soton.ac.uk:3000/']
serverlist9=['https://srv03914.soton.ac.uk:3000/']
serverlist10=['https://srv03915.soton.ac.uk:3000/']
serverlist11=['https://srv03916.soton.ac.uk:3000/']
serverlist12=['https://srv03917.soton.ac.uk:3000/']
serverlist13=['https://srv03918.soton.ac.uk:3000/']
serverlist14=['https://srv03919.soton.ac.uk:3000/']
serverlist15=['https://srv03920.soton.ac.uk:3000/']
serverlist16=['https://srv03921.soton.ac.uk:3000/']
serverlist17=['https://srv03922.soton.ac.uk:3000/']
serverlist18=['https://srv03923.soton.ac.uk:3000/']
serverlist19=['https://srv03924.soton.ac.uk:3000/']
serverlist20=['https://srv03925.soton.ac.uk:3000/']
serverlist21=['https://srv03926.soton.ac.uk:3000/']
serverlist22=['https://srv03927.soton.ac.uk:3000/']
serverlist23=['https://srv03928.soton.ac.uk:3000/']
serverlist24=['https://srv03929.soton.ac.uk:3000/']
serverlist25=['https://srv03930.soton.ac.uk:3000/']
serverlist26=['https://srv03931.soton.ac.uk:3000/']
serverlist27=['https://srv03932.soton.ac.uk:3000/']
serverlist28=['https://srv03933.soton.ac.uk:3000/']
serverlist29=['https://srv03934.soton.ac.uk:3000/']
serverlist30=['https://srv03935.soton.ac.uk:3000/']
serverlist31=['https://srv03936.soton.ac.uk:3000/']
serverlist32=['https://srv03937.soton.ac.uk:3000/']
serverlist33=['https://srv03938.soton.ac.uk:3000/']
serverlist34=['https://srv03939.soton.ac.uk:3000/']
serverlist35=['https://srv03940.soton.ac.uk:3000/']
serverlist36=['https://srv03941.soton.ac.uk:3000/']
serverlist37=['https://srv03942.soton.ac.uk:3000/']
serverlist38=['https://srv03943.soton.ac.uk:3000/']
serverlist39=['https://srv03944.soton.ac.uk:3000/']
serverlist40=['https://srv03945.soton.ac.uk:3000/']
serverlist41=['https://srv03946.soton.ac.uk:3000/']
serverlist42=['https://srv03947.soton.ac.uk:3000/']
serverlist43=['https://srv03948.soton.ac.uk:3000/']
serverlist44=['https://srv03949.soton.ac.uk:3000/']
serverlist45=['https://srv03950.soton.ac.uk:3000/']
serverlist46=['https://srv03951.soton.ac.uk:3000/']
serverlist47=['https://srv03952.soton.ac.uk:3000/']
serverlist48=['https://srv03953.soton.ac.uk:3000/']
serverlist49=['https://srv03954.soton.ac.uk:3000/']
serverlist50=['https://srv03955.soton.ac.uk:3000/']

# source directories for data
sourcedir1='../DatasetSplitter/sourcedir1/'
sourcedir2 = '../DatasetSplitter/sourcedir2/'
sourcedir3 = '../DatasetSplitter/sourcedir3/'
sourcedir4 = '../DatasetSplitter/sourcedir4/'
sourcedir5 = '../DatasetSplitter/sourcedir5/'
sourcedir6 = '../DatasetSplitter/sourcedir6/'
sourcedir7 = '../DatasetSplitter/sourcedir7/'
sourcedir8 = '../DatasetSplitter/sourcedir8/'
sourcedir9 = '../DatasetSplitter/sourcedir9/'
sourcedir10 = '../DatasetSplitter/sourcedir10/'
sourcedir11 = '../DatasetSplitter/sourcedir11/'
sourcedir12 = '../DatasetSplitter/sourcedir12/'
sourcedir13 = '../DatasetSplitter/sourcedir13/'
sourcedir14 = '../DatasetSplitter/sourcedir14/'
sourcedir15 = '../DatasetSplitter/sourcedir15/'
sourcedir16 = '../DatasetSplitter/sourcedir16/'
sourcedir17 = '../DatasetSplitter/sourcedir17/'
sourcedir18 = '../DatasetSplitter/sourcedir18/'
sourcedir19 = '../DatasetSplitter/sourcedir19/'
sourcedir20 = '../DatasetSplitter/sourcedir20/'
sourcedir21 = '../DatasetSplitter/sourcedir21/'
sourcedir22 = '../DatasetSplitter/sourcedir22/'
sourcedir23 = '../DatasetSplitter/sourcedir23/'
sourcedir24 = '../DatasetSplitter/sourcedir24/'
sourcedir25 = '../DatasetSplitter/sourcedir25/'
sourcedir26 = '../DatasetSplitter/sourcedir26/'
sourcedir27 = '../DatasetSplitter/sourcedir27/'
sourcedir28 = '../DatasetSplitter/sourcedir28/'
sourcedir29 = '../DatasetSplitter/sourcedir29/'
sourcedir30 = '../DatasetSplitter/sourcedir30/'
sourcedir31 = '../DatasetSplitter/sourcedir31/'
sourcedir32 = '../DatasetSplitter/sourcedir32/'
sourcedir33 = '../DatasetSplitter/sourcedir33/'
sourcedir34 = '../DatasetSplitter/sourcedir34/'
sourcedir35 = '../DatasetSplitter/sourcedir35/'
sourcedir36 = '../DatasetSplitter/sourcedir36/'
sourcedir37 = '../DatasetSplitter/sourcedir37/'
sourcedir38 = '../DatasetSplitter/sourcedir38/'
sourcedir39 = '../DatasetSplitter/sourcedir39/'
sourcedir40 = '../DatasetSplitter/sourcedir40/'
sourcedir41 = '../DatasetSplitter/sourcedir41/'
sourcedir42 = '../DatasetSplitter/sourcedir42/'
sourcedir43 = '../DatasetSplitter/sourcedir43/'
sourcedir44 = '../DatasetSplitter/sourcedir44/'
sourcedir45 = '../DatasetSplitter/sourcedir45/'
sourcedir46 = '../DatasetSplitter/sourcedir46/'
sourcedir47 = '../DatasetSplitter/sourcedir47/'
sourcedir48 = '../DatasetSplitter/sourcedir48/'
sourcedir49 = '../DatasetSplitter/sourcedir49/'
sourcedir50 = '../DatasetSplitter/sourcedir50/'

numfiles = 9500
#numfiles = 10

# Name of the ESPRESSO pod. ESPRESSO is default.
espressopodname='ESPRESSO'
# Email to register the ESPRESSO pod. espresso@example.com is default.
espressoemail='espresso@example.com'
# Name for the pods in the experiment the pods will be called podname0, podname1, etc.
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
#openperc=0
numwebids=250
#numwebids=20
# number of pods
numpods=9500
#numpods=10
# on average how many webids can read a given file
#themean=1
themean=10
# relative deviation of the percentage of webids that can read a given file, can be left 0
disp=0
    #how many files on average a webid can read
    #initializing the experiment
    
# zip directory name
zipdir='zipdir'

# overlay directory name
overlaydir='overlaydir'

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

    # HO 08/11/2024 BEGIN *************
    #experiment=flexexperiment.ESPRESSOexperiment(espressopodname=espressopodname, espressoemail=espressoemail, espressoindexdir=espressoindexdir, podname=podname,podemail=podemail, podindexdir=podindexdir, password=password)
    experiment=flexexperiment.ESPRESSOexperiment(espressopodname=espressopodname, espressoemail=espressoemail, espressoindexdir=espressoindexdir, podname=podname,podemail=podemail, podindexdir=podindexdir, password=password, podsperserver=numpods)
    # HO 08/11/2024 END *************

    print("Constructed experiment")
    
    # Server list loading
    experiment.loadserverlist(serverlist1, servlab1)

    experiment.loadserverlist(serverlist2, servlab2)

    experiment.loadserverlist(serverlist3, servlab3)

    experiment.loadserverlist(serverlist4, servlab4)

    experiment.loadserverlist(serverlist5, servlab5)

    experiment.loadserverlist(serverlist6, servlab6)

    experiment.loadserverlist(serverlist7, servlab7)

    experiment.loadserverlist(serverlist8, servlab8)

    experiment.loadserverlist(serverlist9, servlab9)

    experiment.loadserverlist(serverlist10, servlab10)

    experiment.loadserverlist(serverlist11, servlab11)

    experiment.loadserverlist(serverlist12, servlab12)

    experiment.loadserverlist(serverlist13, servlab13)

    experiment.loadserverlist(serverlist14, servlab14)

    experiment.loadserverlist(serverlist15, servlab15)

    experiment.loadserverlist(serverlist16, servlab16)

    experiment.loadserverlist(serverlist17, servlab17)

    experiment.loadserverlist(serverlist18, servlab18)

    experiment.loadserverlist(serverlist19, servlab19)

    experiment.loadserverlist(serverlist20, servlab20)

    experiment.loadserverlist(serverlist21, servlab21)

    experiment.loadserverlist(serverlist22, servlab22)

    experiment.loadserverlist(serverlist23, servlab23)

    experiment.loadserverlist(serverlist24, servlab24)

    experiment.loadserverlist(serverlist25, servlab25)

    experiment.loadserverlist(serverlist26, servlab26)

    experiment.loadserverlist(serverlist27, servlab27)

    experiment.loadserverlist(serverlist28, servlab28)

    experiment.loadserverlist(serverlist29, servlab29)

    experiment.loadserverlist(serverlist30, servlab30)

    experiment.loadserverlist(serverlist31, servlab31)

    experiment.loadserverlist(serverlist32, servlab32)

    experiment.loadserverlist(serverlist33, servlab33)

    experiment.loadserverlist(serverlist34, servlab34)

    experiment.loadserverlist(serverlist35, servlab35)

    experiment.loadserverlist(serverlist36, servlab36)

    experiment.loadserverlist(serverlist37, servlab37)

    experiment.loadserverlist(serverlist38, servlab38)

    experiment.loadserverlist(serverlist39, servlab39)

    experiment.loadserverlist(serverlist40, servlab40)

    experiment.loadserverlist(serverlist41, servlab41)

    experiment.loadserverlist(serverlist42, servlab42)

    experiment.loadserverlist(serverlist43, servlab43)

    experiment.loadserverlist(serverlist44, servlab44)

    experiment.loadserverlist(serverlist45, servlab45)

    experiment.loadserverlist(serverlist46, servlab46)

    experiment.loadserverlist(serverlist47, servlab47)

    experiment.loadserverlist(serverlist48, servlab48)

    experiment.loadserverlist(serverlist49, servlab49)

    experiment.loadserverlist(serverlist50, servlab50)

    # user message
    print('serverlist loaded')

    # create pods
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab1,podlabel=podlab1)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab2,podlabel=podlab2)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab3,podlabel=podlab3)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab4,podlabel=podlab4)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab5,podlabel=podlab5)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab6,podlabel=podlab6)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab7,podlabel=podlab7)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab8,podlabel=podlab8)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab9,podlabel=podlab9)

experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab10,podlabel=podlab10)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab11,podlabel=podlab11)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab12,podlabel=podlab12)

experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab13,podlabel=podlab13)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab14,podlabel=podlab14)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab15,podlabel=podlab15)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab16,podlabel=podlab16)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab17,podlabel=podlab17)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab18,podlabel=podlab18)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab19,podlabel=podlab19)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab20,podlabel=podlab20)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab21,podlabel=podlab21)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab22,podlabel=podlab22)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab23,podlabel=podlab23)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab24,podlabel=podlab24)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab25,podlabel=podlab25)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab26,podlabel=podlab26)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab27,podlabel=podlab27)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab28,podlabel=podlab28)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab29,podlabel=podlab29)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab30,podlabel=podlab30)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab31,podlabel=podlab31)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab32,podlabel=podlab32)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab33,podlabel=podlab33)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab34,podlabel=podlab34)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab35,podlabel=podlab35)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab36,podlabel=podlab36)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab37,podlabel=podlab37)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab38,podlabel=podlab38)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab39,podlabel=podlab39)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab40,podlabel=podlab40)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab41,podlabel=podlab41)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab42,podlabel=podlab42)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab43,podlabel=podlab43)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab44,podlabel=podlab44)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab45,podlabel=podlab45)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab46,podlabel=podlab46)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab47,podlabel=podlab47)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab48,podlabel=podlab48)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab49,podlabel=podlab49)
    experiment.createlogicalpods(numberofpods=numpods,serverdisp=0,serverlabel=servlab50,podlabel=podlab50)

    print('logical pods created ')

    experiment.loaddirtopool(sourcedir1, filelab1)

    experiment.loaddirtopool(sourcedir2, filelab2)

    experiment.loaddirtopool(sourcedir3, filelab3)

    experiment.loaddirtopool(sourcedir4, filelab4)

    experiment.loaddirtopool(sourcedir5, filelab5)

    experiment.loaddirtopool(sourcedir6, filelab6)

    experiment.loaddirtopool(sourcedir7, filelab7)

    experiment.loaddirtopool(sourcedir8, filelab8)

    experiment.loaddirtopool(sourcedir9, filelab9)

    experiment.loaddirtopool(sourcedir10, filelab10)

    experiment.loaddirtopool(sourcedir11, filelab11)

    experiment.loaddirtopool(sourcedir12, filelab12)

    experiment.loaddirtopool(sourcedir13, filelab13)

    experiment.loaddirtopool(sourcedir14, filelab14)

    experiment.loaddirtopool(sourcedir15, filelab15)

    experiment.loaddirtopool(sourcedir16, filelab16)

    experiment.loaddirtopool(sourcedir17, filelab17)

    experiment.loaddirtopool(sourcedir18, filelab18)

    experiment.loaddirtopool(sourcedir19, filelab19)

    experiment.loaddirtopool(sourcedir20, filelab20)

    experiment.loaddirtopool(sourcedir21, filelab21)

    experiment.loaddirtopool(sourcedir22, filelab22)

    experiment.loaddirtopool(sourcedir23, filelab23)

    experiment.loaddirtopool(sourcedir24, filelab24)

    experiment.loaddirtopool(sourcedir25, filelab25)

    experiment.loaddirtopool(sourcedir26, filelab26)

    experiment.loaddirtopool(sourcedir27, filelab27)

    experiment.loaddirtopool(sourcedir28, filelab28)

    experiment.loaddirtopool(sourcedir29, filelab29)

    experiment.loaddirtopool(sourcedir30, filelab30)

    experiment.loaddirtopool(sourcedir31, filelab31)

    experiment.loaddirtopool(sourcedir32, filelab32)

    experiment.loaddirtopool(sourcedir33, filelab33)

    experiment.loaddirtopool(sourcedir34, filelab34)

    experiment.loaddirtopool(sourcedir35, filelab35)

    experiment.loaddirtopool(sourcedir36, filelab36)

    experiment.loaddirtopool(sourcedir37, filelab37)

    experiment.loaddirtopool(sourcedir38, filelab38)

    experiment.loaddirtopool(sourcedir39, filelab39)

    experiment.loaddirtopool(sourcedir40, filelab40)

    experiment.loaddirtopool(sourcedir41, filelab41)

    experiment.loaddirtopool(sourcedir42, filelab42)

    experiment.loaddirtopool(sourcedir43, filelab43)

    experiment.loaddirtopool(sourcedir44, filelab44)

    experiment.loaddirtopool(sourcedir45, filelab45)

    experiment.loaddirtopool(sourcedir46, filelab46)

    experiment.loaddirtopool(sourcedir47, filelab47)

    experiment.loaddirtopool(sourcedir48, filelab48)

    experiment.loaddirtopool(sourcedir49, filelab49)

    experiment.loaddirtopool(sourcedir50, filelab50)

    print('loaded source dirs to pool')
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab1,podlabel=podlab1,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab2,podlabel=podlab2,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab3,podlabel=podlab3,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab4,podlabel=podlab4,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab5,podlabel=podlab5,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab6,podlabel=podlab6,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab7,podlabel=podlab7,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab8,podlabel=podlab8,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab9,podlabel=podlab9,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab10,podlabel=podlab10,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab11,podlabel=podlab11,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab12,podlabel=podlab12,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab13,podlabel=podlab13,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab14,podlabel=podlab14,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab15,podlabel=podlab15,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab16,podlabel=podlab16,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab17,podlabel=podlab17,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab18,podlabel=podlab18,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab19,podlabel=podlab19,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab20,podlabel=podlab20,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab21,podlabel=podlab21,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab22,podlabel=podlab22,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab23,podlabel=podlab23,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab24,podlabel=podlab24,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab25,podlabel=podlab25,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab26,podlabel=podlab26,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab27,podlabel=podlab27,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab28,podlabel=podlab28,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab29,podlabel=podlab29,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab30,podlabel=podlab30,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab31,podlabel=podlab31,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab32,podlabel=podlab32,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab33,podlabel=podlab33,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab34,podlabel=podlab34,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab35,podlabel=podlab35,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab36,podlabel=podlab36,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab37,podlabel=podlab37,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab38,podlabel=podlab38,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab39,podlabel=podlab39,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab40,podlabel=podlab40,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab41,podlabel=podlab41,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab42,podlabel=podlab42,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab43,podlabel=podlab43,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab44,podlabel=podlab44,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab45,podlabel=podlab45,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab46,podlabel=podlab46,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab47,podlabel=podlab47,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab48,podlabel=podlab48,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab49,podlabel=podlab49,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)
    experiment.logicaldistfilestopodsfrompool(numberoffiles=numfiles,filedisp=0,filetype=0,filelabel=filelab50,podlabel=podlab50,subdir='file',predicatetopod=URIRef('http://example.org/SOLIDindex/HasFile'),replacebool=False)

    print('files distributed')
    
    # agent nodes
    experiment.initanodelist(numberofwebids=numwebids)
    
    print('agent nodes initialized')
    
    #print('about to call initsanodelist')
    experiment.initsanodelist(percs)
    
    print('special agent nodes initialized')

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab1)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab2)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab3)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab4)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab5)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab6)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab7)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab8)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab9)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab10)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab11)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab12)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab13)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab14)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab15)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab16)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab17)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab18)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab19)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab20)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab21)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab22)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab23)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab24)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab25)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab26)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab27)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab28)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab29)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab30)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab31)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab32)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab33)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab34)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab35)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab36)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab37)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab38)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab39)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab40)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab41)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab42)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab43)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab44)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab45)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab46)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab47)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab48)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab49)

    experiment.imagineaclnormal(openperc=openperc,mean=themean, disp=0,filelabel=filelab50)
    
    print('Normal ACLs distributed')
    
    experiment.imagineaclspecial(filelab1)

    experiment.imagineaclspecial(filelab2)

    experiment.imagineaclspecial(filelab3)

    experiment.imagineaclspecial(filelab4)

    experiment.imagineaclspecial(filelab5)

    experiment.imagineaclspecial(filelab6)

    experiment.imagineaclspecial(filelab7)

    experiment.imagineaclspecial(filelab8)

    experiment.imagineaclspecial(filelab9)

    experiment.imagineaclspecial(filelab10)

    experiment.imagineaclspecial(filelab11)

    experiment.imagineaclspecial(filelab12)

    experiment.imagineaclspecial(filelab13)

    experiment.imagineaclspecial(filelab14)

    experiment.imagineaclspecial(filelab15)

    experiment.imagineaclspecial(filelab16)

    experiment.imagineaclspecial(filelab17)

    experiment.imagineaclspecial(filelab18)

    experiment.imagineaclspecial(filelab19)

    experiment.imagineaclspecial(filelab20)

    experiment.imagineaclspecial(filelab21)

    experiment.imagineaclspecial(filelab22)

    experiment.imagineaclspecial(filelab23)

    experiment.imagineaclspecial(filelab24)

    experiment.imagineaclspecial(filelab25)

    experiment.imagineaclspecial(filelab26)

    experiment.imagineaclspecial(filelab27)

    experiment.imagineaclspecial(filelab28)

    experiment.imagineaclspecial(filelab29)

    experiment.imagineaclspecial(filelab30)

    experiment.imagineaclspecial(filelab31)

    experiment.imagineaclspecial(filelab32)

    experiment.imagineaclspecial(filelab33)

    experiment.imagineaclspecial(filelab34)

    experiment.imagineaclspecial(filelab35)

    experiment.imagineaclspecial(filelab36)

    experiment.imagineaclspecial(filelab37)

    experiment.imagineaclspecial(filelab38)

    experiment.imagineaclspecial(filelab39)

    experiment.imagineaclspecial(filelab40)

    experiment.imagineaclspecial(filelab41)

    experiment.imagineaclspecial(filelab42)

    experiment.imagineaclspecial(filelab43)

    experiment.imagineaclspecial(filelab44)

    experiment.imagineaclspecial(filelab45)

    experiment.imagineaclspecial(filelab46)

    experiment.imagineaclspecial(filelab47)

    experiment.imagineaclspecial(filelab48)

    experiment.imagineaclspecial(filelab49)

    experiment.imagineaclspecial(filelab50)
    
    print('Special agent ACLs distributed')
    
    # saves the experiment as a .ttl file named after the podname plus 'exp'
    experiment.saveexp(podname+'exp.ttl')

    # user progress message
    print('experiment saved') 
    print('===================')

    # build Lucene index
    experiment.buildluceneindex()
    print('Lucene index built, check above for any errors')
    print('===================')
    # return the flexexperiment.ESPRESSOexperiment object

    return experiment

# Pod name template and experiment name
# example podname value: 'ardfhealth'
podname='ardfhealth_vldb'

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
print('Experiment indexed')
print('===================')
