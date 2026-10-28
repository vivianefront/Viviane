import sys
import os
import requests
from colorama import init, Fore, Style

init(autoreset=True)

API_KEY = "API"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={API_KEY}"

# --- Chargement du System Prompt depuis config_gemini.txt ---
SYSTEM_PROMPT = ""
CONFIG_FILE = "config_gemini.txt"

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            SYSTEM_PROMPT = f.read().strip()
        print(f"{Fore.BLUE}[INFO] System prompt chargé depuis {CONFIG_FILE}")
    except Exception as e:
        print(f"{Fore.RED}[AVERTISSEMENT] Impossible de lire {CONFIG_FILE} : {e}")
else:
    print(f"{Fore.YELLOW}[AVERTISSEMENT] Fichier {CONFIG_FILE} introuvable. Exécution sans system prompt.")

print(f"{Style.BRIGHT}{Fore.CYAN}--- Modèle : gemini-2.5-flash | Requêtes HTTP directes ---")
print(f"{Style.BRIGHT}{Fore.YELLOW}--- Chat actif (tapez 'exit' pour quitter) ---")
sys.stdout.flush()

while True:
    try:
        user_msg = input(f"{Style.BRIGHT}{Fore.GREEN}Vous : {Style.RESET_ALL}")
        
        if not user_msg.strip():
            continue
        if user_msg.strip().lower() == "exit":
            print(f"{Fore.RED}Fermeture du chat. À bientôt !")
            break
        
        # Structure du payload incluant le system_instruction
        payload = {
            "contents": [{
                "parts": [{"text": user_msg}]
            }]
        }
        
        # Ajout du system prompt s'il est présent
        if SYSTEM_PROMPT:
            payload["system_instruction"] = {
                "parts": [{"text": SYSTEM_PROMPT}]
            }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(URL, json=payload, headers=headers, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            try:
                answer = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                answer = "Erreur : Format de réponse inattendu de l'API."
        else:
            answer = f"Erreur API (Code {response.status_code}) : {response.text}"
        
        print(f"\n{Style.BRIGHT}{Fore.MAGENTA}Gemini :{Style.RESET_ALL} {answer}\n")
        sys.stdout.flush()

    except (EOFError, KeyboardInterrupt):
        print(f"\n{Fore.RED}Interruption détectée. Arrêt.")
        break
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}Erreur système : {e}")
        sys.stdout.flush()

