from  IO_function import *
from  web_function import *
from  swagger_generator import *

if __name__ == "__main__":
    url_innested = "https://swagger.io/docs/specification/data-models/inheritance-and-polymorphism/"
    url_basic = "https://swagger.io/specification/"
    file_in = "./input/Entity_multiple.java"
    file_out = "./output/Multiple_1.yml"

    text = text_from_file(file_in)

    if check_nested_entities(text):
        url = url_innested  # URL della specifica con innesti
        context = extract_context_from_webpage(url)  # Estrae il contesto dalla specifica OpenAPI
        
    else:
        url = url_basic  # URL della specifica
        context = extract_context_from_webpage(url)


    swagger_yaml = swagger_generator(file_in, context)  # Converte la classe Java in YAML
    if swagger_yaml:
        out_on_file(swagger_yaml, file_out)  # Scrive il YAML sul file di output
