from langchain_openai import ChatOpenAI 
from langchain_core.prompts import PromptTemplate 
from dotenv import load_dotenv 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Carica le variabili di ambiente da un file .env
load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)

def generate_swagger(filename):
    text = text_from_file(filename)
    prompt = ChatPromptTemplate.from_template("Creami la documentazione dello Swagger, con annesse le operazioni CRUD in maniera tale che possano essere richiamate come API RESTfull, della seguente classe Entity: {text}.\n Segui sempre lo standard OPENAI 3.0 per la creazione di Swagger. Non scrivere altri commenti.")
    output_parser = StrOutputParser()

    chain =  prompt | model | output_parser

    response = chain.invoke({"text" :text})
    return response

def text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
            contenuto = f.read()
    return contenuto

def out_on_file(data, file_path):
    with open(file_path, 'w') as f:
        f.write(data)

if __name__ == "__main__":
    file_out = ".\\output\\User_feed2.yml"
    file_in = ".\\input\\User_feed.java"
    out_on_file(generate_swagger(file_in),file_out)



