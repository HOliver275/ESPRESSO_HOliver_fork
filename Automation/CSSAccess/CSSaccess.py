# handles the DPOP preparations
# HO 15/08/2024 BEGIN ***********
from Automation.CSSAccess import dpop_utils
# import dpop_utils
# HO 15/08/2024 END ***********
# json: https://docs.python.org/3/library/json.html
# requests: https://pypi.org/project/requests/
# urllib.parse: https://docs.python.org/3/library/urllib.parse.html
# base64: https://docs.python.org/3/library/base64.html
import json, requests, urllib.parse, base64
# rdflib.Graph: https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph
from rdflib import Graph

class CSSaccess:
    """
    Provides access to a CSS solid server.
    
    param: self
    param: IDP, the identity provider, which would be the Solid server host
    param: USERNAME, the user name
    param: PASSWORD, the password
    """
    def __init__(self, IDP,USERNAME,PASSWORD):
        # set the identity provider
        self.idp = IDP
        # set the username
        self.username = USERNAME
        # set the password
        self.password = PASSWORD
        # set the URL for the credentials with the identity provider
        self.cred_url = IDP+'idp/credentials/'
        # set the URL for the OIDC token
        self.token_url = IDP+'.oidc/token'
        # initialize an empty auth string
        self.authstring =''
        # initialize an empty auth token
        self.authtoken = ''
        # gets a (P-256 EC) JSON Web Key pair
        self.dpopKey = dpop_utils.generate_dpop_key_pair()
        
    def __repr__(self):
        """
        Return identity provider. Can be changed later
        """
        return str(self.idp)

    """
    Creates authorization string.
    
    param: self    
    return: authstring, the auth string consisting of the id and secret
    """    
    def create_authstring(self):
        # create the structure to access the pod data
        data ={ 'email': self.username, 'password': self.password, 'name': 'my-token' }
        # dump the data at that pod
        datajson=json.dumps(data)
        # post the dumped data using the IDP credentials URL
        # HO 25/09/2024 BEGIN ****************
        res = requests.post(self.cred_url, headers={ 'content-type': 'application/json' }, data=str(datajson))
        #res = requests.post(self.cred_url, headers={ 'content-type': 'application/json' }, data=str(datajson), timeout=5000)
        # HO 25/09/2024 END **************
        # JSONify the result
        res=res.json()
        # parse the id and secret to get the authstring
        self.authstring=urllib.parse.quote(res['id'])+':'+urllib.parse.quote(res['secret'])
        # return the authstring consisting of the id and secret
        return self.authstring

    def get_token_list(self):
        data ={ 'email': self.username, 'password': self.password}
        datajson=json.dumps(data)
        res = requests.post(self.cred_url,headers={ 'content-type': 'application/json' }, data=str(datajson))
        tokenlist = list(res.json())
        return tokenlist

    def delete_token(self,token):
        datat ={ 'email': self.username, 'password': self.password, 'delete':token}
        datatjson=json.dumps(datat)
        rest = requests.post(self.cred_url,headers={ 'content-type': 'application/json' }, data=str(datatjson))

    def delete_all_tokens(self):
        tokenlist = self.get_token_list()
        for t in tokenlist:
            self.delete_token(t)

    """
    Creates the auth token.
    
    param: self
    return: authtoken, the auth token from the client credentials
    """    
    def create_authtoken(self):
        # HO 22/09/2024 BEGIN ***********
        
        # HO 22/09/2024 END *************
        # get the auth string as bytes
        s=bytes(self.authstring, 'utf-8')
        # base-64 encode everything from element 2 of the auth string onwards
        auth='Basic %s' % str(base64.standard_b64encode(s))[2:]
        # post the OIDC token URL and headers, using the base-64 encoded auth string,
        # and the DPOP key
        # and you get back the client credentials for this WebID
        res = requests.post(
            self.token_url,
            headers= {
                'content-type': 'application/x-www-form-urlencoded',
                'authorization': auth,
                'DPoP': dpop_utils.create_dpop_header(self.token_url, 'POST', self.dpopKey)
            },
            data={"grant_type":"client_credentials","scope": "webid"},
            timeout=5000
        ) 
        # get the auth token out of the response
        self.authtoken =res.json()['access_token']

        # return the auth token
        return self.authtoken

    def new_session(self):
        self.delete_all_tokens()
        a=self.create_authstring()
        t=self.create_authtoken()

    """
    Do a PUT of a given file to a given pod.
    
    param: self
    param: podname, the target pod name
    param: filename, the name of the file to put
    param: filetext, the text of the file to put
    param: filetype, the type of file to put
    return: res, the server response
    """
    def put_file(self,podname,filename,filetext,filetype):
        # construct a full path to the target file
        targetUrl=self.idp+podname+'/'+filename
        # create authorization headers
        headers={ 'content-type': filetype, 'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", self.dpopKey)}
        # PUT the new text to the file
        res= requests.put(targetUrl,
            headers=headers,
            data=filetext
        )
        # return the response
        return res 

    """
    Does a PUT request with the text of a target file.
    
    param: self
    param: targetURL, the URL of the target file
    param: filetext, the text to PUT to the file
    param: filetype, the filetype
    return: res, the server response
    """
    def put_url(self,targetUrl,filetext,filetype):
        # create request headers
        headers={ 'content-type': filetype, 'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", self.dpopKey)}

        # PUT the new filetext
        # HO 25/09/2024 BEGIN *********
        res= requests.put(targetUrl,
            headers=headers,
            data=filetext
        )
        #res= requests.put(targetUrl,
            #headers=headers,
            #data=filetext,
            #timeout=5000
        #)
        # HO 25/09/2024 END *********
        
        # return server response
        return res 
    
    """
    Gets a file at a target URL.
    
    param: self
    param: targetURL, the target URL
    return: the response text
    """        
    def get_file(self,targetUrl):
        # create the DPOP authorization headers
        # passes: the auth token, and a string representing the encoded JSON Web Token
        headers={  'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "GET", self.dpopKey)}
        # get request headers
        # HO 25/09/2024 BEGIN ***********
        res= requests.get(targetUrl,
           headers=headers
        )
        #res= requests.get(targetUrl,
           #headers=headers,
           #timeout=5000
        #)
        # HO 25/09/2024 BEGIN ***********

        # return response text
        return res.text

    """
    Deletes a file.
    
    param: self
    param: targetURL, the URL of the file to delete
    return: res, the response to the delete request
    """
    def delete_file(self,targetUrl):
        # set up authorization headers
        headers={  'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "DELETE", self.dpopKey)}
        # delete the file
        # HO 25/09/2024 BEGIN ***********
        res= requests.delete(targetUrl,
                headers=headers
        )
        #res= requests.delete(targetUrl,
            #headers=headers,
            #timeout=5000
        #)
        # HO 25/09/2024 END ***********
        # return the response
        return res

    def adddefaultacl(self,fileaddress):
        targetUrl=fileaddress+'.acl'
        #print('Adding .acl to '+ fileaddress)
        acldef='''@prefix : <#>.
@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <profile/card#>.

:ControlReadWrite
a acl:Authorization;
acl:accessTo <'''+fileaddress+'''>;
acl:agent c:me;
acl:mode acl:Control, acl:Read, acl:Write.

:Read
a acl:Authorization;
acl:accessTo <'''+fileaddress+'''>;
acl:mode acl:Read.
'''
        #print(acldef)
        
        headers={ 'content-type': 'text/turtle', 'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", self.dpopKey)}
        res= requests.put(targetUrl,
               headers=headers,
                data=acldef
            )
        return res

    def addreadrights(self,fileaddress,webidlist):
        targetUrl=fileaddress+'.acl'
        headers={ "Content-Type": "application/sparql-update",'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PATCH", self.dpopKey)}
        webidstring='<'+'>,<'.join(webidlist)+'>'
        data="INSERT DATA { <#Read> <acl:agent> "+webidstring+" }"
        #print(data)
        res= requests.patch(targetUrl,
               headers=headers,
                data=data
            )
        #print(res,end='\r')
        #if res.ok:
            #print('Added '+webidstring+' to '+targetUrl,end='\r')

    """
    Makes a file accessible to the experiment through its .acl file.
    
    param: self
    param: podname, the pod where the file is located
    param: filename, the file to make accessible
    return: res, the server response
    """
    def makefileaccessible(self,podname,filename):
        # construct the target URL from the target file's .acl file path
        targetUrl=self.idp+podname+'/'+filename+'.acl'
        # get DPOP headers
        headers={  'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "GET", self.dpopKey)}
        
        # get the file's .acl
        # HO 25/09/2024 BEGIN *********
        res= requests.get(targetUrl,
           headers=headers
        )
        #res= requests.get(targetUrl,
           #headers=headers,
           #timeout=5000
        #)
        # HO 25/09/2024 END *********
        
        # if we couldn't get the .acl file
        if not res.ok:
            # generate the text of an .acl file granting c:me full access to the target file
            acldef='''@prefix : <#>.
@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <profile/card#>.

:ControlReadWrite
a acl:Authorization;
acl:accessTo <'''+filename+'''>;
acl:agent c:me;
acl:agentClass foaf:Agent;
acl:mode acl:Control, acl:Read, acl:Write.'''
            # create DPOP headers 
            headers={ 'content-type': 'text/turtle', 'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", self.dpopKey)}
            # update the target .acl file to grant c:me full access
            # HO 25/09/2024 BEGIN *********
            res= requests.put(targetUrl,
               headers=headers,
                data=acldef
            )
            #res= requests.put(targetUrl,
               #headers=headers,
               #data=acldef,
               #timeout=5000
            #)
            # HO 25/09/2024 END *********
        # if we did manage to get the .acl file
        else:
            # create the headers for a SPARQL update PATCH request
            headers={ "Content-Type": "application/sparql-update",'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PATCH", self.dpopKey)}
            # insert a triple giving full access to an Agent
            # HO 25/09/2024 BEGIN *********
            res= requests.patch(targetUrl,
               headers=headers,
                data="INSERT DATA { <#ControlReadWrite> <acl:agentClass> <foaf:Agent> }"
            )
            #res= requests.patch(targetUrl,
               #headers=headers,
               #data="INSERT DATA { <#ControlReadWrite> <acl:agentClass> <foaf:Agent> }",
               #timeout=5000
            #)
            # HO 25/09/2024 END *********
        # return the response
        return res

    def makeurlaccessible(self,url,filename):
        targetUrl=url+'.acl'
        
        acldef='''@prefix : <#>.
@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <profile/card#>.

:ControlReadWrite
a acl:Authorization;
acl:accessTo <'''+filename+'''>;
acl:agent c:me;
acl:agentClass foaf:Agent;
acl:mode acl:Control, acl:Read, acl:Write.'''
            ##print('no acl')
       #print(acldef)
        headers={ 'content-type': 'text/turtle', 'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", self.dpopKey)}
        res= requests.put(targetUrl,
               headers=headers,
                data=acldef
            )
        
        return res.text

    """
    Make a URL accessible to a list of WebIDs.
    
    param: self
    param: url, the URL to make accessible to the given WebIDs
    param: podaddress, the pod address where the URL is located
    param: webid, [TODO is this ever used?]
    param: webidlist, the list of WebIDs that have access to the file at the given URL
    param: openbool, default: False, flags if this file is open-access or not
    return: res, the server response
    """
    def makeurlaccessiblelist(self, url, podaddress,webid, webidlist,openbool=False):
        # get the URL of the target file's .acl file
        targetUrl=url+'.acl'
        
        # construct the text of an .acl file granting Read access
        # to the WebIDs in the WebID list (and making c:me the owner)
        acldef=returnacllist(url, podaddress, webidlist,openbool)
        # create auth headers for a PUT request
        headers={ 'content-type': 'text/turtle', 'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(targetUrl, "PUT", self.dpopKey)}
        # PUT the text granting access to the WebIDs to the given .acl file
        # HO 25/09/2024 BEGIN **********
        res= requests.put(targetUrl,
               headers=headers,
                data=acldef
            )
        #res= requests.put(targetUrl,
               #headers=headers,
               #data=acldef,
               #timeout=5000
            #)
        # HO 25/09/2024 BEGIN **********
        # return the server response
        return(res)

    def inserttriple(self,url,triple):
        data = self.get_file(url)
        print(data)
        g=Graph().parse(data=data,publicID=url)
        g.add(triple)
        datafixed=g.serialize()
        print(datafixed)
        res=self.put_url(url,datafixed,'text/turtle')
        return(res)

    """
    Inserts a triple string into a pod, using a PATCH request.
    
    param: self
    param: url, the target URL
    param: triplestring, a string representation of an RDF triple
    return: res, the query result
    """
    def inserttriplestring(self,url,triplestring):
        # create the headers for a SPARQL update
        headers={ "Content-Type": "application/sparql-update",'authorization':'DPoP '+self.authtoken, 'DPoP': dpop_utils.create_dpop_header(url, "PATCH", self.dpopKey)}
        # construct the SPARQL query
        data="INSERT DATA {" + triplestring+ "}"
        # do a PATCH request with the SPARQL query
        # HO 25/09/2024 BEGIN *********
        res= requests.patch(url,
               headers=headers,
                data=data
            )
        #res= requests.patch(url,
            #headers=headers,
            #data=data,
            #timeout=5000
        #)
        # HO 25/09/2024 END *********
        
        # return the result
        return res

"""
Gets a file at a given target URL.

param: targetUrl, the target URL
return: res, the server response
"""
def get_file(targetUrl):

    res= requests.get(targetUrl,
           #headers=headers
    )
    # return server response
    return res

""" 
Creates the pod.

param: IDP, the IDP
param: podname, name of the pod to create
param: email, the pod account email
param: password, the pod password
return: res1, response to the POST request
"""
def podcreate(IDP,podname,email,password):
    register_endpoint=IDP+'idp/register/'
    res1 = requests.post(
                        register_endpoint,
                        json={
                            "createWebId": "on",
                            "webId": "",
                            "register": "on",
                            "createPod": "on",
                            "podName": podname,
                            "email": email,
                            "password": password,
                            "confirmPassword": password
                        },
                        timeout=5000,
                    )
    return(res1)
    
"""
Return ACL text granting Read access to a given file for a list of WebIDs.

param: URL, the URL of the file to make accessible
param: podaddress, the pod address where the file is hosted
param: webidlist, the list of WebIDs that have Read access to the file
param: openbool, default: False, is True if the given resource is open access
return: acldef2, text for writing to an .acl file designating the WebIDs that have Read access to it
"""
def returnacllist(url, podaddress, webidlist,openbool=False):
    # format the list of WebIDs for writing
    webidstring='<'+'>,<'.join(webidlist)+'>'
    # initialize a string to say what type of Subject has access to this file
    openstring=''
    # if this is an open access file, grant Read access to all Agents
    if openbool: 
            openstring='acl:agentClass foaf:Agent;'
    
    # built text designating that the file at the given URL is Read accessible to
    # the given list of WebIDs (and giving c:me ownership of it).
    acldef2='''@prefix : <#>.
@prefix acl: <http://www.w3.org/ns/auth/acl#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix c: <'''+podaddress+'''profile/card#>.

:ControlReadWrite
a acl:Authorization;
acl:accessTo <'''+url+'''>;
acl:agent c:me;
acl:mode acl:Control, acl:Read, acl:Write.

:Read
a acl:Authorization;
acl:accessTo <'''+url+'''>;
acl:mode acl:Read;'''+openstring+'''
acl:agent '''+webidstring+'''.'''
    
    # return the .acl text string granting access to a file for a given list of WebIDs.
    return acldef2