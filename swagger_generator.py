from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from IO_function import *
from web_function import *
from  YAML import *

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
            "Genera **esclusivamente** la documentazione Swagger seguendo lo standard OpenAPI 3.0 per il seguente entity bean in Java: {text}. "
            "Crea i metodi CRUD necessari, formattati correttamente in YAML, e non includere **nessun** testo che non faccia parte della documentazione Swagger. "
            "Non includere commenti, spiegazioni o descrizioni aggiuntive. "
            "La documentazione deve essere conforme alle regole dello standard che trovi qui: {context}. "
            "IMPORTANTE: L'output deve essere puramente YAML, senza altri contenuti extra."
        )
        else:
            prompt = ChatPromptTemplate.from_template(
            "Genera **esclusivamente** la documentazione Swagger seguendo lo standard OpenAPI 3.0 per il seguente entity bean in Java: {text}. "
            "Crea i metodi CRUD necessari, formattati correttamente in YAML, e non includere **nessun** testo che non faccia parte della documentazione Swagger. "
            "Non includere commenti, spiegazioni o descrizioni aggiuntive. "
            "La documentazione deve essere conforme alle regole dello standard che trovi qui: {context}. "
            "IMPORTANTE: L'output deve essere puramente YAML, senza altri contenuti extra.")
        
        chain =  prompt | llm | output_parser  # Crea la catena di trasformazione
        response = chain.invoke({"text": chunk, "context": context})  # Invoca il modello con il chunk corrente e il contesto
        yaml_parts.append(response)  # Aggiunge la risposta alla lista delle parti YAML
        
        # Estrai solo il blocco YAML
        validated_yaml = extract_yaml(response)
        if validated_yaml:
            yaml_parts.append(validated_yaml)
    
    final_yaml = "\n".join(yaml_parts)
    out_on_file(final_yaml, "swagger_output.yaml")
    
    return final_yaml


