from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from IO_function import *
from web_function import *

def check_nested_entities(java_code):
    # Analizza il codice Java per determinare la presenza di entity innestate
    nested_entities = False
    
    if "OneToOne" in java_code or "JoinColumn" in java_code:
        nested_entities = True
    
    return nested_entities

# Funzione per convertire una classe Java in un file Swagger YAML
def swagger_generator(java_class_code, context):
    text = text_from_file(java_class_code)  # Legge il contenuto del file Java
    if not text:
        print("La classe Java è vuota\n")
        return ""
    
    # Inizializza il modello LLM con il modello specificato e la "creatività"
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)
    
    # Divide il testo della classe Java in chunk
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    text_chunks = text_splitter.split_text(text)
    
    output_parser = StrOutputParser()
    yaml_parts = []

    # Invia un chunk alla volta al modello e raccoglie le risposte
    for chunk in text_chunks:
        if check_nested_entities(text):
            prompt = ChatPromptTemplate.from_template(
            "Creami la documentazione swagger dei seguenti entity bean in Java: {text},compresi tutti i metodi CRUD "
            "seguendo lo standard OPENAPI 3.0. Le regole dello standard le trovi qui: {context}. "
            "IMPORTANTE Non scrivere altri commenti."
        )
        else:
            prompt = ChatPromptTemplate.from_template(
            "Creami la documentazione swagger del seguente entity bean in Java: {text},compresi tutti i metodi CRUD "
            "seguendo lo standard OPENAPI 3.0. Le regole dello standard le trovi qui: {context}. "
            "IMPORTANTE Non scrivere altri commenti al di fuori della documentazione."
        )
        
        chain =  prompt | llm | output_parser  # Crea la catena di trasformazione
        response = chain.invoke({"text": chunk, "context": context})  # Invoca il modello con il chunk corrente e il contesto
        yaml_parts.append(response)  # Aggiunge la risposta alla lista delle parti YAML
    
    # Combina le parti del YAML in un'unica stringa
    final_yaml = "\n".join(yaml_parts)
    return final_yaml


