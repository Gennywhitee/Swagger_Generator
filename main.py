from  IO_function import *
from  Swagger_gen import *
from  class_cleaner import *
from  dependecy_function import *
from  change_names import *

if __name__ == "__main__":

    input_directory = "java_classes"
    change_names_by_folder(input_directory) # Modifica delle variabili 

    clean_java_directory('java_classes_modified', 'output_dipendenze/final_output.java') # pulizia dei file nella directory

    input_file = "./output_dipendenze/final_output.java"
    getJSONDependecies(input_file) # Creazione dell'albero delle dipendenze in JSON

    # Esecuzione funzione principale
    swagger_generator_from_json("jsonDependecies/dependeciesTree.json", "java_classes_modified",output_folder="output_swagger_folder")