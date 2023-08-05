class QLibBase():
   
    version=''

    def  __init__(self,ver='0.0.1'):
        self.version = ver

    def doSay(self,message="Called from QLibBase"):
        return f"{message} @version={self.version}"

import urllib.request
import urllib.parse
import json

class QApi():
    def __init__(self,url):
        self.url=url

    
    def qhttp_request(self,url, query=None,method=None, headers={}, data=None):
    #Perform an HTTP request and return the associated response  
        url= self.url
        parts = (urllib.parse.urlparse(url))   
        print(f'got parts={parts}, type={type(parts)}')
        print(f'extract out got scheme={parts.scheme}, url={parts.netloc}')
        #if query:
        #    pass       
        #    parts['query'] = urllib.parse.urlencode(query) 
     
        url = parts.geturl()
        print(f'got url={url}')
    #url = urllib.parse.ParseResult(**parts).geturl()    
        r = urllib.request.Request(url=url, method=method,                             
                               headers=headers,                            
                               data=data) 
    
        with urllib.request.urlopen(r) as resp:        
            msg, resp = resp.info(), resp.read()   
        
    
        return msg, resp
