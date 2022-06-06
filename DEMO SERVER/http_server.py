from cgi import test
import http.server
import socketserver,json
import requests, datetime

PORT = 1000

Handler = http.server.SimpleHTTPRequestHandler
class MyHandler(Handler):
    def do_GET(self):
        ip,port = self.client_address
        ts = str(datetime.datetime.now())
        
        # content_len = int(self.headers.get('content-length', 0))
        # post_body = self.rfile.read(content_len)
        # test_data = json.loads(post_body)
        # print(test_data)
        # ,'action':test_data['action']
        data = {'ip':str(ip),'port':str(port),'timestamp':ts,'req_type':'GET'}
        response = requests.post('http://192.168.43.98:8000/save-server-log/', json = data)

        super().do_GET()

    def do_POST(self):
        ip,port = self.client_address
        ts = str(datetime.datetime.now())
        # content_len = int(self.headers.get('content-length', 0))
        # post_body = self.rfile.read(content_len)
        # test_data = json.loads(post_body)

        # print(test_data)
        # ,'action':test_data['action']
        data = {'ip':str(ip),'port':str(port),'timestamp':ts,'req_type':'POST'}
        print(data)
        response = requests.post('http://192.168.43.98:8000/save-server-log/', json = data)
       
        #super().do_POST()
        

with socketserver.TCPServer(("192.168.43.98", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    print(Handler.client_address)