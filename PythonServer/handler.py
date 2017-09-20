"""
Serves files out of its current directory.
Doesn't handle POST requests.
"""
import SocketServer
import SimpleHTTPServer
import subprocess

PORT = 8080

def run_model1(par1,par2):
    """ sample model with 2 params"""

    model_params = [str(par1),str(par2)]
    path_to_script = "/media/luis/media/devongt/GrupoTRT/RModels/model1/run_model.R"
    execution_command = ["Rscript",path_to_script] + model_params
    prediction = subprocess.check_output(execution_command,universal_newlines = True)
    return '{body:{params:{param1:3,param2:2},prediction:'+str(prediction)+'}}'

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        #Sample values in self for URL: http://localhost:8080/jsxmlrpc-0.3/
        #self.path  '/jsxmlrpc-0.3/'
        #self.raw_requestline   'GET /jsxmlrpc-0.3/ HTTP/1.1rn'
        #self.client_address    ('127.0.0.1', 3727)
        if self.path=='/model1':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(run_model1(3,2)) #call sample function here
            return
        else:
            #serve files, and directory listings by following self.path from
            #current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

httpd = SocketServer.ThreadingTCPServer(('localhost', PORT),CustomHandler)

print "serving at port", PORT
httpd.serve_forever()
