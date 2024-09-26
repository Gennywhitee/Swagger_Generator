from  IO_function import *
from  Swagger_gen import *
from  class_cleaner import *
from  dependecy_function import *

if __name__ == "__main__":


    '''swagger_yaml = swagger_generator(file_in, context)  # Converte la classe Java in YAML
    if swagger_yaml:
        out_on_file(swagger_yaml, file_out)  # Scrive il YAML sul file di output'''
    

    swagger_generator_from_json("jsonDependecies/dependeciesTree.json", "java_classes",output_folder="output_swagger_folder")