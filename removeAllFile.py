import os
import shutil

def remove_files_only_in_folders():
    paths_to_clean = [
        './output_swagger_folder',  # Cartella
        './output_dipendenze',      # Cartella
        './jsonDependecies',        # Cartella
        './java_classes_modified',   # Cartella
        './java_classes' 
    ]
    
    for folder_path in paths_to_clean:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):  # Controllo se è una cartella esistente
            # Rimuovi tutto il contenuto interno della cartella (file e sottocartelle)
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):  # Rimuove i file e i collegamenti simbolici
                    os.remove(item_path)
                    print(f"File rimosso: {item_path}")
                elif os.path.isdir(item_path):  # Rimuove ricorsivamente le sottocartelle
                    shutil.rmtree(item_path)
                    print(f"Cartella rimossa: {item_path}")
            print(f"Pulizia completata nella cartella: {folder_path}")
        else:
            print(f"Il path non esiste o non è una cartella: {folder_path}")

# Esegui la funzione