import requests
import re
from bs4 import BeautifulSoup

def find_phrase_by_pattern(url, pattern):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Грешка при зареждане на URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()

    matches = re.findall(pattern, text)
    return matches

# === Пример за използване ===
url = "https://www.otustanausta.com/search.php?keywords=pass"  # <-- смени с твоя URL
pattern = r"pass=[^\s&\"'>]+"  # Улавя pass=стойност

results = find_phrase_by_pattern(url, pattern)

if results:
    print("[Намерени стойности с 'pass=']:")
    with open("key.txt", "w", encoding="utf-8") as file:
        for match in results:
            print(match)
            file.write(match + "\n")
    print("\n[✓] Записано в result.txt")
else:
    print("Няма намерени стойности.")
