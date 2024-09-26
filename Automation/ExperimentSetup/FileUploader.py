# requests: https://pypi.org/project/requests/
import requests
# os: https://docs.python.org/3/library/os.html
# json: https://docs.python.org/3/library/json.html
import os, json
# handles the client credentials for Community Solid Server
# HO 15/08/2024 BEGIN *********************
import sys
sys.path.append('../CSSAccess')
import CSSaccess
#from Automation.CSSAccess import CSSaccess
#import ..Automation
#from .Automation.CSSAccess import CSSaccess
# HO 15/08/2024 END *********************
# tqdm: https://tqdm.github.io/
import tqdm

def putdirCSS (directory,pod,IDP,USERNAME,PASSWORD,indexfile=''):
    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
    #a=CSSA.create_authstring()
    #t=CSSA.create_authtoken()
    CSSA.new_session()

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and filename[0]!='.' and filename != indexfile:
            file = open(f, "rb")
            filetext=file.read().decode('latin1')
            #.decode('utf-8')
            #x.encode('ascii', 'ignore').decode()
            file.close()
            file_url=pod+filename
            print('putting '+filename+' to the pod '+ pod)
            print(CSSA.put_file(pod, filename, filetext, 'text/plain'))
            #api.put_file(file_url, filetext, 'text/markdown')
    indexpath=os.path.join(directory, indexfile)
    if os.path.isfile(indexpath):
        CSSA.put_file(pod, indexfile, filetext, 'text/turtle')
    return pod
    
def putlistCSS (filelist,pod,IDP,USERNAME,PASSWORD):
    CSSA=CSSaccess.CSSaccess(IDP, USERNAME, PASSWORD)
    a=CSSA.create_authstring()
    t=CSSA.create_authtoken()
    #CSSA.new_session()

    for f in filelist:
        # checking if it is a file
        filename=f.rsplit('/')[-1]
        if os.path.isfile(f):
            file = open(f, "rb")
            filetext=file.read().decode('latin1')
            #.decode('utf-8')
            #x.encode('ascii', 'ignore').decode()
            file.close()
            file_url=pod+filename
            print('putting '+filename+' to the pod '+ pod)
            r=CSSA.put_file(pod, filename, filetext, 'text/plain')
            filename=CSSA.idp+pod+'/'+filename
            #print(CSSA.get_file(filename))
            #api.put_file(file_url, filetext, 'text/markdown')
    

def postdirtopod (directory,pod,api):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and filename[0]!='.':
            file = open(f, "rb")
            filetext=file.read().decode('latin1')
            #.decode('utf-8')
            #x.encode('ascii', 'ignore').decode()
            file.close()
            file_url=pod+filename
            print('putting '+filename+' to the pod '+ pod)
            api.put_file(file_url, filetext, 'text/markdown')
    return pod

def uploadllistwithbar (filetuplelist,podaddress,CSSA):
    pbar=tqdm.tqdm(len(filetuplelist),desc=podaddress)
    for f,targetUrl,filetype in filetuplelist:
            file = open(f, "r")
            filetext=file.read()
            file.close()
            res=CSSA.put_url(targetUrl, filetext, filetype)
            if not res.ok:
                print(res)
                continue
            pbar.update(1)
    pbar.close()

"""
Upload the file tuple list to a pod, while replacing designated text, and displaying a progress bar.

param: filetuplelist, the list of file tuples to upload
param: replacetemplate, the template for replacing part of the text
param: podaddress, address of the pod to upload to
param: CSSA, the CSSaccess object with the client credentials
"""
def uploadllistreplacewithbar(filetuplelist,replacetemplate,podaddress,CSSA):
    # set up the progress bar
    pbar=tqdm.tqdm(total=len(filetuplelist),desc=podaddress)
    # initialize a list to hold the files that fail to upload
    faillist=[]
    # now for every file tuple in the list
    for f,targetUrl,filetype,substring in filetuplelist:
            # open the file for reading
            file = open(f, "r")
            # get the text of the file
            filetext=file.read()
            # close the file
            file.close()
            # if there's any replacement text
            if len(substring)>0:
                # replace the designated file text as specified
                filetext=filetext.replace(replacetemplate,substring)
            # PUT the filetext to the target file
            if(str(filetype) == '0'):
                filetype='text/plain'
            # HO 25/09/2024 BEGIN ***********
            #try: 
            res=CSSA.put_url(targetUrl, filetext, filetype)
            #except:
                #print("Couldn't put to " + targeturl + ", trying again: ")
                #res=CSSA.put_url(targetUrl, filetext, filetype)
            # HO 25/09/2024 END ***********
            # if it didn't work
            if not res.ok:
                # add this to the list of failed uploads
                faillist.append((targetUrl,res))
                # move on to the next file
                continue
            # update the progress bar
            pbar.update(1)
    # close the progress bar
    pbar.close()
    # notify how many of the uploads failed
    print('failed',len(faillist),'out of',len(filetuplelist))
    # display the list of failed uploads
    print(faillist)




def uploadllistaclwithbar (filetuplelist,podaddress,CSSA):
    pbar=tqdm.tqdm(len(filetuplelist),desc=podaddress)
    for targetUrl,openfile,webidlist in filetuplelist:
        if openfile:
            CSSA.makeurlaccessible(targetUrl,targetUrl[len(podaddress):])
        else:
            res=CSSA.adddefaultacl(targetUrl)            
        CSSA.addreadrights(targetUrl,webidlist)
        pbar.update(1)
    pbar.close()