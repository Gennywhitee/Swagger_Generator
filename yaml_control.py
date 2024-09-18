import re
import yaml

# Estrae solo il contenuto YAML dall'output rimuovendo commenti o testo non desiderato.
def extract_yaml(content):

    try:
        # Usa una regex per identificare blocchi YAML validi
        yaml_pattern = r"(openapi:.*?)(?=\n[a-zA-Z]|$)"  # Cerca un blocco che inizia con 'openapi:'
        matches = re.findall(yaml_pattern, content, re.DOTALL)

        if matches:
            # Combina tutti i blocchi YAML trovati
            yaml_text = "\n".join(matches)
            yaml.safe_load(yaml_text)  # Valida il YAML
            return yaml_text
        else:
            return ""
    except yaml.YAMLError as e:
        print(f"Errore nel parsing YAML: {e}")
        return ""
