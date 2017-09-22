"""
Serves files out of its current directory.
Doesn't handle POST requests.
"""
import SocketServer
import SimpleHTTPServer
import subprocess
from urlparse import urlparse,parse_qs
import csv

PORT = 8080
BASE_DIRECTORY = "/media/luis/media/devongt/GrupoTRT"
R_EXECUTION_COMMAND = "Rscript"
R_SCRIPTS_FILE_NAME = "run_model.R"
R_PARAMETERS_FILE_NAME = "params.config"

def run_model1(par1,par2):
    """ sample model with 2 params"""

    model_params = [str(par1),str(par2)]
    path_to_script = BASE_DIRECTORY + "/RModels/model1" + "/"+R_SCRIPTS_FILE_NAME
    execution_command = [R_EXECUTION_COMMAND,path_to_script] + model_params
    prediction = subprocess.check_output(execution_command,universal_newlines = True)
    return '{body:{params:{param1:3,param2:2},prediction:'+str(prediction)+'}}'

def run_model2(model_url,parameters_list):
    model_param_names = get_configuration_for_resource(model_url)
    model_param_values = list()
    
    for param in model_param_names:
        model_param_values.append(str(parameters_list[param]))
        
    path_to_script = BASE_DIRECTORY + model_url + "/"+R_SCRIPTS_FILE_NAME
    execution_command = [R_EXECUTION_COMMAND,path_to_script] + model_param_values
    
    prediction = subprocess.check_output(execution_command,universal_newlines = True)
    
    return '{body:{params:{param1:3,param2:2},prediction:'+str(prediction)+'}}'


def get_configuration_for_resource(model_url):
    
    config_file = BASE_DIRECTORY + model_url + "/" +R_PARAMETERS_FILE_NAME
    with open(config_file,'rt') as csv_file:
        parameters_reader = csv.reader(csv_file)
            
        return parameters_reader.next()
    
    
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        request_url = self.path
        parameters_dictionary = parse_qs(urlparse(request_url).query)
        parameters_list = parameters_dictionary.values() #returns a list of lists
        min_size = min(map(len,parameters_list))
        
        for i in range(min_size):
            parameters_dict = dict()
            
            for parameter in parameters_dictionary:
                parameters_dict[parameter] = parameters_dictionary[parameter][i]
                
            response = run_model2(urlparse(request_url).path,parameters_dict)
            self.wfile.write(response+";;;;")
        
        #self.wfile.write(parameters_list)
        #response = run_model2(urlparse(request_url).path,parameters_list)
        #self.wfile.write(response)
        #Sample values in self for URL: http://localhost:8080/jsxmlrpc-0.3/
        #self.path  '/jsxmlrpc-0.3/'
        #self.raw_requestline   'GET /jsxmlrpc-0.3/ HTTP/1.1rn'
        #self.client_address    ('127.0.0.1', 3727)
        

httpd = SocketServer.ThreadingTCPServer(('localhost', PORT),CustomHandler)

print "serving at port", PORT
httpd.serve_forever()
