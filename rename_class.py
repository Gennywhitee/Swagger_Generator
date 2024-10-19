import os
from IO_function import *

# Funzione per rinominare i file in base al nome della classe
def rinomina_file_per_classe(percorso_file):
    # Usa la funzione text_from_file per ottenere il contenuto del file
    contenuto = text_from_file(percorso_file)
    
    # Dividi il contenuto in righe
    righe = contenuto.splitlines()

    # Trova la riga che contiene "public class"
    for riga in righe:
        if "public class" in riga:
            # Estrai il nome della classe dalla riga
            parole = riga.split()
            indice_class = parole.index("class")
            nome_classe = parole[indice_class + 1]
            
            # Aggiungi "Class" al nome della classe
            nuovo_nome = nome_classe + "Class.java"
            
            # Prendi la directory e rinomina il file
            directory, nome_vecchio_file = os.path.split(percorso_file)
            nuovo_percorso_file = os.path.join(directory, nuovo_nome)
            
            # Rinomina il file se non ha già il nome corretto
            if nome_vecchio_file != nuovo_nome:
                os.rename(percorso_file, nuovo_percorso_file)
                print(f"File rinominato: {nome_vecchio_file} -> {nuovo_nome}")
            else:
                print(f"Il file {nome_vecchio_file} è già corretto.")
            return
    
    print(f"Nessuna classe trovata in {percorso_file}.")

# Funzione per scansionare e rinominare tutti i file Java nella cartella
def rinomina_tutti_i_file_in_cartella(percorso_cartella):
    # Scansiona tutti i file nella cartella
    for file_name in os.listdir(percorso_cartella):
        if file_name.endswith(".java"):  # Considera solo i file con estensione .java
            percorso_file = os.path.join(percorso_cartella, file_name)
            rinomina_file_per_classe(percorso_file)



