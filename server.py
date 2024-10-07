import os
import io
import zipfile
from flask import Flask, request, jsonify, send_file
from app import startapp  # Assicurati di importare correttamente la funzione
from flask_cors import CORS  # Importa CORS per consentire richieste cross-origin
from removeAllFile import remove_files_only_in_folders  # Importa la funzione di pulizia dei file

# Crea l'app Flask con la configurazione della cartella di output
app = Flask(__name__)
CORS(app)  # Consenti richieste da altre origini

@app.route('/swagger', methods=['POST'])
def swagger():
    # Rimuovi i file precedenti se presenti
    remove_files_only_in_folders()
    classes_dir = "java_classes"
    output_dir = "output_swagger_folder"  # Directory in cui verranno generati i file di output

    # Assicurati che le directory esistano
    os.makedirs(classes_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)  # Assicurati che la directory di output esista

    # Recupera i file dalla richiesta
    uploadedfiles = request.files.getlist('files')

    saved_files = []  # Lista per tenere traccia dei file salvati
    rejected_files = []  # Lista per tenere traccia dei file rifiutati

    # Salva solo i file .java
    for file in uploadedfiles:
        if file.filename.endswith('.java'):
            print(f"Ricevuto file: {file.filename}")
            file_path = os.path.join(classes_dir, file.filename)
            file.save(file_path)
            saved_files.append(file.filename)  # Aggiungi il file salvato alla lista
        else:
            rejected_files.append(file.filename)  # Aggiungi il file rifiutato alla lista
            print(f"File rifiutato (non .java): {file.filename}")

    # Se non sono stati salvati file .java, restituisci un messaggio di errore
    if not saved_files:
        return {
            "error": "Nessun file .java ricevuto.",
            "rejected_files": rejected_files
        }, 400  # 400 Bad Request

    # Esegui la funzione startapp() per generare i file Swagger
    try:
        startapp()  # Chiama la funzione per generare i file
        print("startapp eseguita con successo.")
    except Exception as e:
        return {
            "error": f"Errore nell'esecuzione di startapp: {str(e)}"
        }, 500  # 500 Internal Server Error

    # Verifica che ci siano file nella directory di output
    if not os.listdir(output_dir):
        print(f"Errore: la cartella {output_dir} è vuota.")
        return {
            "error": f"Nessun file generato nella cartella {output_dir}."
        }, 500  # 500 Internal Server Error

    # Crea lo zip della cartella di output al volo e invialo al client
    memory_file = io.BytesIO()  # Usa un buffer di memoria per creare lo zip
    try:
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Aggiungi ogni file della cartella di output
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"Aggiunta di {file_path} allo zip.")
                    zipf.write(file_path, os.path.relpath(file_path, output_dir))

            # Aggiungi la cartella java_classes_modified/mapping direttamente allo zip
            mapping_dir = "java_classes_modified/mapping"
            if os.path.exists(mapping_dir):
                # Aggiungi la cartella mapping e il suo contenuto al file zip
                for root, dirs, files in os.walk(mapping_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calcola il percorso relativo per mantenere la struttura delle cartelle
                        relative_path = os.path.relpath(file_path, start=mapping_dir)
                        zipf.write(file_path, os.path.join('mapping', relative_path))
                        print(f"Aggiunta di {file_path} allo zip sotto 'mapping/'.")

        print("File zip creato con successo.")
    except Exception as e:
        print(f"Errore durante la creazione dello zip: {str(e)}")
        return {
            "error": f"Errore durante la creazione dello zip: {str(e)}"
        }, 500  # 500 Internal Server Error

    # Imposta il puntatore del file di memoria all'inizio
    memory_file.seek(0)

    # Restituisci il file zip generato al client
    return send_file(
        memory_file,
        mimetype='application/zip',
        download_name='output_swagger_folder.zip',
        as_attachment=True
    )


def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_server()
