import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from  IO_function import *
from  swagger_generator import *

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
