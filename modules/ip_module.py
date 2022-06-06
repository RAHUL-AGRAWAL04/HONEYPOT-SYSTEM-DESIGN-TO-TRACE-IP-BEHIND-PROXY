import IP2Proxy


def check_ip(ip_addr:str):
    db = IP2Proxy.IP2Proxy()
    db.open("data/IP2PROXY-IP-PROXYTYPE-COUNTRY-REGION-CITY-ISP-DOMAIN-USAGETYPE-ASN-LASTSEEN-THREAT-RESIDENTIAL-PROVIDER.BIN")
    return {'ip': ip_addr, 'is_proxy': bool(db.is_proxy(ip_addr))}
    
#C:\Users\DELL\Desktop\PROJECT-8\PROJECT8\PROJECT8\data
def proxy_detail(ip_addr:str):
    db = IP2Proxy.IP2Proxy()
    db.open("data/IP2PROXY-IP-PROXYTYPE-COUNTRY-REGION-CITY-ISP-DOMAIN-USAGETYPE-ASN-LASTSEEN-THREAT-RESIDENTIAL-PROVIDER.BIN")
    
    #if not bool(db.is_proxy(ip_addr)): 
    #    return {'ip':ip_addr,'Error': 'IP is not a proxy IP'}
    
    result = {
    'ip' : ip_addr,
    'is_proxy' : bool(db.is_proxy(ip_addr)),
    'proxy_type' : db.get_proxy_type(ip_addr),
    'country' : db.get_country_long(ip_addr),
    'region' : db.get_region(ip_addr),
    'city' : db.get_city(ip_addr),
    'isp' : db.get_isp(ip_addr),
    'asn' : db.get_asn(ip_addr)
    }
    
    return result

