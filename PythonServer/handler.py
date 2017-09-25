"""
Serves R models through GET requests
- Structure: 1 folder  per R model
- Parent folder specified under env variable R_MODELS_BASE_DIRECTORY
- Maps request url to model folder, for example for request:
    http://<host>:<port>/RModels/model1 is mapped to folder 
    $R_MODELS_BASE_DIRECTORY/RModels/model1
- Every model directory  should have 2 files:
    run_model.R: contains the code to run the R model, last line should be cat(<result>)
    params.config:comma separated ordered list of how the r script expects the parameters 
"""
import SocketServer
import SimpleHTTPServer
import subprocess
from urlparse import urlparse,parse_qs
import csv
from os import environ

PORT = 8080
BASE_DIRECTORY = environ.get("R_MODELS_BASE_DIRECTORY")
R_EXECUTION_COMMAND = "Rscript"
R_SCRIPTS_FILE_NAME = "run_model.R"
R_PARAMETERS_FILE_NAME = "params.config"


def run_model(model_url,parameters_list):
    model_param_names = get_configuration_for_resource(model_url)
    model_param_values = list()
    
    for param in model_param_names:
        model_param_values.append(str(parameters_list[param]))
        
    path_to_script = BASE_DIRECTORY + model_url + "/"+R_SCRIPTS_FILE_NAME
    execution_command = [R_EXECUTION_COMMAND,path_to_script] + model_param_values
    
    prediction = subprocess.check_output(execution_command,universal_newlines = True)
    
    return prediction


def get_configuration_for_resource(model_url):
    
    config_file = BASE_DIRECTORY + model_url + "/" +R_PARAMETERS_FILE_NAME
    with open(config_file,'rt') as csv_file:
        parameters_reader = csv.reader(csv_file)
            
        return parameters_reader.next()
    
    
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    #TODO: add  excepcion and error handling (and return status depending on that)   
    def do_GET(self):
        
        request_url = self.path
        parameters_dictionary = parse_qs(urlparse(request_url).query)
        parameters_list = parameters_dictionary.values() #returns a list of lists
        min_size = min(map(len,parameters_list))
        
        predictions =  list()
        for i in range(min_size):
            parameters_dict = dict()
            prediction_dict = dict()
            
            for parameter in parameters_dictionary:
                parameters_dict[parameter] = parameters_dictionary[parameter][i]
                prediction_dict[parameter] = parameters_dictionary[parameter][i]
                
            response = run_model(urlparse(request_url).path,parameters_dict)
            prediction_dict["prediction"] = response
            predictions.append(prediction_dict)
            
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write({"predictions":predictions})
        

httpd = SocketServer.ThreadingTCPServer(('localhost', PORT),CustomHandler)

print "Serving at port", PORT
httpd.serve_forever()
