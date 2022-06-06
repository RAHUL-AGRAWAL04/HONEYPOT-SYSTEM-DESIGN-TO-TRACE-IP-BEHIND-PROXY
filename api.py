from fastapi import FastAPI
from modules import ip_module as im
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/detect-proxy/{ip_addr}")
async def check_ip(ip_addr:str):
    return im.check_ip(ip_addr)
    
@app.get("/proxy-details/{ip_addr}")
async def get_proxy_details(ip_addr:str):
    return im.proxy_detail(ip_addr)
    
@app.get('/ip-details/{ip_addr}')
async def get_ip_detail(ip_addr:str):
    #if (im.check_ip(ip_addr))['is_proxy'] : return {'Error':'not an actual IP'}
    
    from requests import get
    import json
    url = 'http://ip-api.com/json/{}'.format(ip_addr)
    response = get(url)
    response = json.loads(response.text)
    
    result = {
    'ip' : ip_addr,
    'country': response['country'],
    'region' : response['regionName'],
    'city' : response['city'],
    'zip_code': response['zip'],
    'latitude': response['lat'],
    'longitude': response['lon'],
    'isp': response['isp'],
    'organization' : response['org'],
    'asn': (response['as'].split())[0]
    }
    return result


#for honeypot logging

class Item(BaseModel):
    ip:str
    mac:str
    timestamp:str
    pid_dict = list = []

@app.post('/triggered/')
async def triggered(item:Item):
    tempd = {"IP":item.ip,"MAC":item.mac,'pid_dict':item.pid_dict}
    print(tempd)
    with open('temp/honeypot_log.json','r') as f:
        data = json.load(f)
        print(data)
    
    data[item.timestamp] = tempd
    with open('temp/honeypot_log.json','w') as f:
        json.dump(data,f,indent = 4)

    return 

@app.get('/get-honeypot-log/')
async def honeypot_log():
    with open('temp/honeypot_log.json','r') as f:
        data = json.load(f)
    return data

#honeypot_log complete


#For server Logging
class server_log(BaseModel):
    timestamp : str
    ip : str
    port : int
    req_type : str


@app.post('/save-server-log/')
async def save_server_log(item:server_log):
    tempd = {"IP":item.ip,"PORT":item.port,'REQUEST':item.req_type}
    with open('temp/server_log.json','r') as f:
        data = json.load(f)
        #print(data)
    
    data[item.timestamp] = tempd
    with open('temp/server_log.json','w') as f:
        json.dump(data,f,indent = 4)

    return 

@app.get('/get-server-log/')
async def get_server_log():
    with open('temp/server_log.json','r') as f:
        data = json.load(f)
    return data

class cred(BaseModel):
    uname:str
    passwd:str

@app.post('/validate/')
async def validate(item:cred):
    with open('temp/cred.json','r') as f:
        cred = json.load(f)
    print(item)
    if cred[item.uname] == item.passwd:
        return {'valid':True}
    else:
        return {'valid':False}


@app.post('/admin/add/')
async def add_user(item:cred):
    with open('temp/cred.json','r') as f:
        cred = json.load(f)
    cred[item.uname] = item.passwd
    with open('temp/cred.json','w') as f:
        json.dump(cred,f,indent=4)

class user(BaseModel):
    uname = str
@app.post('/admin/remove/')
async def remove_user(item:user):
    if item.uname=='admin':
        return {'error':'cannot perform operation'}
    else:
        with open('temp/cred.json','r') as f:
            cred = json.load(f)
        del cred.uname
        with open('temp/cred.json','w') as f:
            json.dump(cred,f,indent=4)
