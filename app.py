from  IO_function import *
from  Swagger_gen import *
from  class_cleaner import *
from  dependecy_function import *
from  change_names import *
from removeAllFile import*
from rename_class import *

def startapp():

    rinomina_tutti_i_file_in_cartella('java_classes')

    input_directory = "java_classes"
    change_names_by_folder(input_directory) # Modifica delle variabili 
    print("\nPost change name")

    clean_java_directory('java_classes_modified', 'output_dipendenze/final_output.java') # pulizia dei file nella directory
    print("\nPost clean class")

    input_file = "./output_dipendenze/final_output.java"
    getJSONDependecies(input_file) # Creazione dell'albero delle dipendenze in JSON
    print("\nPost dependecy json")

    # Esecuzione funzione principale
    swagger_generator_from_json("jsonDependecies/dependeciesTree.json", "java_classes_modified",output_folder="output_swagger_folder")
    print("\nPost swagger gen")