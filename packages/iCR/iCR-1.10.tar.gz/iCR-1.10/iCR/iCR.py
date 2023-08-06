''' 
Version 1.10 13th October 2018
Pete White
This is a Python module to simplify operations via F5 iControl REST interface
Installation - copy to your python library directory eg /lib/python2.7

https://devcentral.f5.com/codeshare/icr-python-module-for-icontrol-rest-1008

Example:
#!/usr/bin/env python
from iCR import iCR
# Connect to BIG-IP
bigip = iCR("172.24.9.132","admin","admin")
#Retrieve a list of Virtual Servers
virts = bigip.get("ltm/virtual")
for vs in virts['items']:
   print vs['name']


'''
###############################################################################
import os
import sys
import json
import requests
import hashlib
import base64
import time
# Disable warnings about insecure
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class iCR:
   
   def __init__(self,hostname,username,password,**kwargs):
     # Setup variables
     self.icr_session = ""
     self.raw = ""
     self.code = ""
     self.folder = ""
     self.icr_link = ""
     self.headers = ""
     self.timeout = 30
     self.hostname = hostname
     self.username = username
     self.password = password
     self.port = 443
     self.debug = False
     
     # manage keyword arguments
     self.timeout = kwargs.pop('timeout', 30)
     self.port = kwargs.pop('port', 443)
     self.icontrol_version = kwargs.pop('icontrol_version', '')
     self.folder = kwargs.pop('folder', '')
     self.token = kwargs.pop('token', False)
     self.debug = kwargs.pop('debug', False)
     # Create HTTP session
     icr_session = requests.session()
     # not going to validate the HTTPS certifcation of the iControl REST service
     icr_session.verify = False
     # Create session
     self.icr_session = icr_session
     self.icr_url = 'https://%s/mgmt/tm/' % hostname
     # Set auth
     self._set_auth()
   
   # Set the authentication type to be either token or username/password
   def _set_auth(self):
     if self.token:
        self.icr_session.headers.update({'X-F5-Auth-Token': self.token, 'Authorization': None, 'Content-Type': 'application/json'})
        self.icr_session.auth = None
        if self.debug:
           print ("DEBUG: Using token:" + str(self.token))
     else:
        self.icr_session.auth = (self.username, self.password)
        self.icr_session.headers.update({'Content-Type': 'application/json'})
        if self.debug:
           print ( "DEBUG: Using username and password" )
        
   # Retrieve objects - use GET method
   def get(self,url,**kwargs):
     # Deal with keywords
     select = kwargs.pop('select', '')
     top = kwargs.pop('top', '')
     skip = kwargs.pop('skip', '')
     # Deal with URI and select, top, etc
     if "?" not in url:
       url_delimeter = "?"
     else:
       url_delimeter = "&"
     
     if select:
       url = url + url_delimeter + "$select=" + str(select)
       url_delimeter = "&"
     if top:
       url = url + url_delimeter + "$top=" + str(top)
       url_delimeter = "&"
     if skip:
       url = url + url_delimeter + "$skip=" + str(skip)
       url_delimeter = "&"
     if self.folder:
         url = url + url_delimeter +"$filter=partition+eq+" + self.folder
         url_delimeter = "&"      
     if self.icontrol_version:
         url = url + url_delimeter + 'ver=' + self.icontrol_version
         url_delimeter = "&"
     
     request_url = self.icr_url + url
     if self.debug:
        print ("DEBUG: GET URL:" + request_url)
        print  ("DEBUG: headers:" + str(self.icr_session.headers))
     self._set_auth()
     try:
        response = self.icr_session.get(request_url,timeout = self.timeout)
     except Exception as e:
        self.error = e
        if self.debug:
           print ( "DEBUG: Get requests error:" + str(self.error) )
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
        print ( "DEBUG: Get Response Status Code:" + str(self.code) )
        print ( "DEBUG: GET response headers:" + str(response.headers) )
     self.headers = response.headers
     if response.status_code < 400:
       return json.loads(response.text)
     else:
       return False
   
   # Retrieve large objects - use GET method and top/skip
   def getlarge(self,url,size,**kwargs):
     selectValue = kwargs.pop('select', '')
     sleepValue = kwargs.pop('sleep',0.1)
     returnValue = {}
     if self.debug:
       print ( "DEBUG: getlarge select:" + selectValue  )
     skipValue = 0
     while True:
       if not selectValue == '':
         resp = self.get(url,top=size,skip=skipValue,select=selectValue)
       else:
         resp = self.get(url,top=size,skip=skipValue)
       # Check that the response hasn't failed
       if resp:
         if 'items' in resp:
         # There is a list of items - used for list of objects
         # Have to individually add to items otherwise they are overwritten by update()
           for item in resp['items']:
             if 'items' in returnValue:
               returnValue['items'].append(item)
             else:
               returnValue['items'] = [item]
         elif 'entries' in resp:
           # There is a list of entries - used for stats
           for entry in resp['entries']:
             if not 'entries' in returnValue:
               returnValue['entries'] = {}
             returnValue['entries'][entry] = resp['entries'][entry]    
         else:
           # No 'items' field - could be a specific object
           returnValue.update(resp)
         if 'selflink' in resp:
           returnValue['selflink'] = resp['selflink']
         if 'kind' in resp:
           returnValue['kind'] = resp['kind']
         
       else:
           # resp failed
           return False
           
       # Increment the skipValue to grab the next block
       skipValue += size
       # Stop when there is no nextLink
       if not 'nextLink' in resp.keys():
         break
       # Sleep for a while to reduce load on BIG-IP
       time.sleep(sleepValue)
     return returnValue
     
   # Create objects - use POST and send data
   def create(self,url,data):
     if self.icontrol_version:
       request_url = self.icr_url + url + '?ver=' + self.icontrol_version
     else:
       request_url = self.icr_url + url
     json_data = json.dumps(data) 
     if self.debug:
        print ( "DEBUG: Create URL:" + request_url )
        print ( "DEBUG: Create Data:" + str(data) )
        print ( "DEBUG: Create JSON Data:" + str(json_data) )
     self._set_auth()
     try:
        response = self.icr_session.post(request_url,json_data,timeout = self.timeout)
     except Exception as e:
        self.error = e
        if self.debug:
           print ( "DEBUG: Create requests error:" + str(self.error) )
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
        print ( "DEBUG: Create Response Status Code:" + str(self.code) )
        print ( "DEBUG: GET response headers:" + str(response.headers) )
     self.headers = response.headers
     if response.status_code < 400:
       return json.loads(response.text)
     else:
       return False

   # Modify existing objects - use PUT and send data
   def modify(self,url,data,**kwargs):
     # Deal with keywords
     patch = kwargs.pop('patch', '')
     
     if self.icontrol_version:
       request_url = self.icr_url + url + '?ver=' + self.icontrol_version
     else:
       request_url = self.icr_url + url
     json_data = json.dumps(data)   
       
     if self.debug:
        print ( "DEBUG: Modify URL:" + request_url )
        print ( "DEBUG: Modify Data:" + str(data) )
        print ( "DEBUG: Modify JSON Data:" + str(json_data) )
     self._set_auth()
     try:
        if patch:
           response = self.icr_session.patch(request_url,json_data,timeout = self.timeout)
        else:
           response = self.icr_session.put(request_url,json_data,timeout = self.timeout)
     except Exception as e:
        self.error = e
        if self.debug:
           print ( "DEBUG: Modify requests error:" + str(self.error) )
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
        print ( "DEBUG: Modify Response Status Code:" + str(self.code) )
        print ( "DEBUG: GET response headers:" + str(response.headers) )
     self.headers = response.headers
     if response.status_code < 400:
       return json.loads(response.text)
     else:
       return False
	   
   # Delete existing objects - use PUT and send data
   def delete(self,url):
     if self.icontrol_version:
       request_url = self.icr_url + url + '?ver=' + self.icontrol_version
     else:
       request_url = self.icr_url + url
     if self.debug:
        print ( "DEBUG: Delete URL:" + request_url )
     self._set_auth()
     try:
        response = self.icr_session.delete(request_url,timeout = self.timeout)
     except Exception as e:
        self.error = e
        if self.debug:
           print ( "DEBUG: Delete requests error:" + str(self.error) )
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
        print ( "DEBUG: Delete Response Status Code:" + str(self.code) )
        print ( "DEBUG: GET response headers:" + str(response.headers) )
     self.headers = response.headers
     if response.status_code < 400:
       return True
     else:
       return False



    # File upload and download       
    # Borrowed from https://devcentral.f5.com/articles/demystifying-icontrol-rest-part-5-transferring-files
    # Works on TMOS >12.0, prior to that, create directory /var/config/rest/downloads/tmp
    # Files uploaded to /var/config/rest/downloads
    # return is boolean True or False
   def upload(self,fp):
     # Have to use requests directly because of the URL and the fact that data is not JSON-formatted   
     chunk_size = 512 * 1024
     headers = {
            'Content-Type': 'application/octet-stream'
     }
     # Open file and retrieve details
     try:
       fileobj = open(fp, 'rb')
     except IOError:
       print ( "File ",fp," opening failed" )
       self.error = "File ",fp," opening failed"
       return False
     filename = os.path.basename(fp)
     size = os.path.getsize(fp)
      
     if os.path.splitext(filename)[-1] == '.iso':
       url = 'https://%s/mgmt/cm/autodeploy/software-image-uploads/%s' % (self.hostname,filename)
     else:
       url = 'https://%s/mgmt/shared/file-transfer/uploads/%s' % (self.hostname,filename)
     
     if self.icontrol_version:
       request_url = url + '?ver=' + self.icontrol_version
     else:
       request_url = url
     if self.debug:
       print ( "DEBUG: Upload URL:" + request_url )
     
     start = 0
     while True:
       file_slice = fileobj.read(chunk_size)
       if not file_slice:
         break
       current_bytes = len(file_slice)
       if current_bytes < chunk_size:
         end = size
       else:
         end = start + current_bytes
     
       headers['Content-Range'] = "%s-%s/%s" % (start, end - 1, size)
       self._set_auth()
       try:
         response = self.icr_session.post(request_url,data=file_slice,headers=headers,timeout = self.timeout)
       except Exception as e:
         self.error = e
         if self.debug:
           print ( "DEBUG: Upload requests error:" + str(self.error) )
         return False
       self.raw = response.text
       self.code = response.status_code
       if self.debug:
         print ( "DEBUG: Upload Response Status Code:" + str(self.code) )
       self.headers = response.headers
       
       start += current_bytes
     return True    
       
       
   # File download
   def download(self,fp):
     # fp is a file located in /shared/images
     # return is boolean True or False
     # Have to use requests directly because of the URL and the fact that data is not JSON-formatted
     chunk_size = 512 * 1024
     headers = {
        'Content-Type': 'application/octet-stream'
     }
     filename = os.path.basename(fp)
     url = 'https://%s/mgmt/cm/autodeploy/software-image-downloads/%s' % (self.hostname, filename)
     if self.icontrol_version:
       request_url = url + '?ver=' + self.icontrol_version
     else:
       request_url = url
     if self.debug:
       print ( "DEBUG: Download URL:" + request_url )
     self._set_auth()
     with open(fp, 'wb') as f:
       start = 0
       end = chunk_size - 1
       size = 0
       current_bytes = 0

       while True:              
            headers['Content-Range'] = "%s-%s/%s" % (start, end, size)
            try:
              response = self.icr_session.get(request_url,headers=headers,stream=True,timeout = self.timeout)
            except Exception as e:
              self.error = e
              if self.debug:
                print ( "DEBUG: Upload requests error:" + str(self.error) )
              return False
 
            if response.status_code == 200:
                # If the size is zero, then this is the first time through the
                # loop and we don't want to write data because we haven't yet
                # figured out the total size of the file.
                if size > 0:
                    current_bytes += chunk_size
                    for chunk in response.iter_content(chunk_size):
                        f.write(chunk)
                # Once we've downloaded the entire file, we can break out of the loop
                if end == size:
                    break
            crange = response.headers['Content-Range']
 
            # Determine the total number of bytes to read
            if size == 0:
              size = int(crange.split('/')[-1]) - 1
              if self.debug:
                print ( "DEBUG: File size is " + str(size) + " Bytes" )
 
              # If the file is smaller than the chunk size, BIG-IP will
              # return an HTTP 400. So adjust the chunk_size down to the
              # total file size...
              if chunk_size > size:
                end = size
              # ...and pass on the rest of the code
              continue
 
            start += chunk_size
            if self.debug:
              sys.stdout.write(".")
              sys.stdout.flush()
            if (current_bytes + chunk_size) > size:
              end = size
            else:
              end = start + chunk_size - 1
     return True
     
   def create_cert(self,files):
    # This is a method to create SSL certs from local files
    # files is an array containing the cert and key paths
    # returns cert name or false
    f1 = os.path.basename(files[0])
    f2 = os.path.basename(files[1])
    if f1.endswith('.crt'):
      certfilename = f1
      keyfilename = f2
    else:
      keyfilename = f1
      certfilename = f2
    # certname is the name of the certificates and will become the object name  
    certname = f1.split('.')[0]
    # Upload the files to the device
    try:
      if not self.upload(files[0]):
        if self.debug:
          print ( "DEBUG: upload failed:" + str(self.error) )
        return False
      if not self.upload(files[1]):
        if self.debug:
          print ( "DEBUG: upload failed:" + str(self.error) )
        return False
    except Exception as e:
      self.error = e
      if self.debug:
        print ( "DEBUG: Uploading cert/key error:" + str(self.error) )
      return False
    if self.debug:
        print ( "DEBUG: Cert & key uploaded" )
    self._set_auth()
    
    payload = {}
    payload['command'] = 'install'
    if self.folder:
      payload['name'] = "/" + self.folder + "/" + certname
    else:
      payload['name'] = certname
    #
    payload['from-local-file'] = '/var/config/rest/downloads/%s' % certfilename
    response = self.create('sys/crypto/cert',payload)
    if self.debug:
      print ( "DEBUG: create cert response:" + str(response.status_code) )
    if not response.status_code == 200:
      self.error = str(response.text)
      return False
    if self.debug:
        print ( "DEBUG: response code " + str(response.status_code) )
        print ( "DEBUG: Cert " + certname + " created" )
   
    # Create key
    
    if self.debug:
      print ( "DEBUG: Create key URL:" + request_url )
    payload['from-local-file'] = '/var/config/rest/downloads/%s' % keyfilename
    response = self.create('sys/crypto/key',payload)
    if self.debug:
      print ( "DEBUG: create key response:" + str(response.status_code) )
    if not response.status_code == 200:
      self.error = str(response.text)
      return False
    if self.debug:
        print ( "DEBUG: Key " + certname + " created" )
        
    return payload['name']
    
   # create SSL profile
   def create_ssl_profile(self,name,certname,keyname):
      # returns profile name or false
      payload = {}
      if self.folder:
        payload['name'] = "/" + self.folder + "/" + name
      else:
        payload['name'] = name
      payload['cert'] = certname
      payload['key'] = keyname
      
      response = self.create('ltm/profile/client-ssl',payload)
      if self.debug:
        print ( "DEBUG: create SSL Profile response:" + str(response.status_code) )
      if not response.status_code == 200:
        self.error = str(response.text)
        return False
      if self.debug:
        print ( "DEBUG: SSL profile " + name + " created" )
      return True
   
   # Method to retrieve an ASM ID from a given name
   # returns a list of IDs or false
   # Only returns the first match, does not work with multiples
   def get_asm_id(self,name):
     policies = self.get("asm/policies",select="name,id")
     matches = 0
     id = []
     for item in policies['items']:
       if item['name'] == name:
         matches += 1
         id.append(item['id'])
         if self.debug:
           print ( "Found policy " + name + " as ID " +item['id'] )
     if matches > 0:    
       return id
     else:
       return False

   # Change a name into a hash such as is used by ASM
   # Note that this should include the partition eg /Common/testpolicy
   def create_hash(self,name):
       algo = hashlib.md5() 
       algo.update(name)
       digest = base64.b64encode(algo.digest(),'-_').replace('=','')
       if self.debug:
           print ( "DEBUG: create_hash: String:" + name + ", Digest:" + digest )
       return digest
       
   # Retrieve a token   
   def get_token(self):
     # Have to use the requests session here because of the changed URL ie /mgmt/shared, not /mgmt/tm
     request_url = 'https://%s/mgmt/shared/authn/login' % (self.hostname)
     payload = {}
     payload['username'] = self.username
     payload['password'] = self.password
     payload['loginProviderName'] = "tmos"
     if self.debug:
           print ( "DEBUG: Current token:" + str(self.token) )
     try:
        response = self.icr_session.post(request_url,data = json.dumps(payload), timeout = self.timeout)
        if response.status_code > 200:
          if self.debug:
            print ( "DEBUG: token retrieval error:" + str(response.text) )
          return False
     except Exception as e:
        self.error = e
        if self.debug:
           print ( "DEBUG: token retrieval error:" + str(self.error) )
        return False
     token = json.loads(response.text)['token']['token']
     if self.debug:
           print ( "DEBUG: Token:" + token )
     self.raw = response.text
     self.code = response.status_code
     self.token = token
     self._set_auth()
     return token
     
   # Delete a token    
   def delete_token(self):
     if not self.token:
       self.error = "No token set to be able to delete"
       return False
     request_url = 'https://%s/mgmt/shared/authz/tokens/%s' % (self.hostname,self.token)
     if self.debug:
            print ( "DEBUG: Deleting token " + self.token    )
     try:
        response = self.icr_session.delete(request_url,timeout = self.timeout)
        if response.status_code > 200:
          if self.debug:
            print ( "DEBUG: token retrieval error:" + str(response.text) )
          return False
     except Exception as e:
        self.error = e
        if self.debug:
           print ( "DEBUG: token retrieval error:" + str(self.error) )
        return False
     self.raw = response.text
     self.code = response.status_code
     self.token = None
     self._set_auth()
     return True    
     
     
