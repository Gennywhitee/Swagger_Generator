import os
from dotenv import load_dotenv 
from IO_function import *
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser


input_file = "./output_dipendenze/final_output.java"
# raw_dependecies è il file in java delle dipendenze restituito dalla funzione class_cleaner.py
raw_dependencies = text_from_file(input_file)

# Carichiamo il file env del progetto 
load_dotenv()

# Recupera la chiave API da una variabile d'ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

# Dato un file di dipendenze in Java, trasforma tutto in un dependecy tree in formato JSON
def getJSONDependecies(raw_dependecies):

   # Inizializza il modello LLM con il modello specificato e la "creatività"
   llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)

   #Viene impostato come deve essere l'output
   output_parser = StrOutputParser()

   #Creazione del prompt da dare alla AI generativa
   prompt = ChatPromptTemplate.from_template("Generate **exclusively** the dependency tree of the following java classes," +
                                             " in a JSON format, **without** adding any other type of comment or text that " + 
                                             "is not useful for the JSON file. Here are the followings java classes {text}."+
                                             " Change the names of class adding at the end the keyword Class, if it is not already there" +
                                             " and using camelCase format.")
   
   chain =  prompt | llm | output_parser

   #invocazione della chain appena creata
   dependecyJson = chain.invoke({"text":raw_dependencies})
   out_on_file(dependecyJson, "./jsonDependecies/dependeciesTree.json")

   return dependecyJson
    
