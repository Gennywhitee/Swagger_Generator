from  IO_function import *
from  web_function import *
from  Swagger_gen import *
from  class_cleaner import *
from  dependecy_function import *

if __name__ == "__main__":
    url = "https://swagger.io/specification/"
    file_in = "./input/Entity_innestate_3.java"
    file_out = "./output/innestate_3_1.yml"
    # Viene estratto il contesto dalla pagina url
    context = extract_context_from_webpage(url)


    '''swagger_yaml = swagger_generator(file_in, context)  # Converte la classe Java in YAML
    if swagger_yaml:
        out_on_file(swagger_yaml, file_out)  # Scrive il YAML sul file di output'''
    

    swagger_generator_from_json("jsonDependecies/dependeciesTree.json", "java_classes", context, output_folder="output_swagger_folder")