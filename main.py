from  IO_function import *
from  Swagger_gen import *
from  class_cleaner import *
from  dependecy_function import *

if __name__ == "__main__":

    input_file = "./output_dipendenze/final_output.java"
    # raw_dependecies è il file in java delle dipendenze restituito dalla funzione class_cleaner.py
    raw_dependencies = text_from_file(input_file)
    
    process_java_directory('java_classes', 'output_dipendenze/final_output.java')
    getJSONDependecies(raw_dependencies)
    swagger_generator_from_json("jsonDependecies/dependeciesTree.json", "java_classes",output_folder="output_swagger_folder")