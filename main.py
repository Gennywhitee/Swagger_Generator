from pathlib import Path
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import PromptTemplate 
from dotenv import load_dotenv 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from contextlib import redirect_stdout

from langchain.agents import tool



# Carica le variabili di ambiente da un file .env
load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)
# Modifica la funzione generate_pet_name per creare un oggetto StringPromptValue dal template prima di passarlo alla funzione invoke
def generate_pet_name(animal_type, pet_color):
    prompt = ChatPromptTemplate.from_template("Ho un {animal_type} e vorrei un nome per lui. Suggeriscimi cinque nomi da dargli se il suo colore è {pet_color}. Senza altri commenti.")
    output_parser = StrOutputParser()

    
    chain = prompt | model | output_parser

    response = chain.invoke({"animal_type" :animal_type, "pet_color":pet_color})

    return response

def generate_swagger(filename):
    text = text_from_file(filename)
    prompt = ChatPromptTemplate.from_template("Creami lo swagger della seguente classe in Java, seguendo lo standard OPENAI 3.0. Non scrivere altri commenti\n\n"+ text)
    output_parser = StrOutputParser()

    chain =  prompt | model | output_parser

    response = chain.invoke({})
    return response

def text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
            contenuto = f.read()
    return contenuto

def out_on_file(data,file_path):
    with open(file_path,'x') as f:
        with redirect_stdout(f):
            print(data)

if __name__ == "__main__":
    file_out = ".\\output\\file1.txt"
    file_in = ".\\input\\Biblioteca.java"
    print(text_from_file(file_in))
    out_on_file(generate_swagger(file_in),file_out)



