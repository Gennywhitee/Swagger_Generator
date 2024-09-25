# Funzione per leggere il contenuto di un file
def text_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()  # Restituisce il contenuto del file
    except FileNotFoundError:
        print(f"File non trovato: {filename}")  # Stampa un messaggio di errore se il file non è trovato
        return ""
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        return ""
    
# Funzione per scrivere i dati su un file
def out_on_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)  # Scrive i dati sul file
    except Exception as e:
        print(f"Errore durante la scrittura del file: {e}")
