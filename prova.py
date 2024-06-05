import os
import requests
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser


# Funzione per ottenere il contenuto di una pagina web
def get_webpage_content(url):
    try:
        response = requests.get(url)  # Effettua una richiesta GET all'URL
        response.raise_for_status()   # Verifica che la richiesta abbia avuto successo
        return response.text          # Restituisce il contenuto della pagina web
    except requests.exceptions.RequestException as e:
        print(f"Errore durante il recupero dell'URL: {e}")  # Stampa un messaggio di errore in caso di eccezione
        return None

# Funzione per estrarre il contesto da una pagina web limitando il numero di token
def extract_context_from_webpage(url, max_tokens=3000):
    html_content = get_webpage_content(url)  # Ottiene il contenuto HTML della pagina
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')  # Parsing del contenuto HTML con BeautifulSoup
    text = soup.get_text(separator='\n')  # Estrae tutto il testo dalla pagina
    
    # Divide il testo in chunk di 2000 caratteri con sovrapposizione di 200 caratteri
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    document_chunks = text_splitter.split_text(text)
    
    # Limita il numero di chunk utilizzati per generare il contesto
    context_chunks = document_chunks[:max_tokens // 2000]
    
    # Combina i chunk selezionati in un unico stringa
    context = "\n".join(context_chunks)
    
    return context

# Funzione per leggere il contenuto di un file
def text_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()  # Restituisce il contenuto del file
    except FileNotFoundError:
        print(f"File non trovato: {filename}")  # Stampa un messaggio di errore se il file non è trovato
        return ""
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")  # Stampa un messaggio di errore in caso di altre eccezioni
        return ""

# Funzione per convertire una classe Java in un file Swagger YAML
def java_class_to_swagger_yaml(java_class_code, context):
    text = text_from_file(java_class_code)  # Legge il contenuto del file Java
    if not text:
        return ""
    
    # Inizializza il modello LLM con il modello specificato e la temperatura
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)
    
    # Divide il testo della classe Java in chunk
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    text_chunks = text_splitter.split_text(text)
    
    output_parser = StrOutputParser()
    yaml_parts = []

    # Invia un chunk alla volta al modello e raccoglie le risposte
    for chunk in text_chunks:
        prompt = ChatPromptTemplate.from_template(
            "Creami la documentazione swagger del seguente entity bean in Java: {text}, "
            "seguendo lo standard OPENAPI 3.0. Le regole dello standard le trovi qui: {context}. "
            "Non scrivere altri commenti."
        )
        
        chain =  prompt | llm | output_parser  # Crea la catena di trasformazione
        response = chain.invoke({"text": chunk, "context": context})  # Invoca il modello con il chunk corrente e il contesto
        yaml_parts.append(response)  # Aggiunge la risposta alla lista delle parti YAML
    
    # Combina le parti del YAML in un'unica stringa
    final_yaml = "\n".join(yaml_parts)
    return final_yaml

# Funzione per scrivere i dati su un file
def out_on_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)  # Scrive i dati sul file
    except Exception as e:
        print(f"Errore durante la scrittura del file: {e}")  # Stampa un messaggio di errore in caso di eccezione

# Esecuzione principale del programma
if __name__ == "__main__":
    url = "https://swagger.io/specification/"  # URL della specifica OpenAPI
    context = extract_context_from_webpage(url)  # Estrae il contesto dalla specifica OpenAPI

    file_in = "./input/User_feed.java"  # Percorso del file di input Java
    file_out = "./output/User_feed5.yml"  # Percorso del file di output YAML
    
    swagger_yaml = java_class_to_swagger_yaml(file_in, context)  # Converte la classe Java in YAML
    if swagger_yaml:
        out_on_file(swagger_yaml, file_out)  # Scrive il YAML sul file di output
